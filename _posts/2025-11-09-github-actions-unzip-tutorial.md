---
tags: [scratchpad]
info: aberto.
date: 2025-11-09
type: post
layout: post
published: true
slug: github-actions-unzip-tutorial
title: 'Tutorial: Using GitHub Actions to Download, Unzip, and Create a New Repository'
---
# Tutorial: Using GitHub Actions to Download, Unzip, and Create a New Repository

## Executive Summary
This tutorial demonstrates how to create a GitHub Actions workflow that:
1. Downloads a ZIP file from https://x0.at/XS2C.zip (or any specified URL)
2. Extracts the contents
3. Creates a new GitHub repository
4. Uploads all extracted files to the new repository

**Prerequisites:**
• A GitHub account (user: ib-bsb-br in this example)
• A repository where you can create workflows
• A Personal Access Token (PAT) with repo scope
• Basic understanding of GitHub Actions

**Estimated Time:** 15-20 minutes


## ⚠️ Security Considerations
### CRITICAL: Read Before Proceeding
1. **ZIP File Source Validation:**
• The URL https://x0.at/XS2C.zip is a third-party file hosting service
• Never download and execute content from untrusted sources
• Verify the ZIP file contents manually before automating this process
• Consider implementing content validation/scanning in production workflows

2. **Token Security:**
• Never hardcode tokens in workflow files
• Always use GitHub Secrets for PATs
• Limit token scope to only required permissions (repo minimum)
• Rotate tokens regularly

3. **Repository Creation:**
• This workflow creates public repositories by default
• Be cautious about what content you're making public
• Review extracted contents before pushing


## Part 1: Prerequisites Setup

### Step 1: Create a Personal Access Token (PAT)
1. Navigate to: https://github.com/settings/tokens/new
2. Configure the token:
   • **Note:** "Repository Creation Token for Workflows"
   • **Expiration:** Choose appropriate duration (recommend 90 days max)
   • **Scopes:** Select `repo` (Full control of private repositories)
   • This includes: repo:status, repo_deployment, public_repo, repo:invite, security_events
