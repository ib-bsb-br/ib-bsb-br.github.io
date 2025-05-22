---
categories: []
tags:
  - scratchpad
comment: 
info: 
date: '2025-05-22'
type: post
layout: post
published: true
sha: 
slug: lightrag-arm64
title: 'Running LightRAG on Baremetal Linux (ARM64)'

---
This guide provides instructions and considerations for running LightRAG on a baremetal Linux machine with an ARM64 architecture.

## 1. System Prerequisites

Before installing LightRAG, ensure your ARM64 Linux system meets the following prerequisites:

*   **Python:** Python 3.10 or newer is required. You can check your Python version with `python3 --version`. If you need to install or upgrade Python, consult your Linux distribution's package manager (e.g., `apt` for Debian/Ubuntu, `yum` for CentOS/RHEL, `dnf` for Fedora).
    ```bash
    # Example for Debian/Ubuntu
    sudo apt update
    sudo apt install python3 python3-pip python3-venv
    ```

*   **Build Tools:** Since some Python packages may need to be compiled from source on ARM64 (if pre-built wheels are not available), you'll need standard build tools.
    ```bash
    # Example for Debian/Ubuntu
    sudo apt install build-essential python3-dev
    # For other distributions, you might need packages like 'gcc', 'g++', 'make'
    ```

*   **Pip:** Ensure `pip` for Python 3 is installed. It's usually included with Python or can be installed separately.
    ```bash
    python3 -m ensurepip --upgrade
    ```

*   **Git:** You'll need Git to clone the repository.
    ```bash
    # Example for Debian/Ubuntu
    sudo apt install git
    ```

*   **System Dependencies for `textract` (Optional but Recommended for Full File Support):**
    LightRAG uses the `textract` library to extract text from various file types (PDF, DOCX, etc.). To enable support for these formats, you'll need to install their underlying system dependencies. The specific packages can vary slightly by distribution, but the following are common for Debian-based systems. Adapt them for your specific Linux distribution.
    *   For **.docx** files: `libxml2-dev`, `libxslt1-dev`
    *   For **.doc** files: `antiword`
    *   For **.rtf** files: `unrtf`
    *   For **.pdf** files: `poppler-utils` (provides `pdftotext`)
    *   For **.ps** files: `pstotext` (may require manual installation or be part of a larger PostScript handling package)
    *   For image-based text extraction (OCR for **.jpg, .png, .gif**): `tesseract-ocr` and its language data packs (e.g., `tesseract-ocr-eng` for English).
    *   For audio files (**.mp3, .ogg, .wav**): `sox`, `libsox-fmt-all`, `ffmpeg`, `lame`, `libmad0`
    *   Other potentially useful packages mentioned by `textract` documentation: `libjpeg-dev`, `swig`, `flac`.

    A comprehensive command for Debian/Ubuntu to install most `textract` dependencies would be:
    ```bash
    sudo apt install libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr tesseract-ocr-eng sox libsox-fmt-all ffmpeg lame libmad0 libjpeg-dev swig flac
    ```
    **Note:** Some dependencies like `pstotext` might be harder to find in all distributions. `textract` has fallbacks for some formats (e.g., a pure Python PDF parser if `pdftotext` is missing), but functionality might be limited. Refer to your distribution's package repositories and the `textract` documentation for the most accurate package names.

## 2. Installation from Source

Installing from source is recommended for a baremetal setup, as it gives you the most control and ensures compatibility with your ARM64 architecture.

1.  **Clone the Repository:**
    Open your terminal and clone the LightRAG repository from GitHub:
    ```bash
    git clone https://github.com/HKUDS/LightRAG.git
    cd LightRAG
    ```

2.  **Create and Activate a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with system-wide packages.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(To deactivate the virtual environment later, simply type `deactivate`)*

