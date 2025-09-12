<?php
declare(strict_types=1);

function sanitize_filename(string $filename): string {
    // Remove characters that are illegal in most filesystems or could be used for traversal.
    $filename = str_replace(['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|'], '_', $filename);
    // Remove control characters
    $filename = preg_replace('/[\x00-\x1F\x7F]/u', '', $filename);
    // Trim whitespace and dots from the ends
    $filename = trim($filename, ' .-_');
    return $filename ?: 'unnamed_file';
}

function handle_files_request(?string $id): void {
    $method = $_SERVER['REQUEST_METHOD'];

    switch ($method) {
        case 'GET':
            get_all_files();
            break;
        case 'POST':
            upload_new_file();
            break;
        default:
            emit_json(['error' => 'Method not allowed for this resource.'], 405);
            break;
    }
}

function get_all_files(): void {
    $pdo = get_pdo();
    $stmt = $pdo->query("SELECT id, filename, filesize, mime_type, created_at FROM files ORDER BY created_at DESC");
    $files = $stmt->fetchAll();

    // Add the public URL to each file for convenience
    foreach ($files as &$file) {
        $file['url'] = FILE_PUBLIC_URL . rawurlencode($file['filename']);
        // Map to the keys expected by the original frontend JS for easier migration
        $file['name'] = $file['filename'];
        $file['size'] = $file['filesize'];
        $file['lastModified'] = $file['created_at'];
        $file['displayType'] = explode('/', $file['mime_type'])[0];
    }

    emit_json(['status' => 'success', 'data' => $files]);
}

function upload_new_file(): void {
    if (!isset($_FILES['fileToUpload'])) {
        emit_json(['error' => 'No file data received in fileToUpload field.'], 400);
        return;
    }

    $file = $_FILES['fileToUpload'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        emit_json(['error' => 'File upload error code: ' . $file['error']], 400);
        return;
    }

    // Sanitize the filename
    $client_filename = $file['name'];
    $pathinfo = pathinfo($client_filename);
    $base = sanitize_filename($pathinfo['filename']);
    $ext = isset($pathinfo['extension']) ? '.' . strtolower($pathinfo['extension']) : '';

    // Append a short random string to the filename to prevent race conditions and overwrites.
    $unique_id = bin2hex(random_bytes(4)); // 8 hex characters
    $unique_filename = $base . '-' . $unique_id . $ext;

    $destination = UPLOAD_DIR . $unique_filename;

    if (move_uploaded_file($file['tmp_name'], $destination)) {
        try {
            $pdo = get_pdo();
            $stmt = $pdo->prepare(
                "INSERT INTO files (filename, filesize, mime_type) VALUES (?, ?, ?)"
            );
            $stmt->execute([$unique_filename, $file['size'], $file['type']]);
            $new_file_id = $pdo->lastInsertId();

            // --- BEGIN "Capture -> Process" WORKFLOW ---
            // After successful upload, automatically create a task in the 'inbox' board.
            $file_url = FILE_PUBLIC_URL . rawurlencode($unique_filename);
            $taskText = "Process new file: [{$unique_filename}]({$file_url})";
            $taskPayload = json_encode(['op' => 'add', 'text' => $taskText]);

            // Use cURL to make a fire-and-forget POST to our own tasks API.
            // This is an internal, server-to-server call.
            $ch = curl_init();
            $tasks_api_url = API_INTERNAL_URL . '/tasks/inbox';
            curl_setopt($ch, CURLOPT_URL, $tasks_api_url);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $taskPayload);
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_TIMEOUT, 2); // Use a short timeout; don't make the user wait.

            // Execute the call and add error logging for robustness
            $curl_response = curl_exec($ch);
            if ($curl_response === false) {
                // Log cURL errors (e.g., connection timeout)
                error_log("Failed to create task for '{$unique_filename}': cURL error: " . curl_error($ch));
            } else {
                $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                if ($http_code < 200 || $http_code >= 300) {
                    // Log API errors (e.g., 4xx or 5xx responses from the tasks API)
                    error_log("Failed to create task for '{$unique_filename}': HTTP status {$http_code}, response: {$curl_response}");
                }
            }
            curl_close($ch);
            // --- END WORKFLOW ---

            emit_json([
                'status' => 'success',
                'message' => 'File uploaded and task created: ' . htmlspecialchars($unique_filename),
                'id' => $new_file_id,
                'filename' => $unique_filename,
                'url' => FILE_PUBLIC_URL . rawurlencode($unique_filename)
            ], 201);

        } catch (PDOException $e) {
            // If DB insert fails, try to clean up the uploaded file
            unlink($destination);
            emit_json(['error' => 'Failed to save file metadata to database.'], 500);
        }
    } else {
        emit_json(['error' => 'Failed to move uploaded file. Check permissions for ' . UPLOAD_DIR], 500);
    }
}
?>