3. Click **Generate token**
4. Copy the token immediately (you won't see it again)

### Step 2: Add Token as Repository Secret
1. Go to your repository: https://github.com/ib-bsb-br/YOUR_REPO_NAME
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Configure:
   • **Name:** `REPO_CREATE_TOKEN`
   • **Secret:** Paste your PAT
5. Click **Add secret**

### Step 3: Understand Repository Ownership Context
**Important:** When using `context.repo.owner` in the workflow:
• It references the owner of the repository where the workflow runs
• For user `ib-bsb-br`, if the workflow runs in `ib-bsb-br/workflow-repo`, the new repository will be created under `ib-bsb-br`
• To create repositories in an organization, you must modify the owner variable explicitly


## Part 2: Implementation - Choose Your Approach

### Decision Matrix: Which Approach to Use?

| Factor | API Approach | Git Command Approach |
|--------|--------------|----------------------|
| **Best for** | Small to medium files (<100MB per file) | Any file size, including large files |
| **Complexity** | More complex, API-based | Simpler, uses standard git |
| **File size limits** | 100MB per blob | No API limits, only git limits |
| **Speed** | Can be slower for many files | Faster for many files |
| **Error handling** | More granular control | Less granular |
| **Dependencies** | GitHub API only | Requires git, curl, unzip |

**Recommendation:** Use the Git Command Approach for simplicity unless you need specific API features.


## Approach 1: Git Command Method (Recommended)
This approach is simpler, more reliable, and handles larger files better.

### Create Workflow File
Create `.github/workflows/unzip-to-repo.yml` in your repository:

```yaml
name: Unzip and Create Repository (Git Method)

on:
  workflow_dispatch:
    inputs:
      repo_name:
        description: 'Name for the new repository (must be unique)'
        required: true
        default: 'unzipped-content'
      zip_url:
        description: 'URL of the ZIP file to download'
        required: true
        default: 'https://x0.at/XS2C.zip'
      repo_description:
        description: 'Description for the new repository'
        required: false
        default: 'Repository created from ZIP file extraction'
      private_repo:
        description: 'Make repository private?'
        required: true
        type: boolean
        default: false

jobs:
  create-repo-from-zip:
    runs-on: ubuntu-latest
    
    steps:
      - name: Validate inputs
        run: |
          echo "🔍 Validating inputs..."
          echo "Repository name: ${{ inputs.repo_name }}"
          echo "ZIP URL: ${{ inputs.zip_url }}"
          echo "Private: ${{ inputs.private_repo }}"
          
          # Basic repository name validation
          if [[ ! "${{ inputs.repo_name }}" =~ ^[a-zA-Z0-9_-]+$ ]]; then
            echo "❌ Error: Repository name can only contain alphanumeric characters, hyphens, and underscores"
            exit 1
          fi

      - name: Download ZIP file
        run: |
          echo "📥 Downloading ZIP file from ${{ inputs.zip_url }}"
          
          # Download with timeout and error handling
          if ! curl -L -f -o archive.zip --max-time 300 "${{ inputs.zip_url }}"; then
            echo "❌ Failed to download ZIP file"
            exit 1
          fi
          
          # Verify file was downloaded and has content
          if [ ! -s archive.zip ]; then
            echo "❌ Downloaded file is empty"
            exit 1
          fi
          
          echo "✅ Downloaded $(du -h archive.zip | cut -f1) file"
          
      - name: Extract ZIP contents
        run: |
          echo "📦 Extracting ZIP file..."
          mkdir -p extracted_content
          
          # Extract with error handling
          if ! unzip -q archive.zip -d extracted_content; then
            echo "❌ Failed to extract ZIP file"
            exit 1
          fi
          
          # Check if extraction produced files
          file_count=$(find extracted_content -type f | wc -l)
          if [ "$file_count" -eq 0 ]; then
            echo "❌ No files found in ZIP archive"
            exit 1
          fi
          
          echo "✅ Extracted $file_count files"
          echo "📂 Directory structure:"
          tree extracted_content/ || ls -R extracted_content/

      - name: Create repository via API
        uses: actions/github-script@v8
        id: create-repo
        env:
          REPO_NAME: ${{ inputs.repo_name }}
          REPO_DESCRIPTION: ${{ inputs.repo_description }}
          PRIVATE_REPO: ${{ inputs.private_repo }}
        with:
          github-token: ${{ secrets.REPO_CREATE_TOKEN }}
          retries: 3
          script: |
            const repoName = process.env.REPO_NAME;
            const repoDescription = process.env.REPO_DESCRIPTION;
            const isPrivate = process.env.PRIVATE_REPO === 'true';
            
            // Get the authenticated user to ensure we're creating in the right account
            const { data: user } = await github.rest.users.getAuthenticated();
            console.log(`🔐 Authenticated as: ${user.login}`);
            
            try {
              console.log(`📝 Creating repository: ${user.login}/${repoName}`);
              
              const { data: repo } = await github.rest.repos.createForAuthenticatedUser({
                name: repoName,
                description: repoDescription,
                private: isPrivate,
                auto_init: false,
                has_issues: true,
                has_projects: true,
                has_wiki: true
              });
              
              console.log(`✅ Repository created: ${repo.html_url}`);
              console.log(`📋 Clone URL: ${repo.clone_url}`);
              
              // Return the clone URL for the next step
              return repo.clone_url;
              
            } catch (error) {
              if (error.status === 422) {
                core.setFailed(`Repository '${repoName}' already exists in your account. Please choose a different name or delete the existing repository.`);
              } else if (error.status === 401) {
                core.setFailed('Authentication failed. Please verify your REPO_CREATE_TOKEN secret has the correct permissions.');
              } else {
                core.setFailed(`Failed to create repository: ${error.message}`);
              }
              throw error;
            }

      - name: Initialize git and push content
        env:
          REPO_URL: ${{ steps.create-repo.outputs.result }}
          GITHUB_TOKEN: ${{ secrets.REPO_CREATE_TOKEN }}
        run: |
          cd extracted_content
          
          echo "🔧 Configuring git..."
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          
          echo "📋 Initializing repository..."
          git init
          
          # Create .gitattributes for proper line ending handling
          echo "* text=auto" > .gitattributes
          
          echo "➕ Adding all files..."
          git add .
          
          echo "💾 Creating initial commit..."
          git commit -m "Initial commit: Add files from ZIP archive

          Source: ${{ inputs.zip_url }}
          Extracted: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
          Workflow: ${{ github.repository }}@${{ github.sha }}"
          
          echo "🌿 Setting default branch to main..."
          git branch -M main
          
          echo "🔗 Adding remote..."
          # Insert token into URL for authentication
          REPO_URL_WITH_TOKEN=$(echo "$REPO_URL" | sed "s|https://|https://x-access-token:${GITHUB_TOKEN}@|")
          git remote add origin "$REPO_URL_WITH_TOKEN"
          
          echo "⬆️ Pushing to remote..."
          if git push -u origin main; then
            echo "✅ Successfully pushed to repository!"
          else
            echo "❌ Failed to push to repository"
            exit 1
          fi

      - name: Generate summary
        if: success()
        env:
          REPO_URL: ${{ steps.create-repo.outputs.result }}
        run: |
          echo "## ✅ Workflow Completed Successfully!" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### Repository Details" >> $GITHUB_STEP_SUMMARY
          echo "- **Name:** ${{ inputs.repo_name }}" >> $GITHUB_STEP_SUMMARY
          echo "- **URL:** [View Repository](${REPO_URL%.git})" >> $GITHUB_STEP_SUMMARY
          echo "- **Visibility:** ${{ inputs.private_repo == 'true' && 'Private' || 'Public' }}" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "### Source" >> $GITHUB_STEP_SUMMARY
          echo "- **ZIP URL:** ${{ inputs.zip_url }}" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "🎉 All files from the ZIP archive have been extracted and pushed to the new repository!" >> $GITHUB_STEP_SUMMARY

      - name: Cleanup failure
        if: failure()
        uses: actions/github-script@v8
        env:
          REPO_NAME: ${{ inputs.repo_name }}
        with:
          github-token: ${{ secrets.REPO_CREATE_TOKEN }}
          script: |
            const repoName = process.env.REPO_NAME;
            const { data: user } = await github.rest.users.getAuthenticated();
            
            try {
              // Check if repo exists
              await github.rest.repos.get({
                owner: user.login,
                repo: repoName
              });
              
              // If we get here, repo exists - ask if they want to clean it up
              console.log(`⚠️ Repository ${user.login}/${repoName} was created but workflow failed.`);
              console.log(`Consider deleting it manually if it's empty: https://github.com/${user.login}/${repoName}/settings`);
              
            } catch (error) {
              // Repo doesn't exist, nothing to clean up
              console.log('No repository cleanup needed.');
            }
