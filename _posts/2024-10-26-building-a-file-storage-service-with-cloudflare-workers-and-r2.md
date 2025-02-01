---

tags: [scripts>cloud, scripts>serverless]
info: aberto.
date: 2024-10-26
type: post
layout: post
published: true
slug: building-a-file-storage-service-with-cloudflare-workers-and-r2
title: 'Building a File Storage Service with Cloudflare Workers and R2'
---
How to create a file storage service that handles multiple file types using Cloudflare Workers for the RESTful API and Cloudflare R2 for storage. This implementation allows secure uploading, retrieving, and deleting of files.

### Introduction

The goal is to build a self-hosted file storage solution (图床) that leverages Cloudflare Workers and R2, inspired by the tutorials:

- [自建图床小记一——图床架构与 DNS 解析](https://zhul.in/2024/08/12/new-picbed-based-on-cloudflare-and-upyun/)
- [自建图床小记二——使用 Workers 为 R2 构建 Restful API](https://zhul.in/2024/08/13/build-restful-api-for-cloudflare-r2-with-cloudflare-workers/)

This service will:

- Support multiple file types (images, documents, etc.).
- Use Cloudflare R2 for object storage.
- Provide a RESTful API for file operations.
- Include basic authentication for secure access.

### Implementation

Below is the Cloudflare Worker script with explanations and comments.

```javascript
// Cloudflare Worker Script for File Storage Service

export default {
  async fetch(request, env, ctx) {
    return await handleRequest(request, env);
  },
};

/**
 * Handles incoming requests and routes them based on the HTTP method.
 * @param {Request} request - The incoming HTTP request.
 * @param {Object} env - Environment bindings (e.g., R2 bucket).
 */
async function handleRequest(request, env) {
  // Parse the URL to get the file path
  const url = new URL(request.url);
  const filePath = decodeURIComponent(url.pathname.slice(1)); // Remove leading '/'

  // Authentication for write operations
  const AUTH_KEY = env.AUTH_KEY_SECRET;
  const method = request.method.toUpperCase();
  if (['PUT', 'DELETE'].includes(method)) {
    const authHeader = request.headers.get('X-Custom-Auth-Key');
    if (authHeader !== AUTH_KEY) {
      return new Response('Forbidden', { status: 403 });
    }
  }

  switch (method) {
    case 'PUT':
      // Handle file upload
      return await uploadFile(request, env, filePath);
    case 'GET':
      // Handle file retrieval
      return await getFile(env, filePath);
    case 'DELETE':
      // Handle file deletion
      return await deleteFile(env, filePath);
    default:
      return new Response('Method Not Allowed', {
        status: 405,
        headers: { Allow: 'GET, PUT, DELETE' },
      });
  }
}

/**
 * Uploads a file to the R2 bucket.
 * @param {Request} request - The incoming HTTP request.
 * @param {Object} env - Environment bindings.
 * @param {string} key - The file path in the bucket.
 */
async function uploadFile(request, env, key) {
  // Optional: Validate file size, type, etc.

  // Save the file to R2
  const contentType =
    request.headers.get('Content-Type') || 'application/octet-stream';
  await env.MY_BUCKET.put(key, request.body, {
    httpMetadata: { contentType },
    // Optional: Set cache control
    httpMetadata: { cacheControl: 'public, max-age=31536000' },
  });
  return new Response(`File '${key}' uploaded successfully`, { status: 200 });
}

/**
 * Retrieves a file from the R2 bucket.
 * @param {Object} env - Environment bindings.
 * @param {string} key - The file path in the bucket.
 */
async function getFile(env, key) {
  const object = await env.MY_BUCKET.get(key);
  if (!object) {
    return new Response('File Not Found', { status: 404 });
  }

  // Return the file with appropriate headers
  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set('ETag', object.httpEtag);

  return new Response(object.body, { headers });
}

/**
 * Deletes a file from the R2 bucket.
 * @param {Object} env - Environment bindings.
 * @param {string} key - The file path in the bucket.
 */
async function deleteFile(env, key) {
  await env.MY_BUCKET.delete(key);
  return new Response(`File '${key}' deleted successfully`, { status: 200 });
}
```

### Setup Instructions

#### 1. Create an R2 Bucket

- Log in to your Cloudflare dashboard.
- Navigate to **R2** and create a new bucket (e.g., `my-file-storage`).

#### 2. Write the Worker Script

- Use the script provided above.
- Save it in your Cloudflare Workers dashboard or use the [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/).

#### 3. Bind the R2 Bucket to the Worker

- In your Worker settings, go to **Variables > R2 Buckets**.
- Bind the `MY_BUCKET` variable to your R2 bucket (`my-file-storage`).

#### 4. Set the Authentication Key

- In **Variables > Environment Variables**, add `AUTH_KEY_SECRET` with a secure value (your secret key).

#### 5. Deploy the Worker

- Assign a route or domain to your Worker (e.g., `https://files.example.com`).
- Deploy the Worker.

### Usage Examples

#### Uploading a File

```bash
curl -X PUT 'https://files.example.com/path/to/file.jpg' \
  -H 'Content-Type: image/jpeg' \
  -H 'X-Custom-Auth-Key: your_auth_key' \
  --data-binary '@local/path/to/file.jpg'
```

#### Retrieving a File

```bash
curl -X GET 'https://files.example.com/path/to/file.jpg' --output file.jpg
```

#### Deleting a File

```bash
curl -X DELETE 'https://files.example.com/path/to/file.jpg' \
  -H 'X-Custom-Auth-Key: your_auth_key'
```

### Notes and Considerations

- **Supported File Types:**

  - All file types are supported. Ensure the `Content-Type` is correctly set when uploading.

- **Authentication:**

  - Only `PUT` and `DELETE` requests require the `X-Custom-Auth-Key` header.
  - `GET` requests are public. Implement additional checks if you need to restrict access.

- **Caching:**

  - The `Cache-Control` header is set for one year (`max-age=31536000`).
  - Adjust caching policies as needed.

- **Error Handling:**

  - The script provides basic error responses.
  - Expand error handling for production use.

- **Limits:**

  - Cloudflare Workers have [limits](https://developers.cloudflare.com/workers/platform/limits/) on request size, CPU time, etc.
  - For large files, consider using direct uploads to R2 or multipart uploads.
