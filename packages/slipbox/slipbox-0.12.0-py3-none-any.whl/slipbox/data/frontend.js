import cytoscape from 'https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.15.2/cytoscape.esm.min.js';
import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.0/dist/fuse.esm.js';

function graphArea () {
  const div = document.createElement('div');
  div.style.width = '100%';
  div.style.height = '60vh';
  div.style.position = 'relative';
  div.style.top = '0px';
  div.style.left = '0px';
  return div
}

function noteElement (note, currentNote = false) {
  return {
    data: {
      id: note.id,
      title: note.title,
      filename: note.filename,
      label: note.id,
      color: 'white',
      bgColor: currentNote ? 'black' : 'gray'
    }
  }
}

function linkElement (type, source, target) {
  console.assert(['backlink', 'direct', 'sequence'].includes(type));
  const id = type.slice(0, 1) + `${source}-${target}`;
  const style = type === 'sequence' ? 'dashed' : 'solid';
  const color = 'black';
  return {
    data: { id, source, target, arrow: 'triangle', style, color }
  }
}

function dfs (graph, src) {
  if (!graph[src]) return []
  const edges = [];
  const done = new Set();
  const stack = [src];
  while (stack.length > 0) {
    const top = stack.pop();
    if (done.has(top)) continue
    const children = graph[top] || [];
    for (const child of children) {
      edges.push([top, child]);
      stack.push(child);
    }
    done.add(top);
  }
  return edges
}

function traverse (query, id) {
  const edges = [];
  for (const { forward, reverse } of Object.values(query.db.data.clusters)) {
    edges.push(...dfs(forward, id));
    edges.push(...dfs(reverse, id).map(([a, b]) => [b, a]));
  }
  return Array.from(new Set(edges.filter(([a, b]) => a !== b)))
}

function * neighborElements (query, note) {
  yield noteElement(note, true);

  for (const backlink of note.backlinks()) {
    yield noteElement(backlink.src);
    yield linkElement('backlink', backlink.src.id, note.id);
  }
  for (const link of note.links()) {
    yield noteElement(link.dest);
    yield linkElement('direct', note.id, link.dest.id);
  }
  for (const [src, dest] of traverse(query, note.id)) {
    yield noteElement(query.note(src));
    yield noteElement(query.note(dest));
    yield linkElement('sequence', src, dest);
  }
}

function createCytoscape (container, elements) {
  return cytoscape({
    directed: true,
    multigraph: true,
    container: container,
    elements: elements,
    selectionType: 'additive',
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          height: 'label',
          width: 'label',
          padding: '8px',
          shape: 'round-rectangle',
          color: 'data(color)',
          'background-color': 'data(bgColor)',
          'text-halign': 'center',
          'text-valign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': 100
        }
      },
      {
        selector: 'edge',
        style: {
          width: 2,
          'curve-style': 'bezier',
          'line-color': 'data(color)',
          'line-style': 'data(style)'
        }
      },
      {
        selector: 'edge[arrow]',
        style: {
          'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'data(arrow)'
        }
      }
    ]
  })
}

function noteInfoDiv () {
  const div = document.createElement('div');
  div.style.bottom = 0;
  div.style.right = 0;
  div.style.padding = '20px';
  div.style.position = 'fixed';
  div.style.maxWidth = '30em';
  div.style.zIndex = 1;
  return div
}

function hoverHandlers (container) {
  const header = document.createElement('header');
  header.innerHTML = '<h3><a href=""></a></h3><p></p>';
  const a = header.querySelector('a');
  const p = header.querySelector('p');

  const infoDiv = noteInfoDiv();
  infoDiv.appendChild(header);
  container.appendChild(infoDiv);

  const show = event => {
    const title = event.target.data('title');
    const filename = event.target.data('filename');
    a.textContent = title;
    a.href = '#' + event.target.data('id');
    p.textContent = filename;
    event.target.data('label', title);
  };
  const hide = event => {
    event.target.data('label', event.target.data('id'));
    a.textContent = '';
    p.textContent = '';
  };
  return [show, hide]
}

function init (query) {
  let container = graphArea();
  let infoContainer = document.createElement('div');
  const hr = document.createElement('hr');

  function resetGraph () {
    hr.remove();
    container.remove();
    infoContainer.remove();

    const id = Number(window.location.hash.slice(1));
    if (!Number.isInteger(id)) return

    const note = query.note(id);
    const elements = [];
    if (note != null) {
      elements.push(...neighborElements(query, note));
    }
    if (elements.length < 2) return

    container = graphArea();
    infoContainer = document.createElement('div');
    document.body.appendChild(hr);
    document.body.appendChild(infoContainer);
    document.body.appendChild(container);

    const cy = createCytoscape(container, elements);
    cy.layout({ name: 'cose' }).run();
    cy.reset();
    cy.center();

    const [show, hide] = hoverHandlers(infoContainer);
    cy.on('select', 'node', show);
    cy.on('unselect', 'node', hide);
  }

  resetGraph();
  window.addEventListener('hashchange', resetGraph);
}

