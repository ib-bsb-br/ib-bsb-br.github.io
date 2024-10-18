---
tags: scripts>cloud, tools>github
info: aberto.
date: 2024-10-18
type: post
layout: post
published: true
slug: serverless-lift-gha
title: 'Github actions workflow dispatch + Webhooks using `Serverless.com` Lift plugin'
---

# 1. `serverless.yml` Configuration:

{% codeblock yaml %}
service: github-webhook-service

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  environment:  
    GITHUB_TOKEN: ${env:GITHUB_TOKEN}  # Securely store your GitHub Personal Access Token
    GITHUB_REPOSITORY: ib-bsb-br/ib-bsb-br.github.io  # Replace with your GitHub repository
    WORKFLOW_ID: dispatch-workflow.yml # The filename or ID of the GitHub Actions workflow to trigger

plugins:
  - serverless-lift

functions:
  handleWebhook:
    handler: handler.handleWebhook
    events:
      - http:
          path: /webhook  # Webhook endpoint path
          method: post
          cors: true
      - eventBridge:
          eventBus: ${construct:webhook.busName}
          pattern:
            source:
              - webhook
            detail-type:
              - new_comment

  triggerGithubWorkflow:
    handler: handler.triggerGithubWorkflow
    events:
      - http:
          path: /trigger_github_workflow
          method: post
          cors: true

constructs:
  webhook:
    type: webhook
    path: /webhook
    method: POST
    eventType: $request.body.eventType  # Maps to 'detail-type' in EventBridge event
    insecure: true

package:
  patterns:
    - '!node_modules/aws-sdk/**'
    - '!node_modules/@aws-sdk/**'
{% endcodeblock %}

# 2. Handler Functions (`handler.mjs`):

{% codeblock javascript %}
import { Octokit } from "@octokit/rest";
import { Base64 } from "js-base64";

/**
 * Converts a string to a URL-friendly slug.
 * @param {string} text - The text to slugify.
 * @return {string} Slugified text.
 */
const slugify = (text) => {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')       // Replace spaces with -
    .replace(/[^\w\-]+/g, '')   // Remove all non-word chars
    .replace(/\-\-+/g, '-')     // Replace multiple - with single -
    .replace(/^-+/, '')         // Trim - from start of text
    .replace(/-+$/, '');        // Trim - from end of text
};

/**
 * Formats a date string to YYYY-MM-DD.
 * @param {string|Date} date - The date to format.
 * @return {string} Formatted date string.
 */
const formatDate = (date) => {
  const d = new Date(date);
  if (isNaN(d.getTime())) {
    throw new Error('Invalid date provided');
  }
  return d.toISOString().split('T')[0];
};

/**
 * Creates the content for a blog post in Markdown format.
 * @param {Object} data - Data for the blog post.
 * @param {string} data.by_nickname - Author's nickname.
 * @param {string} data.by_email - Author's email.
 * @param {string} data.content - Post content.
 * @param {string|Date} data.time - Timestamp of the post.
 * @return {string} Formatted blog post content.
 */
