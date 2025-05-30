---
tags: [scratchpad]
info: aberto.
date: 2025-05-19
type: post
layout: post
published: true
slug: messy-folder-reorganizer-documentation
title: 'messy folder reorganizer documentation'
---
~~~
<!-- [![codecov](/gh/PerminovEugene/messy-folder-reorganizer-ai/branch/main/graph/badge.svg)](/gh/PerminovEugene/messy-folder-reorganizer-ai) -->

![Build](/github/actions/workflow/status/PerminovEugene/messy-folder-reorganizer-ai/ci.yml?branch=main)
![License](/github/license/PerminovEugene/messy-folder-reorganizer-ai)
![Language](/github/languages/top/PerminovEugene/messy-folder-reorganizer-ai)
![Local AI](/badge/AI-local--only-green?logo=ai)

## messy-folder-reorganizer-ai - 🤖 AI-powered CLI for file reorganization.

### Runs fully locally — no data leaves your machine.

### How It Works

CLI supports multiple commands:

#### Process

1. **User Input** – The user runs the app and provides:

   - a **source folder** path containing the files to organize
   - a **destination folder** path where organized files will be placed
   - an **AI model name** (loaded in Ollama) used to generate folder names
   - an **embedding model name** (also loaded in Ollama) used to generate vector embeddings

2. **Destination Folder Scan**

   - The app scans the destination folder and generates embeddings for each folder name.
   - These embeddings are stored in a **Qdrant** vector database.

3. **Source Folder Scan**

   - The app scans the source folder and generates embeddings for each file name.
   - It compares each file’s embedding to existing folder embeddings in the database.
   - Files without a sufficiently close match are marked for further processing.

4. **Clustering & AI Folder Naming**

   - Unmatched file embeddings are grouped using **agglomerative hierarchical clustering**.
   - Each cluster is sent to the LLM to generate a suggested folder name.

5. **Preview Results**

   - A table is displayed showing the proposed destination for each file.

6. **User Decision**
   - The user reviews the suggested structure and decides whether to apply the changes.

#### Apply

If you decided to not apply changes after `process`, you can apply changes later with `apply` command. It expects that you didn't change files locations. This command applied migrations from the latest succesfull `process` launch.

#### Rollback

For the case if after files migrations you are changed your mind and want to return everything back.

> ⚠️ **Warning:** Do not use `messy-folder-reorganizer-ai` on important files such as passwords, confidential documents, or critical system files.  
> In the event of a bug or interruption, the app may irreversibly modify or delete files. Always create backups before using it on valuable data.  
> The author assumes no responsibility for data loss or misplaced files caused by this application.

## Small articles for the curious minds

📌 [Adding RAG & ML to the CLI](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3)

📌 [How cosine similarity helped files find their place](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3)

📌 [Teaching embeddings to understand folders](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg)

📌 [Hierarchical clustering for file grouping](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k)

## Setup

1. Install core developer tools

- macOS

  ```
  Install or update **Xcode**
  ```

- Linux x86_64

  ```sh
  sudo apt update
  sudo apt install -y build-essential
  ```

2. Install **Ollama** and start the service.
3. Download the required LLM via Ollama:

   ```sh
   ollama pull deepseek-r1:latest
   ```

   > Recommended: Use models with a higher number of parameters for better accuracy.  
   > This project has been tested with `deepseek-r1:latest` (4.7 GB, 7.6B params).

4. Download the embedding model:

   ```sh
   ollama pull mxbai-embed-large:latest
   ```

5. Launch Qdrant vector database (easiest via Docker):

   ```sh
   docker pull qdrant/qdrant
   docker run -p 6333:6333 \
     -v $(pwd)/path/to/data:/qdrant/storage \
     qdrant/qdrant
   ```

6. Download the latest app release:

- Apple Silicon (macOS ARM64):

  ```sh
  curl -s https://api.github.com/repos/PerminovEugene/messy-folder-reorganizer-ai/releases/tags/v0.2.0 | \
    grep "browser_download_url.*messy-folder-reorganizer-ai-v0.2.0-aarch64-apple-darwin.tar.gz" | \
    cut -d '"' -f 4 | \
    xargs curl -L -o messy-folder-reorganizer-ai-macos-arm64.tar.gz
  ```

- Intel Mac (macOS x86_64):

  ```sh
  curl -s https://api.github.com/repos/PerminovEugene/messy-folder-reorganizer-ai/releases/tags/v0.2.0 | \
    grep "browser_download_url.*messy-folder-reorganizer-ai-v0.2.0-x86_64-apple-darwin.tar.gz" | \
    cut -d '"' -f 4 | \
    xargs curl -L -o messy-folder-reorganizer-ai-macos-x64.tar.gz
  ```

- Linux x86_64:

  ```sh
  curl -s https://api.github.com/repos/PerminovEugene/messy-folder-reorganizer-ai/releases/tags/v0.2.0 | \
    grep "browser_download_url.*messy-folder-reorganizer-ai-v0.2.0-x86_64-unknown-linux-gnu.tar.gz" | \
    cut -d '"' -f 4 | \
    xargs curl -L -o messy-folder-reorganizer-ai-linux-x64.tar.gz
  ```

7. Extract and install:

- Apple Silicon (macOS ARM64):

  ```sh
  tar -xvzf messy-folder-reorganizer-ai-macos-arm64.tar.gz
  sudo mv messy-folder-reorganizer-ai /usr/local/bin/messy-folder-reorganizer-ai
  ```

- Intel Mac (macOS x86_64):

  ```sh
  tar -xvzf messy-folder-reorganizer-ai-macos-x64.tar.gz
  sudo mv messy-folder-reorganizer-ai /usr/local/bin/messy-folder-reorganizer-ai
  ```

- Linux x86_64:

  ```sh
  tar -xvzf messy-folder-reorganizer-ai-linux-x64.tar.gz
  sudo mv messy-folder-reorganizer-ai /usr/local/bin/messy-folder-reorganizer-ai
  ```

8. Verify the installation:

   ```sh
   messy-folder-reorganizer-ai --help
   ```

## Build from Source

1. Clone the repository:

   ```sh
   git clone git@github.com:PerminovEugene/messy-folder-reorganizer-ai.git
   ```

2. Build the project:

   ```sh
   cargo build --release
   ```

3. Run it:

   ```sh
   cargo run -- \
     -E mxbai-embed-large \
     -L deepseek-r1:latest \
     -S ./test_cases/clustering/messy-folder \
     -D ./test_cases/clustering/structured-folder
   ```

## Usage

### Run the App

```sh
messy-folder-reorganizer-ai process \
  -E <EMBEDDING_MODEL_NAME> \
  -L <LLM_MODEL_NAME> \
  -S <SOURCE_FOLDER_PATH> \
  -D <DESTINATION_FOLDER_PATH>
```

```sh
messy-folder-reorganizer-ai apply \
  -i <SESSION_ID>
```

```sh
messy-folder-reorganizer-ai rollback \
 -i <SESSION_ID>
```

## Command-Line Arguments

The CLI supports the following subcommands:

---

### `process`

Processes source files, finds best-matching destination folders using embeddings, and generates a migration plan.

