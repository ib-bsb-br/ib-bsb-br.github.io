---
tags: [scratchpad]
info: aberto.
date: 2025-09-10
type: post
layout: post
published: true
slug: coolice-todo-webapp
title: 'coolice todo webapp'
---
```php
<?php
declare(strict_types=1);

/*
UX upgrades (fully implemented)
- Inline edits: Enter commits, Esc cancels and reverts, Tab moves to next, Shift+Tab to prev.
- Title: Enter saves, Esc cancels.
- Keyboard on list: Space toggles, Delete removes, E starts edit for focused item.
- Drag-and-drop reorder (disabled while filtering/searching); persists via new "reorder" API op.
- Filters & search: All/Active/Completed + text search; persists in localStorage.
- Bulk ops: "Complete all"/"Uncheck all", "Clear completed", "Clear all" (with confirm).
- Undo for delete and clear completed (10s window).
- Recent boards history with datalist for quick switching.
- Accessibility and feedback: aria-live, counts, last updated, consistent flash messages.
- PWA retained with single-file assets; safer limits and headers; ETag + Last-Modified + 304 for fetch.
*/

/////////////////////////////
// Security & headers
/////////////////////////////

header('X-Content-Type-Options: nosniff');

$isHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
  || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https');
if ($isHttps) {
  header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
}

/////////////////////////////
// Config and helpers
/////////////////////////////

$scheme = ($isHttps ? 'https' : 'http');
$host   = $_SERVER['HTTP_HOST'] ?? 'localhost';
$origin = $scheme . '://' . $host;

$dataDir = realpath(__DIR__ . '/..') ? (realpath(__DIR__ . '/..') . '/data') : (__DIR__ . '/../data');
if (!is_dir($dataDir)) {
  @mkdir($dataDir, 0755, true);
}

const MAX_TEXT_LEN  = 2000;
const MAX_TITLE_LEN = 200;

function id(): string {
  return rtrim(strtr(base64_encode(random_bytes(6)), '+/', '-_'), '=');
}
function safeSlug(string $b): string {
  $b = preg_replace('/[^a-zA-Z0-9_-]/', '_', $b);
  $b = substr($b, 0, 64);
  return $b !== '' ? $b : 'public';
}
function pathOf(string $b): string {
  return $GLOBALS['dataDir'] . '/' . safeSlug($b) . '.json';
}
function emptyBoard(): array {
  $t = time();
  return ['title' => 'My Todo', 'tasks' => [], 'created' => $t, 'updated' => $t];
}
function loadBoard(string $b): array {
  $f = pathOf($b);
  if (!is_file($f)) return emptyBoard();
  $raw = file_get_contents($f);
  $j = $raw ? json_decode($raw, true) : null;
  return is_array($j) ? $j : emptyBoard();
}
function saveBoard(string $b, array $d): void {
  $f = pathOf($b);
  $d['updated'] = time();
  $h = fopen($f, 'c+');
  if ($h) {
    flock($h, LOCK_EX);
    ftruncate($h, 0);
    fwrite($h, json_encode($d, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    fflush($h);
    flock($h, LOCK_UN);
    fclose($h);
    @chmod($f, 0644);
  }
}
function emitJSON($x, array $headers = []): never {
  foreach ($headers as $k => $v) header("$k: $v");
  header('Content-Type: application/json; charset=utf-8');
  header('Cache-Control: no-cache, must-revalidate');
  echo json_encode($x, JSON_UNESCAPED_UNICODE);
  exit;
}
function notModified(): never {
  header('HTTP/1.1 304 Not Modified');
  exit;
}
function htmlHeader(): void {
  header('Content-Type: text/html; charset=utf-8');
  header('Cache-Control: no-cache');
}

/////////////////////////////
// Asset router (manifest, sw, icons, favicon)
/////////////////////////////

if (isset($_GET['asset'])) {
  $asset = $_GET['asset'];
  if ($asset === 'manifest') {
    header('Content-Type: application/manifest+json; charset=utf-8');
    header('Cache-Control: public, max-age=3600');
    // Minimal base64 1x1 PNG
    $icon1x1 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=';
    echo json_encode([
      'name' => 'memor.ia.br — Todos',
      'short_name' => 'memor',
      'start_url' => '/?b=public',
      'display' => 'standalone',
      'background_color' => '#ffffff',
      'theme_color' => '#111111',
      'icons' => [
        ['src' => $icon1x1, 'sizes' => '192x192', 'type' => 'image/png'],
        ['src' => $icon1x1, 'sizes' => '512x512', 'type' => 'image/png'],
        ['src' => $origin . '/?asset=favicon', 'sizes' => 'any', 'type' => 'image/svg+xml', 'purpose' => 'any maskable'],
      ],
      'scope' => '/',
    ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
  }
  if ($asset === 'sw') {
    header('Content-Type: application/javascript; charset=utf-8');
    header('Cache-Control: public, max-age=3600');
    ?>
// Service Worker for memor.ia.br
const CACHE_NAME = 'memor-cache-v1.2';
const SHELL = [
  '/?b=public',
  '/?asset=manifest',
  '/?asset=favicon'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.map(k => (k!==CACHE_NAME ? caches.delete(k) : Promise.resolve()))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  // API fetch for board -> stale-while-revalidate
  if (url.searchParams.get('action') === 'fetch' && url.searchParams.get('b')) {
    e.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(e.request);
      const fetchPromise = fetch(e.request).then(res => {
        if (res && (res.status === 200 || res.status === 304)) {
          cache.put(e.request, res.clone());
        }
        return res;
      }).catch(() => cached);
      return cached || fetchPromise;
    })());
    return;
  }
  // HTML/other GET: network first; fallback to cache; simple offline page if none
  if (e.request.method === 'GET') {
    e.respondWith((async () => {
      try {
        const net = await fetch(e.request);
        const cache = await caches.open(CACHE_NAME);
        cache.put(e.request, net.clone());
        return net;
      } catch (err) {
        const cache = await caches.open(CACHE_NAME);
        const cached = await cache.match(e.request);
        return cached || new Response('<!doctype html><meta charset="utf-8"><title>Offline</title><h1>Offline</h1><p>The app is offline. Retry when back online.</p>', { headers: {'Content-Type':'text/html; charset=utf-8'} });
      }
    })());
  }
});
    <?php
    exit;
  }
  if ($asset === 'favicon') {
    header('Content-Type: image/svg+xml; charset=utf-8');
    header('Cache-Control: public, max-age=86400');
    echo '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect fill="#111" width="64" height="64" rx="12"/><path d="M48 20L27 41l-11-9" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>';
    exit;
  }
  header('HTTP/1.1 404 Not Found');
  exit;
}

/////////////////////////////
// API: Board fetch (GET) with ETag/Last-Modified
/////////////////////////////

$action = $_GET['action'] ?? '';
$bParam = $_GET['b'] ?? '';

if ($action === 'new') {
  $bid = id();
  header('Location: ' . $origin . '/?b=' . urlencode($bid));
  exit;
}

if ($action === 'fetch' && $bParam !== '') {
  $b = safeSlug($bParam);
  $f = pathOf($b);
  $board = loadBoard($b);
  $raw = json_encode($board, JSON_UNESCAPED_UNICODE);
  $etag = '"' . md5($raw) . '"';
  $lastModTs = file_exists($f) ? filemtime($f) : $board['updated'];
  $lastMod = gmdate('D, d M Y H:i:s', $lastModTs) . ' GMT';

  $inm = $_SERVER['HTTP_IF_NONE_MATCH'] ?? '';
  $ims = $_SERVER['HTTP_IF_MODIFIED_SINCE'] ?? '';
  if ($inm === $etag || $ims === $lastMod) {
    header('ETag: ' . $etag);
    header('Last-Modified: ' . $lastMod);
    notModified();
  }

  emitJSON($board, [
    'ETag' => $etag,
    'Last-Modified' => $lastMod
  ]);
}

/////////////////////////////
// POST ops
/////////////////////////////

if ($bParam !== '' && $_SERVER['REQUEST_METHOD'] === 'POST') {
  $b = safeSlug($bParam);
  $in = json_decode((string)file_get_contents('php://input'), true) ?: [];
  $op = $in['op'] ?? '';
  $board = loadBoard($b);

  if ($op === 'add') {
    $t = trim((string)($in['text'] ?? ''));
    if ($t !== '') {
      $t = mb_substr($t, 0, MAX_TEXT_LEN, 'UTF-8');
      $board['tasks'][] = ['id' => id(), 'text' => $t, 'done' => false, 'ts' => time()];
      saveBoard($b, $board);
    }
    emitJSON($board);
  }
  if ($op === 'toggle') {
    $idv = (string)($in['id'] ?? '');
    foreach ($board['tasks'] as &$t) {
      if ($t['id'] === $idv) {
        $t['done'] = !$t['done'];
        break;
      }
    }
    unset($t);
    saveBoard($b, $board);
    emitJSON($board);
  }
  if ($op === 'edit') {
    $idv = (string)($in['id'] ?? '');
    $txt = trim((string)($in['text'] ?? ''));
    $txt = mb_substr($txt, 0, MAX_TEXT_LEN, 'UTF-8');
    foreach ($board['tasks'] as &$t) {
      if ($t['id'] === $idv) {
        $t['text'] = $txt;
        break;
      }
    }
    unset($t);
    saveBoard($b, $board);
    emitJSON($board);
  }
  if ($op === 'del') {
    $idv = (string)($in['id'] ?? '');
    $board['tasks'] = array_values(array_filter($board['tasks'], fn($t) => $t['id'] !== $idv));
    saveBoard($b, $board);
    emitJSON($board);
  }
  if ($op === 'title') {
    $ttl = trim((string)($in['title'] ?? ''));
    if ($ttl !== '') $ttl = mb_substr($ttl, 0, MAX_TITLE_LEN, 'UTF-8');
    $board['title'] = $ttl !== '' ? $ttl : 'My Todo';
    saveBoard($b, $board);
    emitJSON($board);
  }
  if ($op === 'clear_done') {
    $board['tasks'] = array_values(array_filter($board['tasks'], fn($t) => empty($t['done'])));
    saveBoard($b, $board);
    emitJSON($board);
  }
  // New: set all done/undone
  if ($op === 'set_all') {
    $done = (bool)($in['done'] ?? false);
    foreach ($board['tasks'] as &$t) {
      $t['done'] = $done;
    }
    unset($t);
    saveBoard($b, $board);
    emitJSON($board);
  }
  // New: clear all
  if ($op === 'clear_all') {
    $board['tasks'] = [];
    saveBoard($b, $board);
    emitJSON($board);
  }
  // New: reorder tasks by id list
  if ($op === 'reorder') {
    $order = $in['order'] ?? [];
    if (is_array($order)) {
      $idx = [];
      foreach ($order as $pos => $tid) { $idx[(string)$tid] = (int)$pos; }
      usort($board['tasks'], function($a, $b) use ($idx) {
        $ai = $idx[$a['id']] ?? PHP_INT_MAX;
        $bi = $idx[$b['id']] ?? PHP_INT_MAX;
        return $ai <=> $bi;
      });
      saveBoard($b, $board);
    }
    emitJSON($board);
  }
  emitJSON(['error' => 'unknown op']);
}

/////////////////////////////
// Quick add by URL (?add=Text) -> add to board and redirect
/////////////////////////////

if (isset($_GET['add'])) {
  $b = safeSlug($bParam !== '' ? $bParam : 'public');
  $txt = trim((string)$_GET['add']);
  if ($txt !== '') {
    $txt = mb_substr($txt, 0, MAX_TEXT_LEN, 'UTF-8');
    $board = loadBoard($b);
    $board['tasks'][] = ['id' => id(), 'text' => $txt, 'done' => false, 'ts' => time()];
    saveBoard($b, $board);
  }
  header('Location: ' . $origin . '/?b=' . urlencode($b), true, 303);
  exit;
}

/////////////////////////////
// HTML App
/////////////////////////////

$boardSlug = safeSlug($bParam !== '' ? $bParam : 'public');
htmlHeader();
?>
<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<link rel="manifest" href="<?= htmlspecialchars($origin, ENT_QUOTES, 'UTF-8') ?>/?asset=manifest">
<link rel="icon" href="<?= htmlspecialchars($origin, ENT_QUOTES, 'UTF-8') ?>/?asset=favicon" type="image/svg+xml">
<meta name="theme-color" content="#111111">
<title>memor.ia.br &mdash; Todos</title>
<style>
  :root { color-scheme: light dark; --bg:#fff; --fg:#111; --muted:#777; --border:#ddd; --accent:#111; --ok:#0a7f2e; --warn:#a00; --chip:#f1f1f1; --chipA:#d1e9ff; --focus:#5b9cff; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0c0c0c; --fg:#eee; --muted:#aaa; --border:#222; --accent:#e5e5e5; --ok:#4cc27f; --warn:#ff736a; --chip:#171717; --chipA:#0f3050; --focus:#6aa3ff; }
  }
  html,body{height:100%}
  body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,Segoe UI,Roboto,Arial}
  .wrap{max-width:920px;margin:0 auto;padding:18px}
  .box{border:1px solid var(--border);border-radius:12px;padding:14px;background:rgba(0,0,0,0.02)}
  .row{display:flex;gap:.5rem;align-items:center}
  input[type=text], input[type=search]{flex:1;padding:.65rem;border:1px solid var(--border);border-radius:10px;background:transparent;color:var(--fg)}
  button{padding:.6rem .9rem;border:0;border-radius:10px;background:var(--accent);color:#fff;cursor:pointer}
  button.secondary{background:transparent;color:var(--fg);border:1px solid var(--border)}
  button.warn{background:var(--warn)}
  button.ok{background:var(--ok)}
  ul{list-style:none;padding:0;margin:12px 0}
  li{display:flex;align-items:center;gap:.5rem;padding:.45rem .3rem;border-bottom:1px solid var(--border)}
  li:focus{outline:2px solid var(--focus);outline-offset:2px;border-radius:8px}
  li.done .txt{text-decoration:line-through;color:var(--muted)}
  .txt{flex:1;outline:none}
  .txt:focus{background:rgba(127,127,127,.1);border-radius:4px;padding:2px}
  .meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
  .small{font-size:.9rem;color:var(--muted)}
  .pill{padding:.1rem .5rem;border:1px solid var(--border);border-radius:999px}
  .share{display:inline-flex;gap:.5rem;align-items:center}
  .offline{display:none;margin:12px 0;padding:10px;border-radius:10px;background:#fffbcc;color:#333;border:1px solid #e0dca6}
  .offline.show{display:block}
  .right{margin-left:auto}
  .kbd{font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;background:rgba(127,127,127,.18);border:1px solid var(--border);border-bottom-color:rgba(0,0,0,.3);border-radius:6px;padding:0 .3rem}
  .toolbar{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin-bottom:.6rem}
  .chips{display:flex;gap:.4rem;flex-wrap:wrap}
  .chip{padding:.35rem .6rem;border-radius:999px;border:1px solid var(--border);background:var(--chip);cursor:pointer}
  .chip.active{background:var(--chipA)}
  .drag{cursor:grab;user-select:none;color:var(--muted);padding:0 .4rem}
  .count{margin-left:.4rem}
  .status{min-height:1.4rem}
  .status button{margin-left:.5rem}
  .sr{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden;}
</style>

<div class="wrap">
  <div class="toolbar">
    <div class="row" style="flex:1;gap:.5rem">
      <span class="small pill">Board</span>
      <input id="slug" type="text" value="<?= htmlspecialchars($boardSlug, ENT_QUOTES, 'UTF-8') ?>" aria-label="Board slug" style="max-width:240px" list="boards">
      <datalist id="boards"></datalist>
      <button class="secondary" id="switch" title="Open board by slug">Open</button>
      <button class="secondary" id="newBoard" title="Create a new random board">New</button>
    </div>
    <div class="row right">
      <span class="small">Shortcuts: <span class="kbd">Enter</span> add/edit, <span class="kbd">Esc</span> cancel, <span class="kbd">Ctrl</span>+<span class="kbd">/</span> focus</span>
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
const origin = <?= json_encode($origin) ?>;
const bid = <?= json_encode($boardSlug) ?>;
const $ = s => document.querySelector(s);
const list = $('#list'), input = $('#newtodo'), title = $('#title'), statusEl = $('#status');
const offlineBanner = $('#offline'), slugInput = $('#slug'), shareUrl = $('#shareUrl');
const countsEl = $('#counts'), updatedEl = $('#updated'), undoBtn = $('#undo'), srmsg = $('#srmsg');
const chips = document.querySelectorAll('.chip');
const boardsDL = $('#boards');

let boardETag = null;
let boardLastMod = null;
let isSyncing = false;
let boardData = {title:'My Todo', tasks:[], created:Date.now()/1000|0, updated:Date.now()/1000|0};
let filter = localStorage.getItem('memor_filter') || 'all';
let searchQuery = localStorage.getItem('memor_search') || '';
let pendingEdit = null; // {id, orig}
let lastAction = null; // for undo
let undoTimer = null;

const outboxKey = (b) => `memor_outbox_${b}`;
const recentBoardsKey = 'memor_recent_boards_v1';

// Register SW
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/?asset=sw', {scope:'/'});
  });
}

// Online/offline indicators
function updateOnlineUI() {
  if (navigator.onLine) {
    offlineBanner.classList.remove('show');
  } else {
    offlineBanner.classList.add('show');
  }
}
window.addEventListener('online', () => { updateOnlineUI(); flushOutbox(); fetchBoard(true); });
window.addEventListener('offline', updateOnlineUI);
updateOnlineUI();

// Copy/share URL setup
const boardURL = `${origin}/?b=${encodeURIComponent(bid)}`;
shareUrl.value = boardURL;
$('#copy').onclick = async () => {
  try { await navigator.clipboard.writeText(boardURL); flash('Copied link', 1200); } catch(e){ flash('Copy failed', 1500); }
};

// Helper: small status message
let flashTimer = null;
function flash(msg, persistMs=1500) {
  clearTimeout(flashTimer);
  statusEl.textContent = msg;
  if (persistMs > 0) {
    flashTimer = setTimeout(() => statusEl.textContent = '', persistMs);
  }
  srmsg.textContent = msg;
}

// Undo handling
function showUndo(action) {
  lastAction = action; // {type, payload}
  undoBtn.style.display = 'inline-block';
  clearTimeout(undoTimer);
  undoTimer = setTimeout(() => { hideUndo(); }, 10000);
}
function hideUndo() {
  lastAction = null;
  undoBtn.style.display = 'none';
}
undoBtn.onclick = async () => {
  if (!lastAction) return;
  const act = lastAction;
  hideUndo();
  if (act.type === 'del') {
    const t = act.payload;
    await op({op:'add', text: t.text});
    flash('Undid delete', 1000);
  } else if (act.type === 'clear_done') {
    for (const t of act.payload) {
      await op({op:'add', text: t.text});
    }
    flash('Restored completed', 1200);
  }
};

// Render helpers
function fmtRelTime(ts) {
  const s = Math.max(0, Math.floor(Date.now()/1000 - ts));
  if (s < 5) return 'just now';
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s/60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m/60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h/24);
  return `${d}d ago`;
}
function updateMeta(d) {
  const activeCount = (d.tasks || []).filter(t => !t.done).length;
  const total = (d.tasks || []).length;
  countsEl.textContent = total ? `${activeCount} item${activeCount!==1?'s':''} left • ${total} total` : 'No tasks';
  updatedEl.textContent = `Updated ${fmtRelTime(d.updated||Date.now()/1000|0)}`;
  $('#toggleAll').textContent = activeCount > 0 ? 'Complete all' : 'Uncheck all';
}

// Filtering
function applyFilter(tasks) {
  let arr = tasks.slice();
  const q = (searchQuery||'').toLowerCase();
  if (filter === 'active') arr = arr.filter(t => !t.done);
  if (filter === 'done') arr = arr.filter(t => t.done);
  if (q) arr = arr.filter(t => (t.text||'').toLowerCase().includes(q));
  return arr;
}
function updateFilterUI() {
  chips.forEach(ch => {
    const isActive = ch.getAttribute('data-filter') === filter;
    ch.classList.toggle('active', isActive);
    ch.setAttribute('aria-selected', isActive ? 'true' : 'false');
  });
  $('#search').value = searchQuery;
}
function reorderAllowed() {
  return filter === 'all' && !searchQuery;
}

// Recent boards
function pushRecentBoard(slug) {
  try {
    const raw = localStorage.getItem(recentBoardsKey);
    let arr = raw ? JSON.parse(raw) : [];
    arr = arr.filter(s => s !== slug);
    arr.unshift(slug);
    if (arr.length > 10) arr.length = 10;
    localStorage.setItem(recentBoardsKey, JSON.stringify(arr));
    renderBoardsList();
  } catch (e) {}
}
function renderBoardsList() {
  try {
    const raw = localStorage.getItem(recentBoardsKey);
    const arr = raw ? JSON.parse(raw) : [];
    boardsDL.innerHTML = arr.map(s => `<option value="${s}"></option>`).join('');
  } catch (e) {}
}

// Render board
function render(d) {
  boardData = d;
  title.value = d.title || 'My Todo';
  updateMeta(d);
  renderBoardsList();

  const tasks = applyFilter(d.tasks || []);
  list.innerHTML = '';

  const allowDrag = reorderAllowed();
  if (!allowDrag) {
    list.setAttribute('data-drag-disabled', 'true');
  } else {
    list.removeAttribute('data-drag-disabled');
  }

  tasks.forEach((t) => {
    const li = document.createElement('li');
    li.setAttribute('tabindex', '0');
    if (t.done) li.classList.add('done');
    li.dataset.id = t.id;
    li.draggable = allowDrag;
    li.innerHTML =
      `<span class="drag" title="${allowDrag?'Drag to reorder':'Reorder disabled while filtering/searching'}">⋮⋮</span>
       <input type="checkbox" ${t.done?'checked':''} data-id="${t.id}" aria-label="Mark task done">
       <span class="txt" contenteditable="true" data-id="${t.id}" spellcheck="false" role="textbox" aria-multiline="false"></span>
       <button class="secondary" data-del="${t.id}" aria-label="Delete task">Delete</button>`;
    li.querySelector('.txt').textContent = t.text;

    // Drag events
    if (allowDrag) {
      li.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', t.id);
        li.classList.add('dragging');
      });
      li.addEventListener('dragend', () => {
        li.classList.remove('dragging');
      });
      li.addEventListener('dragover', (e) => {
        e.preventDefault();
        const dragging = list.querySelector('.dragging');
        if (!dragging || dragging === li) return;
        const rect = li.getBoundingClientRect();
        const before = (e.clientY - rect.top) < rect.height / 2;
        list.insertBefore(dragging, before ? li : li.nextSibling);
      });
      li.addEventListener('drop', async (e) => {
        e.preventDefault();
        const order = Array.from(list.querySelectorAll('li')).map(node => node.dataset.id);
        await op({op:'reorder', order});
        flash('Reordered', 800);
      });
    }
    list.appendChild(li);
  });
}

// Fetch with ETag support
async function fetchBoard(force=false) {
  const url = `?action=fetch&b=${encodeURIComponent(bid)}`;
  const headers = {};
  if (boardETag && !force) headers['If-None-Match'] = boardETag;
  if (boardLastMod && !force) headers['If-Modified-Since'] = boardLastMod;
  try {
    const r = await fetch(url, {headers});
    if (r.status === 304) return;
    if (!r.ok) throw new Error('Network error');
    const d = await r.json();
    boardETag = r.headers.get('ETag');
    boardLastMod = r.headers.get('Last-Modified');
    render(d);
    pushRecentBoard(bid);
    flash('Loaded', 800);
  } catch (e) {
    flash('Offline (cached view)', 1500);
  }
}

// Queue ops if offline/errors
function queueOp(payload) {
  const k = outboxKey(bid);
  const arr = JSON.parse(localStorage.getItem(k) || '[]');
  arr.push(payload);
  localStorage.setItem(k, JSON.stringify(arr));
  offlineBanner.classList.add('show');
}

// Flush queued ops
async function flushOutbox() {
  if (isSyncing) return;
  const k = outboxKey(bid);
  let arr = JSON.parse(localStorage.getItem(k) || '[]');
  if (!arr.length || !navigator.onLine) return;
  isSyncing = true;
  try {
    while (arr.length && navigator.onLine) {
      const p = arr[0];
      await op(p, {silent:true});
      arr.shift();
      localStorage.setItem(k, JSON.stringify(arr));
    }
    if (arr.length === 0) {
      offlineBanner.classList.remove('show');
      flash('Synced', 1000);
      fetchBoard(true);
    }
  } catch (e) {
    // keep queue for retry
  } finally {
    isSyncing = false;
  }
}

// Perform operation
async function op(p, opts={}) {
  try {
    const r = await fetch(`?b=${encodeURIComponent(bid)}`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(p)
    });
    if (!r.ok) throw new Error('Bad response');
    const d = await r.json();
    if (!opts.silent) render(d);
    return d;
  } catch (e) {
    queueOp(p);
    if (!opts.silent) flash('Queued (offline)', 1500);
    return null;
  }
}

// Event handlers
document.addEventListener('DOMContentLoaded', async () => {
  // Initialize filter UI
  chips.forEach(ch => {
    ch.addEventListener('click', () => {
      filter = ch.getAttribute('data-filter');
      localStorage.setItem('memor_filter', filter);
      updateFilterUI();
      render(boardData);
    });
  });
  $('#search').addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    localStorage.setItem('memor_search', searchQuery);
    render(boardData);
  });
  updateFilterUI();

  await fetchBoard(true);
  await flushOutbox();

  // Add new task
  $('#add').onclick = () => {
    const v = input.value.trim();
    if (v) {
      op({op:'add', text: v}).then(() => { input.value=''; input.focus(); flash('Added', 800); });
    }
  };
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); $('#add').click(); }
    if (e.key === 'Escape') { input.value=''; input.blur(); }
    if (e.ctrlKey && e.key === '/') { e.preventDefault(); input.focus(); }
  });

  // Title save/cancel
  let titleOrig = '';
  title.addEventListener('focus', () => { titleOrig = title.value; });
  $('#saveTitle').onclick = () => {
    const ttl = title.value.trim() || 'My Todo';
    op({op:'title', title: ttl}).then(()=>flash('Saved', 900));
  };
  title.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') { e.preventDefault(); $('#saveTitle').click(); title.blur(); }
    if (e.key === 'Escape') { e.preventDefault(); title.value = titleOrig; title.blur(); flash('Canceled', 800); }
  });
  title.addEventListener('blur', () => $('#saveTitle').click());

  // Bulk buttons
  $('#clearDone').onclick = () => {
    const cleared = (boardData.tasks||[]).filter(t=>t.done);
    if (!cleared.length) { flash('No completed tasks', 1200); return; }
    op({op:'clear_done'}).then(()=>{ flash('Cleared completed', 1000); showUndo({type:'clear_done', payload: cleared}); });
  };
  $('#clearAll').onclick = () => {
    const total = (boardData.tasks||[]).length;
    if (!total) { flash('No tasks to clear', 1200); return; }
    if (confirm(`Delete all ${total} tasks?`)) {
      op({op:'clear_all'}).then(()=>flash('All cleared', 1000));
    }
  };
  $('#toggleAll').onclick = () => {
    const anyActive = (boardData.tasks||[]).some(t=>!t.done);
    op({op:'set_all', done: anyActive}).then(()=>flash(anyActive?'Completed all':'Unchecked all', 1000));
  };

  // Switch/open board by slug
  $('#switch').onclick = () => {
    const s = (slugInput.value||'').trim();
    if (!s) return;
    window.location = `${origin}/?b=${encodeURIComponent(s)}`;
  };
  $('#newBoard').onclick = () => window.location = `${origin}/?action=new`;

  // Global keyboard
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === '/') { e.preventDefault(); input.focus(); }
    if (e.key === 'n' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      if (document.activeElement !== input && document.activeElement !== title) {
        input.focus();
      }
    }
  });

  // List interactions
  list.addEventListener('change', e => {
    const id = e.target.getAttribute('data-id');
    if (id && e.target.type === 'checkbox') { op({op:'toggle', id}); }
  });
  list.addEventListener('click', e => {
    const id = e.target.getAttribute('data-del');
    if (id) {
      const t = (boardData.tasks||[]).find(x=>x.id===id);
      op({op:'del', id}).then(()=>{ flash('Deleted', 900); if (t) showUndo({type:'del', payload: t}); });
    }
  });

  // List keyboard (item-level)
  list.addEventListener('keydown', (e) => {
    const li = e.target.closest('li');
    if (!li) return;
    // Per-item shortcuts when LI itself is focused
    if (e.target === li) {
      if (e.key === ' ') { e.preventDefault(); const cb = li.querySelector('input[type=checkbox]'); if (cb) { cb.checked = !cb.checked; cb.dispatchEvent(new Event('change')); } }
      if (e.key === 'Delete' || e.key === 'Backspace') {
        e.preventDefault();
        const id = li.querySelector('[data-del]')?.getAttribute('data-del');
        if (id) {
          const t = (boardData.tasks||[]).find(x=>x.id===id);
          op({op:'del', id}).then(()=>{ flash('Deleted', 900); if (t) showUndo({type:'del', payload: t}); });
        }
      }
      if (e.key.toLowerCase() === 'e') {
        e.preventDefault();
        const txt = li.querySelector('.txt');
        if (txt) txt.focus();
      }
    }
    // Contenteditable shortcuts
    if (e.target.classList.contains('txt')) {
      if (e.key === 'Enter') {
        e.preventDefault();
        e.target.blur(); // commit on blur
      } else if (e.key === 'Escape') {
        e.preventDefault();
        if (pendingEdit && pendingEdit.id === e.target.getAttribute('data-id')) {
          e.target.textContent = pendingEdit.orig;
        }
        e.target.blur();
        flash('Canceled', 800);
      } else if (e.key === 'Tab') {
        e.preventDefault();
        const els = Array.from(list.querySelectorAll('.txt'));
        const i = els.indexOf(e.target);
        const next = els[i + (e.shiftKey ? -1 : 1)];
        e.target.blur();
        if (next) next.focus();
      }
    }
  });

  // Inline edit lifecycle (commit-on-blur if changed)
  list.addEventListener('focusin', (e) => {
    if (e.target.classList.contains('txt')) {
      pendingEdit = { id: e.target.getAttribute('data-id'), orig: e.target.textContent };
      const range = document.createRange();
      range.selectNodeContents(e.target);
      range.collapse(false);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    }
  });
  list.addEventListener('blur', e => {
    if (e.target.classList.contains('txt')) {
      const id = e.target.getAttribute('data-id');
      const text = e.target.textContent.trim();
      if (pendingEdit && pendingEdit.id === id) {
        if (text !== pendingEdit.orig) {
          op({op:'edit', id, text}).then(()=>flash('Saved', 800));
        }
      }
      pendingEdit = null;
    }
  }, true);
});

// Initialize UI state
(function initUI() {
  updateFilterUI();
})();
</script>
```