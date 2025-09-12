<?php
declare(strict_types=1);

function handle_links_request(?string $slug): void {
    $method = $_SERVER['REQUEST_METHOD'];

    switch ($method) {
        case 'GET':
            if (empty($slug)) {
                emit_json(['error' => 'Link slug not specified.'], 400);
            } else {
                get_long_link($slug);
            }
            break;
        case 'POST':
            create_short_link();
            break;
        default:
            emit_json(['error' => 'Method not allowed for this resource.'], 405);
            break;
    }
}

function get_long_link(string $slug): void {
    $pdo = get_pdo();
    $stmt = $pdo->prepare("SELECT url FROM links WHERE slug = ?");
    $stmt->execute([$slug]);
    $result = $stmt->fetch();

    if ($result) {
        // Update view count
        $update_stmt = $pdo->prepare("UPDATE links SET views = views + 1 WHERE slug = ?");
        $update_stmt->execute([$slug]);
        emit_json($result);
    } else {
        emit_json(['error' => 'Link not found.'], 404);
    }
}

function create_short_link(): void {
    $input = json_decode(file_get_contents('php://input'), true) ?? [];
    $url = trim((string)($input['url'] ?? ''));

    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        emit_json(['error' => 'Invalid URL provided.'], 400);
        return;
    }

    $pdo = get_pdo();
    $slug = generate_unique_slug($pdo);

    try {
        $stmt = $pdo->prepare("INSERT INTO links (slug, url) VALUES (?, ?)");
        $stmt->execute([$slug, $url]);

        emit_json([
            'status' => 'success',
            'slug' => $slug,
            'short_url' => 'https://cut.ia.br/?s=' . $slug, // Assumes cut.ia.br will be the frontend
            'long_url' => $url
        ], 201);

    } catch (PDOException $e) {
        emit_json(['error' => 'Failed to create short link in database.'], 500);
    }
}

function generate_unique_slug(PDO $pdo, int $length = 5): string {
    $chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $max_attempts = 10;
    for ($i = 0; $i < $max_attempts; $i++) {
        $slug = '';
        for ($j = 0; $j < $length; $j++) {
            $slug .= $chars[random_int(0, 61)];
        }
        $stmt = $pdo->prepare("SELECT 1 FROM links WHERE slug = ?");
        $stmt->execute([$slug]);
        if (!$stmt->fetch()) {
            return $slug; // Found a unique slug
        }
    }
    // Fallback if we can't find a unique slug after several tries
    return 'long_' . id(4);
}
?>