class Database {
  // Schema
  // {
  //   clusters: {
  //     [tag: string]: {
  //       forward: {
  //         [src: number]: Array<number>
  //       },
  //       reverse: {
  //         [dest: number]: Array<number>
  //       }
  //     }
  //   }
  //   notes: [
  //     {
  //       title: <str>,
  //       filename: <str>,
  //       links: [{ src: <int>, dest: <int>, annotation: <str> }],
  //       backlinks: [<link>]
  //     }
  //   ]
  // }

  constructor () {
    this.data = { notes: [], clusters: {} };
  }

  add (record) {
    return record.addTo(this) || record
  }
}

class IntegrityError extends Error {}
class DomainError extends IntegrityError {}
class ReferenceError extends IntegrityError {}

function check (condition, message) {
  if (!condition) throw new DomainError(message)
}

class Note {
  constructor (id, title, filename) {
    check(Number.isInteger(id), 'invalid Note.id');
    check(typeof title === 'string', 'invalid Note.title');
    check(typeof filename === 'string', 'invalid Note.filename');
    check(title, 'empty Note.title');
    check(filename, 'missing Note.filename');

    this.id = id;
    this.title = title;
    this.filename = filename;
  }

  addTo (db) {
    // Overwrite existing entry in notes.
    db.data.notes[this.id] = {
      title: this.title,
      filename: this.filename,
      links: [],
      backlinks: [],
      clusters: {}
    };
  }

  equals (note) {
    return this.id === note.id && this.title === note.title && this.filename === note.filename
  }
}

class Link {
  constructor (src, dest, annotation) {
    check(src instanceof Note, 'invalid src Note');
    check(dest instanceof Note, 'invalid dest Note');
    check(typeof annotation === 'string', 'non-string Link.annotation');

    this.src = src;
    this.dest = dest;
    this.annotation = annotation;
  }

  addTo (db) {
    const src = db.data.notes[this.src.id];
    const dest = db.data.notes[this.dest.id];
    if (!src) return new ReferenceError('Link.src')
    if (!dest) return new ReferenceError('Link.dest')

    // Existing entries get overwritten.
    const link = {
      src: this.src,
      dest: this.dest,
      annotation: this.annotation
    };
    src.links.push(link);
    dest.backlinks.push(link);
  }
}

class Cluster {
  constructor (tag, src, dest) {
    check(typeof tag === 'string', 'non-string Cluster.tag');
    check(tag, 'invalid Cluster.tag');
    check(typeof src === 'number', 'non-number Cluster.src');
    check(typeof dest === 'number', 'non-number Cluster.dest');
    this.tag = tag;
    this.src = src;
    this.dest = dest;
  }

  addTo (db) {
    const src = this.src;
    const dest = this.dest;
    if (!db.data.notes[src]) return new ReferenceError('Cluster.src')
    if (!db.data.notes[dest]) return new ReferenceError('Cluster.dest')
    const result = db.data.clusters[this.tag] || {
      forward: {},
      reverse: {}
    };
    const forward = result.forward[src] || [];
    const reverse = result.reverse[dest] || [];
    forward.push(dest);
    reverse.push(src);
    result.forward[src] = forward;
    result.reverse[dest] = reverse;
    db.data.clusters[this.tag] = result;
  }
}

class Query {
  constructor (db) {
    this.db = db;
  }

  note (id) {
    const record = this.db.data.notes[id];
    if (!record) return null

    const note = new Note(id, record.title, record.filename);

    note.links = () => this.links(note);
    note.backlinks = () => this.backlinks(note);
    return note
  }

  * links (note) {
    const src = this.db.data.notes[note.id];
    if (src && src.links) {
      yield * src.links;
    }
  }

  * backlinks (note) {
    const dest = this.db.data.notes[note.id];
    if (dest && dest.backlinks) {
      yield * dest.backlinks;
    }
  }
}

var Model = /*#__PURE__*/Object.freeze({
  __proto__: null,
  Cluster: Cluster,
  Database: Database,
  DomainError: DomainError,
  Link: Link,
  Note: Note,
  Query: Query,
  ReferenceError: ReferenceError
});

