<?php
declare(strict_types=1);

// --- IMPORTANT: EDIT THESE DETAILS ---
define('DB_HOST', 'localhost');
define('DB_NAME', 'your_database_name'); // e.g., user_db1
define('DB_USER', 'your_database_user'); // e.g., user_db1
define('DB_PASS', 'your_database_password');
// ------------------------------------

// --- FILE STORAGE CONFIGURATION ---
// The absolute path to the directory where uploaded files will be stored.
// Using `__DIR__ . '/../../'` assumes your public_html is the web root
// and you want to store files one level above it for security.
// Adjust if your structure is different. A common setup is a `storage`
// or `uploads` directory alongside `public_html`.
define('UPLOAD_DIR', __DIR__ . '/../../storage_arcreformas/');

// The public-facing base URL for accessing the files.
// This MUST correspond to how the UPLOAD_DIR is served. If it's outside the
// web root, you may need a separate script (e.g., download.php) to serve files.
// For simplicity, we'll assume a symlink or direct mapping for now.
define('FILE_PUBLIC_URL', 'https://arcreformas.com.br/files/');

// The base URL for internal, server-to-server API calls.
// Using a fixed constant is more secure than relying on $_SERVER['HTTP_HOST'].
define('API_INTERNAL_URL', 'https://arcreformas.com.br/api');


// --- GITHUB PUBLISHING CONFIGURATION ---
// Create a GitHub Personal Access Token (classic) with 'repo' and 'workflow' scopes.
// It is strongly recommended to store this token in an environment variable named 'GITHUB_TOKEN'.
// For example, in Apache you can use `SetEnv GITHUB_TOKEN your_token_here` in your .htaccess or vhost config.
// The constant below is used as a fallback for simpler setups.
define('GITHUB_TOKEN', getenv('GITHUB_TOKEN') ?: 'your_github_personal_access_token_here');
define('GITHUB_REPO', 'ib-bsb-br/ib-bsb-br.github.io'); // The owner/repo slug
define('GITHUB_WORKFLOW_ID', 'refresh-content.yml'); // The workflow filename

// Validate that a real token is available if publishing is intended.
// This check is here to fail early if the configuration is incomplete.
// Note: This simple check runs on every API call. In a more complex app,
// this might be moved to a dedicated health check endpoint.
if (empty(getenv('GITHUB_TOKEN')) && GITHUB_TOKEN === 'your_github_personal_access_token_here') {
    // The publish feature will fail if no valid token is provided.
    // Log a warning for the administrator to make this easier to debug.
    error_log('[WARNING] GITHUB_TOKEN is not set via environment variable and the fallback placeholder is being used. GitHub publishing will fail.');
}


// --- GENERAL HELPERS ---

function get_pdo(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        try {
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        } catch (PDOException $e) {
            // In a real app, you'd log this error. For this frictionless setup, we die.
            http_response_code(500);
            emit_json(['error' => 'Database connection failed.']);
            exit;
        }
    }
    return $pdo;
}

function emit_json(mixed $data, int $statusCode = 200): void {
    http_response_code($statusCode);
    header('Content-Type: application/json; charset=utf-8');
    // Allow cross-domain requests from our other domains
    header('Access-Control-Allow-Origin: *'); // Insecure as requested
    header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization');
    echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}

function handle_cors_preflight(): void {
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        header('Access-Control-Allow-Origin: *');
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization');
        http_response_code(204); // No Content
        exit;
    }
}

function id(int $length = 6): string {
    return substr(str_shuffle(str_repeat('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', $length)), 0, $length);
}

// Ensure upload directory exists
if (!is_dir(UPLOAD_DIR)) {
    // The second is_dir() check handles a potential race condition.
    if (!mkdir(UPLOAD_DIR, 0755, true) && !is_dir(UPLOAD_DIR)) {
        // Log the error for the administrator.
        error_log('Failed to create upload directory: ' . UPLOAD_DIR);
    }
}
?>
