---
tags: [tools]
layout: default
slug: extract-urls
comment: https://tools.simonwillison.net/extract-urls
---
<h2>Paste content here to extract URLs:</h2>
<div id="input" contenteditable="true"
     aria-label="Pasting Area"
     tabindex="0"
     role="textbox"
     aria-multiline="true"
     style="width: 90%; height: 150px; border: 1px solid black; padding: 8px; margin-bottom: 10px;">
  <p>Paste your content here...</p>
</div>

<div id="output-container" style="display: none; margin-top: 20px;">
  <h2>Extracted URLs <span id="url-count" aria-live="polite"></span></h2>
  <textarea id="output" readonly aria-label="Extracted URLs" style="width: 90%; height: 150px; padding: 8px; margin-bottom: 10px;"></textarea>
  <div class="button-container">
    <button id="copy-button" aria-label="Copy URLs to clipboard">Copy to clipboard</button>
    <span id="status-message" aria-live="polite" style="margin-left: 10px;"></span>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/dompurify@latest/dist/purify.min.js"></script>
<script>
  // DOM Element References
  const inputDiv = document.getElementById('input');
  const outputContainer = document.getElementById('output-container');
  const outputTextarea = document.getElementById('output');
  const copyButton = document.getElementById('copy-button');
  const statusMessage = document.getElementById('status-message');
  const urlCount = document.getElementById('url-count');

  /**
   * Sanitizes HTML content to prevent XSS attacks using DOMPurify.
   * DOMPurify is essential for safely handling HTML from clipboard.
   * @param {string} html - The HTML content to sanitize
   * @returns {string} - Sanitized HTML string
   * @see {@link https://github.com/cure53/DOMPurify}
   */
  function sanitizeHtml(html) {
    return DOMPurify.sanitize(html);
  }

  /**
   * Validates and cleans a URL, ensuring it's a valid HTTP or HTTPS URL.
   * Also removes trailing punctuation that is unlikely to be part of the URL.
   * @param {string} url - The URL to validate and clean
   * @returns {string|null} - Cleaned URL or null if invalid
   */
  function validateAndCleanUrl(url) {
    // Remove trailing punctuation that might be part of surrounding text
    const cleanedUrl = url.replace(/[)\]\}\.,!?;:'"]+$/, '').trim();

    try {
      // Use URL constructor for robust URL validation
      const urlObj = new URL(cleanedUrl);
      // Ensure protocol is either HTTP or HTTPS
      if (!['http:', 'https:'].includes(urlObj.protocol)) {
        return null; // Not a valid HTTP/HTTPS URL
      }
      return cleanedUrl;
    } catch (e) {
      // URL constructor throws error for invalid URLs
      return null; // Invalid URL format
    }
  }

  /**
   * Extracts URLs from the pasted content, handling HTML, markdown, and plain text formats.
   * Prioritizes HTML link extraction for rich content, then falls back to markdown and plain text.
   * @param {string} htmlContent - The HTML content if available (sanitized)
   * @param {string} plainText - The plain text content
   * @returns {string[]} - Array of unique, validated, and cleaned URLs
   */
  function extractUrls(htmlContent, plainText) {
    const urls = new Set(); // Using Set to automatically handle duplicate URLs

    // 1. Extract URLs from HTML content (if available and sanitized)
    if (htmlContent) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = htmlContent; // Already sanitized by sanitizeHtml function

      // Extract URLs from anchor tags (<a> elements with href attribute)
      Array.from(tempDiv.querySelectorAll('a[href]'))
        .map(link => link.getAttribute('href'))
        .forEach(url => {
          const validatedUrl = validateAndCleanUrl(url);
          if (validatedUrl) {
            urls.add(validatedUrl);
          }
        });
    }

    // 2. Extract markdown-style links [text](url) from plain text
    const markdownLinkRegex = /\[(?:[^\]]*)\]\((https?:\/\/[^\s)]+)\)/g;
    let markdownMatch;
    while ((markdownMatch = markdownLinkRegex.exec(plainText)) !== null) {
      const validatedUrl = validateAndCleanUrl(markdownMatch[1]);
      if (validatedUrl) {
        urls.add(validatedUrl);
      }
    }

    // 3. Extract plain URLs from plain text (excluding markdown links to avoid duplicates)
    const textWithoutMarkdownLinks = plainText.replace(markdownLinkRegex, '');
    // Improved regex for plain URLs to catch more complex URL patterns including international characters and paths
    const plainUrlRegex = /\bhttps?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)/gi;
    const plainTextMatches = textWithoutMarkdownLinks.match(plainUrlRegex) || [];
    plainTextMatches.forEach(url => {
      const validatedUrl = validateAndCleanUrl(url);
      if (validatedUrl) {
        urls.add(validatedUrl);
      }
    });

    return Array.from(urls); // Convert Set to Array for output
  }

  /**
   * Updates the UI status message with feedback for the user.
   * Uses ARIA live regions for accessibility, making status updates screen reader friendly.
   * @param {string} message - The status message to display
   * @param {string} type - Type of message (success, info, error) for styling and semantics
   * @param {number} duration - Duration in milliseconds to show message (0 for persistent)
   */
  function showStatus(message, type = 'info', duration = 2000) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`; // For potential CSS styling
    statusMessage.setAttribute('aria-live', 'polite'); // For screen reader announcements

    if (duration > 0) {
      setTimeout(() => {
        statusMessage.textContent = '';
        statusMessage.className = 'status-message';
        statusMessage.removeAttribute('aria-live');
      }, duration);
    }
  }

  /**
   * Handles the paste event, extracts URLs from clipboard data, and updates the UI.
   * Processes both 'text/html' and 'text/plain' clipboard data formats.
   * @param {ClipboardEvent} event - The paste event
   */
  function handlePaste(event) {
    event.preventDefault(); // Prevent default paste behavior

    const clipboardData = event.clipboardData || window.clipboardData;
    const plainText = clipboardData.getData('text/plain') || '';
    const htmlContent = clipboardData.getData('text/html') || '';

    try {
      // Sanitize HTML content before processing to prevent XSS
      const sanitizedHtml = htmlContent ? sanitizeHtml(htmlContent) : null;
      const extractedUrls = extractUrls(sanitizedHtml, plainText);

      if (extractedUrls.length > 0) {
        outputTextarea.value = extractedUrls.join('\n');
        urlCount.textContent = `(${extractedUrls.length} found)`; // Update URL count display
        inputDiv.innerHTML = '<p>Content pasted. URLs extracted.</p>'; // Update input area message
        showStatus(`Extracted ${extractedUrls.length} URLs`, 'success', 3000); // Show success status
      } else {
        outputTextarea.value = ''; // Clear output textarea
        urlCount.textContent = '(none found)';
        inputDiv.innerHTML = '<p>Content pasted. No URLs found.</p>'; // Update input area message
        showStatus('No URLs found in pasted content', 'info', 3000); // Show info status
      }
      outputContainer.style.display = 'block'; // Make output container visible

    } catch (extractionError) {
      // Handle any errors during URL extraction process
      console.error('URL Extraction Error:', extractionError);
      outputTextarea.value = '';
      urlCount.textContent = '(error)';
      inputDiv.innerHTML = '<p>Error processing pasted content.</p>'; // Update input area message
      showStatus('Error extracting URLs. Please try again.', 'error', 0); // Show persistent error status
      outputContainer.style.display = 'block'; // Ensure output container is visible to show error
    }
  }

  /**
   * Handles the focus event for the input div, clearing any placeholder messages.
   * Improves user experience by resetting input area for new input.
   */
  function handleFocus() {
    const placeholderMessages = [
      '<p>Content pasted. URLs extracted.</p>',
      '<p>Content pasted. No URLs found.</p>',
      '<p>Error processing pasted content.</p>',
      '<p>Paste your content here...</p>'
    ];
    if (placeholderMessages.some(message => inputDiv.innerHTML === message)) {
      inputDiv.innerHTML = ''; // Clear input area content
    }
  }

  /**
   * Handles the copy button click event, copying extracted URLs to the clipboard.
   * Uses modern clipboard API if available, falls back to document.execCommand('copy') for older browsers.
   */
  async function handleCopy() {
    const urlsToCopy = outputTextarea.value.trim();

    if (!urlsToCopy) {
      showStatus('No URLs to copy!', 'error'); // Show error status if no URLs to copy
      return; // Exit function early
    }

    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        // Modern Clipboard API is supported
        await navigator.clipboard.writeText(urlsToCopy);
        showStatus('URLs copied to clipboard!', 'success'); // Show success status
      } else {
        // Fallback for older browsers using document.execCommand('copy')
        outputTextarea.select(); // Select textarea content
        document.execCommand('copy'); // Execute copy command
        showStatus('URLs copied to clipboard!', 'success'); // Show success status
        outputTextarea.selectionStart = outputTextarea.selectionEnd; // Deselect text
      }
    } catch (copyError) {
      // Handle clipboard copy errors
      console.error('Clipboard Copy Error:', copyError);
      showStatus('Failed to copy URLs. Please try again or copy manually.', 'error', 0); // Show persistent error status
    }
  }

  // Event Listeners setup
  inputDiv.addEventListener('paste', handlePaste); // Attach paste event handler
  inputDiv.addEventListener('focus', handleFocus); // Attach focus event handler
  copyButton.addEventListener('click', handleCopy); // Attach copy button click handler
</script>

<style>
  /* Basic styling for status messages and button container */
  .status-message {
    margin-left: 10px;
    font-size: 0.9em;
  }
  .status-message.success {
    color: green;
  }
  .status-message.error {
    color: red;
  }
  .status-message.info {
    color: black;
  }
  .button-container {
    display: flex; /* Use flexbox to align button and status message */
    align-items: center; /* Vertically align items in container */
  }
</style>
