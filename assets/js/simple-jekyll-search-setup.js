(function () {
  const STORAGE_KEY = 'sjs-search-state';
  const STATE_TTL_MS = 30 * 60 * 1000;
  const SKIP_KEYS = new Set([
    'Enter', 'Shift', 'Control', 'Alt', 'Meta', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    'Escape', 'Tab', 'CapsLock', 'PageUp', 'PageDown', 'Home', 'End'
  ]);

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function findLiteralMatches(text, criteria) {
    const input = criteria.trim().toLowerCase();
    if (!input) return [];
    const words = criteria.endsWith(' ') ? [input] : input.split(/\s+/);
    const lowerText = text.toLowerCase();
    if (!words.every((word) => lowerText.includes(word))) return [];

    const matches = [];
    words.forEach((word) => {
      let index = 0;
      while (word && (index = lowerText.indexOf(word, index)) !== -1) {
        matches.push({ start: index, end: index + word.length, type: 'exact' });
        index += word.length;
      }
    });

    return matches;
  }

  function findFuzzyMatches(text, criteria) {
    const query = criteria.trimEnd();
    if (!query) return [];
    const lowerText = text.toLowerCase();
    const lowerQuery = query.toLowerCase();

    let ti = 0;
    let qi = 0;
    const indices = [];

    while (ti < lowerText.length && qi < lowerQuery.length) {
      if (lowerText[ti] === lowerQuery[qi]) {
        indices.push(ti);
        qi += 1;
      }
      ti += 1;
    }

    if (qi !== lowerQuery.length || indices.length === 0) {
      return [];
    }

    return [{
      start: indices[0],
      end: indices[indices.length - 1] + 1,
      type: 'fuzzy'
    }];
  }

  function wildcardRegex(pattern) {
    const escaped = pattern
      .replace(/[.+?^${}()|[\]\\]/g, '\\$&')
      .replace(/\*/g, '[^ ]*(?: [^ ]*)?');
    return new RegExp(escaped, 'gi');
  }

  function findWildcardMatches(text, criteria) {
    if (!criteria.includes('*')) return [];
    const re = wildcardRegex(criteria.trim());
    const matches = [];
    let match;
    while ((match = re.exec(text)) !== null) {
      matches.push({ start: match.index, end: match.index + match[0].length, type: 'wildcard' });
      if (re.lastIndex === match.index) re.lastIndex += 1;
    }
    return matches;
  }

  function hybridFind(text, criteria) {
    if (criteria.includes('*')) {
      const wildcard = findWildcardMatches(text, criteria);
      if (wildcard.length) return wildcard;
    }

    const literal = findLiteralMatches(text, criteria);
    if (literal.length) return literal;

    if (criteria.trim().length >= 4) {
      const fuzzy = findFuzzyMatches(text, criteria);
      if (fuzzy.length) return fuzzy;
    }

    return [];
  }

  function mergeRanges(ranges) {
    if (!ranges.length) return [];
    const sorted = [...ranges].sort((a, b) => a.start - b.start || a.end - b.end);
    const merged = [sorted[0]];

    for (let i = 1; i < sorted.length; i += 1) {
      const current = sorted[i];
      const last = merged[merged.length - 1];
      if (current.start <= last.end) {
        last.end = Math.max(last.end, current.end);
      } else {
        merged.push({ ...current });
      }
    }

    return merged;
  }

  function highlightText(text, matches) {
    const safeText = escapeHtml(text);
    if (!matches.length) return safeText;

    const merged = mergeRanges(matches);
    let html = '';
    let cursor = 0;

    merged.forEach((match) => {
      const start = Math.max(0, Math.min(match.start, text.length));
      const end = Math.max(start, Math.min(match.end, text.length));
      html += escapeHtml(text.slice(cursor, start));
      html += '<mark class="search-highlight">' + escapeHtml(text.slice(start, end)) + '</mark>';
      cursor = end;
    });

    html += escapeHtml(text.slice(cursor));
    return html;
  }

  function saveState(query) {
    if (!query.trim()) {
      sessionStorage.removeItem(STORAGE_KEY);
      return;
    }

    const payload = {
      query,
      timestamp: Date.now(),
      path: window.location.pathname
    };

    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  }

  function loadState() {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return '';

    try {
      const state = JSON.parse(raw);
      const validPath = typeof state.path === 'string' && state.path === window.location.pathname;
      const validQuery = typeof state.query === 'string';
      const validTimestamp = typeof state.timestamp === 'number';
      const fresh = validTimestamp && Date.now() - state.timestamp <= STATE_TTL_MS;

      if (!validPath || !validQuery || !fresh) {
        sessionStorage.removeItem(STORAGE_KEY);
        return '';
      }

      return state.query;
    } catch (_error) {
      sessionStorage.removeItem(STORAGE_KEY);
      return '';
    }
  }

  function withQuery(url, query) {
    try {
      const parsed = new URL(url, window.location.origin);
      parsed.searchParams.set('query', query);
      return parsed.toString();
    } catch (_error) {
      return url;
    }
  }

  function mountSearch(posts) {
    const input = document.getElementById('search-input');
    const results = document.getElementById('results-container');
    const status = document.getElementById('search-status');

    if (!input || !results || !status) return;

    function render(query) {
      const trimmed = query.trim();
      results.innerHTML = '';

      if (!trimmed) {
        status.textContent = 'Type to search all posts.';
        return;
      }

      const found = posts
        .map((post) => {
          const haystack = [post.title, post.desc, post.tags].join(' ');
          const matches = hybridFind(haystack, trimmed);
          return { post, matches };
        })
        .filter((entry) => entry.matches.length)
        .slice(0, 20);

      if (!found.length) {
        status.textContent = 'No results found.';
        results.innerHTML = '<li class="search-empty">No results found</li>';
        return;
      }

      status.textContent = `Showing ${found.length} result(s).`;
      found.forEach(({ post }) => {
        const titleMatches = hybridFind(post.title, trimmed);
        const descMatches = hybridFind(post.desc, trimmed);
        const item = document.createElement('li');
        item.className = 'search-item';
        item.innerHTML = [
          '<a href="' + escapeHtml(withQuery(post.url, trimmed)) + '">',
          '<span class="search-title">' + highlightText(post.title, titleMatches) + '</span>',
          '<span class="search-desc">' + highlightText(post.desc, descMatches) + '</span>',
          '<span class="search-meta">' + escapeHtml(post.date) + '</span>',
          '</a>'
        ].join('');
        results.appendChild(item);
      });
    }

    input.addEventListener('keyup', (event) => {
      if (SKIP_KEYS.has(event.key)) return;
      saveState(input.value);
      render(input.value);
    });

    input.addEventListener('search', () => {
      saveState(input.value);
      render(input.value);
    });

    const qp = new URLSearchParams(window.location.search).get('query');
    const initial = (qp || loadState() || '').trim();
    if (initial) {
      input.value = initial;
      saveState(initial);
      render(initial);
    }
  }

  window.addEventListener('DOMContentLoaded', async () => {
    try {
      const dataUrl = new URL('assets/data/search.json', document.baseURI).toString();
      const response = await fetch(dataUrl, { cache: 'no-cache' });
      const posts = await response.json();
      if (!Array.isArray(posts)) throw new Error('Invalid search data payload');
      mountSearch(posts);
    } catch (_error) {
      const status = document.getElementById('search-status');
      if (status) {
        status.textContent = 'Search index could not be loaded.';
      }
    }
  });
})();
