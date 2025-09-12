<?php
declare(strict_types=1);

// --- CONFIGURATION ---
const API_BASE_URL = 'https://arcreformas.com.br/api';

// --- ROUTER ---
$op = $_GET['op'] ?? '';
$slug = $_GET['s'] ?? '';

// 1. Handle Quick Add Task
if ($op === 'task_add') {
    $text = trim((string)($_GET['text'] ?? ''));
    $board = trim((string)($_GET['b'] ?? 'inbox'));

    if ($text !== '') {
        // Make a server-to-server call to the central API to create the task
        $taskPayload = json_encode(['op' => 'add', 'text' => $text]);
        $ch = curl_init();
        $tasks_api_url = API_BASE_URL . '/tasks/' . rawurlencode($board);
        curl_setopt($ch, CURLOPT_URL, $tasks_api_url);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $taskPayload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 3);
        curl_exec($ch);
        curl_close($ch);
    }

    // Redirect the user to their board to see the new task
    header('Location: https://memor.ia.br/?b=' . rawurlencode($board), true, 303);
    exit;
}


// 2. Handle Redirection
if ($slug !== '') {
        // For better error handling or if allow_url_fopen is off, use cURL.
        $context = stream_context_create(['http' => ['ignore_errors' => true]]);
        $response_json = file_get_contents(API_BASE_URL . '/links/' . rawurlencode($slug), false, $context);
        $response_data = $response_json ? json_decode($response_json, true) : null;

        if (isset($response_data['url'])) {
            header('Location: ' . $response_data['url'], true, 302);
            exit;
        }
    }
    // If slug not found or empty, show an error
    http_response_code(404);
    echo '<!doctype html><meta charset="utf-8"><title>Not Found</title><h1>Link Not Found</h1><p>The short link you requested does not exist or has been removed.</p><p><a href="/">Create a new short link</a></p>';
    exit;
}

// If not a redirection, render the HTML page below.
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex">
  <title>cut.ia.br — URL shortener</title>
  <style>
    :root { color-scheme: light dark; --bg: #fff; --fg: #111; --border: #ccc; --accent: #111; --err: #c00; --ok: #080; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #0c0c0c; --fg: #eee; --border: #444; --accent: #eee; }
    }
    body { font: 16px/1.5 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem auto; padding: 0 1rem; max-width: 720px; background: var(--bg); color: var(--fg); }
    h1 { margin-bottom: 1.5rem; }
    form { display: flex; flex-direction: column; }
    input[type=url] { width: 100%; padding: .75rem; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; background: transparent; color: var(--fg); box-sizing: border-box; }
    button { margin-top: .75rem; padding: .75rem 1.25rem; border: 0; border-radius: 8px; background: var(--accent); color: var(--bg); cursor: pointer; font-size: 1rem; font-weight: 500; }
    #result { margin-top: 1.5rem; padding: 1rem; border-radius: 8px; word-wrap: break-word; display: none; }
    #result.success { background-color: rgba(0, 128, 0, 0.1); border: 1px solid var(--ok); color: var(--ok); }
    #result.error { background-color: rgba(204, 0, 0, 0.1); border: 1px solid var(--err); color: var(--err); }
    #result a { color: var(--ok); font-weight: bold; }
    small { color: #777; margin-top: 2rem; display: block; }
  </style>
</head>
<body>
  <h1>URL Shortener</h1>
  <form id="shortenForm">
    <input type="url" name="url" id="urlInput" placeholder="https://example.com/a/very/long/link/to/shorten" required>
    <button type="submit">Shorten</button>
  </form>
  <div id="result"></div>
  <p><small>Tip: bookmarklet — drag this to your toolbar: <a href="javascript:location.href='https://<?= htmlspecialchars($_SERVER['HTTP_HOST'] ?? '') ?>/?add='+encodeURIComponent(location.href)">shorten page</a></small></p>

<script>
  const form = document.getElementById('shortenForm');
  const urlInput = document.getElementById('urlInput');
  const resultDiv = document.getElementById('result');
  const apiEndpoint = '<?= API_BASE_URL ?>/links';

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const longUrl = urlInput.value.trim();
    if (!longUrl) return;

    resultDiv.style.display = 'none';
    resultDiv.className = '';

    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: longUrl })
      });

      const data = await response.json();

      if (!response.ok || data.status !== 'success') {
        throw new Error(data.error || 'An unknown error occurred.');
      }

      resultDiv.className = 'success';
      resultDiv.innerHTML = `Success! Your short link is: <a href="${data.short_url}" target="_blank">${data.short_url}</a>`;
      resultDiv.style.display = 'block';
      urlInput.value = ''; // Clear input on success

    } catch (err) {
      resultDiv.className = 'error';
      resultDiv.textContent = `Error: ${err.message}`;
      resultDiv.style.display = 'block';
    }
  });
</script>
</body>
</html>
