---
tags: tools
layout: default
slug: extract-urls
comment: 'bibref: https://tools.simonwillison.net/extract-urls'
---


<h1>Extract URLs</h1>
<p>Copy content from a web page and paste here to extract linked URLs:</p>

<div id="output-container" contenteditable="true"></div>

<div id="output-container">
    <h2>Extracted</h2>
    <textarea id="output" readonly></textarea>
    <button id="copy-button">Copy to clipboard</button>
</div>

<script>
    const input = document.getElementById('input');
    const outputContainer = document.getElementById('output-container');
    const output = document.getElementById('output');
    const copyButton = document.getElementById('copy-button');

    input.addEventListener('paste', function(e) {
        e.preventDefault();

        const clipboardData = e.clipboardData || window.clipboardData;
        const pastedData = clipboardData.getData('text/html');

        const temp = document.createElement('div');
        temp.innerHTML = pastedData;

        const links = temp.getElementsByTagName('a');
        const urls = Array.from(links)
            .map(link => link.href)
            .filter(url => url.startsWith('http'));

        if (urls.length > 0) {
            output.value = urls.join('\n');
            outputContainer.style.display = 'block';
        } else {
            outputContainer.style.display = 'none';
        }

        input.textContent = 'Content pasted. URLs extracted.';
    });

    input.addEventListener('focus', function() {
        if (input.textContent === 'Content pasted. URLs extracted.') {
            input.textContent = '';
        }
    });

    copyButton.addEventListener('click', function() {
        output.select();
        document.execCommand('copy');

        const originalText = copyButton.textContent;
        copyButton.textContent = 'Copied!';

        setTimeout(() => {
            copyButton.textContent = originalText;
        }, 1500);
    });
</script>