3.  **Install LightRAG and its Dependencies:**
    LightRAG uses `pip` for installation. You have two main options:
    *   **To install the core LightRAG engine along with the API server and web UI components:**
        ```bash
        pip install -e ".[api]"
        ```
    *   **To install only the core LightRAG engine (if you don't need the API server or web UI):**
        ```bash
        pip install -e .
        ```

    **Note on Compilation:** This step might take a significant amount of time, especially on ARM64 devices, as some dependencies may need to be compiled from source. Ensure your system has a stable internet connection and sufficient resources (RAM, CPU).

4.  **Troubleshooting Compilation Issues:**
    If you encounter errors during the `pip install` step, they are often due to missing development libraries for a particular package.
    *   Carefully read the error messages. They usually indicate which library is missing.
    *   Use your system's package manager to search for and install the required development package. For example, if an error mentions something related to `xyz`, you might need to install `libxyz-dev` (on Debian/Ubuntu) or a similarly named package.
    *   Ensure your build tools (`gcc`, `python3-dev`, etc.) are correctly installed.

## 3. Configuration for Baremetal Deployment

After successful installation, you need to configure LightRAG for your baremetal environment. This is primarily done through an `.env` file.

1.  **Create the `.env` File:**
    Navigate to the root directory of your cloned LightRAG project (if you're not already there) and copy the example environment file:
    ```bash
    cp env.example .env
    ```

2.  **Edit the `.env` File:**
    Open the `.env` file with a text editor. Here are some key configurations to consider for a baremetal ARM64 setup:

    *   **LLM Configuration:**
        You'll likely want to use LLMs that can run locally on your ARM64 machine.
        *   **Using Ollama (Recommended for local models):**
            If you have Ollama installed and serving a model:
            ```env
            LLM_BINDING=ollama
            LLM_BINDING_HOST=http://localhost:11434 # Or your Ollama server address
            LLM_MODEL=your_ollama_model_name # e.g., llama3, gemma2
            ```
            Ensure Ollama is running and the specified model is pulled (`ollama pull your_ollama_model_name`).
            The `README.md` has specific instructions for increasing Ollama's context window (`num_ctx`), which is important for LightRAG.
        *   **Using Hugging Face Models (Directly or via a local inference server):**
            The `README.md` provides examples for using Hugging Face models. This might involve more manual setup to ensure the model runs efficiently on your ARM64 hardware.
            ```env
            # Example (refer to LightRAG docs for specific HuggingFace setup)
            # LLM_BINDING=hf 
            # LLM_MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct 
            ```
        *   **Using OpenAI (If you have internet access and an API key):**
            While this is a baremetal guide, you can still use OpenAI if desired:
            ```env
            LLM_BINDING=openai
            OPENAI_API_KEY=your_openai_api_key
            LLM_MODEL=gpt-4o-mini # Or other model
            ```

    *   **Embedding Model Configuration:**
        Similar to LLMs, you'll need to configure embedding models.
        *   **Using Ollama:**
            ```env
            EMBEDDING_BINDING=ollama
            EMBEDDING_BINDING_HOST=http://localhost:11434 # Or your Ollama server address
            EMBEDDING_MODEL=nomic-embed-text # Or another Ollama embedding model
            ```
            Ensure the embedding model is pulled in Ollama (`ollama pull nomic-embed-text`).
        *   **Using Hugging Face Models:**
            Refer to the main `README.md` for Hugging Face embedding examples.
        *   **Using OpenAI:**
            ```env
            EMBEDDING_BINDING=openai
            # OPENAI_API_KEY should already be set if using OpenAI LLM
            EMBEDDING_MODEL=text-embedding-3-small # Or other model
            ```

    *   **Storage Configuration:**
        LightRAG supports various storage backends. For a simple baremetal setup, the defaults (using local JSON files) are often sufficient to get started.
        *   **Default (JSON-based):** No specific `.env` changes are typically needed for the default storage, as data will be stored in the `working_dir` (defaults to `lightrag_cache_<timestamp>` or as specified in your scripts).
        *   **Using PostgreSQL or Neo4j (Advanced):**
            If you prefer a more robust local database, you can set up PostgreSQL (with pgvector and Apache AGE extensions) or Neo4j on your ARM64 machine.
            The main `README.md` provides guidance on configuring LightRAG to use these:
            - Set `KV_STORAGE`, `VECTOR_STORAGE`, `GRAPH_STORAGE`, `DOC_STATUS_STORAGE` variables in the `.env` file or directly in your Python scripts when initializing `LightRAG`.
            - Example for Neo4j (ensure Neo4j server is running and configured):
              ```env
              GRAPH_STORAGE=Neo4JStorage
              NEO4J_URI=neo4j://localhost:7687
              NEO4J_USERNAME=neo4j
              NEO4J_PASSWORD=your_neo4j_password
              ```
            - Example for PostgreSQL (ensure PostgreSQL server is running with necessary extensions):
              ```env
              # In your Python script or set as environment variables
              # os.environ["DB_USER"] = "your_postgres_user"
              # os.environ["DB_PASSWORD"] = "your_postgres_password"
              # os.environ["DB_HOST"] = "localhost"
              # os.environ["DB_PORT"] = "5432"
              # os.environ["DB_NAME"] = "your_database_name"
              # KV_STORAGE=PGKVStorage
              # VECTOR_STORAGE=PGVectorStorage
              # GRAPH_STORAGE=AGEStorage 
              ```
            Refer to the "Storage" section in the main `README.md` and the example `examples/lightrag_zhipu_postgres_demo.py` for more details.

    *   **API Server Configuration (if using `.[api]` installation):**
        *   `HOST`: Server host (default: `0.0.0.0` to listen on all interfaces)
        *   `PORT`: Server port (default: `9621`)
        *   `LIGHTRAG_API_KEY`: Set a secure API key if you plan to expose the API.

    *   **Other Parameters:**
        *   `MAX_ASYNC`: Maximum async operations.
        *   `MAX_TOKENS`: Maximum token size for LLM.
        *   `WORKING_DIR`: Default directory for storing data if not overridden in scripts. Can be set in `.env` as `LIGHTRAG_WORKING_DIR`.
          ```env
          # LIGHTRAG_WORKING_DIR=./my_lightrag_data 
          ```

3.  **Save the `.env` File:**
    After making your changes, save the file. LightRAG will load these settings when it starts.

## 4. Running LightRAG

Once LightRAG is installed and configured, you can start using it.

### Running the LightRAG Server (Optional)

If you installed LightRAG with the API extras (`pip install -e ".[api]"`) and want to use the Web UI or API:

1.  **Ensure your `.env` file is configured**, especially `HOST`, `PORT`, `LIGHTRAG_API_KEY`, and your LLM/embedding model settings.
2.  **Activate your virtual environment** (if not already active):
    ```bash
    source venv/bin/activate
    ```
3.  **Start the server:**
    The main `README.md` mentions running the server. Typically, this involves a command like `python -m lightrag.api.lightrag_server` or a specific script if provided. Refer to the main `README.md` or `./lightrag/api/README.md` for the precise command to start the server.
    You might also use `docker compose up` if you later decide to use Docker and have configured `docker-compose.yml` appropriately for arm64.

    Once started, the API should be accessible at `http://<your_host>:<your_port>` and the Web UI (if included) at a similar address.

### Running Example Scripts (Core Engine)

The `examples/` directory contains various scripts demonstrating how to use the LightRAG core engine.

1.  **Activate your virtual environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Ensure your `.env` file is configured** with your chosen LLM and embedding models (e.g., local Ollama models). The example scripts often default to OpenAI, so you'll need to modify them or ensure your LightRAG initialization in the script picks up the `.env` settings or is explicitly set to your local models.

3.  **Prepare a test document (Optional, for some demos):**
    Some demos, like `lightrag_openai_demo.py`, use a sample text file.
    ```bash
    # From the LightRAG root directory
    curl https://raw.githubusercontent.com/gusye1234/nano-graphrag/main/tests/mock_data.txt > ./book.txt
    ```

4.  **Run an example script:**
    Navigate to the LightRAG root directory. Let's take `examples/lightrag_openai_demo.py` as a base.
    *   **If you configured OpenAI in `.env`:**
        ```bash
        # Ensure OPENAI_API_KEY is in your .env or exported
        python examples/lightrag_openai_demo.py
        ```
    *   **If you configured a local model (e.g., Ollama) in `.env` and the script is set up to use it, or if you modify the script:**
        Many examples in the `examples` directory show how to initialize `LightRAG` with specific model functions (e.g., `ollama_model_complete`, `hf_model_complete`). You might need to adapt `lightrag_openai_demo.py` or use a different example that's closer to your setup (like `examples/lightrag_ollama_demo.py`).

        For `lightrag_ollama_demo.py`:
        ```python
        # Inside lightrag_ollama_demo.py, you'd typically see:
        # from lightrag.llm.ollama import ollama_model_complete, ollama_embed
        # ...
        # rag = LightRAG(
        #     llm_model_func=ollama_model_complete,
        #     llm_model_name="your_ollama_model_from_env_or_hardcoded",
        #     embedding_func=EmbeddingFunc(
        #         embedding_dim=..., # set based on your ollama embedding model
        #         max_token_size=...,
        #         func=lambda texts: ollama_embed(texts, embed_model="your_ollama_embedding_model")
        #     ),
        #     ...
        # )
        ```
        To run such a script:
        ```bash
        python examples/lightrag_ollama_demo.py
        ```
        **Important:** Review the script you choose. Ensure the `LightRAG` initialization parameters (like `llm_model_func`, `embedding_func`, model names, dimensions) match your ARM64 setup and the models you have available. The `.env` file settings are used by default by the server, but scripts can override these if they explicitly pass parameters to `LightRAG()`.

    **Note on `WORKING_DIR`:** LightRAG will create a directory (e.g., `rag_storage` or `lightrag_cache_<timestamp>`) to store data, indexes, and caches. Make sure you have write permissions in the location where the script is run or where `WORKING_DIR` points. If you switch embedding models, you might need to clear this directory as per the main README's advice.

## 5. Alternative: Using Docker on ARM64

While this guide focuses on baremetal installation, you can also run LightRAG using Docker on your ARM64 Linux machine, provided Docker is installed.

*   **Dockerfiles Provided:** The repository includes a `Dockerfile` and a `docker-compose.yml` file, which are the starting points for a Docker-based deployment.

*   **ARM64 Docker Image:**
    *   Check if the project provides official multi-arch Docker images that support `linux/arm64`. You can find information on this in the main `README.md` or on the project's container registry (e.g., Docker Hub, GitHub Packages).
    *   If an official arm64 image is not available, you may need to build the Docker image directly on your ARM64 machine. This can be done using `docker build` or `docker compose build`. Ensure the `Dockerfile` is compatible with ARM64 (e.g., base images are available for ARM64, and any compiled dependencies can be built for ARM64).

*   **Configuration:** You would still use an `.env` file (or Docker Compose environment variables) to configure LightRAG, similar to the baremetal setup, paying attention to aspects like `LLM_BINDING_HOST` (which might need to be `host.docker.internal` or a specific container network IP if Ollama or other services are also running in Docker).

*   **Further Docker Instructions:** For more detailed information on Docker deployment, refer to the [DockerDeployment.md](./DockerDeployment.md) file in the `docs/` directory.

Using Docker can simplify dependency management but adds a layer of abstraction. Choose the method that best suits your comfort level and technical requirements.

## 6. Performance Considerations for ARM64

Running Large Language Models (LLMs) and associated processes (like embeddings and graph analysis) can be resource-intensive. When deploying LightRAG on a baremetal ARM64 machine, keep the following performance considerations in mind:

*   **Hardware Limitations:** The performance of LightRAG will heavily depend on the capabilities of your ARM64 hardware:
    *   **CPU:** A powerful multi-core ARM64 CPU will significantly speed up processing.
    *   **RAM:** LLMs, especially larger ones, require a substantial amount of RAM. Insufficient RAM can lead to slow performance or out-of-memory errors. Monitor your RAM usage closely.
    *   **Storage Speed:** Fast storage (e.g., NVMe SSD) can improve loading times for models and data.
    *   **Accelerators:** While many ARM64 SoCs include AI/ML accelerators, the ability to leverage them depends on the specific LLM serving framework (e.g., Ollama, llama.cpp) and model compatibility with those accelerators on Linux.

*   **Model Choice:** The size and type of the LLM and embedding models you choose will be the primary determinant of performance and resource consumption.
    *   **Start Small:** If you are unsure about your hardware's capacity or if you have limited resources (e.g., on a Raspberry Pi or similar single-board computer), start with the smallest available models (e.g., 2B or 3B parameter models if using Ollama).
    *   **Quantization:** Using quantized versions of models can significantly reduce their size and computational requirements, often with a manageable impact on performance. Check if your chosen LLM framework supports quantized models (e.g., GGUF for llama.cpp-based backends like Ollama).

*   **Batch Sizes and Concurrency:**
    *   Parameters like `MAX_ASYNC` in the `.env` file, `embedding_batch_num`, and `llm_model_max_async` in the `LightRAG` initialization can be tuned. However, on resource-constrained ARM64 devices, increasing concurrency too much might lead to thrashing rather than improved performance. Start with conservative values.

*   **System Optimization:**
    *   Ensure your Linux system is optimized. Minimize background processes to free up resources.
    *   Consider performance governors for your CPU if applicable (e.g., setting to `performance` mode if thermal headroom allows, though be mindful of heat on passively cooled devices).

*   **Monitoring:**
    *   Use system monitoring tools (`htop`, `vmstat`, `iotop`) to observe CPU, RAM, and disk I/O usage while LightRAG is processing data or handling queries. This can help you identify bottlenecks.

Running complex RAG pipelines on ARM64 is feasible, especially with newer, more powerful ARM64 processors. However, managing expectations and carefully selecting models appropriate for your hardware are key to a successful deployment.