| Argument                  | Short | Default                  | Description                                                                          |
| ------------------------- | ----- | ------------------------ | ------------------------------------------------------------------------------------ |
| `--language-model`        | `-L`  | _required_               | Ollama LLM model name used to generate semantic folder names.                        |
| `--embedding-model`       | `-E`  | _required_               | Embedding model used for representing folder and file names as vectors.              |
| `--source`                | `-S`  | _required_               | Path to the folder with unorganized files.                                           |
| `--destination`           | `-D`  | `home`                   | Path to the folder where organized files should go.                                  |
| `--recursive`             | `-R`  | `false`                  | Whether to scan subfolders of the source folder recursively.                         |
| `--force-apply`           | `-F`  | `false`                  | Automatically apply changes after processing without showing preview.                |
| `--continue-on-fs-errors` | `-C`  | `false`                  | Allow skipping files/folders that throw filesystem errors (e.g., permission denied). |
| `--llm-address`           | `-n`  | `http://localhost:11434` | Address of the local or remote Ollama LLM server.                                    |
| `--qdrant-address`        | `-q`  | `http://localhost:6334`  | Address of the Qdrant vector database instance.                                      |

---

### `apply`

Applies a previously saved migration plan using the session ID.
Session Id will be printed during `process` execution.

| Argument       | Short | Description                                        |
| -------------- | ----- | -------------------------------------------------- |
| `--session-id` | `-i`  | The session ID generated by the `process` command. |

---

### 🔙 `rollback`

Rolls back a previously applied migration using the session ID.
Session Id will be printed during `process` execution.

| Argument       | Short | Description                                              |
| -------------- | ----- | -------------------------------------------------------- |
| `--session-id` | `-i`  | The session ID used to identify which migration to undo. |

## Configuration

### Model & ML Configuration

On the first run, the app creates a `.messy-folder-reorganizer-ai/` directory in your home folder containing:

- llm_config.toml – LLM model request configuration options
- embeddings_config.toml – Embedding model request configuration options
- rag_ml_config.toml – RAG and ML behavior settings

Model request configurations are commented out by default and will fall back to built-in values unless edited.

More information about LLM and Embedding model configuration options can be found [https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values](here).

RAG and ML configuration parameters are required and should always be present in rag_ml_config.toml.
You also can set up ignore lists for destionation and source pathes in that config file.

You can change the path where `.messy-folder-reorganizer-ai` will be created. Simply add `MESSY_FOLDER_REORGANIZER_AI_PATH` environment variable with path with desired location.

### Prompt Customization

Prompts are stored in:

```sh
~/.messy-folder-reorganizer-ai/prompts/
```

You can edit these to experiment with different phrasing.  
The source file list will be appended automatically, so **do not** use `{}` or other placeholders in the prompt.

Feel free to contribute improved prompts via PR!

### Auto-Recovery

If you break or delete any config/prompt files, simply re-run the app — missing files will be regenerated with default values.

### Additional help

