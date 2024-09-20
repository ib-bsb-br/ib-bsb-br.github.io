---
tags:
  - tools
layout: default
slug: dedup-spaces
---
<div class="editor-container">
    <div class="editor-ui">
        <textarea id="input-data" placeholder="Paste your text here..."></textarea>
    </div>
    <div>
        <button class="convert-btn" id="remove-duplicate-spaces" onclick="remove_duplicate_spaces()">Remove Duplicate Spaces</button>
        <button class="convert-btn" id="copy-btn" onclick="copyTextToClipboard()">Copy</button>
    </div>
    <div class="editor-ui">
        <textarea id="result" placeholder="Result will show here..." readonly></textarea>
    </div>
</div>
<script type="text/javascript">
    function remove_duplicate_spaces() {
        var input_data = document.getElementById("input-data");
        var result = document.getElementById("result");
        result.value = input_data.value.replace(/\s+/g,' ');
    }
</script>
<script>
    function fallbackCopyTextToClipboard(text) {
        var textArea = document.createElement("textarea");
        textArea.value = text;

        // Avoid scrolling to bottom
        textArea.style.top = "0";
        textArea.style.left = "0";
        textArea.style.position = "fixed";

        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Fallback: Copying text command was ' + msg);
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
        }

        document.body.removeChild(textArea);
    }

    function copyTextToClipboard() {

        let text = document.getElementById('result').value
    
        if (!navigator.clipboard) {
            fallbackCopyTextToClipboard(text);
            return;
        }
        navigator.clipboard.writeText(text).then(function () {
            console.log('Async: Copying to clipboard was successful!');
        }, function (err) {
            console.error('Async: Could not copy text: ', err);
        });
    }
</script>
