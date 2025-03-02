---
tags: [tools]
layout: default
slug: extract-urls
comment: https://tools.simonwillison.net/extract-urls
---
<h2>Paste content here to extract URLs:</h2>
<div id="input" contenteditable="true"
     aria-label="Pasting Area"
     style="width: 90%; height: 150px; border: 1px solid black;">
  <p>Paste your content here...</p>
</div>

<h2>Extracted URLs</h2>
<textarea id="output" readonly style="width: 90%; height: 150px;"></textarea>
<br>
<button id="copy-button">Copy to clipboard</button>

<script>
  const inputDiv = document.getElementById('input');
  const outputTextarea = document.getElementById('output');
  const copyButton = document.getElementById('copy-button');

  /**
   * Removes trailing punctuation from URLs safely.
   */
  function cleanUrl(url) {
    return url.replace(/[)\]\}\.,!?;:'"]+$/, '');
  }

  /**
   * Extracts URLs explicitly from markdown links and plain text.
   */
  function extractUrls(text) {
    const urls = [];

    // Extract markdown-style links [text](url)
    const markdownLinkRegex = /\[.*?\]\((https?:\/\/[^\s)]+)\)/g;
    let match;
    while ((match = markdownLinkRegex.exec(text)) !== null) {
      urls.push(cleanUrl(match[1]));
    }

    // Remove markdown links from text to avoid duplication
    const textWithoutMarkdownLinks = text.replace(markdownLinkRegex, '');

    // Extract plain URLs (robustly handling parentheses)
    const plainUrlRegex = /\bhttps?:\/\/[^\s<>"'`)\]]+/gi;
    const plainUrls = textWithoutMarkdownLinks.match(plainUrlRegex) || [];
    plainUrls.forEach(url => urls.push(cleanUrl(url)));

    return urls;
  }

  /**
   * Handles paste events and displays extracted URLs.
   */
  function handlePaste(e) {
    e.preventDefault();
    const clipboardData = e.clipboardData || window.clipboardData;
    const pastedText = clipboardData.getData('text/plain');

    const urls = extractUrls(pastedText);

    if (urls.length > 0) {
      outputTextarea.value = urls.join('\n');
      inputDiv.innerText = 'Content pasted. URLs extracted.';
    } else {
      outputTextarea.value = 'No valid URLs found.';
      inputDiv.innerText = 'Content pasted. No URLs found.';
    }
  }

  /**
   * Copies extracted URLs to clipboard.
   */
  async function handleCopy() {
    if (!outputTextarea.value.trim()) {
      alert('No URLs to copy!');
      return;
    }
    try {
      await navigator.clipboard.writeText(outputTextarea.value);
      copyButton.textContent = 'Copied!';
      setTimeout(() => copyButton.textContent = 'Copy to clipboard', 1500);
    } catch {
      alert('Failed to copy. Please try again.');
    }
  }

  // Event listeners
  inputDiv.addEventListener('paste', handlePaste);
  copyButton.addEventListener('click', handleCopy);
</script>
