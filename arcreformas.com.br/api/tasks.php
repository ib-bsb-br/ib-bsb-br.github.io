<?php
declare(strict_types=1);

function handle_tasks_request(?string $board_slug): void {
    if (empty($board_slug)) {
        emit_json(['error' => 'Board slug not specified.'], 400);
        return;
    }

    $method = $_SERVER['REQUEST_METHOD'];
    $pdo = get_pdo();

    // Ensure board exists, or create it on demand. This requires a UNIQUE index on the 'slug' column.
    $stmt = $pdo->prepare("INSERT IGNORE INTO boards (slug, title) VALUES (?, ?)");
    $stmt->execute([$board_slug, 'Board: ' . htmlspecialchars($board_slug)]);

    switch ($method) {
        case 'GET':
            emit_json(get_board_state($pdo, $board_slug));
            break;
        case 'POST':
            handle_task_operations($pdo, $board_slug);
            break;
        default:
            emit_json(['error' => 'Method not allowed for this resource.'], 405);
            break;
    }
}

function get_board_state(PDO $pdo, string $board_slug): array {
    $stmt = $pdo->prepare("SELECT title, created_at, updated_at FROM boards WHERE slug = ?");
    $stmt->execute([$board_slug]);
    $board = $stmt->fetch();
    if (!$board) {
        // This should not happen due to the check in handle_tasks_request
        return ['title' => 'New Board', 'tasks' => [], 'created' => time(), 'updated' => time()];
    }

    $stmt = $pdo->prepare("SELECT id, text, is_done AS done, created_at AS ts FROM tasks WHERE board_slug = ? ORDER BY sort_order ASC, created_at ASC");
    $stmt->execute([$board_slug]);
    $tasks = $stmt->fetchAll();

    // Convert timestamps to unix timestamps for JS
    $board['created'] = strtotime($board['created_at']);
    $board['updated'] = strtotime($board['updated_at']);
    unset($board['created_at'], $board['updated_at']);

    foreach ($tasks as &$task) {
        $task['done'] = (bool)$task['done'];
        $task['ts'] = strtotime($task['ts']);
    }

    $board['tasks'] = $tasks;
    return $board;
}

function handle_task_operations(PDO $pdo, string $board_slug): void {
    $input = json_decode(file_get_contents('php://input'), true) ?? [];
    $op = $input['op'] ?? '';

    $pdo->beginTransaction();
    try {
        switch ($op) {
            case 'add':
                $text = trim((string)($input['text'] ?? ''));
                if ($text !== '') {
                    $stmt = $pdo->prepare("INSERT INTO tasks (id, board_slug, text) VALUES (?, ?, ?)");
                    $stmt->execute([id(), $board_slug, $text]);
                }
                break;

            case 'toggle':
                $id = (string)($input['id'] ?? '');
                $stmt = $pdo->prepare("UPDATE tasks SET is_done = !is_done WHERE id = ? AND board_slug = ?");
                $stmt->execute([$id, $board_slug]);
                break;

            case 'edit':
                $id = (string)($input['id'] ?? '');
                $text = trim((string)($input['text'] ?? ''));
                $stmt = $pdo->prepare("UPDATE tasks SET text = ? WHERE id = ? AND board_slug = ?");
                $stmt->execute([$text, $id, $board_slug]);
                break;

            case 'del':
                $id = (string)($input['id'] ?? '');
                $stmt = $pdo->prepare("DELETE FROM tasks WHERE id = ? AND board_slug = ?");
                $stmt->execute([$id, $board_slug]);
                break;

            case 'title':
                $title = trim((string)($input['title'] ?? 'My Board'));
                $stmt = $pdo->prepare("UPDATE boards SET title = ? WHERE slug = ?");
                $stmt->execute([$title, $board_slug]);
                break;

            case 'clear_done':
                $stmt = $pdo->prepare("DELETE FROM tasks WHERE is_done = 1 AND board_slug = ?");
                $stmt->execute([$board_slug]);
                break;

            case 'set_all':
                $done = (bool)($input['done'] ?? false);
                $stmt = $pdo->prepare("UPDATE tasks SET is_done = ? WHERE board_slug = ?");
                $stmt->execute([$done, $board_slug]);
                break;

            case 'clear_all':
                $stmt = $pdo->prepare("DELETE FROM tasks WHERE board_slug = ?");
                $stmt->execute([$board_slug]);
                break;

            case 'reorder':
                $order = $input['order'] ?? [];
                if (is_array($order)) {
                    $reorder_stmt = $pdo->prepare("UPDATE tasks SET sort_order = ? WHERE id = ? AND board_slug = ?");
                    foreach ($order as $index => $task_id) {
                        $reorder_stmt->execute([(int)$index, (string)$task_id, $board_slug]);
                    }
                }
                break;

            case 'publish': // New operation for PKM
                $id = (string)($input['id'] ?? '');
                $stmt = $pdo->prepare("UPDATE tasks SET is_published = 1 WHERE id = ? AND board_slug = ?");
                $stmt->execute([$id, $board_slug]);

                // --- BEGIN "Process -> Publish" WORKFLOW ---
                // After flagging the task, trigger the GitHub Actions workflow for instant publishing.
                if (defined('GITHUB_TOKEN') && GITHUB_TOKEN !== 'your_github_personal_access_token_here') {
                    $ch = curl_init();
                    $url = "https://api.github.com/repos/" . GITHUB_REPO . "/actions/workflows/" . GITHUB_WORKFLOW_ID . "/dispatches";
                    $payload = json_encode(['ref' => 'main']);

                    curl_setopt($ch, CURLOPT_URL, $url);
                    curl_setopt($ch, CURLOPT_POST, 1);
                    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
                    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
                        'Accept: application/vnd.github.v3+json',
                        'Authorization: Bearer ' . GITHUB_TOKEN,
                        'User-Agent: arcreformas-api-publisher'
                    ));
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                    curl_setopt($ch, CURLOPT_TIMEOUT, 5); // Fire-and-forget

                    $curl_response = curl_exec($ch);
                    if ($curl_response === false) {
                        error_log("GitHub Actions dispatch failed: cURL error: " . curl_error($ch));
                    } else {
                        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                        // GitHub returns 204 No Content on success
                        if ($http_code !== 204) {
                            error_log("GitHub Actions dispatch failed: HTTP status {$http_code}, response: {$curl_response}");
                        }
                    }
                    curl_close($ch);
                }
                // --- END WORKFLOW ---
                break;

            default:
                // Do nothing, just fetch the state
                break;
        }

        // After any operation, update the board's timestamp
        $pdo->prepare("UPDATE boards SET updated_at = NOW() WHERE slug = ?")->execute([$board_slug]);
        $pdo->commit();

    } catch (Exception $e) {
        $pdo->rollBack();
        emit_json(['error' => 'Database operation failed: ' . $e->getMessage()], 500);
        return;
    }

    // Always return the full, updated board state
    emit_json(get_board_state($pdo, $board_slug));
}

?>