- [Ollama GitHub](https://github.com/ollama/ollama)
- [Embedding Models with Ollama](https://ollama.com/blog/embedding-models)
- [Qdrant Docs](https://qdrant.tech/documentation/guides/installation/)

## Contributing

1. Run the setup script before contributing:

   ```sh
   bash setup-hooks.sh
   ```

2. Lint & format code:

   ```sh
   cargo clippy
   cargo fmt
   ```

3. Check for unused dependencies:

   ```sh
   cargo +nightly udeps
   ```

### Running tests:

To run all tests

```sh
cargo test
```

To run integration tests

```sh
cargo test --test '*' -- --nocapture
```

To run specific integration test (file_collision for example)

```sh
cargo test file_collision -- --nocapture
```

## Uninstall & Purge

```sh
rm -f /usr/local/bin/messy-folder-reorganizer-ai
rm -rf ~/.messy-folder-reorganizer-ai
```

## License

This project is dual-licensed under either:

- [MIT License](./LICENSE-MIT)
- [Apache License, Version 2.0](./LICENSE-APACHE)

at your option.

It interacts with external services including:

- [Ollama](https://github.com/ollama/ollama) – MIT License
- [Qdrant](https://github.com/qdrant/qdrant) – Apache 2.0 License
~~~

:::

~~~
Title: How I Built a Local LLM-Powered File Reorganizer with Rust

URL Source: /evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip

Published Time: 2025-02-19T15:20:29Z

Markdown Content:
[[1: Cover image for How I Built a Local LLM-Powered File Reorganizer with Rust](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F0x60v2k0khd050bbcyfn.png)](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F0x60v2k0khd050bbcyfn.png)

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#introduction-diving-back-into-rust) Introduction: Diving (Back) Into Rust
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Some time ago, I decided to dive into Rust **once again**—this must be my _nth_ attempt. I’d tried learning it before, but each time I either got swamped by the borrow checker or got sidetracked by other projects. This time, I wanted a small, _practical_ project to force myself to stick with Rust. The result is [messy-folder-reorganizer-ai](https://github.com/PerminovEugene/messy-folder-reorganizer-ai/tree/main), a command-line tool for file organization powered by a local LLM.

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#the-inspiration-a-bloated-downloads-folder) The Inspiration: A Bloated Downloads Folder
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The main motivation was my messy **Downloads** folder, which often ballooned to hundreds of files—images, documents, installers—essentially chaos. Instead of manually sorting through them, I thought, “Why not let an AI propose a structure?”

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#discovering-local-llms) Discovering Local LLMs
----------------------------------------------------------------------------------------------------------------------------------------------

While brainstorming, I stumbled upon the possibility of running LLMs **locally**, like Ollama or other self-hosted frameworks. I loved the idea of **not sending** my data to some cloud service. So I decided to build a Rust-based CLI that **queries** a local LLM server for suggestions on how to reorganize my folders.

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#challenges-llm-amp-large-folders) Challenges: LLM & Large Folders
-----------------------------------------------------------------------------------------------------------------------------------------------------------------

*   **Initial Model:** I started using `llama3.2:1b`, but the responses didn’t follow prompt instructions well, so I switched to **deepseek-r1**, which performed much better. 
*   **Context Limits:** When testing on folders with many files, the model began forgetting the beginning of the prompt and stopped following instructions properly. Increasing `num_ctx` (which defines the model’s context size) helped partially, but the model still struggles with **100+ files**. 
*   **Possible Solutions:**
    *   **Batching Requests:** Split the file list into smaller chunks and send multiple prompts. 
    *   **Other Ideas?:** If you’re an LLM expert—especially with local models like Ollama—I’d love advice on how to handle larger sets without hitting memory or context limits.

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#cli-features) CLI Features
--------------------------------------------------------------------------------------------------------------------------

*   **Configurable Model:** Specify the local LLM endpoint, model name, or other model options. 
*   **Customizable Prompts:** Tweak the AI prompt to fine-tune how the model interprets your folder’s contents. 
*   **Confirmation Prompt:** The tool shows you the proposed structure and asks for confirmation before reorganizing any files.

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#looking-for-feedback) Looking for Feedback
------------------------------------------------------------------------------------------------------------------------------------------

*   **Rust Community:** I’d love code feedback — best practices, performance tips, or suggestions on how to structure the CLI. 
*   **LLM Gurus:** Any advice on optimizing local model inference for large file sets or advanced chunking strategies would be invaluable.

* * *

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#conclusion) Conclusion
----------------------------------------------------------------------------------------------------------------------

This project has been a great way to re-learn some Rust features and experiment with local AI solutions. While it works decently for medium-sized folders, there’s plenty of room to grow. If this concept resonates with you—maybe your Downloads folder is as messy as mine—give it a try, open an issue, or contribute a pull request.

**Thanks for reading!**

Feel free to reach out on the [GitHub issues page](https://github.com/PerminovEugene/messy-folder-reorganizer-ai/issues), or drop me a note if you have any thoughts, suggestions, or just want to talk about Rust and AI!

[[2: Heroku](width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FEtkoO96.png)](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)

[](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip#built-for-developers-by-developers)[Built for developers, by developers.](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Whether you're building a simple prototype or a business-critical product, Heroku's fully-managed platform gives you the simplest path to delivering apps quickly — using the tools and languages you already love!

[Learn More](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)
~~~


:::

~~~
Title: Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)

URL Source: /evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3

Published Time: 2025-03-28T15:41:36Z

Markdown Content:
Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai) - DEV Community
===============
[Skip to content](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#main-content)

[[1: DEV Community](quality=100/https://dev-to-uploads.s3.amazonaws.com/uploads/logos/resized_logo_UQww2soKuUsjaOGNB38o.png)](/)

[Powered by Algolia](https://www.algolia.com/developers/?utm_source=devto&utm_medium=referral)

[Log in](/enter)[Create account](/enter?state=new-user)

DEV Community
-------------

[2](heart-plus-active-9ea3b22f2bc311281db911d416166c5f430636e76b15cd5df6b3b841d830eefa.svg)1 Add reaction 

[3](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)1 Like [4](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)0 Unicorn [5](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)0 Exploding Head [6](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)0 Raised Hands [7](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)0 Fire 

0 Jump to Comments 0 Save  Boost 

 Moderate 

Copy link

Copied to Clipboard

[Share to X](https://twitter.com/intent/tweet?text=%22Adding%20RAG%20and%20ML%20to%20AI%20files%20reorganization%20CLI%20%28messy-folder-reorganizer-ai%29%22%20by%20Evgenii%20Perminov%20%23DEVCommunity%20https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fadding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3)[Share to LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fadding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3&title=Adding%20RAG%20and%20ML%20to%20AI%20files%20reorganization%20CLI%20%28messy-folder-reorganizer-ai%29&summary=A%20month%20ago%2C%20I%20created%20the%20first%20naive%20version%20of%20a%20CLI%20tool%20for%20AI-powered%20file%20reorganization%20in...&source=DEV%20Community)[Share to Facebook](https://www.facebook.com/sharer.php?u=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fadding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3)[Share to Mastodon](https://toot.kytta.dev/?text=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fadding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3)

[Share Post via...](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#)[Report Abuse](/report-abuse)

[[8: Cover image for Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzgjimz33n68u6crsuf89.png)](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fzgjimz33n68u6crsuf89.png)

[[9: Evgenii Perminov](width=50,height=50,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1973401%2F3bc0834c-aae8-4342-9fbb-14588e5533f9.jpg)](/evgeniiperminov)

[Evgenii Perminov](/evgeniiperminov)
Posted on Mar 28

[10](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)1[11](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)[12](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)[13](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)[14](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)

Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)
==============================================================================

[#llm](/t/llm)[#cli](/t/cli)[#opensource](/t/opensource)[#rag](/t/rag)

[messy-folder-reorganizer-ai (4 Part Series)](/evgeniiperminov/series/30981)
------------------------------------------------------------------------------------------

[1 Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3 "Published Mar 28")[2 How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai)](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3 "Published Mar 28")[3 Making Embeddings Understand Files and Folders with Simple Sentences (messy-folder-reorganizer-ai)](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg "Published Mar 28")[4 Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k "Published Mar 28")

A month ago, I created the first naive version of a CLI tool for AI-powered file reorganization in Rust — [messy-folder-reorganizer-ai](https://github.com/PerminovEugene/messy-folder-reorganizer-ai). It sent file names and paths to Ollama and asked the LLM to generate new paths for each file. This worked fine for a small number of files, but once the count exceeded around 50, the LLM context filled up quickly.

So, I decided to improve the entire workflow by integrating RAG (Retrieval-Augmented Generation).

* * *

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#version-02-workflow-updates) Version 0.2 Workflow Updates
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Here’s how adding RAG and a bit of ML helped improve the file reorganization flow in the CLI:

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#1-custom-source-and-destination-paths) 1. Custom Source and Destination Paths

First, I allowed users to specify different paths:

*   A **source path** where files are located.
*   A **destination path** where files will be moved.

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#2-adding-rag-with-qdrant) 2. Adding RAG with Qdrant

Next, I introduced RAG into the system. As a vector database, I chose [Qdrant](https://qdrant.tech/) — an open-source, easy-to-run local vector store.

> _Currently, users need to manually download and launch Qdrant. Automatic setup is planned for future versions._

The core of RAG is generating embeddings from text. Here's the step-by-step:

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#3-embedding-folder-and-file-names) 3. Embedding Folder and File Names

The CLI sends destination folder names and source file names to an Ollama embedding model. The model returns an embedding (vector) for each name.

#### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#contextualizing-the-input) Contextualizing the Input

Instead of sending raw names, I added context like:

`"This is a folder name: {folder_name}"`

> _A more detailed explanation will be in the next article._

#### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#embedding-model-selection) Embedding Model Selection

Different models return vectors of different dimensions. I used the **mxbai-embed-large:latest** model from Ollama, which produces 1024-dimensional vectors. It performed well for most use cases.

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#4-storing-folder-embeddings-in-qdrant) 4. Storing Folder Embeddings in Qdrant

Each destination folder's embedding is stored in Qdrant, with the original folder name included as payload metadata.

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#5-matching-files-to-closest-folders) 5. Matching Files to Closest Folders

For each source file embedding, the CLI searches Qdrant for the closest destination folder vector.

 Qdrant returns the most similar match along with a similarity score.

> _More about similarity measures and why I picked a particular one will be covered in the third article._

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#6-thresholdbased-filtering) 6. Threshold-Based Filtering

The CLI compares each similarity score to a configurable threshold (set via config files). If no suitable match is found, the file is filtered out and sent to an additional step — **clustering** and **folder name generation via LLM**.

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#7-clustering-unmatched-files) 7. Clustering Unmatched Files

Since LLMs struggle with large input contexts, we split unmatched files into clusters using machine learning — specifically **agglomerative hierarchical clustering**.

> _More details about clustering are in the fourth article in this series._

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#8-naming-clusters-via-llm) 8. Naming Clusters via LLM

Once clustering is complete, we end up with small, manageable groups of files. For each cluster, we send a prompt to the LLM to generate a suitable folder name.

After some LLM thinking time, we receive the missing folder names and can show the user a preview of the proposed file reorganization.

### [](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#9-applying-the-changes) 9. Applying the Changes

If the user is happy with the proposed structure, they can confirm it. The CLI will then move the files to their new paths accordingly.

* * *

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#conclusion) Conclusion
-----------------------------------------------------------------------------------------------------------------------------------------

In the upcoming articles, I’ll dive into some of the more technical and interesting parts of the project:

*   How to choose a similarity search method.
*   Ways to improve embeddings for files and folders.
*   Selecting and preparing data for clustering.

* * *

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#looking-for-feedback) Looking for Feedback
-------------------------------------------------------------------------------------------------------------------------------------------------------------

I’d really appreciate any feedback — positive or critical — on the project, the codebase, the article series, or the general approach used in the CLI.

* * *

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#thanks-for-reading)**Thanks for Reading!**
-------------------------------------------------------------------------------------------------------------------------------------------------------------

Feel free to reach out here or connect with me on:

*   [GitHub](https://github.com/PerminovEugene)
*   [LinkedIn](https://www.linkedin.com/in/eugene-perminov/)

Or just drop me a note if you want to chat about Rust, AI, or creative ways to clean up messy folders!

[messy-folder-reorganizer-ai (4 Part Series)](/evgeniiperminov/series/30981)
------------------------------------------------------------------------------------------

[1 Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3 "Published Mar 28")[2 How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai)](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3 "Published Mar 28")[3 Making Embeddings Understand Files and Folders with Simple Sentences (messy-folder-reorganizer-ai)](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg "Published Mar 28")[4 Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k "Published Mar 28")

[[15: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F123%2F38b10714-65da-4f1d-88ae-e9b28c1d7a5e.png) Heroku](/heroku)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=217501)

[[16: Heroku](width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FEtkoO96.png)](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#built-for-developers-by-developers)[Built for developers, by developers.](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Whether you're building a simple prototype or a business-critical product, Heroku's fully-managed platform gives you the simplest path to delivering apps quickly — using the tools and languages you already love!

[Learn More](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)

 Read More 

Top comments (0)
----------------

Subscribe

[17: pic](width=256,height=,fit=scale-down,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8j7kvp660rqzt99zui8e.png)

Personal Trusted User[Create template](/settings/response-templates)
Templates let you quickly answer FAQs or store snippets for re-use.

Submit Preview[Dismiss](/404.html)

[Code of Conduct](/code-of-conduct)•[Report abuse](/report-abuse)

Are you sure you want to hide this comment? It will become hidden in your post, but will still be visible via the comment's [permalink](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#).

- [x] 
Hide child comments as well

 
Confirm

For further actions, you may consider blocking this person and/or [reporting abuse](/report-abuse)

[[18: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F1726%2Fe01690b9-c8bd-4eb9-bbe2-a4db25a702a9.png) AWS](/aws)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=228259)

[[19: AWS Security LIVE! Stream](width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2F9Zvgtm6.png)](https://aws.bpc.digital/3Cxb0RL?bb=228259)

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#stream-aws-security-live)[Stream AWS Security LIVE!](https://aws.bpc.digital/3Cxb0RL?bb=228259)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

See how AWS is redefining security by design with simple, seamless solutions on Security LIVE!

[Learn More](https://aws.bpc.digital/3Cxb0RL?bb=228259)

Read next
---------

[[20: fallon_jimmy profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F2191871%2F01077452-5ffd-4131-9dde-caaffa7e2af8.jpg) ### Suna AI: Open-Source General Software: Cost and Deployment Tutorial🔥 Fallon Jimmy - May 6](/fallon_jimmy/suna-ai-open-source-general-software-cost-and-deployment-tutorial-3bk9)[[21: aairom profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F430591%2F85dbea8d-e5cb-47db-a4a7-ddb98f739bb5.jpeg) ### Using Docling’s OCR features with RapidOCR Alain Airom - Apr 3](/aairom/using-doclings-ocr-features-with-rapidocr-29hd)[[22: deepanshup04 profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1404950%2Fd5728a67-8686-40aa-8e4a-e5ace47349ef.jpg) ### Unlocking Efficiency: The Power of Kong AI Gateway Deepanshu Pandey - Apr 26](/deepanshup04/unlocking-efficiency-the-power-of-kong-ai-gateway-4f9m)[[23: seuros profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F766706%2F3d9f585d-7da2-4e5f-a994-9e0c8b4db410.png) ### Smarter RAG Systems with Graphs Abdelkader Boudih - May 6](/seuros/smarter-rag-systems-with-graphs-4bg)

[[24](width=90,height=90,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1973401%2F3bc0834c-aae8-4342-9fbb-14588e5533f9.jpg) Evgenii Perminov](/evgeniiperminov)

Follow

 Hey! My name is Evgenii and I am software engineer with 10 years of experience. Currently working on Rust+AI based CLI for files reorganization. 

*    Location   Estonia  
*    Joined  Aug 24, 2024 

### More from [Evgenii Perminov](/evgeniiperminov)

[Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai) #vectordatabase#ai#machinelearning#cli](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k)[How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai) #llm#rust#cli#opensource](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3)[How I Built a Local LLM-Powered File Reorganizer with Rust #llm#rust#cli#opensource](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip)

[[25: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F5369%2Fbf0b17ac-3757-4494-ae6d-69f47c5be2c2.png) Stellar Development Foundation](/stellar)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=225974)

[[26: Image of Stellar post](width=350%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FFHXRlQs.png)](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#how-a-hackathon-win-led-to-my-startup-getting-funded)[How a Hackathon Win Led to My Startup Getting Funded](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

In this episode, you'll see:

*   The hackathon wins that sparked the journey.
*   The moment José and Joseph decided to go all-in.
*   Building a working prototype on Stellar.
*   Using the PassKeys feature of Soroban.
*   Getting funded via the Stellar Community Fund.

[Watch the video 🎥](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)

👋 Kindness is contagious

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=225483)

Dive into this thoughtful article, cherished within the supportive DEV Community. **Coders of every background** are encouraged to share and grow our collective expertise.

A genuine "thank you" can brighten someone’s day—drop your appreciation in the comments below!

On DEV, **sharing knowledge smooths our journey** and strengthens our community bonds. Found value here? A quick thank you to the author makes a big difference.

[](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3#-cta-httpsdevtoenterstatenewuser-)[Okay](/enter?state=new-user&bb=225483)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

💎 DEV Diamond Sponsors

Thank you to our Diamond Sponsors for supporting the DEV Community

[[27: Neon - Official Database Partner](width=880%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fbnl88cil6afxzmgwrgtt.png)](https://neon.tech/?ref=devto&bb=146443)
Neon is the official database partner of DEV

[[28: Algolia - Official Search Partner](width=880%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fv30ephnolfvnlwgwm0yz.png)](https://www.algolia.com/developers/?utm_source=devto&utm_medium=referral&bb=146443)
Algolia is the official search partner of DEV

[DEV Community](/) — A space to discuss and keep up software development and manage your software career

*   [Home](/)
*   [DEV++](/++)
*   [Podcasts](/pod)
*   [Videos](/videos)
*   [Tags](/tags)
*   [DEV Help](/help)
*   [Forem Shop](https://shop.forem.com/)
*   [Advertise on DEV](/advertise)
*   [DEV Challenges](/challenges)
*   [DEV Showcase](/showcase)
*   [About](/about)
*   [Contact](/contact)
*   [Free Postgres Database](/free-postgres-database-tier)
*   [Software comparisons](/software-comparisons)

*   [Code of Conduct](/code-of-conduct)
*   [Privacy Policy](/privacy)
*   [Terms of use](/terms)

Built on [Forem](https://www.forem.com/) — the [open source](/t/opensource) software that powers [DEV](/) and other inclusive communities.

Made with love and [Ruby on Rails](/t/rails). DEV Community © 2016 - 2025.

[29: DEV Community](width=190,height=,fit=scale-down,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8j7kvp660rqzt99zui8e.png)

We're a place where coders share, stay up-to-date and grow their careers.

[Log in](/enter)[Create account](/enter?state=new-user)

[30](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)[31](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)[32](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)[33](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)[34](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)
~~~


:::

~~~
Title: How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai)

URL Source: /evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3

Published Time: 2025-03-28T15:41:57Z

Markdown Content:
[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#introduction) Introduction
----------------------------------------------------------------------------------------------------------------------------------------------------------

In version 0.2 of [messy-folder-reorganizer-ai](https://github.com/PerminovEugene/messy-folder-reorganizer-ai), I used the Qdrant vector database to search for similar vectors. This was necessary to determine which folder a file should go into based on its embedding. Because of this, I needed to revisit different distance/similarity metrics and choose the most appropriate one.

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#choosing-the-right-vector-similarity-metric-in-qdrant) Choosing the Right Vector Similarity Metric in Qdrant
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Qdrant supports the following distance/similarity metrics:

*   **Dot Product**
*   **Cosine Similarity**
*   **Euclidean Distance**
*   **Manhattan Distance**

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#distancesimilarity-formulas) Distance/Similarity Formulas

Let **x** and **y** be two vectors of dimensionality _n_.

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#cosine-similarity) Cosine Similarity

cosine(x, y) = (x · y) / (‖x‖ · ‖y‖)

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#dot-product) Dot Product

dot(x, y) = Σ (xᵢ * yᵢ)

> ⚠️ If vectors are normalized to unit length, then: `cosine(x, y) = dot(x, y)`

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#euclidean-distance) Euclidean Distance

euclidean(x, y) = sqrt(Σ (xᵢ - yᵢ)²)

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#manhattan-distance-l1) Manhattan Distance (L1)

manhattan(x, y) = Σ |xᵢ - yᵢ|

When working with high-dimensional vectors (e.g., 1024 dimensions, as in the **mxbai-embed-large:latest** Ollama model) that have **small magnitudes**, **Cosine Similarity** is often the best choice — especially for embeddings.

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#why-cosine-similarity-is-a-good-choice) Why Cosine Similarity is a Good Choice
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#focuses-on-orientation-not-magnitude) Focuses on orientation, not magnitude

Cosine similarity measures the angle between vectors. It tells you 

 how similar the directions are*, regardless of vector length. This 

 is useful when comparing embeddings, where absolute length may not 

 be meaningful.

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#builtin-normalization) Built-in normalization

Cosine similarity is equivalent to the dot product of **L2-

 normalized vectors**, which helps reduce the effect of the "curse 

 of dimensionality."

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#great-for-semantic-embeddings) Great for semantic embeddings

Works very well when vectors represent meaning or context. Many models (e.g., OpenAI, BERT, Sentence Transformers) are trained 

 with cosine similarity in mind.

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#efficient) Efficient

Can be computed quickly even in high dimensions.

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#cosine-similarity-in-detail) Cosine Similarity in Detail
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Imagine two arrows (vectors) starting from the origin in a multi-dimensional space. Cosine similarity measures the **angle between them**:

*   If they point in **exactly the same direction**, similarity = `1.0`
*   If they are **completely opposite**, similarity = `-1.0`
*   If they are **orthogonal** (90° apart), similarity = `0.0`

The closer the angle is to zero, the more similar the vectors are.

* * *

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#formula) Formula

Given two vectors **A** and **B**, cosine similarity is calculated as:

cos(θ) = (A · B) / (||A|| * ||B||)

*   `A · B` is the dot product of the vectors 
*   `||A||` and `||B||` are the magnitudes (lengths) of the vectors

* * *

### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#example) Example

Let's take two simple 2D vectors:

A = [1, 2] B = [2, 3]

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#1-dot-product) 1. Dot Product:

A · B = (1 * 2) + (2 * 3) = 2 + 6 = 8

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#2-magnitudes) 2. Magnitudes:

||A|| = √(1² + 2²) = √5 ≈ 2.236 ||B|| = √(2² + 3²) = √13 ≈ 3.606

#### [](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#3-cosine-similarity) 3. Cosine Similarity:

cos(θ) = 8 / (2.236 * 3.606) ≈ 8 / 8.062 ≈ 0.993

**Result: 0.993** — Very high similarity!

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#in-the-context-of-the-cli) In the Context of the CLI
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

In `messy-folder-reorganizer-ai`, embeddings represent file and folder names. Cosine similarity allows the CLI to:

*   Find files with similar meaning or content 
*   Group files together 
*   Match files to folder "themes" based on vector similarity

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#looking-for-feedback) Looking for Feedback
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I’d really appreciate any feedback — positive or critical — on the project, the codebase, the article series, or the general approach used in the CLI.

* * *

[](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3#thanks-for-reading)**Thanks for Reading!**
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Feel free to reach out here or connect with me on:

*   [GitHub](https://github.com/PerminovEugene)
*   [LinkedIn](https://www.linkedin.com/in/eugene-perminov/)

Or just drop me a note if you want to chat about Rust, AI, or creative ways to clean up messy folders!
~~~


:::

~~~
Title: Making Embeddings Understand Files and Folders with Simple Sentences (messy-folder-reorganizer-ai)

URL Source: /evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg

Published Time: 2025-03-28T15:42:08Z

Markdown Content:
[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#do-embeddings-need-context-a-practical-look-at-filetofolder-matching) Do Embeddings Need Context? A Practical Look at File-to-Folder Matching
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

When building smart systems that classify or match content — such as automatically sorting files into folders — embeddings are a powerful tool. But how well do they work with minimal input? And does adding natural language context make a difference?

During development [messy-folder-reorganizer-ai](https://github.com/PerminovEugene/messy-folder-reorganizer-ai) I found how adding **contextual phrasing** to file and folder names significantly improved the performance of embedding models and in this article I will share it with the reader.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-case-matching-files-to-valid-folder-names) Test Case: Matching Files to Valid Folder Names
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-a-using-only-file-and-folder-names) Test A: Using Only File and Folder Names

```
| File Name               | Folder Name | Score     |
|-------------------------|-------------|-----------|
| crack.exe               | apps        | 0.5147713 |
| lovecraft novels.txt    | books       | 0.5832841 |
| police report.docx      | docs        | 0.6303186 |
| database admin.pkg      | docs        | 0.5538312 |
| invoice from google.pdf | docs        | 0.5381457 |
| meme.png                | images      | 0.6993392 |
| funny cat.jpg           | images      | 0.5511819 |
| lord of the ring.avi    | movies      | 0.5454072 |
| harry potter.mpeg4      | movies      | 0.5410566 |
```

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-b-adding-natural-language-context) Test B: Adding Natural Language Context

Each string was framed like:

*   `"This is a file name: {file_name}"`
*   `"This is a folder name: {folder_name}"`

```
| File Name                       | Folder Name | Score    |
|--------------------------------|-------------|-----------|
| crack.exe                      | apps        | 0.6714907 |
| lovecraft novels.txt           | books       | 0.7517922 |
| database admin.pkg             | dest        | 0.7194574 |
| police report.docx             | docs        | 0.7456068 |
| invoice from google.pdf        | docs        | 0.7141885 |
| meme.png                       | images      | 0.7737676 |
| funny cat.jpg                  | images      | 0.7438067 |
| harry potter.mpeg4             | movies      | 0.7156760 |
| lord of the ring.avi           | movies      | 0.6718528 |
```

#### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#observations) Observations:

*   **Scores were consistently higher** across the board when context was added.
*   The model **made more accurate matches**, such as correctly associating `database admin.pkg` with `dest` instead of `books`.
*   This suggests that **embeddings perform better with structured, semantic context**, not just bare tokens.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-case-only-some-files-have-valid-matches) Test Case: Only Some Files Have Valid Matches
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Now let's delete the movies and images folders and observe how the matching behavior changes:

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-a-using-only-file-and-folder-names) Test A: Using Only File and Folder Names

```
| File Name               | Folder Name | Score      |
|-------------------------|-------------|------------|
| hobbit.fb2              | apps        | 0.55056566 |
| crack.exe               | apps        | 0.5147713  |
| lovecraft novels.txt    | books       | 0.57081085 |
| police report.docx      | docs        | 0.6303186  |
| meme.png                | docs        | 0.58589196 |
| database admin.pkg      | docs        | 0.5538312  |
| invoice from google.pdf | docs        | 0.5381457  |
| lord of the ring.avi    | docs        | 0.492918   |
| funny cat.jpg           | docs        | 0.45956808 |
| harry potter.mpeg4      | docs        | 0.45733657 |
```

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#test-b-adding-natural-language-context) Test B: Adding Natural Language Context

Same context generation pattern as in previous test case

```
| File Name               | Folder Name | Score      |
|-------------------------|-------------|------------|
| crack.exe               | apps        | 0.6714907  |
| lovecraft novels.txt    | books       | 0.72899115 |
| database admin.pkg      | dest        | 0.7194574  |
| meme.png                | dest        | 0.68507683 |
| funny cat.jpg           | dest        | 0.6797525  |
| lord of the ring.avi    | dest        | 0.5323342  |
| police report.docx      | docs        | 0.7456068  |
| invoice from google.pdf | docs        | 0.71418846 |
| hobbit.fb2              | docs        | 0.6780642  |
| harry potter.mpeg4      | docs        | 0.5984984  |
```

#### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#observations) Observations:

*   In Test A, files like meme.png, funny cat.jpg, and lord of the ring.avi were incorrectly matched to the docs folder. In Test B, they appeared in the more appropriate dest folder.

*   There are still some mismatches — for example, hobbit.fb2 was matched with docs instead of books, likely due to the less common .fb2 format. harry potter.mpeg4 also matched with docs, though with a relatively low score.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#why-does-this-happen) Why Does This Happen?
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#1-context-gives-structure) 1. **Context Gives Structure**

Embedding models are trained on natural language. So when we provide structured inputs like:

> “This is a file name: invoice from google.pdf”
> 
> 
> “This is a folder name: docs”

...the model better understands the **semantic role** of each string. It knows these aren't just tokens — they are _types of things_, which makes embeddings more aligned.

* * *

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#2-its-not-just-word-overlap) 2. **It’s Not Just Word Overlap**

Yes, phrases like `"this is a file name"` and `"this is a folder name"` are similar. But if word overlap were the only reason for higher scores, all scores would rise evenly — regardless of actual content.

Instead, we're seeing better matching. That means the model is using **true context** to judge compatibility — a sign that semantic meaning is being used, not just lexical similarity.

* * *

### [](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#3-raw-strings-without-context-can-be-misleading) 3. **Raw Strings Without Context Can Be Misleading**

A folder named `docs` or `my-pc` is vague. A file named `database admin.pkg` is even more so. Embeddings of such raw strings might be overly similar due to lack of semantic separation.

Adding even a light wrapper like `"This is a file name..."` or `"This is a folder name..."` gives the model **clearer context and role assignment**, helping it avoid false positives and improve semantic accuracy.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#conclusion) Conclusion
-------------------------------------------------------------------------------------------------------------------------------------------------------------

*   **Embeddings require context to be effective**, especially for classification or matching tasks.
*   Providing **natural-language-like structure** (even just a short prefix) significantly improves performance.
*   It’s not just about higher scores — it’s about **better semantics and more accurate results**.

If you're building tools that rely on embeddings, especially for classification, recommendation, or clustering — **don't be afraid to add a little helpful context.** It goes a long way.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#looking-for-feedback) Looking for Feedback
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I’d really appreciate any feedback — positive or critical — on the project, the codebase, the article series, or the general approach used in the CLI.

* * *

[](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg#thanks-for-reading)**Thanks for Reading!**
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Feel free to reach out here or connect with me on:

*   [GitHub](https://github.com/PerminovEugene)
*   [LinkedIn](https://www.linkedin.com/in/eugene-perminov/)

Or just drop me a note if you want to chat about Rust, AI, or creative ways to clean up messy folders!
~~~

:::

~~~
Title: Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)

URL Source: /evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k

Published Time: 2025-03-28T15:42:16Z

Markdown Content:
Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai) - DEV Community
===============
[Skip to content](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#main-content)

[[1: DEV Community](quality=100/https://dev-to-uploads.s3.amazonaws.com/uploads/logos/resized_logo_UQww2soKuUsjaOGNB38o.png)](/)

[Powered by Algolia](https://www.algolia.com/developers/?utm_source=devto&utm_medium=referral)

[Log in](/enter)[Create account](/enter?state=new-user)

DEV Community
-------------

[2](heart-plus-active-9ea3b22f2bc311281db911d416166c5f430636e76b15cd5df6b3b841d830eefa.svg)1 Add reaction 

[3](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)1 Like [4](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)0 Unicorn [5](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)0 Exploding Head [6](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)0 Raised Hands [7](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)0 Fire 

0 Jump to Comments 0 Save  Boost 

 Moderate 

Copy link

Copied to Clipboard

[Share to X](https://twitter.com/intent/tweet?text=%22Embeddings%20clustering%20with%20Agglomerative%20Hierarchical%20Clustering%20%28messy-folder-reorganizer-ai%29%22%20by%20Evgenii%20Perminov%20%23DEVCommunity%20https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fembeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k)[Share to LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fembeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k&title=Embeddings%20clustering%20with%20Agglomerative%20Hierarchical%20Clustering%20%28messy-folder-reorganizer-ai%29&summary=Adding%20RAG%20and%20ML%20to%20Messy-Folder-Reorganizer-AI%20%20%20%20%20%20%20%20%20%20%20%20Why%20ML%20Methods%20for...&source=DEV%20Community)[Share to Facebook](https://www.facebook.com/sharer.php?u=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fembeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k)[Share to Mastodon](https://toot.kytta.dev/?text=https%3A%2F%2Fdev.to%2Fevgeniiperminov%2Fembeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k)

[Share Post via...](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#)[Report Abuse](/report-abuse)

[[8: Cover image for Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fpvnzlztc87l4nn2wa19d.png)](width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fpvnzlztc87l4nn2wa19d.png)

[[9: Evgenii Perminov](width=50,height=50,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1973401%2F3bc0834c-aae8-4342-9fbb-14588e5533f9.jpg)](/evgeniiperminov)

[Evgenii Perminov](/evgeniiperminov)
Posted on Mar 28

[10](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)1[11](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)[12](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)[13](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)[14](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)

Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)
==============================================================================================

[#vectordatabase](/t/vectordatabase)[#ai](/t/ai)[#machinelearning](/t/machinelearning)[#cli](/t/cli)

[messy-folder-reorganizer-ai (4 Part Series)](/evgeniiperminov/series/30981)
------------------------------------------------------------------------------------------

[1 Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3 "Published Mar 28")[2 How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai)](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3 "Published Mar 28")[3 Making Embeddings Understand Files and Folders with Simple Sentences (messy-folder-reorganizer-ai)](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg "Published Mar 28")[4 Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k "Published Mar 28")

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#adding-rag-and-ml-to-messyfolderreorganizerai) Adding RAG and ML to Messy-Folder-Reorganizer-AI
===================================================================================================================================================================================================================================

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#why-ml-methods-for-clustering) Why ML Methods for Clustering
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

As we discovered in previous articles, all LLMs have context restrictions, so we cannot send hundreds of file names to an LLM and ask it to create folder names for all of them. On the other hand, sending a request for each file separately is not only inefficient and redundant—it also breaks the global context.

For example, if you have files like `bill_for_electricity.pdf` and `bill_for_leasing.docx`, you don’t want to end up with folder names like `bills` for the first and `documents` for the second. These results are technically valid, but they’re disconnected. **We need to group related files together first**, and the best way to do that is by clustering their embeddings.

 For [messy-folder-reorganizer-ai](https://github.com/PerminovEugene/messy-folder-reorganizer-ai) I picked agglomerative hierarchical clustering and I will try to explain my choice to the reader.

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#selecting-a-clustering-method) Selecting a Clustering Method
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

There are many clustering algorithms out there, but not all are suitable for the nature of embeddings. We're working with:

*   **High-dimensional vectors** (e.g., 384, 768, or more dimensions).
*   **Relatively small datasets** (e.g., a few hundred or thousand files).

Here's a comparison of a few clustering options:

| Algorithm | Pros | Cons |
| --- | --- | --- |
| **K-Means** | Fast, simple, widely used | Requires choosing `k`, assumes spherical clusters |
| **DBSCAN** | Detects arbitrary shapes, noise handling | Sensitive to parameters, poor with high dimensions |
| **HDBSCAN** | Improved DBSCAN, handles hierarchy | Slower, more complex |
| **Agglomerative** | No need for `k`, builds hierarchy, flexible distances | Slower, high memory use |

**Agglomerative hierarchical clustering** is a strong fit because it:

*   Doesn’t require you to predefine the number of clusters.
*   Works well with custom distance metrics (like cosine).
*   Builds a dendrogram that can be explored at different levels of granularity.

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#agglomerative-clustering-preparations) Agglomerative Clustering Preparations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### [](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#input-embedding-matrix) Input: Embedding Matrix

We assume an input matrix of shape **M x N**:

*   `M`: Number of files (embeddings).
*   `N`: Dimensionality of the embeddings (depends on the model used).

### [](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#building-a-normalized-matrix) Building a Normalized Matrix

**What is normalization?**

 Normalization ensures that all vectors are of unit length, which is especially important when using cosine distance.

**Why normalize?**

*   Prevents length from affecting similarity.
*   Ensures cosine distance reflects angular difference only.

**Formula:**

 For vector (x), normalize it as:

x̂ = x / ||x||

Where ||x|| is the Euclidean norm (i.e., the square root of the sum of squares of the elements of x).

### [](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#building-the-distance-matrix-using-cosine-distance) Building the Distance Matrix Using Cosine Distance

**Why cosine distance?**

*   It captures **semantic similarity** better in high-dimensional embedding spaces.
*   More stable than Euclidean in high dimensions.

**Does it help with the curse of dimensionality?**

 To some extent, yes. While no method fully escapes the curse, **cosine similarity** is more robust than Euclidean for textual or semantic data.

**Formula:**

 Given two normalized vectors (x) and (y):

cosine_similarity(x, y) = (x · y) / (‖x‖ · ‖y‖)

cosine_distance(x, y) = 1 - cosine_similarity(x, y)

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#agglomerative-clustering-algorithm) Agglomerative Clustering Algorithm
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Once we have the distance matrix, the agglomerative process begins:

1.   **Start**: Treat each embedding as its own cluster.
2.   **Merge**: Find the two closest clusters using the selected linkage method: 
    *   **Single**: Minimum distance between points across clusters.
    *   **Complete**: Maximum distance.
    *   **Average**: Mean distance.
    *   **Ward**: Minimizes variance (works only with Euclidean distance).

3.   **Repeat**: Merge the next closest pair until one cluster remains or a distance threshold is reached.
4.   **Cut the dendrogram**: Decide how many clusters to extract based on height (distance) or desired granularity.

This method gives you **interpretable, connected groupings**—a critical step before folder naming or generating structured representations.

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#implementation) Implementation
------------------------------------------------------------------------------------------------------------------------------------------------------------------

If you are interested, you can check out implementation on Rust

[here](https://github.com/PerminovEugene/messy-folder-reorganizer-ai/blob/main/src/ml/agglomerative_clustering.rs)

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#looking-for-feedback) Looking for Feedback
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

I’d really appreciate any feedback — positive or critical — on the project, the codebase, the article series, or the general approach used in the CLI.

* * *

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#thanks-for-reading)**Thanks for Reading!**
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Feel free to reach out here or connect with me on:

*   [GitHub](https://github.com/PerminovEugene)
*   [LinkedIn](https://www.linkedin.com/in/eugene-perminov/)

Or just drop me a note if you want to chat about Rust, AI, or creative ways to clean up messy folders!

[messy-folder-reorganizer-ai (4 Part Series)](/evgeniiperminov/series/30981)
------------------------------------------------------------------------------------------

[1 Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai)](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3 "Published Mar 28")[2 How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai)](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3 "Published Mar 28")[3 Making Embeddings Understand Files and Folders with Simple Sentences (messy-folder-reorganizer-ai)](/evgeniiperminov/making-embeddings-understand-files-and-folders-with-simple-sentences-messy-folder-reorganizer-ai-mjg "Published Mar 28")[4 Embeddings clustering with Agglomerative Hierarchical Clustering (messy-folder-reorganizer-ai)](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k "Published Mar 28")

[[15: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F123%2F38b10714-65da-4f1d-88ae-e9b28c1d7a5e.png) Heroku](/heroku)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=217501)

[[16: Heroku](width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FEtkoO96.png)](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#built-for-developers-by-developers)[Built for developers, by developers.](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Whether you're building a simple prototype or a business-critical product, Heroku's fully-managed platform gives you the simplest path to delivering apps quickly — using the tools and languages you already love!

[Learn More](https://www.heroku.com/?utm_source=devto&utm_medium=paid&utm_campaign=heroku_2025&bb=217501)

 Read More 

Top comments (0)
----------------

Subscribe

[17: pic](width=256,height=,fit=scale-down,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8j7kvp660rqzt99zui8e.png)

Personal Trusted User[Create template](/settings/response-templates)
Templates let you quickly answer FAQs or store snippets for re-use.

Submit Preview[Dismiss](/404.html)

[Code of Conduct](/code-of-conduct)•[Report abuse](/report-abuse)

Are you sure you want to hide this comment? It will become hidden in your post, but will still be visible via the comment's [permalink](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#).

- [x] 
Hide child comments as well

 
Confirm

For further actions, you may consider blocking this person and/or [reporting abuse](/report-abuse)

[[18: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F10846%2Fb8131f88-3d8a-476d-bcf0-2e0fb946e4d5.png) ACI.dev](/acidev)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=231138)

[[19: ACI image](width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FJdwzkK1.jpeg)](https://bit.ly/4mdlYOl?bb=231138)

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#acidev-the-only-mcp-server-your-ai-agents-need)[ACI.dev: The Only MCP Server Your AI Agents Need](https://bit.ly/4mdlYOl?bb=231138)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ACI.dev’s open-source tool-use platform and Unified MCP Server turns 600+ functions into two simple MCP tools on one server—search and execute. Comes with multi-tenant auth and natural-language permission scopes. 100% open-source under Apache 2.0.

[Star our GitHub!](https://bit.ly/4mdlYOl?bb=231138)

Read next
---------

[[20: yasiga_3 profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F3080683%2F63757d20-cd24-413e-9287-f5c41bb27471.jpg) ### Docker Image creation and pushing to DockerHub yasiga - Apr 28](/yasiga_3/docker-image-creation-and-pushing-to-dockerhub-42eh)[[21: dev_kumar_9a1db98e34077b6 profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F2556866%2F5b2f1e16-9acb-4454-9d17-afd33e81fd60.png) ### The Impact of AI on Retail Shopping Experiences Dev Kumar - Apr 28](/dev_kumar_9a1db98e34077b6/the-impact-of-ai-on-retail-shopping-experiences-35jf)[[22: koolkamalkishor profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1372052%2Fcc05edd7-e6c0-42f5-b52c-8dd7a6f826e7.webp) ### How to Upload Your Project to Hugging Face Spaces: A Beginner's Step-by-Step Guide KAMAL KISHOR - May 2](/koolkamalkishor/how-to-upload-your-project-to-hugging-face-spaces-a-beginners-step-by-step-guide-1pkn)[[23: reachyugesh profile image](width=100,height=100,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F3095083%2Fa0a1c7b8-9e2d-4650-b86a-d21083028be4.jpg) ### Embedded Real-Time Systems: The Engine Behind Precision Healthcare Robotics Yugesh Anne - Apr 27](/reachyugesh/embedded-real-time-systems-the-engine-behind-precision-healthcare-robotics-j14)

[[24](width=90,height=90,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Fuser%2Fprofile_image%2F1973401%2F3bc0834c-aae8-4342-9fbb-14588e5533f9.jpg) Evgenii Perminov](/evgeniiperminov)

Follow

 Hey! My name is Evgenii and I am software engineer with 10 years of experience. Currently working on Rust+AI based CLI for files reorganization. 

*    Location   Estonia  
*    Joined  Aug 24, 2024 

### More from [Evgenii Perminov](/evgeniiperminov)

[How Cosine Similarity Helped My CLI Decide Where Files Belong (messy-folder-reorganizer-ai) #llm#rust#cli#opensource](/evgeniiperminov/how-cosine-similarity-helped-my-cli-decide-where-files-belong-messy-folder-reorganizer-ai-fm3)[Adding RAG and ML to AI files reorganization CLI (messy-folder-reorganizer-ai) #llm#cli#opensource#rag](/evgeniiperminov/adding-rag-and-ml-to-ai-files-reorganization-cli-messy-folder-reorganizer-ai-1d3)[How I Built a Local LLM-Powered File Reorganizer with Rust #llm#rust#cli#opensource](/evgeniiperminov/how-i-built-a-local-llm-powered-file-reorganizer-in-rust-1bip)

[[25: profile](width=64,height=64,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F5369%2Fbf0b17ac-3757-4494-ae6d-69f47c5be2c2.png) Stellar Development Foundation](/stellar)Promoted

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=225974)

[[26: Image of Stellar post](width=350%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fi.imgur.com%2FFHXRlQs.png)](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#how-a-hackathon-win-led-to-my-startup-getting-funded)[How a Hackathon Win Led to My Startup Getting Funded](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

In this episode, you'll see:

*   The hackathon wins that sparked the journey.
*   The moment José and Joseph decided to go all-in.
*   Building a working prototype on Stellar.
*   Using the PassKeys feature of Soroban.
*   Getting funded via the Stellar Community Fund.

[Watch the video 🎥](https://www.youtube.com/watch?v=FInE2PSx1es&t=1s&bb=225974)

👋 Kindness is contagious

*   [What's a billboard?](/billboards)
*   [Manage preferences](/settings/customization#sponsors)

* * *

*   [Report billboard](/report-abuse?billboard=225474)

### [](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#dive-into-this-informative-piece-backed-by-our-vibrant-dev-community) Dive into this informative piece, backed by our vibrant DEV Community

**Whether you’re a novice or a pro**, your perspective enriches our collective insight.

A simple “thank you” can lift someone’s spirits—share your gratitude in the comments!

On DEV, **the power of shared knowledge paves a smoother path** and tightens our community ties. Found value here? A quick thanks to the author makes a big impact.

[](/evgeniiperminov/embeddings-clustering-with-agglomerative-hierarchical-clustering-messy-folder-reorganizer-ai-520k#-cta-httpsdevtoenterstatenewuser-)[Okay](/enter?state=new-user&bb=225474)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

💎 DEV Diamond Sponsors

Thank you to our Diamond Sponsors for supporting the DEV Community

[[27: Neon - Official Database Partner](width=880%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fbnl88cil6afxzmgwrgtt.png)](https://neon.tech/?ref=devto&bb=146443)
Neon is the official database partner of DEV

[[28: Algolia - Official Search Partner](width=880%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fv30ephnolfvnlwgwm0yz.png)](https://www.algolia.com/developers/?utm_source=devto&utm_medium=referral&bb=146443)
Algolia is the official search partner of DEV

[DEV Community](/) — A space to discuss and keep up software development and manage your software career

*   [Home](/)
*   [DEV++](/++)
*   [Podcasts](/pod)
*   [Videos](/videos)
*   [Tags](/tags)
*   [DEV Help](/help)
*   [Forem Shop](https://shop.forem.com/)
*   [Advertise on DEV](/advertise)
*   [DEV Challenges](/challenges)
*   [DEV Showcase](/showcase)
*   [About](/about)
*   [Contact](/contact)
*   [Free Postgres Database](/free-postgres-database-tier)
*   [Software comparisons](/software-comparisons)

*   [Code of Conduct](/code-of-conduct)
*   [Privacy Policy](/privacy)
*   [Terms of use](/terms)

Built on [Forem](https://www.forem.com/) — the [open source](/t/opensource) software that powers [DEV](/) and other inclusive communities.

Made with love and [Ruby on Rails](/t/rails). DEV Community © 2016 - 2025.

[29: DEV Community](width=190,height=,fit=scale-down,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F8j7kvp660rqzt99zui8e.png)

We're a place where coders share, stay up-to-date and grow their careers.

[Log in](/enter)[Create account](/enter?state=new-user)

[30](sparkle-heart-5f9bee3767e18deb1bb725290cb151c25234768a0e9a2bd39370c382d02920cf.svg)[31](multi-unicorn-b44d6f8c23cdd00964192bedc38af3e82463978aa611b4365bd33a0f1f4f3e97.svg)[32](exploding-head-daceb38d627e6ae9b730f36a1e390fca556a4289d5a41abb2c35068ad3e2c4b5.svg)[33](raised-hands-74b2099fd66a39f2d7eed9305ee0f4553df0eb7b4f11b01b6b1b499973048fe5.svg)[34](fire-f60e7a582391810302117f987b22a8ef04a2fe0df7e3258a5f49332df1cec71e.svg)
~~~