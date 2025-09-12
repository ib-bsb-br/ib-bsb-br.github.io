<?php
// This is now a static file loader.
// The slug is extracted from the URL query string `?b=...` by client-side JavaScript.
// We keep the .php extension for hosting compatibility, but no server-side logic is executed here.
$boardSlug = htmlspecialchars($_GET['b'] ?? 'public', ENT_QUOTES, 'UTF-8');
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="theme-color" content="#111111">
  <title>memor.ia.br &mdash; Todos</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="pkm-nav">
      <span class="brand">PKM System</span>
      <a href="https://memor.ia.br/?b=inbox" title="Tasks and Notes">Workshop</a>
      <a href="https://arcreformas.com.br" title="File Storage">Storage</a>
      <a href="https://cut.ia.br" title="Capture and Tools">Gateway</a>
      <a href="https://ib-bsb-br.github.io/" title="Public Site" target="_blank" rel="noopener">Published</a>
    </nav>
<div class="wrap">
  <div class="toolbar">
    <div class="row" style="flex:1;gap:.5rem">
      <span class="small pill">Board</span>
      <input id="slug" type="text" value="<?= $boardSlug ?>" aria-label="Board slug" style="max-width:240px" list="boards">
      <datalist id="boards"></datalist>
      <button class="secondary" id="switch" title="Open board by slug">Open</button>
      <button class="secondary" id="newBoard" title="Create a new random board">New</button>
    </div>
    <div class="row right">
      <span class="small">Shortcuts: <kbd>Enter</kbd> add/edit, <kbd>Esc</kbd> cancel, <kbd>Ctrl</kbd>+<kbd>/</kbd> focus</span>
    </div>
  </div>

  <div id="offline" class="offline" role="status" aria-live="polite">You are offline. Changes will queue and sync when back online.</div>

  <div class="box" aria-label="Todo app">
    <div class="row" style="margin-bottom:.6rem">
      <input id="title" type="text" value="My Todo" aria-label="List title" title="Title (Enter to save, Esc to cancel)">
      <button id="saveTitle" class="secondary" title="Save title">Save title</button>
      <button id="toggleAll" class="secondary" title="Toggle all tasks">Complete all</button>
      <button id="clearDone" class="secondary" title="Remove completed tasks">Clear completed</button>
      <button id="clearAll" class="warn" title="Remove all tasks">Clear all</button>
    </div>

    <div class="row" style="margin-bottom:.6rem">
      <input id="newtodo" type="text" placeholder="Add a task" autofocus aria-label="New task">
      <button id="add">Add</button>
      <input id="search" type="search" placeholder="Search" aria-label="Search tasks" style="max-width:240px">
      <div class="chips" role="tablist" aria-label="Filter tasks">
        <button class="chip active" data-filter="all" role="tab" aria-selected="true">All</button>
        <button class="chip" data-filter="active" role="tab" aria-selected="false">Active</button>
        <button class="chip" data-filter="done" role="tab" aria-selected="false">Completed</button>
      </div>
    </div>

    <ul id="list" aria-live="polite"></ul>

    <div class="meta">
      <div>
        <span class="small">Share this board URL:</span>
        <input id="shareUrl" type="text" readonly style="max-width:380px" aria-label="Share URL">
        <button class="secondary" id="copy">Copy</button>
        <span class="small count" id="counts"></span>
      </div>
      <span class="small right" id="updated"></span>
    </div>

    <div class="meta">
      <div class="status small" id="status" aria-live="polite"></div>
      <button id="undo" class="secondary" style="display:none">Undo</button>
      <span class="sr" id="srmsg" aria-live="polite"></span>
    </div>
  </div>
</div>

<script>
// --- CONFIGURATION ---
const API_BASE_URL = 'https://arcreformas.com.br/api';
const bid = new URLSearchParams(window.location.search).get('b') || 'public';
const origin = window.location.origin;

// --- DOM ELEMENTS ---
const $ = s => document.querySelector(s);
const list = $('#list'), input = $('#newtodo'), title = $('#title'), statusEl = $('#status');
const offlineBanner = $('#offline'), slugInput = $('#slug'), shareUrl = $('#shareUrl');
const countsEl = $('#counts'), updatedEl = $('#updated'), undoBtn = $('#undo'), srmsg = $('#srmsg');
const chips = document.querySelectorAll('.chip');
const boardsDL = $('#boards');

