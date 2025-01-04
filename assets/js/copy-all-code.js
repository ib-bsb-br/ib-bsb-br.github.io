document.addEventListener('DOMContentLoaded', function () {
  const copyAllButton = document.getElementById('copyAllButton');

  if (copyAllButton) {
    copyAllButton.addEventListener('click', function () {
      // Collect all code block contents
      const codeBlocks = document.querySelectorAll('pre code, code[class*="language-"]');
      let combinedCode = '';

      codeBlocks.forEach(function (block, index) {
        combinedCode += block.textContent.trim();
        if (index < codeBlocks.length - 1) {
          combinedCode += '\n\n'; // Add spacing between code blocks
        }
      });

      if (!combinedCode) {
        showCopyErrorMessage('No code blocks found.');
        return;
      }

      // Copy the combined code to the clipboard
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(combinedCode).then(function () {
          showCopySuccessMessage();
        }, function (err) {
          console.error('Failed to copy text: ', err);
          showCopyErrorMessage('Failed to copy code blocks.');
        });
      } else {
        fallbackCopyTextToClipboard(combinedCode);
      }
    });
  }

  function showCopySuccessMessage() {
    displayMessage('All code blocks have been copied to the clipboard!', true);
  }

  function showCopyErrorMessage(message) {
    displayMessage(message || 'Failed to copy code blocks. Please try again.', false);
  }

  function displayMessage(text, isSuccess) {
    const message = document.createElement('div');
    message.textContent = text;
    message.style.position = 'fixed';
    message.style.bottom = '20px';
    message.style.left = '50%';
    message.style.transform = 'translateX(-50%)';
    message.style.backgroundColor = isSuccess ? '#4caf50' : '#f44336';
    message.style.color = 'white';
    message.style.padding = '10px 20px';
    message.style.borderRadius = '5px';
    message.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
    message.style.zIndex = '1000';
    message.setAttribute('role', 'alert');

    document.body.appendChild(message);

    setTimeout(function () {
      message.style.transition = 'opacity 0.5s';
      message.style.opacity = '0';
      setTimeout(function () {
        document.body.removeChild(message);
      }, 500);
    }, 3000); // Message disappears after 3 seconds
  }

  function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;

    // Move textarea off-screen
    textArea.style.position = 'fixed';
    textArea.style.top = '-9999px';
    textArea.setAttribute('readonly', '');

    document.body.appendChild(textArea);
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      if (successful) {
        showCopySuccessMessage();
      } else {
        showCopyErrorMessage();
      }
    } catch (err) {
      console.error('Fallback: Could not copy text', err);
      showCopyErrorMessage();
    }

    document.body.removeChild(textArea);
  }
});