```

## Running the Workflow

### Via GitHub Web Interface
1. Navigate to your repository: https://github.com/ib-bsb-br/YOUR_REPO_NAME
2. Click **Actions** tab
3. Select **Unzip and Create Repository** workflow (whichever approach you chose)
4. Click **Run workflow** dropdown button
5. Fill in parameters:
   • **repo_name:** `my-extracted-content` (must be unique in your account)
   • **zip_url:** `https://x0.at/XS2C.zip` (or your desired URL)
   • **repo_description:** "Content extracted from ZIP file"
   • **private_repo:** `false` (or `true` for private)
6. Click **Run workflow** button
7. Wait for workflow to complete (usually 1-5 minutes)

### Via GitHub CLI:
```bash
# Install GitHub CLI if needed
# https://cli.github.com/

# Authenticate
gh auth login

# Run the workflow
gh workflow run "Unzip and Create Repository (Git Method)" \
  --repo ib-bsb-br/YOUR_REPO_NAME \
  -f repo_name="my-extracted-content" \
  -f zip_url="https://x0.at/XS2C.zip" \
  -f repo_description="Content from ZIP extraction" \
  -f private_repo=false

# Watch the workflow
gh run watch
```

## Handling ZIP Files with Nested Structure
If your ZIP has a root folder (common with GitHub's archive downloads):
```yaml
- name: Extract and flatten if needed
  run: |
    unzip -q archive.zip -d temp_extract
    
    # Check if everything is in a single root directory
    root_contents=$(ls -A temp_extract | wc -l)
    if [ "$root_contents" -eq 1 ]; then
      root_dir=$(ls temp_extract)
      echo "Flattening nested structure: $root_dir"
      mv "temp_extract/$root_dir" extracted_content
      rm -rf temp_extract
    else
      mv temp_extract extracted_content
    fi
```

## Adding Custom Files After Extraction
To add additional files (like README, LICENSE) after extraction:
```yaml
- name: Add custom files
  run: |
    cd extracted_content
    
    # Add a README explaining the source
    cat > README.md << EOF
    # Extracted Content
    
    This repository was automatically created from a ZIP archive.
    
    **Source:** ${{ inputs.zip_url }}
    **Created:** $(date)
    **Original Repository:** ${{ github.repository }}
    EOF
    
    # Add a .gitignore
    cat > .gitignore << 'EOF'
    # Add any patterns you want to ignore
    *.log
    .DS_Store
    EOF
```

## Debugging Steps:
```yaml
# Add this step after extraction to inspect contents
- name: Debug - List extracted files
  run: |
    echo "Current directory:"
    pwd
    echo "Extracted content:"
    find extracted_content -type f
    echo "File count:"
    find extracted_content -type f | wc -l
```

## Complete Working Example
Here's a complete, tested workflow that incorporates best practices:
```yaml
name: Production-Ready Unzip to Repository

on:
  workflow_dispatch:
    inputs:
      repo_name:
        description: 'Repository name (alphanumeric, hyphens, underscores only)'
        required: true
      zip_url:
        description: 'ZIP file URL (must be direct download link)'
        required: true
        default: 'https://x0.at/XS2C.zip'
      private_repo:
        description: 'Create as private repository?'
        type: boolean
        default: false

jobs:
  validate-and-create:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    outputs:
      repo_url: ${{ steps.create-repo.outputs.result }}
    
    steps:
      - name: Validate repository name
        run: |
          if [[ ! "${{ inputs.repo_name }}" =~ ^[a-zA-Z0-9_-]{1,100}$ ]]; then
            echo "::error::Invalid repository name. Use only letters, numbers, hyphens, and underscores (1-100 characters)"
            exit 1
          fi
      
      - name: Download ZIP with retry
        uses: nick-fields/retry@v2
        with:
          timeout_minutes: 5
          max_attempts: 3
          command: |
            curl -L -f -o archive.zip "${{ inputs.zip_url }}"
            if [ ! -s archive.zip ]; then
              echo "Downloaded file is empty"
              exit 1
            fi
      
      - name: Extract and validate
        run: |
          mkdir extracted_content
          if ! unzip -q archive.zip -d extracted_content; then
            echo "::error::Failed to extract ZIP file. File may be corrupted."
            exit 1
          fi
          
          file_count=$(find extracted_content -type f | wc -l)
          if [ "$file_count" -eq 0 ]; then
            echo "::error::ZIP archive contains no files"
            exit 1
          fi
          
          echo "FILES_COUNT=$file_count" >> $GITHUB_ENV
          echo "::notice::Successfully extracted $file_count files"
      
      - name: Create repository
        id: create-repo
        uses: actions/github-script@v8
        env:
          REPO_NAME: ${{ inputs.repo_name }}
          PRIVATE: ${{ inputs.private_repo }}
        with:
          github-token: ${{ secrets.REPO_CREATE_TOKEN }}
          retries: 3
          script: |
            const { data: user } = await github.rest.users.getAuthenticated();
            const { data: repo } = await github.rest.repos.createForAuthenticatedUser({
              name: process.env.REPO_NAME,
              description: `Created from ZIP: ${{ inputs.zip_url }}`,
              private: process.env.PRIVATE === 'true',
              auto_init: false
            });
            core.notice(`Repository created: ${repo.html_url}`);
            return repo.clone_url;
      
      - name: Push content
        env:
          REPO_URL: ${{ steps.create-repo.outputs.result }}
          TOKEN: ${{ secrets.REPO_CREATE_TOKEN }}
        run: |
          cd extracted_content
          git init -b main
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Initial commit from ZIP archive"
          git remote add origin "$(echo $REPO_URL | sed "s|https://|https://x-access-token:$TOKEN@|")"
          git push -u origin main
      
      - name: Success summary
        run: |
          cat >> $GITHUB_STEP_SUMMARY << EOF
          ## ✅ Repository Created Successfully
          
          - **Name:** ${{ inputs.repo_name }}
          - **URL:** $(echo "${{ steps.create-repo.outputs.result }}" | sed 's/.git$//')
          - **Files:** ${{ env.FILES_COUNT }}
          - **Visibility:** ${{ inputs.private_repo == 'true' && 'Private 🔒' || 'Public 🌍' }}
          
          [View Repository →]($(echo "${{ steps.create-repo.outputs.result }}" | sed 's/.git$//'))
          EOF
```