const createPostContent = (data) => {
  const { by_nickname, by_email, content, time } = data;
  const slugName = slugify(by_nickname);
  const date = formatDate(time);
  return `---
tags: ${by_email}
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
 * Triggers a GitHub Actions workflow using workflow_dispatch.
 * @param {Octokit} octokit - Authenticated Octokit instance.
 * @param {string} owner - Repository owner.
 * @param {string} repo - Repository name.
 * @param {string} ref - Git reference (branch or tag).
 * @param {string} workflowId - Workflow file name or ID.
 * @param {Object} inputs - Inputs for the workflow.
 */
const triggerWorkflowDispatch = async (octokit, owner, repo, ref, workflowId, inputs = {}) => {
  try {
    const response = await octokit.request(
      'POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches',
      {
        owner,
        repo,
        workflow_id: workflowId,
        ref,
        inputs,
      }
    );

    if (response.status !== 204) {
      throw new Error(`Failed to dispatch workflow. GitHub API status: ${response.status}`);
    }

    console.log(`Workflow '${workflowId}' dispatched successfully on ${repo}`);
    return response.data;
  } catch (error) {
    console.error('Error dispatching workflow:', error);
    throw error;
  }
};

/**
 * Returns CORS headers.
 * @return {Object} CORS headers.
 */
const getCorsHeaders = () => {
  return {
    'Access-Control-Allow-Origin': 'https://ib.bsb.br',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
};

/**
 * Handles incoming webhook events to create/update a blog post and trigger a workflow.
 * @param {Object} event - Event data from AWS Lambda invocation.
 * @return {Object} Response object with statusCode, headers, and body.
 */
export const handleWebhook = async (event) => {
  try {
    console.log('Event received:', JSON.stringify(event, null, 2));

    let body;

    // Determine if the event is from an HTTP request or EventBridge
    if (event.body) {
      // HTTP request
      body = JSON.parse(event.body);
    } else if (event.detail) {
      // EventBridge event
      body = event.detail;
    } else {
      throw new Error('No data received in the event.');
    }

    // Handle nested 'data' object if present
    const data = body.data || body;

    // Extract and validate data from the webhook event
    const { by_nickname, by_email, content } = data;

    if (!by_email || !by_nickname || !content) {
      throw new Error('Missing required fields: by_email, by_nickname, or content.');
    }

    // Use 'createdAt' or 'updatedAt' as the time, or default to current time
    let eventTime = data.createdAt || data.updatedAt || new Date().toISOString();

    // Validate and format the time
    try {
      eventTime = formatDate(eventTime);
    } catch (e) {
      // If invalid, default to current date
      eventTime = formatDate(new Date().toISOString());
    }

    // Validate required environment variables
    const githubToken = process.env.GITHUB_TOKEN;
    const githubRepository = process.env.GITHUB_REPOSITORY;
    const workflowId = process.env.WORKFLOW_ID;

    if (!githubToken || !githubRepository || !workflowId) {
      throw new Error('Missing required environment variables.');
    }

    const [owner, repo] = githubRepository.split('/');
    const octokit = new Octokit({ auth: githubToken });

    // Create or update the blog post file in the repository
    const slugName = slugify(by_nickname);
    const path = `_posts/${eventTime}-${slugName}.md`;
    const message = `New post by ${by_nickname}`;
    const postContent = createPostContent({
      by_nickname,
      by_email,
      content,
      time: eventTime,
    });
    const contentEncoded = Base64.encode(postContent);

    // Check if the file already exists
    let sha;
    try {
      const { data: fileData } = await octokit.repos.getContent({
        owner,
        repo,
        path,
      });
      sha = fileData.sha; // File exists, so we'll update it
    } catch (err) {
      if (err.status !== 404) {
        console.error('Error fetching file content:', err);
        throw err;
      }
      // File does not exist; proceed to create it
    }

    // Create or update the file in the repository
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message,
      content: contentEncoded,
      sha, // Include sha if updating an existing file
    });

    // Dispatch the workflow
    const ref = 'main'; // You can make this dynamic if needed
    await triggerWorkflowDispatch(octokit, owner, repo, ref, workflowId);

    return {
      statusCode: 200,
      headers: getCorsHeaders(),
      body: JSON.stringify({
        message: 'File created/updated and workflow triggered',
        path,
      }),
    };
  } catch (error) {
    console.error('Error in handleWebhook:', error);
    return {
      statusCode: error.statusCode || 500,
      headers: getCorsHeaders(),
      body: JSON.stringify({
        message: error.message || 'An unexpected error occurred.',
      }),
    };
  }
};

/**
 * Handles requests to manually trigger a GitHub Actions workflow via HTTP endpoint.
 * @param {Object} event - Event data from AWS Lambda invocation.
 * @return {Object} Response object with statusCode, headers, and body.
 */
export const triggerGithubWorkflow = async (event) => {
  try {
    if (event.httpMethod === 'OPTIONS') {
      // Respond to CORS preflight request
      return {
        statusCode: 200,
        headers: getCorsHeaders(),
        body: '',
      };
    }

    console.log('Event received:', JSON.stringify(event, null, 2));

    const body = event.body ? JSON.parse(event.body) : {};
    const { ref = 'main', workflow_id, inputs = {} } = body;

    // Validate required environment variables
    const githubToken = process.env.GITHUB_TOKEN;
    const githubRepository = process.env.GITHUB_REPOSITORY;

    if (!githubToken || !githubRepository) {
      throw new Error('Missing required environment variables.');
    }

    const workflowId = workflow_id || process.env.WORKFLOW_ID;
    if (!workflowId) {
      throw new Error('Workflow ID is required.');
    }

    const [owner, repo] = githubRepository.split('/');
    const octokit = new Octokit({ auth: githubToken });

    // Dispatch the workflow
    await triggerWorkflowDispatch(octokit, owner, repo, ref, workflowId, inputs);

    return {
      statusCode: 200,
      headers: getCorsHeaders(),
      body: JSON.stringify({ message: 'Workflow dispatched successfully.' }),
    };
  } catch (error) {
    console.error('Error in triggerGithubWorkflow:', error);
    return {
      statusCode: error.statusCode || 500,
      headers: getCorsHeaders(),
      body: JSON.stringify({
        message: error.message || 'Failed to dispatch workflow.',
      }),
    };
  }
};
{% endcodeblock %}

# 3. Client-Side JavaScript (If Applicable):

{% codeblock javascript %}
<button id="triggerWorkflow">Events</button>
<div id="calendar"></div>
<script>
  document.getElementById('triggerWorkflow').addEventListener('click', async () => {
    const webhookEndpoint = 'https://8k5ij92zn4.execute-api.us-east-1.amazonaws.com/dev/trigger_github_workflow'; // Replace with your actual endpoint

    const payload = {
      ref: 'main',
      workflow_id: 'dispatch-workflow.yml', // Ensure this matches your GitHub Actions workflow filename
      inputs: {
        some_input: 'An example input' // Replace with actual inputs your workflow expects
      }
    };

    try {
      const response = await fetch(webhookEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Server error: ${response.status} - ${errorData.message}`);
      }

      const data = await response.json();
      console.log('Workflow dispatched successfully:', data);
      alert('Workflow has been successfully triggered.');
    } catch (error) {
      console.error('Error triggering workflow:', error);
      alert(`Failed to trigger workflow: ${error.message}`);
    }
  });
