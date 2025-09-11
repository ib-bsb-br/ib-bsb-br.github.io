<?php
declare(strict_types=1);

require_once __DIR__ . '/config.php';

// Handle CORS pre-flight requests for cross-domain JS
handle_cors_preflight();

// Simple router
$request_uri = $_GET['q'] ?? '';
$parts = explode('/', $request_uri);
$resource = $parts[0] ?? null;
$resource_id = $parts[1] ?? null;

try {
    switch ($resource) {
        case 'files':
            require_once __DIR__ . '/files.php';
            handle_files_request($resource_id);
            break;

        case 'tasks':
            require_once __DIR__ . '/tasks.php';
            handle_tasks_request($resource_id);
            break;

        case 'links':
            require_once __DIR__ . '/links.php';
            handle_links_request($resource_id);
            break;

        case 'published':
            // A simple endpoint to fetch all published content for the Jekyll site
            $pdo = get_pdo();
            $stmt = $pdo->query("SELECT id, board_slug, text, updated_at FROM tasks WHERE is_published = 1 ORDER BY updated_at DESC");
            $published_tasks = $stmt->fetchAll();
            emit_json(['tasks' => $published_tasks]);
            break;

        default:
            emit_json(['error' => 'Resource not found.'], 404);
            break;
    }
} catch (Exception $e) {
    // Basic global error handler
    // In a real app, you would log the error message.
    error_log($e->getMessage());
    emit_json(['error' => 'An internal server error occurred.'], 500);
}
?>