// --- STATE ---
let isSyncing = false;
let boardData = {title:'My Todo', tasks:[], created:Date.now()/1000|0, updated:Date.now()/1000|0};
let filter = localStorage.getItem('memor_filter') || 'all';
let searchQuery = localStorage.getItem('memor_search') || '';
let pendingEdit = null; // {id, orig}
let lastAction = null; // for undo
let undoTimer = null;
const outboxKey = (b) => `memor_outbox_${b}`;
const recentBoardsKey = 'memor_recent_boards_v1';

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', main);

function main() {
  // Register SW
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js', {scope:'/'}));
  }

  // Set up UI and fetch initial data
  setupUI();
  attachEventListeners();
  fetchBoard(true);
  flushOutbox();
}

function setupUI() {
  // Online/offline indicators
  updateOnlineUI();
  window.addEventListener('online', () => { updateOnlineUI(); flushOutbox(); fetchBoard(true); });
  window.addEventListener('offline', updateOnlineUI);

  // Copy/share URL setup
  const boardURL = `${origin}/?b=${encodeURIComponent(bid)}`;
  shareUrl.value = boardURL;

  // Set initial filter UI from localStorage
  chips.forEach(ch => {
    const isActive = ch.getAttribute('data-filter') === filter;
    ch.classList.toggle('active', isActive);
    ch.setAttribute('aria-selected', isActive ? 'true' : 'false');
  });
  $('#search').value = searchQuery;
}

// --- CORE LOGIC ---

async function fetchBoard(force = false) {
  const url = `${API_BASE_URL}/tasks/${encodeURIComponent(bid)}`;
  try {
    const r = await fetch(url, { cache: force ? 'reload' : 'default' });
    if (!r.ok) throw new Error('Network error');
    const d = await r.json();
    if (d.error) throw new Error(d.error);
    render(d);
    pushRecentBoard(bid);
    flash('Loaded', 800);
  } catch (e) {
    flash(`Offline (${e.message})`, 2000);
  }
}

