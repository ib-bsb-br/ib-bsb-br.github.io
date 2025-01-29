---
tags: tools
layout: default
slug: extract-urls
comment: https://tools.simonwillison.net/extract-urls
---
<div id="input-container">
  <h2>Copy content and paste here to extract linked URLs:</h2>
  <div id="input" contenteditable="true" aria-label="Input Area" tabindex="0" role="textbox" aria-multiline="true">
    <p>Paste your content here...</p>
  </div>
</div>

<div id="output-container" style="display: none;">
  <h2>Extracted URLs</h2>
  <textarea id="output" readonly aria-label="Extracted URLs"></textarea>
  <button id="copy-button">Copy to clipboard</button>
</div>

<script>
  const inputDiv = document.getElementById('input');
  const outputContainer = document.getElementById('output-container');
  const outputTextarea = document.getElementById('output');
  const copyButton = document.getElementById('copy-button');

  /**
   * Extracts URLs from the pasted content.
   * @param {ClipboardEvent} e - The paste event.
   */
  const handlePaste = (e) => {
    e.preventDefault();
    const clipboardData = e.clipboardData || window.clipboardData;
    const pastedData = clipboardData.getData('text/html') || clipboardData.getData('text/plain');

    let urls = [];

    if (clipboardData.types.includes('text/html')) {
      // Extract URLs from HTML content
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = pastedData;
      // If robust sanitization is needed, consider using a library like DOMPurify:
      // tempDiv.innerHTML = DOMPurify.sanitize(pastedData);
      const links = tempDiv.getElementsByTagName('a');
      urls = Array.from(links)
        .map(link => link.href)
        .filter(url => url.startsWith('http'));
    } else {
      // Extract URLs from plain text using a regular expression
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      urls = pastedData.match(urlRegex) || [];
    }

    if (urls.length > 0) {
      outputTextarea.value = urls.join('\n');
      outputContainer.style.display = 'block';
      inputDiv.innerHTML = '<p>Content pasted. URLs extracted.</p>';
    } else {
      outputContainer.style.display = 'block'; // Show output container even if no URLs are found
      outputTextarea.value = 'No valid URLs found in the pasted content.';
      inputDiv.innerHTML = '<p>Content pasted. No URLs found.</p>';
    }
  };

  /**
   * Clears the input message when the input area gains focus.
   */
  const handleFocus = () => {
    const messages = ['Content pasted. URLs extracted.', 'Content pasted. No URLs found.', '<p>Paste your content here...</p>'];
    if (messages.includes(inputDiv.innerHTML)) {
      inputDiv.innerHTML = '';
    }
  };

  /**
   * Copies the extracted URLs to the clipboard.
   */
  const handleCopy = async () => {
    if (outputTextarea.value.trim() === '') {
      outputTextarea.value = 'No content to copy!';
      return;
    }
    try {
      await navigator.clipboard.writeText(outputTextarea.value);
      const originalText = copyButton.textContent;
      copyButton.textContent = 'Copied!';
      setTimeout(() => {
        copyButton.textContent = originalText;
      }, 1500);
    } catch (err) {
      console.error('Failed to copy!', err);
      outputTextarea.value = 'Failed to copy the URLs. Please try again.';
    }
  };

  // Event Listeners
  inputDiv.addEventListener('paste', handlePaste);
  inputDiv.addEventListener('focus', handleFocus);
  copyButton.addEventListener('click', handleCopy);
</script>
