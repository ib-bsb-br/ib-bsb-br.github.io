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
    GITHUB_TOKEN: ${env:GITHUB_TOKEN} # Secure GitHub token for API authentication
    GITHUB_REPOSITORY: your-github-username/your-repo-name # Format: owner/repo
    WORKFLOW_ID: your-workflow-file.yml # Default workflow ID, can be overridden

plugins:
  - serverless-lift

functions:
  handleWebhook:
    handler: handler.handleWebhook
    events:
      - http:
          path: /webhook  # Webhook endpoint path
          method: post
          cors: true # Enable CORS for cross-origin requests

  # Optional: Function to manually trigger GitHub workflows
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
    const response = await octokit.request('POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches', {
      owner,
      repo,
      workflow_id: workflowId,
      ref,
      inputs,
    });

    if (response.status !== 204) {
      throw new Error(`Failed to dispatch workflow. GitHub API status: ${response.status}`);
    }

    console.log(`Workflow '${workflowId}' dispatched successfully on ${repo}`);
    return response.data;

  } catch (error) {
    console.error('Error dispatching workflow:', error);
    throw error; // Re-throw to be caught in calling function
  }
};

/**
 * Handles incoming webhook events to create/update a blog post and trigger a workflow.
 * @param {Object} event - Event data from AWS Lambda invocation.
 * @return {Object} Response object with statusCode and body.
 */
export const handleWebhook = async (event) => {
  try {
    const body = event.body ? JSON.parse(event.body) : {};
    const { inputs } = body; // Get inputs from request body if any

    // Validate required environment variables
    const githubToken = process.env.GITHUB_TOKEN;
    const githubRepository = process.env.GITHUB_REPOSITORY;
    const workflowId = process.env.WORKFLOW_ID;

    if (!githubToken || !githubRepository || !workflowId) {
      throw new Error('Missing required environment variables.');
    }

    const [owner, repo] = githubRepository.split('/');
    const octokit = new Octokit({ auth: githubToken });

    // Extract and validate data from the webhook event
    const eventData = body || {};
    const { by_nickname, by_email, content } = eventData;
    const time = eventData.time || new Date().toISOString();

    if (!by_email || !by_nickname || !content) {
      throw new Error('Missing required fields: by_email, by_nickname, or content.');
    }

    // Create or update the blog post file in the repository
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

    // Dispatch the workflow
    const ref = 'main'; // You can make this dynamic if needed
    await triggerWorkflowDispatch(octokit, owner, repo, ref, workflowId, inputs);

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'File created/updated and workflow triggered', path }),
    };

  } catch (error) {
    console.error('Error in handleWebhook:', error);
    return {
      statusCode: error.status || 500,
      body: JSON.stringify({ message: error.message || 'An unexpected error occurred.' }),
    };
  }
};

/**
 * Optional function to manually trigger a GitHub Actions workflow via HTTP endpoint.
 * @param {Object} event - Event data from AWS Lambda invocation.
 * @return {Object} Response object with statusCode and body.
 */
export const triggerGithubWorkflow = async (event) => {
  try {
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
    const response = await triggerWorkflowDispatch(octokit, owner, repo, ref, workflowId, inputs);

    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Workflow dispatched successfully.', details: response }),
    };

  } catch (error) {
    console.error('Error in triggerGithubWorkflow:', error);
    return {
      statusCode: error.status || 500,
      body: JSON.stringify({ message: error.message || 'Failed to dispatch workflow.' }),
    };
  }
};
{% endcodeblock %}

# 3. Client-Side JavaScript (If Applicable):

{% codeblock javascript %}
const webhookEndpoint = '/webhook'; // Path to your webhook endpoint

document.getElementById('triggerWorkflow').addEventListener('click', async () => {
  // Display status message to user
  // ...

  try {
    const inputs = { run_workflow: 'yes', testParam: Math.random() }; // Example inputs

    const response = await fetch(webhookEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        by_nickname: 'John Doe', // Example data
        by_email: 'john.doe@example.com',
        content: 'This is a test post.',
        inputs, // Send inputs in the request body
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Server error: ${response.status} - ${errorData.message}`);
    }

    const data = await response.json();
    // Handle successful response
    // ...

  } catch (error) {
    // Handle error and display message to user
    // ...
  }
});
{% endcodeblock %}

---

# Deployment and Configuration Instructions:

1. **Set Environment Variables:**

   - `GITHUB_TOKEN`: Personal Access Token with appropriate permissions (stored securely).
   - `GITHUB_REPOSITORY`: Your GitHub repository in the format `owner/repo`.
   - `WORKFLOW_ID`: The filename or ID of the GitHub Actions workflow to trigger.

{% codeblock bash %}
$env:GITHUB_TOKEN="your_personal_access_token"
$env:GITHUB_REPOSITORY="owner/repo"
$env:WORKFLOW_ID="main.yml"
{% endcodeblock %}

2. **Deploy the Serverless Application:**

   - Install dependencies: `npm install`
   - Deploy using the Serverless Framework: `serverless deploy`

3. **Configure GitHub Actions Workflow:**

   - Create a workflow file in your repository (e.g., `your-workflow-file.yml`).
   - Ensure it includes `workflow_dispatch` in the `on` section:
     {% codeblock yaml %}
     on:
       workflow_dispatch:
         inputs:
           run_workflow:
             description: 'Trigger to run the workflow'
             required: true
             default: 'yes'
     {% endcodeblock %}
   - Define the jobs and steps as needed for your application.

4. **Testing the Functions:**

   - Test the `handleWebhook` function by sending a POST request to the `/webhook` endpoint.
     - Include required data fields in the request body (`by_nickname`, `by_email`, `content`).
     - Optionally include `inputs` for the workflow.

   - If the `triggerGithubWorkflow` function is added, test it by sending a POST request to the `/trigger_github_workflow` endpoint.
     - Include `workflow_id`, `ref`, and `inputs` in the request body as needed.

5. **Security Considerations:**

   - Ensure that all tokens and sensitive data are securely stored and not exposed to users.
   - Regularly review and update dependencies to fix any known vulnerabilities.
   - Monitor logs for any suspicious activities or errors.