async function op(payload, opts = {}) {
  // Optimistic UI update for speed
  if (!opts.silent) {
    const optimisticData = applyOperationOptimistically(boardData, payload);
    render(optimisticData);
  }

  try {
    const r = await fetch(`${API_BASE_URL}/tasks/${encodeURIComponent(bid)}`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error('Bad response');
    const d = await r.json();
    if (d.error) throw new Error(d.error);

    // Server is source of truth, re-render with its response
    render(d);
    return d;
  } catch (e) {
    queueOp(payload);
    if (!opts.silent) flash('Queued (offline)', 1500);
    // No need to re-render, optimistic update is already shown
    return null;
  }
}

// --- OFFLINE & QUEUING ---

function queueOp(payload) {
  const k = outboxKey(bid);
  const arr = JSON.parse(localStorage.getItem(k) || '[]');
  arr.push(payload);
  localStorage.setItem(k, JSON.stringify(arr));
  offlineBanner.classList.add('show');
}

async function flushOutbox() {
  if (isSyncing) return;
  const k = outboxKey(bid);
  let arr = JSON.parse(localStorage.getItem(k) || '[]');
  if (!arr.length || !navigator.onLine) return;

  isSyncing = true;
  flash('Syncing queued changes...');
  try {
    while (arr.length > 0) {
      await op(arr[0], {silent: true});
      arr.shift();
      localStorage.setItem(k, JSON.stringify(arr));
    }
    flash('Synced', 1000);
    await fetchBoard(true); // Fetch definitive state after sync
  } catch (e) {
    flash('Sync failed, will retry later.', 2000);
  } finally {
    isSyncing = false;
    updateOnlineUI();
  }
}

function updateOnlineUI() {
  offlineBanner.classList.toggle('show', !navigator.onLine);
}

// --- RENDER & UI HELPERS ---

function render(d) {
  boardData = d;
  title.value = d.title || 'My Todo';
  updateMeta(d);
  renderBoardsList();

  const tasks = applyFilter(d.tasks || []);
  const allowDrag = reorderAllowed();
  list.innerHTML = '';
  list.setAttribute('data-drag-disabled', !allowDrag);

  tasks.forEach(t => {
    const li = document.createElement('li');
    li.className = t.done ? 'done' : '';
    if (t.is_published) li.classList.add('published');
    li.tabIndex = 0;
    li.dataset.id = t.id;
    li.draggable = allowDrag;
    li.innerHTML = `
      <span class="drag" title="${allowDrag?'Drag to reorder':'Reorder disabled'}">⋮⋮</span>
      <input type="checkbox" ${t.done?'checked':''} data-id="${t.id}" aria-label="Mark task done">
      <span class="txt" contenteditable="true" data-id="${t.id}" spellcheck="false" role="textbox"></span>
      <button class="secondary" data-del="${t.id}" aria-label="Delete task">Del</button>
      <button class="secondary publish" data-pub="${t.id}" aria-label="Publish task" title="Publish to PKM">Pub</button>`;
    li.querySelector('.txt').textContent = t.text;
    list.appendChild(li);
  });
}

function updateMeta(d) {
  const activeCount = (d.tasks || []).filter(t => !t.done).length;
  const total = (d.tasks || []).length;
  countsEl.textContent = total ? `${activeCount} item${activeCount!==1?'s':''} left • ${total} total` : 'No tasks';
  updatedEl.textContent = `Updated ${fmtRelTime(d.updated || 0)}`;
  $('#toggleAll').textContent = activeCount > 0 ? 'Complete all' : 'Uncheck all';
}

function applyFilter(tasks) {
  const q = searchQuery.toLowerCase();
  return tasks.filter(t => {
    const matchesFilter = (filter === 'all') || (filter === 'active' && !t.done) || (filter === 'done' && t.done);
    const matchesSearch = !q || (t.text || '').toLowerCase().includes(q);
    return matchesFilter && matchesSearch;
  });
}

function reorderAllowed() {
  return filter === 'all' && !searchQuery;
}

let flashTimer = null;
function flash(msg, persistMs = 1500) {
  clearTimeout(flashTimer);
  statusEl.textContent = msg;
  srmsg.textContent = msg; // For screen readers
  if (persistMs > 0) {
    flashTimer = setTimeout(() => { statusEl.textContent = ''; srmsg.textContent = ''; }, persistMs);
  }
}

function fmtRelTime(ts) {
  const s = Math.max(0, Math.floor(Date.now() / 1000 - ts));
  if (s < 5) return 'just now';
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s/60); if (m < 60) return `${m}m ago`;
  const h = Math.floor(m/60); if (h < 24) return `${h}h ago`;
  return `${Math.floor(h/24)}d ago`;
}

function pushRecentBoard(slug) {
  try {
    let arr = JSON.parse(localStorage.getItem(recentBoardsKey) || '[]');
    arr = arr.filter(s => s !== slug);
    arr.unshift(slug);
    if (arr.length > 10) arr.length = 10;
    localStorage.setItem(recentBoardsKey, JSON.stringify(arr));
    renderBoardsList();
  } catch (e) {}
}

function renderBoardsList() {
  try {
    const arr = JSON.parse(localStorage.getItem(recentBoardsKey) || '[]');
    boardsDL.innerHTML = arr.map(s => `<option value="${s}"></option>`).join('');
  } catch (e) {}
}