function createFuse () {
  const options = {
    includeMatches: true,
    ignoreLocation: true,
    keys: ['textContent'],
    threshold: 0.45
  };
  const nodes = document.body.querySelectorAll('section.level1');
  const sections = Array.prototype.filter.call(nodes, function (node) {
    return Number.isInteger(Number(node.id))
  });
  return new Fuse(sections, options)
}

function displayResults (results, container) {
  // Display results in container.
  const div = container;
  div.textContent = '';
  for (const result of results) {
    const p = document.createElement('p');
    const h3 = document.createElement('h3');
    h3.innerHTML = `<a href="#${result.item.id}">${result.item.title}</a>`;
    p.appendChild(h3);

    let count = 3;
    for (const child of result.item.children) {
      const clone = child.cloneNode(true);
      if (count-- <= 0) break
      if (clone.tagName === 'H1' && clone.title === result.item.title) {
        continue
      }
      p.appendChild(clone);
    }

    div.appendChild(p);
    div.appendChild(document.createElement('hr'));
  }
}

function searchBar (fuse, container) {
  // Container will contain search results.
  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Search notes...';
  input.classList.add('search-bar');
  input.style.width = '100%';
  input.style.background = 'transparent';
  input.style.border = 'none';
  input.style.borderBottomStyle = 'solid';
  input.style.borderWidth = 'thin';

  input.addEventListener('change', function () {
    window.location.hash = '#search';
    const results = fuse.search(input.value);
    displayResults(results, container);
  });
  return input
}

function searchResults () {
  const div = document.createElement('div');
  div.classList.add('search-results');
  return div
}

function searchPage (container) {
  // Container will contain search results.
  const page = document.createElement('section');
  page.id = 'search';
  page.title = 'Search';
  page.classList.add('level1');
  page.appendChild(container);
  return page
}

function searchSpan () {
  const span = document.createElement('span');
  span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M23.809 21.646l-6.205-6.205c1.167-1.605 1.857-3.579 1.857-5.711 0-5.365-4.365-9.73-9.731-9.73-5.365 0-9.73 4.365-9.73 9.73 0 5.366 4.365 9.73 9.73 9.73 2.034 0 3.923-.627 5.487-1.698l6.238 6.238 2.354-2.354zm-20.955-11.916c0-3.792 3.085-6.877 6.877-6.877s6.877 3.085 6.877 6.877-3.085 6.877-6.877 6.877c-3.793 0-6.877-3.085-6.877-6.877z"/></svg>';
  span.firstChild.style.height = '1em';
  return span
}

function searchForm (container) {
  // Container will contain search results.
  const button = searchSpan();
  const input = searchBar(createFuse(), container);
  input.style.display = 'none';

  button.addEventListener('click', function () {
    button.style.display = 'none';
    input.style.display = '';
    input.focus();
  });

  input.addEventListener('focusout', function () {
    button.style.display = '';
    input.style.display = 'none';
  });

  const div = document.createElement('div');
  div.appendChild(button);
  div.appendChild(input);
  return div
}

function init$1 () {
  const container = searchResults();
  document.body.appendChild(searchPage(container));
  document.body.insertBefore(searchForm(container), document.body.firstChild);
}

function getSectionFromHash (hash) {
  const id = hash.substring(1);
  if (!id) { return null }
  const elem = document.getElementById(id);
  if (elem) {
    return elem.closest('section.level1')
  }
}

function sectionChanger () {
  let _previousHash = window.location.hash;
  return function () {
    const oldSection = getSectionFromHash(_previousHash);
    if (oldSection) {
      oldSection.style.display = 'none';
    }
    _previousHash = window.location.hash;
    const newSection = getSectionFromHash(_previousHash);
    if (newSection) {
      newSection.style.display = '';
      document.title = newSection.title || 'Slipbox';
    } else {
      window.location.hash = '#0';
    }
    window.scrollTo(0, 0);
  }
}

function notFoundSection () {
  const section = document.createElement('section');
  section.id = '0';
  section.classList.add('level1');
  section.style.display = 'none';
  const h1 = document.createElement('h1');
  h1.innerText = 'Note not found';
  section.appendChild(h1);
  return section
}

function init$2 () {
  document.body.appendChild(notFoundSection());
  const changeSection = sectionChanger();
  changeSection();
  window.addEventListener('hashchange', changeSection);
}

window.query = new Query(new Database());

window.Model = Model;

window.initSlipbox = function () {
  const title = document.getElementById('title-block-header');
  if (title) { title.remove(); }
  init$1();
  init$2();
  init(window.query);
};