</script>
{% endcodeblock %}

---

# Deployment and Configuration Instructions:

1. **Set Environment Variables:**

   - `GITHUB_TOKEN`: Personal Access Token with appropriate permissions (stored securely).
   - `GITHUB_REPOSITORY`: Your GitHub repository in the format `owner/repo`.
   - `WORKFLOW_ID`: The filename or ID of the GitHub Actions workflow to trigger.

{% codeblock bash %}
export GITHUB_TOKEN="your_personal_access_token"
export GITHUB_REPOSITORY="owner/repo"
export WORKFLOW_ID="main.yml"
{% endcodeblock %}

2. **Deploy the Serverless Application:**

   - Install dependencies: `npm install`
   - Deploy using the Serverless Framework: (1) `{npx serverless print`; (2) `serverless deploy`.

3. **Configure GitHub Actions Workflow:**

   - Create a workflow file in your repository (e.g., `your-workflow-file.yml`).
   - Ensure it includes `workflow_dispatch` in the `on` section:

     {% codeblock yaml %}
name: Trigger Workflow

on:
  workflow_dispatch:
    inputs:
      some_input:
        description: 'An example input'
        required: false
  
jobs:
  trigger-workflow:
    runs-on: ubuntu-latest
    name: Dispatch Event
    steps:
      - name: Trigger target workflow
        run: |
          curl -X POST \
          -H "Accept: application/vnd.github+json" \
          -H "Authorization: Bearer ${{ secrets.WORKFLOW_DISPATCH_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{"event_type":"trigger-jekyll", "client_payload": {"message": "Triggered from main workflow"}}'
          https://api.github.com/repos/${{ github.repository }}/dispatches
      {% endcodeblock %}