// --- EVENT LISTENERS ---
function attachEventListeners() {
  $('#copy').onclick = () => navigator.clipboard.writeText(shareUrl.value).then(() => flash('Copied!', 1000), () => flash('Copy failed', 1500));

  $('#add').onclick = () => {
    const v = input.value.trim();
    if (v) op({op:'add', text: v}).then(() => { input.value=''; input.focus(); flash('Added', 800); });
  };
  input.onkeydown = e => { if (e.key === 'Enter') { e.preventDefault(); $('#add').click(); } };

  let titleOrig = '';
  title.onfocus = () => { titleOrig = title.value; };
  title.onblur = () => { if (title.value !== titleOrig) op({op:'title', title: title.value.trim() || 'My Board'}).then(()=>flash('Saved', 900)); };
  title.onkeydown = e => { if (e.key === 'Enter') e.target.blur(); if (e.key === 'Escape') { title.value = titleOrig; e.target.blur(); }};
  $('#saveTitle').onclick = () => title.blur();

  $('#clearDone').onclick = () => op({op:'clear_done'}).then(()=>flash('Cleared completed'));
  $('#clearAll').onclick = () => confirm('Delete all tasks?') && op({op:'clear_all'}).then(()=>flash('All cleared'));
  $('#toggleAll').onclick = () => {
    const anyActive = (boardData.tasks||[]).some(t=>!t.done);
    op({op:'set_all', done: anyActive}).then(()=>flash(anyActive?'Completed all':'Unchecked all'));
  };

  $('#switch').onclick = () => {
    const s = (slugInput.value||'').trim();
    if (s) window.location = `${origin}/?b=${encodeURIComponent(s)}`;
  };
  $('#newBoard').onclick = () => {
    const newSlug = Math.random().toString(36).substring(2, 8);
    window.location = `${origin}/?b=${encodeURIComponent(newSlug)}`;
  };

  chips.forEach(ch => ch.onclick = () => {
    filter = ch.dataset.filter;
    localStorage.setItem('memor_filter', filter);
    document.querySelector('.chip.active').classList.remove('active');
    ch.classList.add('active');
    render(boardData);
  });

  $('#search').oninput = e => {
    searchQuery = e.target.value.trim();
    localStorage.setItem('memor_search', searchQuery);
    render(boardData);
  };

  list.addEventListener('change', e => {
    const id = e.target.dataset.id;
    if (id && e.target.type === 'checkbox') op({op:'toggle', id});
  });

  list.addEventListener('click', e => {
    const delId = e.target.dataset.del;
    if (delId) op({op:'del', id: delId}).then(()=>flash('Deleted'));

    const pubId = e.target.dataset.pub;
    if (pubId) op({op:'publish', id: pubId}).then(()=>flash('Published!'));
  });

  let dragSrcEl = null;
  list.addEventListener('dragstart', e => {
    if (!e.target.matches('li')) return;
    dragSrcEl = e.target;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target.dataset.id);
  });
  list.addEventListener('dragover', e => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    const target = e.target.closest('li');
    if (target && target !== dragSrcEl) {
      list.insertBefore(dragSrcEl, target.nextSibling || target);
    }
  });
  list.addEventListener('drop', e => {
    e.preventDefault();
    if (!dragSrcEl) return;
    const order = Array.from(list.querySelectorAll('li')).map(node => node.dataset.id);
    op({op:'reorder', order});
  });

  list.addEventListener('blur', e => {
    if (e.target.classList.contains('txt')) {
      const id = e.target.dataset.id;
      const text = e.target.textContent.trim();
      const originalTask = boardData.tasks.find(t => t.id === id);
      if (originalTask && text !== originalTask.text) {
        op({op:'edit', id, text}).then(()=>flash('Saved', 800));
      }
    }
  }, true);
}


// --- OPTIMISTIC UPDATES ---
// This function applies changes to the local data immediately for a faster UI feel.
// The server response will eventually overwrite this, providing consistency.
function applyOperationOptimistically(data, payload) {
    let newData = JSON.parse(JSON.stringify(data)); // Deep copy
    const { op, id, text, done, order } = payload;

    switch (op) {
        case 'add':
            newData.tasks.push({ id: `temp-${Date.now()}`, text, done: false, ts: Date.now()/1000 });
            break;
        case 'toggle':
            newData.tasks.forEach(t => { if (t.id === id) t.done = !t.done; });
            break;
        case 'edit':
            newData.tasks.forEach(t => { if (t.id === id) t.text = text; });
            break;
        case 'del':
            newData.tasks = newData.tasks.filter(t => t.id !== id);
            break;
        case 'title':
            newData.title = payload.title;
            break;
        case 'clear_done':
            newData.tasks = newData.tasks.filter(t => !t.done);
            break;
        case 'set_all':
            newData.tasks.forEach(t => t.done = done);
            break;
        case 'clear_all':
            newData.tasks = [];
            break;
        case 'reorder':
             const taskMap = new Map(newData.tasks.map(t => [t.id, t]));
             newData.tasks = order.map(orderedId => taskMap.get(orderedId)).filter(Boolean);
            break;
        case 'publish':
            newData.tasks.forEach(t => { if (t.id === id) t.is_published = 1; });
            break;
    }
    newData.updated = Date.now() / 1000;
    return newData;
}
</script>
</body>
</html>
