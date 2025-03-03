---
tags: [scratchpad]
info: aberto.
date: 2025-03-03
type: post
layout: post
published: true
slug: claude-code
title: 'Claude Code'
---
Title: Claude Code overview - Anthropic

URL Source: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code

Markdown Content:
Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands. By integrating directly with your development environment, Claude Code streamlines your workflow without requiring additional servers or complex setup.

Claude Code’s key capabilities include:

*   Editing files and fixing bugs across your codebase
*   Answering questions about your code’s architecture and logic
*   Executing and fixing tests, linting, and other commands
*   Searching through git history, resolving merge conflicts, and creating commits and PRs

* * *

Before you begin
----------------

### Check system requirements

*   **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows via WSL
*   **Hardware**: 4GB RAM minimum
*   **Software**:
    *   Node.js 18+
    *   [git](https://git-scm.com/downloads) 2.23+ (optional)
    *   [GitHub](https://cli.github.com/) or [GitLab](https://gitlab.com/gitlab-org/cli) CLI for PR workflows (optional)
    *   [ripgrep](https://github.com/BurntSushi/ripgrep?tab=readme-ov-file#installation) (rg) for enhanced file search (optional)
*   **Network**: Internet connection required for authentication and AI processing
*   **Location**: Available only in [supported countries](https://www.anthropic.com/supported-countries)

### Install and authenticate

* * *

Core features and workflows
---------------------------

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed. Claude Code uses `claude-3-7-sonnet-20250219` by default.

### Security and privacy by design

Your code’s security is paramount. Claude Code’s architecture ensures:

*   **Direct API connection**: Your queries go straight to Anthropic’s API without intermediate servers
*   **Works where you work**: Operates directly in your terminal
*   **Understands context**: Maintains awareness of your entire project structure
*   **Takes action**: Performs real operations like editing files and creating commits

### From questions to solutions in seconds

* * *

### Initialize your project

For first-time users, we recommend:

1.  Start Claude Code with `claude`
2.  Try a simple command like `summarize this project`
3.  Generate a CLAUDE.md project guide with `/init`
4.  Ask Claude to commit the generated CLAUDE.md file to your repository

Use Claude Code for common tasks
--------------------------------

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed.

### Understand unfamiliar code

### Automate Git operations

### Edit code intelligently

### Test and debug your code

### Encourage deeper thinking

For complex problems, explicitly ask Claude to think more deeply:

* * *

Control Claude Code with commands
---------------------------------

### CLI commands

| Command | Description | Example |
| --- | --- | --- |
| `claude` | Start interactive REPL | `$ claude` |
| `claude "query"` | Start REPL with initial prompt | `$ claude "explain this project"` |
| `claude -p "query"` | Run one-off query, then exit | `$ claude -p "explain this function"` |
| `cat file | claude -p "query"` | Process piped content | `$ cat logs.txt | claude -p "explain"` |
| `claude config` | Configure settings | `$ claude config set --global theme dark` |
| `claude update` | Update to latest version | `$ claude update` |
| `claude mcp` | Configure Model Context Protocol servers | [See MCP section in tutorials](https://docs.anthropic.com/en/docs/agents/claude-code/tutorials#set-up-model-context-protocol-mcp) |

**CLI flags**:

*   `--print`: Print response without interactive mode
*   `--verbose`: Enable verbose logging
*   `--dangerously-skip-permissions`: Skip permission prompts (only in Docker containers without internet)

### Slash commands

Control Claude’s behavior within a session:

| Command | Purpose |
| --- | --- |
| `/bug` | Report bugs (sends conversation to Anthropic) |
| `/clear` | Clear conversation history |
| `/compact` | Compact conversation to save context space |
| `/config` | View/modify configuration |
| `/cost` | Show token usage statistics |
| `/doctor` | Checks the health of your Claude Code installation |
| `/help` | Get usage help |
| `/init` | Initialize project with CLAUDE.md guide |
| `/login` | Switch Anthropic accounts |
| `/logout` | Sign out from your Anthropic account |
| `/pr_comments` | View pull request comments |
| `/review` | Request code review |
| `/terminal-setup` | Install Shift+Enter key binding for newlines (iTerm2 and VSCode only) |

Manage permissions and security
-------------------------------

Claude Code uses a tiered permission system to balance power and safety:

| Tool Type | Example | Approval Required | ”Yes, don’t ask again” Behavior |
| --- | --- | --- | --- |
| Read-only | File reads, LS, Grep | No | N/A |
| Bash Commands | Shell execution | Yes | Permanently per project directory and command |
| File Modification | Edit/write files | Yes | Until session end |

### Tools available to Claude

Claude Code has access to a set of powerful tools that help it understand and modify your codebase:

| Tool | Description | Permission Required |
| --- | --- | --- |
| **AgentTool** | Runs a sub-agent to handle complex, multi-step tasks | No |
| **BashTool** | Executes shell commands in your environment | Yes |
| **GlobTool** | Finds files based on pattern matching | No |
| **GrepTool** | Searches for patterns in file contents | No |
| **LSTool** | Lists files and directories | No |
| **FileReadTool** | Reads the contents of files | No |
| **FileEditTool** | Makes targeted edits to specific files | Yes |
| **FileWriteTool** | Creates or overwrites files | Yes |
| **NotebookReadTool** | Reads and displays Jupyter notebook contents | No |
| **NotebookEditTool** | Modifies Jupyter notebook cells | Yes |

### Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant’s instructions by inserting malicious text. Claude Code includes several safeguards against these attacks:

*   **Permission system**: Sensitive operations require explicit approval
*   **Context-aware analysis**: Detects potentially harmful instructions by analyzing the full request
*   **Input sanitization**: Prevents command injection by processing user inputs
*   **Command blocklist**: Blocks risky commands that fetch arbitrary content from the web like `curl` and `wget`

**Best practices for working with untrusted content**:

1.  Review suggested commands before approval
2.  Avoid piping untrusted content directly to Claude
3.  Verify proposed changes to critical files
4.  Report suspicious behavior with `/bug`

### Configure network access

Claude Code requires access to:

*   api.anthropic.com
*   statsig.anthropic.com
*   sentry.io

Allowlist these URLs when using Claude Code in containerized environments.

* * *

Configure Claude Code
---------------------

Configure Claude Code by running `claude config` in your terminal, or the `/config` command when using the interactive REPL.

### Configuration options

Claude Code supports global and project-level configuration.

To manage your configurations, use the following commands:

*   List settings: `claude config list`
*   See a setting: `claude config get <key>`
*   Change a setting: `claude config set <key> <value>`
*   Push to a setting (for lists): `claude config add <key> <value>`
*   Remove from a setting (for lists): `claude config remove <key> <value>`

By default `config` changes your project configuration. To manage your global configuration, use the `--global` (or `-g`) flag.

#### Global configuration

To set a global configuration, use `claude config set -g <key> <value>`:

| Key | Value | Description |
| --- | --- | --- |
| `autoUpdaterStatus` | `disabled` or `enabled` | Enable or disable the auto-updater (default: `enabled`) |
| `preferredNotifChannel` | `iterm2`, `iterm2_with_bell`, `terminal_bell`, or `notifications_disabled` | Where you want to receive notifications (default: `iterm2`) |
| `theme` | `dark`, `light`, `light-daltonized`, or `dark-daltonized` | Color theme |
| `verbose` | `true` or `false` | Whether to show full bash and command outputs (default: `false`) |

### Auto-updater permission options

When Claude Code detects that it doesn’t have sufficient permissions to write to your global npm prefix directory (required for automatic updates), you’ll see a warning that points to this documentation page.

#### Recommended: Create a new user-writable npm prefix

**Why we recommend this option:**

*   Avoids modifying system directory permissions
*   Creates a clean, dedicated location for your global npm packages
*   Follows security best practices

Since Claude Code is actively developing, we recommend setting up auto-updates using the recommended option above.

#### Project configuration

Manage project configuration with `claude config set <key> <value>` (without the `-g` flag):

| Key | Value | Description |
| --- | --- | --- |
| `allowedTools` | array of tools | Which tools can run without manual approval |
| `ignorePatterns` | array of glob strings | Which files/directories are ignored when using tools |

For example:

### Optimize your terminal setup

Claude Code works best when your terminal is properly configured. Follow these guidelines to optimize your experience.

**Supported shells**:

*   Bash
*   Zsh (Fish shell not currently supported)

#### Themes and appearance

Claude cannot control the theme of your terminal. That’s handled by your terminal application. You can match Claude Code’s theme to your terminal during onboarding or any time via the `/config` command

#### Line breaks

You have several options for entering linebreaks into Claude Code:

*   **Quick escape**: Type `\` followed by Enter to create a newline
*   **Keyboard shortcut**: Press Option+Enter (Meta+Enter) with proper configuration

To set up Option+Enter in your terminal:

**For Mac Terminal.app:**

1.  Open Settings → Profiles → Keyboard
2.  Check “Use Option as Meta Key”

**For iTerm2 and VSCode terminal:**

1.  Open Settings → Profiles → Keys
2.  Under General, set Left/Right Option key to “Esc+”

**Tip for iTerm2 and VSCode users**: Run `/terminal-setup` within Claude Code to automatically configure Shift+Enter as a more intuitive alternative.

#### Notification setup

Never miss when Claude completes a task with proper notification configuration:

##### Terminal bell notifications

Enable sound alerts when tasks complete:

**For macOS users**: Don’t forget to enable notification permissions in System Settings → Notifications → \[Your Terminal App\].

##### iTerm 2 system notifications

For iTerm 2 alerts when tasks complete:

1.  Open iTerm 2 Preferences
2.  Navigate to Profiles → Terminal
3.  Enable “Silence bell” and “Send notification when idle”
4.  Set your preferred notification delay

Note that these notifications are specific to iTerm 2 and not available in the default macOS Terminal.

#### Handling large inputs

When working with extensive code or long instructions:

*   **Avoid direct pasting**: Claude Code may struggle with very long pasted content
*   **Use file-based workflows**: Write content to a file and ask Claude to read it
*   **Be aware of VS Code limitations**: The VS Code terminal is particularly prone to truncating long pastes

By configuring these settings, you’ll create a smoother, more efficient workflow with Claude Code.

* * *

Manage costs effectively
------------------------

Claude Code consumes tokens for each interaction. Typical usage costs range from $5-10 per developer per day, but can exceed $100 per hour during intensive use.

### Track your costs

*   Use `/cost` to see current session usage
*   Review cost summary displayed when exiting
*   Check historical usage in [Anthropic Console](https://console.anthropic.com/)
*   Set [Spend limits](https://console.anthropic.com/settings/limits)

### Reduce token usage

*   **Compact conversations:** Use `/compact` when context gets large
*   **Write specific queries:** Avoid vague requests that trigger unnecessary scanning
*   **Break down complex tasks:** Split large tasks into focused interactions
*   **Clear history between tasks:** Use `/clear` to reset context

Costs can vary significantly based on:

*   Size of codebase being analyzed
*   Complexity of queries
*   Number of files being searched or modified
*   Length of conversation history
*   Frequency of compacting conversations

* * *

Use with third-party APIs
-------------------------

### Connect to Amazon Bedrock

Optional: Override the default model (Claude 3.7 Sonnet is used by default):

If you don’t have prompt caching enabled, also set:

Requires standard AWS SDK credentials (e.g., `~/.aws/credentials` or relevant environment variables like `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`). Contact Amazon Bedrock for prompt caching for reduced costs and higher rate limits.

### Connect to Google Vertex AI

Requires standard GCP credentials configured through google-auth-library. For the best experience, contact Google for heightened rate limits.

* * *

Development container reference implementation
----------------------------------------------

Claude Code provides a development container configuration for teams that need consistent, secure environments. This preconfigured [devcontainer setup](https://code.visualstudio.com/docs/devcontainers/containers) works seamlessly with VS Code’s Remote - Containers extension and similar tools.

The container’s enhanced security measures (isolation and firewall rules) allow you to run `claude --dangerously-skip-permissions` to bypass permission prompts for unattended operation. We’ve included a [reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) that you can customize for your needs.

### Key features

*   **Production-ready Node.js**: Built on Node.js 20 with essential development dependencies
*   **Security by design**: Custom firewall restricting network access to only necessary services
*   **Developer-friendly tools**: Includes git, ZSH with productivity enhancements, fzf, and more
*   **Seamless VS Code integration**: Pre-configured extensions and optimized settings
*   **Session persistence**: Preserves command history and configurations between container restarts
*   **Works everywhere**: Compatible with macOS, Windows, and Linux development environments

### Getting started in 4 steps

1.  Install VS Code and the Remote - Containers extension
2.  Clone the [Claude Code reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) repository
3.  Open the repository in VS Code
4.  When prompted, click “Reopen in Container” (or use Command Palette: Cmd+Shift+P → “Remote-Containers: Reopen in Container”)

### Configuration breakdown

The devcontainer setup consists of three primary components:

*   [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controls container settings, extensions, and volume mounts
*   [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Defines the container image and installed tools
*   [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establishes network security rules

### Security features

The container implements a multi-layered security approach with its firewall configuration:

*   **Precise access control**: Restricts outbound connections to whitelisted domains only (npm registry, GitHub, Anthropic API, etc.)
*   **Default-deny policy**: Blocks all other external network access
*   **Startup verification**: Validates firewall rules when the container initializes
*   **Isolation**: Creates a secure development environment separated from your main system

### Customization options

The devcontainer configuration is designed to be adaptable to your needs:

*   Add or remove VS Code extensions based on your workflow
*   Modify resource allocations for different hardware environments
*   Adjust network access permissions
*   Customize shell configurations and developer tooling

* * *

Next steps
----------

* * *

License and data usage
----------------------

Claude Code is provided as a Beta research preview under Anthropic’s [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms).

### How we use your data

We aim to be fully transparent about how we use your data. We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.

#### Feedback transcripts

If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic may use that feedback to debug related issues and improve Claude Code’s functionality (e.g., to reduce the risk of similar bugs occurring in the future). We will not train generative models using this feedback.

### Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

### License

© Anthropic PBC. All rights reserved. Use is subject to Anthropic’s [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms).

Title: Claude Code tutorials - Anthropic

URL Source: https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials

Markdown Content:
This guide provides step-by-step tutorials for common workflows with Claude Code. Each tutorial includes clear instructions, example commands, and best practices to help you get the most from Claude Code.

Table of contents
-----------------

*   [Understand new codebases](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#understand-new-codebases)
*   [Fix bugs efficiently](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#fix-bugs-efficiently)
*   [Refactor code](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#refactor-code)
*   [Work with tests](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#work-with-tests)
*   [Create pull requests](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#create-pull-requests)
*   [Handle documentation](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#handle-documentation)
*   [Use advanced git workflows](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#use-advanced-git-workflows)
*   [Work with images](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#work-with-images)
*   [Set up project memory](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-project-memory)
*   [Use Claude as a unix-style utility](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#use-claude-as-a-unix-style-utility)
*   [Set up Model Context Protocol (MCP)](https://docs.anthropic.com/_sites/docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp)

Understand new codebases
------------------------

### Get a quick codebase overview

**When to use:** You’ve just joined a new project and need to understand its structure quickly.

**Tips:**

*   Start with broad questions, then narrow down to specific areas
*   Ask about coding conventions and patterns used in the project
*   Request a glossary of project-specific terms

### Find relevant code

**When to use:** You need to locate code related to a specific feature or functionality.

**Tips:**

*   Be specific about what you’re looking for
*   Use domain language from the project

* * *

Fix bugs efficiently
--------------------

### Diagnose error messages

**When to use:** You’ve encountered an error message and need to find and fix its source.

**Tips:**

*   Tell Claude the command to reproduce the issue and get a stack trace
*   Mention any steps to reproduce the error
*   Let Claude know if the error is intermittent or consistent

* * *

Refactor code
-------------

### Modernize legacy code

**When to use:** You need to update old code to use modern patterns and practices.

**Tips:**

*   Ask Claude to explain the benefits of the modern approach
*   Request that changes maintain backward compatibility when needed
*   Do refactoring in small, testable increments

* * *

Work with tests
---------------

### Add test coverage

**When to use:** You need to add tests for uncovered code.

**Tips:**

*   Ask for tests that cover edge cases and error conditions
*   Request both unit and integration tests when appropriate
*   Have Claude explain the testing strategy

* * *

Create pull requests
--------------------

### Generate comprehensive PRs

**When to use:** You need to create a well-documented pull request for your changes.

**Tips:**

*   Ask Claude directly to make a PR for you
*   Review Claude’s generated PR before submitting
*   Ask Claude to highlight potential risks or considerations

Handle documentation
--------------------

### Generate code documentation

**When to use:** You need to add or update documentation for your code.

**Tips:**

*   Specify the documentation style you want (JSDoc, docstrings, etc.)
*   Ask for examples in the documentation
*   Request documentation for public APIs, interfaces, and complex logic

Work with images
----------------

### Analyze images and screenshots

**When to use:** You need to work with images in your codebase or get Claude’s help analyzing image content.

**Tips:**

*   Use images when text descriptions would be unclear or cumbersome
*   Include screenshots of errors, UI designs, or diagrams for better context
*   You can work with multiple images in a conversation
*   Image analysis works with diagrams, screenshots, mockups, and more

* * *

Set up project memory
---------------------

### Create an effective CLAUDE.md file

**When to use:** You want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands.

**Tips:**

*   Include frequently used commands (build, test, lint) to avoid repeated searches
*   Document code style preferences and naming conventions
*   Add important architectural patterns specific to your project
*   You can add CLAUDE.md files to the folder you run Claude in, parent directories (Claude reads these automatically), or child directories (Claude pulls these in on demand)

* * *

Use Claude as a unix-style utility
----------------------------------

### Add Claude to your verification process

**When to use:** You want to use Claude Code as a linter or code reviewer.

**Steps:**

### Pipe in, pipe out

**When to use:** You want to pipe data into Claude, and get back data in a structured format.

* * *

Set up Model Context Protocol (MCP)
-----------------------------------

Model Context Protocol (MCP) is an open protocol that enables LLMs to access external tools and data sources. For more details, see the [MCP documentation](https://modelcontextprotocol.io/introduction).

### Configure MCP servers

**When to use:** You want to enhance Claude’s capabilities by connecting it to specialied tools and external servers using the Model Context Protocol.

**Tips:**

*   Use the `-s` or `--scope` flag with `project` (default) or `global` to specify where the configuration is stored
*   Set environment variables with `-e` or `--env` flags (e.g., `-e KEY=value`)
*   MCP follows a client-server architecture where Claude Code (the client) can connect to multiple specialized servers

### Connect to a Postgres MCP server

**When to use:** You want to give Claude read-only access to a PostgreSQL database for querying and schema inspection.

**Tips:**

*   The Postgres MCP server provides read-only access for safety
*   Claude can help you explore database structure and run analytical queries
*   You can use this to quickly understand database schemas in unfamiliar projects
*   Make sure your connection string uses appropriate credentials with minimum required permissions

* * *

Next steps
----------

[Claude Code reference implementation ------------------------------------ Clone our development container reference implementation.](https://github.com/anthropics/claude-code/tree/main/.devcontainer)