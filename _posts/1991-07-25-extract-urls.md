---
tags: tools
layout: default
slug: extract-urls
comment: https://tools.simonwillison.net/extract-urls
---

<h2>Copy content from a web page and paste here to extract linked URLs:</h2>

<!-- Pasting Area -->
<div id="paste-area" contenteditable="true" style="
  border: 1px solid #ccc;
  padding: 1em;
  min-height: 5em;
  margin-bottom: 1em;
">
  <!-- The user will paste HTML content here -->
</div>

<!-- Output Container (hidden by default) -->
<div id="output-container" style="display: none;">
  <h2>Extracted URLs</h2>
  <textarea id="output" readonly style="width: 100%; height: 6em;"></textarea>
  <button id="copy-button">Copy URLs</button>
</div>

<script>
(function() {
  'use strict';

  const pasteArea = document.getElementById('paste-area');
  const outputContainer = document.getElementById('output-container');
  const output = document.getElementById('output');
  const copyButton = document.getElementById('copy-button');

  // Optional: Basic sanitization to text (removes HTML tags)
  // A thorough approach would require a specialized library.
  function sanitizeHTML(html) {
    const temp = document.createElement('div');
    temp.textContent = html;
    return temp.innerHTML;
  }

  // Extract URLs from pasted HTML
  pasteArea.addEventListener('paste', (e) => {
    e.preventDefault();
    const clipboardData = e.clipboardData || window.clipboardData;
    // Attempt to read HTML; fallback to plain text if unavailable
    let pastedContent = clipboardData.getData('text/html')
      || clipboardData.getData('text/plain')
      || '';

    // Sanitize if we wish to avoid embedding HTML
    pastedContent = sanitizeHTML(pastedContent);

    // Create a temporary container to parse the HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = pastedContent;

    const links = tempDiv.querySelectorAll('a');
    const urls = Array.from(links)
      .map(link => link.href)
      .filter(url => url.startsWith('http'));

    if (urls.length > 0) {
      output.value = urls.join('\\n');
      outputContainer.style.display = 'block';
    } else {
      output.value = '';
      outputContainer.style.display = 'none';
      alert('No valid URLs found.');
    }

    // Replace the user’s pasted content with a simple message (optional)
    pasteArea.textContent = 'URLs extracted – you can paste again.';
  });

  // Copy to clipboard
  copyButton.addEventListener('click', () => {
    // Try the modern API first
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(output.value)
        .then(() => {
          showCopyFeedback();
        })
        .catch(() => {
          fallbackCopy();
        });
    } else {
      fallbackCopy();
    }
  });

  // Provide fallback for older browsers
  function fallbackCopy() {
    output.select();
    document.execCommand('copy');
    showCopyFeedback();
  }

  // Give user a quick “Copied!” feedback
  function showCopyFeedback() {
    const originalText = copyButton.textContent;
    copyButton.textContent = 'Copied!';
    setTimeout(() => {
      copyButton.textContent = originalText;
    }, 1500);
  }
})();
</script>
