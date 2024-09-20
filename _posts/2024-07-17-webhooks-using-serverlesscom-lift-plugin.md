---
tags: scripts>cloud
info: aberto.
date: 2024-07-17
type: post
layout: post
published: true
slug: webhooks-using-serverlesscom-lift-plugin
title: 'Webhooks using `Serverless.com` Lift plugin'
---

***
serverless.yml

```yml
service: github-webhook-service

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  environment:
    GITHUB_TOKEN: ${env:GITHUB_TOKEN}
    
plugins:
  - serverless-lift

constructs:
  webhook:
    type: webhook
    path: /webhook
    method: POST
    eventType: $request.body.type
    insecure: true

functions:
  handleWebhook:
    handler: handler.handleWebhook
    events:
      - eventBridge:
          eventBus: ${construct:webhook.busName}
          pattern:
            source:
              - webhook
            detail-type:
              - new_comment
    
package:
  patterns:
    - '!node_modules/aws-sdk/**'
    - '!node_modules/@aws-sdk/**'
```
***

---
handler.mjs

~~~mjs
import { Octokit } from "@octokit/rest";
import { Base64 } from "js-base64";

/**
 * Converts a string to a URL-friendly slug.
 * @param {string} text - The text to be slugified.
 * @return {string} The slugified text.
 */
const slugify = (text) => {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
};

/**
 * Formats a date string to YYYY-MM-DD.
 * @param {string} date - The date string to format.
 * @return {string} The formatted date string.
 */
const formatDate = (date) => {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    throw new Error('Invalid date provided');
  }
  return d.toISOString().split('T')[0];
};

/**
 * Creates the content for a blog post.
 * @param {Object} data - The data for the blog post.
 * @param {string} data.by_nickname - The author's nickname.
 * @param {string} data.by_email - The author's email.
 * @param {string} data.content - The content of the post.
 * @param {string} data.time - The timestamp of the post.
 * @return {string} The formatted blog post content.
 */
const createPostContent = (data) => {
  const { by_nickname, by_email, content, time } = data;
  const slugName = slugify(by_nickname);
  const date = formatDate(time);

  return `---
tags:
  - ${by_email}
info: aberto.
date: ${date}
type: post
layout: post
published: true
slug: ${slugName}
title: '${by_nickname}'
---

${content}`;
};

/**
 * Handles the webhook event for creating a new blog post.
 * @param {Object} event - The webhook event object.
 * @return {Object} The response object.
 */
export const handleWebhook = async (event) => {
  try {
    if (!event || !event.detail || !event.detail.data) {
      throw new Error('Invalid event structure');
    }

    const { by_nickname, by_email, content } = event.detail.data;
    const time = event.time || new Date().toISOString();

    if (!by_email || !by_nickname || !content) {
      throw new Error('Missing required fields: email, nickname, or content');
    }

    const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

    if (!process.env.GITHUB_TOKEN) {
      throw new Error('GitHub token is not set');
    }

    const owner = "${REPO_OWNER}";
    const repo = "${REPO_NAME}";
    const date = formatDate(time);
    const slugName = slugify(by_nickname);
    const path = `_posts/${date}-${slugName}.md`;
    const message = `New post by ${by_nickname}`;
    const postContent = createPostContent({ by_nickname, by_email, content, time });
    const contentEncoded = Base64.encode(postContent);

    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message,
      content: contentEncoded,
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "File created/updated successfully", path }),
    };
  } catch (error) {
    console.error('Error in handleWebhook:', error);
    return {
      statusCode: error.status || 500,
      body: JSON.stringify({ message: error.message || "An unexpected error occurred" }),
    };
  }
};
~~~
---
