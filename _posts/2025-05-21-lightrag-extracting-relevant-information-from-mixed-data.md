---
tags: [scratchpad]
info: aberto.
date: 2025-05-21
type: post
layout: post
published: true
slug: lightrag-extracting-relevant-information-from-mixed-data
title: 'LightRAG - extracting relevant information from mixed data'
---
## Introduction: Can LightRAG Solve Your Problem?

Based on the provided `LightRAG` documentation, your assessment of its capabilities is largely correct—and, in some respects, the tool is even more powerful than you might expect. `LightRAG` is designed as a lightweight, high-performance Retrieval-Augmented Generation (RAG) system with a strong focus on knowledge graph construction, semantic search, and efficient document management. It supports a range of file formats, offers robust document ingestion and indexing pipelines, and provides advanced querying and referencing features. Its architecture is optimized for handling large, disorganized collections, making it well-suited to your scenario: quickly filtering, searching, and referencing only the relevant content from a "sea of mixed files."

While `LightRAG` has specific requirements for certain file types (e.g., legacy `.doc` files), it covers many common research file formats. The system is also extensible, supporting multiple storage backends and LLM/embedding providers, and can be operated entirely via its user-friendly web interface or API.

**Please note:** This tutorial is based *exclusively* on the `LightRAG` documentation provided. Features, UI elements, and behavior might differ with other `LightRAG` versions or if the documentation isn't fully comprehensive for your setup.

This tutorial will guide you step-by-step from the `LightRAG` homepage, focusing on how to leverage its features to tackle your specific file organization and information retrieval challenges.

---

## Part 1: Getting Started with LightRAG's Web Interface

This part guides you through accessing the `LightRAG` WebUI and understanding its main layout, assuming you have successfully installed `LightRAG` via `Docker` and created an account.

### Step 1: Access the LightRAG WebUI

1.  **Open** your web browser.
2.  **Navigate** to `http://localhost:9621/webui`. (This is the default URL; if you configured a different port during `Docker` setup, use that port number instead of `9621`.)
3.  You should be greeted by the `LightRAG` homepage. If authentication is enabled (as configured in your `.env` file or server arguments), you will be prompted to **log in**.

### Step 2: Overview of the Homepage and Main Sections

The `LightRAG` web interface, as suggested by its source files (e.g., `lightrag_webui/src/features/SiteHeader.tsx`) and UI text definitions (`lightrag_webui/src/locales/en.json`), typically presents a top navigation bar. This bar provides access to the main sections of the application:

*   **Documents:** Your primary workspace for uploading, managing, and monitoring the processing status of your research files. (Tab label: **"Documents"**)
*   **Knowledge Graph:** Allows you to visualize and interactively explore the entities (e.g., concepts, people, organizations) and relationships that `LightRAG` automatically extracts from your documents. (Tab label: **"Knowledge Graph"**)
*   **Retrieval:** The main interface for querying your indexed documents to find specific information and get answers. (Tab label: **"Retrieval"**)
*   **API:** Provides access to `LightRAG`'s API documentation (usually Swagger UI or ReDoc), which is useful for developers or for understanding the underlying API endpoints. (Tab label: **"API"**)
*   **Project Repository:** A direct link to the `LightRAG` GitHub project page.
*   **Logout:** Allows you to **log out** of your `LightRAG` session.
*   **Settings (Gear Icon):** Access application-level settings, such as theme preferences and language selection.
*   **Theme Toggle (Sun/Moon Icon):** Quickly **switch** between light and dark visual themes for the interface.

For your immediate goal of organizing files and extracting information, this tutorial will focus primarily on the **Documents** and **Retrieval** sections.

---

## Part 2: Ingesting Your Research Files into LightRAG

This crucial step involves preparing your files and getting them into `LightRAG` for processing.

### Step 1: Understand Supported File Formats and Important Notes

`LightRAG`'s ability to process your files effectively depends on their format. Based on the `Dockerfile` and the backend code (`lightrag/api/routers/document_routes.py`):

*   **Well-Supported by Default `Docker` Installation:**
    *   **PDF (`.pdf`):** Processed using `PyPDF2`. **Crucial:** Ensure your PDFs are text-searchable (contain actual selectable text, not just scanned images).
    *   **Microsoft Word (`.docx`):** Processed using `python-docx`.
    *   **Text Files (`.txt`, `.md`):** Read directly. Markdown (`.md`) is also supported.
    *   **Microsoft PowerPoint (`.pptx`):** Processed using `python-pptx`.
    *   **Microsoft Excel (`.xlsx`):** Processed using `openpyxl`.
    *   **Common Text-Based Formats:** Many other formats listed in `DocumentManager`'s `SUPPORTED_EXTENSIONS` (e.g., `.csv`, `.json`, `.xml`, `.html`, `.py`, `.java`, `.css`) are generally processed by attempting a UTF-8 decode.

*   **Critical Note on Legacy `.doc` files (Microsoft Word 97-2003):**
    *   The `SUPPORTED_EXTENSIONS` list in `DocumentManager` (`document_routes.py`) does **not** include `.doc`.
    *   The `Dockerfile` for `LightRAG` **does not install** the `docling` library, which the backend code (`pipeline_enqueue_file` function in `document_routes.py`) would conditionally attempt to use for converting some other formats (like RTF, ODT).
    *   **Conclusion:** `LightRAG`, with its default `Docker` setup, will **fail to process `.doc` files**.
    *   **Action Required:** You **must convert** your `.doc` files to a supported format like `.docx`, text-searchable `.pdf`, or `.txt` *before* uploading them to `LightRAG`.

*   **Other Listed Formats (e.g., `.rtf`, `.odt`, `.epub`, `.tex`, `.htm`):**
    *   While these extensions are listed in `SUPPORTED_EXTENSIONS` (`document_routes.py`), the `pipeline_enqueue_file` function attempts to process them using `docling` if available.
    *   Since `docling` is **not installed by default** in the `Docker` image, these formats will also **likely fail to process**.
    *   **Recommendation:** For critical research files in these formats, it's safest to **convert** them to `PDF` (text-searchable), `DOCX`, or `TXT` if you encounter processing issues.

### Step 2: Choose Your File Ingestion Method

`LightRAG` offers two main ways to ingest your documents:

1.  **Direct Upload via the Web UI:** Select files from your computer and upload them through the interface.
2.  **Input Directory Scan:** Place files into a specific directory that `LightRAG` monitors, then trigger a scan.

For your initial large, disorganized collection, using the **"Upload"** feature via the UI (Method B below) might be more straightforward as you can directly **select** files. If you later establish a workflow where new research files are regularly saved to a specific folder, setting up that folder as `LightRAG`'s `INPUT_DIR` and using the **"Scan"** feature (Method A) can be very efficient for ongoing updates.

#### Method A: Placing Files Directly in the Input Directory and Scanning

This method is efficient for batch processing if you can easily copy files into `LightRAG`'s monitored folder.

1.  **Locate and Prepare Your Input Directory:**
    *   Your `LightRAG` `Docker` setup (as per `docker-compose.yml`) maps a directory on your host machine to its internal input directory. By default, this is usually a folder named `./data/inputs` located in the same directory where you run `docker-compose up`. The `Dockerfile` and `lightrag/api/config.py` reference this as `INPUT_DIR` (defaulting to `/app/data/inputs` inside the container).
    *   **Action:** **Copy** your selected research files (ensuring all `.doc` files are converted to a supported format!) into this `./data/inputs` directory on your computer.

2.  **Initiate a Scan from the Web UI:**
    *   In the `LightRAG` WebUI, **navigate** to the **"Documents"** tab.
    *   Look for a button labeled **"Scan"** (often accompanied by a refresh icon, as per `lightrag_webui/src/locales/en.json`: `"documentPanel.documentManager.scanButton": "Scan"`).
    *   **Action:** **Click** the **"Scan"** button.
    *   **Purpose:** This tells `LightRAG` to check its `INPUT_DIR` for any new files it hasn't processed yet and begin indexing them.
    *   **Expected Feedback:** A notification might appear (e.g., "Scanning documents started."). The document list in the UI should update as new files are discovered and their processing status changes.

#### Method B: Uploading Files Directly via the Web UI

This method allows you to select specific files from any location on your computer.

1.  **Access the Upload Dialog:**
    *   In the `LightRAG` WebUI, **navigate** to the **"Documents"** tab.
    *   Look for a button labeled **"Upload"** (as per `lightrag_webui/src/locales/en.json`: `"documentPanel.uploadDocuments.button": "Upload"`).
    *   **Action:** **Click** the **"Upload"** button.
    *   **Expected Feedback:** An **"Upload Documents"** dialog will appear (controlled by `lightrag_webui/src/components/documents/UploadDocumentsDialog.tsx`). It will likely prompt you to "Drag and drop your documents here or click to browse." (from `"documentPanel.uploadDocuments.description"`).

2.  **Select Your Research Files:**
    *   **Action:** Inside the **"Upload Documents"** dialog:
        *   Either **drag and drop** your selected research files (PDF, TXT, DOCX, etc., ensuring `.doc` files are converted!) onto the designated area.
        *   Or, **click** on the upload area to open your computer's file selection window. **Navigate** to your disorganized folder and **select** the files you want to upload.
    *   The documentation (`lightrag/api/routers/document_routes.py` for the `/documents/batch` endpoint, and `UploadDocumentsDialog.tsx`) confirms you can **select** and **upload** multiple files at once.

3.  **Initiate Upload:**
    *   After **selecting** files, they will appear listed in the dialog.
    *   **Action:** **Click** the primary confirmation button (likely labeled **"Upload"** or similar, based on the UI's general "confirm" action text).
    *   **Expected Feedback:** `LightRAG` will begin uploading and then processing your files. The dialog or the main **"Documents"** page should display progress. You might see messages like "Uploading {{name}}: {{percent}}%" for individual files (from `locales/en.json`: `"documentPanel.uploadDocuments.single.uploading"`).
    *   This ingestion step might take some time, depending on the number and size of your files.

### Step 3: Understanding What Happens Behind the Scenes (Conceptual Overview)

You don't need to perform these actions directly, but understanding this background process helps in troubleshooting and using `LightRAG` effectively. After you upload or scan files, `LightRAG` (as inferred from `lightrag.py`, `operate.py`, and the `lightrag/core/` module structure):

1.  **Parses Content:** **Reads** and **extracts** text and structural information from your files.
2.  **Chunks Documents:** **Divides** long documents into smaller, semantically coherent "chunks" (default is 1200 tokens per chunk, with some overlap to maintain context, configurable via `chunk_token_size` in the `LightRAG` class). This is crucial for efficient retrieval.
3.  **Extracts Entities & Relationships:** **Identifies** key entities (like people, organizations, specific topics) and the relationships between them within the text. This data forms the basis of the knowledge graph.
4.  **Generates Embeddings:** **Converts** each text chunk, entity, and relationship into a numerical representation called an "embedding" using a sophisticated language model (as referenced in `lightrag/core/embedder.py`). Embeddings capture the semantic meaning, enabling searches based on concepts rather than just exact keywords.
5.  **Indexes Data:** **Stores** these embeddings and their associated text/metadata in specialized databases (a vector store for similarity search and a graph store for relationship data). This allows for rapid retrieval.

---

## Part 3: Monitoring Document Processing & Understanding the Pipeline

After initiating file ingestion, it's important to monitor the progress and status of your documents.

### Step 1: View Document Statuses in the Document Manager

The **"Documents"** tab (`lightrag_webui/src/features/DocumentManager.tsx`) is your central dashboard for this.

*   **Document List:** A table will display your ingested documents.
*   **Key Columns to Observe** (based on `lightrag_webui/src/locales/en.json` and the `DocStatusResponse` model in `lightrag/api/routers/document_routes.py`):
    *   **ID** / **File Name**: You can usually **toggle** between a system ID and the original file name (look for a **"File Name"** toggle or button, as suggested by `DocumentManager.tsx` and `locales/en.json`'s `"fileNameLabel"`). The **File Path** is also tracked internally and is crucial for referencing.
    *   **Summary**: A brief preview of the document's content.
    *   **Status**: The current processing state of the document.
    *   **Length**: The size or length of the document content.
    *   **Chunks**: The number of chunks the document was divided into.
    *   **Created / Updated**: Timestamps for document creation and last update.
*   **Document Status Categories** (`DocStatus` enum in `lightrag/base.py` and `document_routes.py`):
    *   **Pending**: Queued for processing.
    *   **Processing**: Actively being analyzed (chunking, embedding, entity extraction).
    *   **Processed** (or **Completed**): Successfully indexed and ready for querying.
    *   **Failed**: An error occurred during processing. The `error` field in the status might provide details.
*   **Filtering by Status:** The UI typically allows you to **filter** the document list by these statuses (e.g., view only "Failed" documents to troubleshoot).

### Step 2: Check the Pipeline Status Dialog for Detailed Progress

For a more granular view of `LightRAG`'s background operations:

1.  **Open Pipeline Status Dialog:**
    *   On the **"Documents"** page, look for and **click** the **"Pipeline Status"** button (as per `lightrag_webui/src/locales/en.json`).
    *   **Expected Feedback:** A dialog titled **"Pipeline Status"** should open (controlled by `lightrag_webui/src/components/documents/PipelineStatusDialog.tsx`).

2.  **Interpret Pipeline Information** (based on `PipelineStatusResponse` in `document_routes.py` and `lightrag_webui/src/locales/en.json`):
    *   **"Pipeline Busy"**: Indicates if the system is actively processing documents.
    *   **"Request Pending"**: Shows if there are more documents in the queue waiting to be processed.
    *   **"Job Name"**: Describes the current high-level task (e.g., "indexing files").
    *   **"Progress"**: Displays batch processing information (e.g., "Current Batch: X / Y total documents").
    *   **"Latest Message"** and **"History Messages"**: Provide logs and specific updates from the processing pipeline, which can be helpful for diagnosing issues.

### Step 3: Handling Processing Errors

*   If a document's **Status** is "Failed," **examine** any error messages provided in the document list or pipeline status.
*   **Common Causes for Failure:**
    *   Unsupported file format (e.g., an uncoverted `.doc` file).
    *   Corrupted or unreadable file.
    *   Password-protected documents that `LightRAG` cannot decrypt.
*   **Action:**
    1.  **Identify** the problematic file(s).
    2.  **Address** the issue (e.g., **convert** the file to a supported format like `.docx` or text-searchable PDF, **ensure** it's not corrupted).
    3.  You can then either **re-upload** the corrected file(s) or, if you placed them in the `INPUT_DIR`, **trigger** another **"Scan"**. The documentation (`lightrag/api/README.md`) notes: "Reprocessing of failed files can be initiated by pressing the 'Scan' button on the web UI."

---

## Part 4: Finding Relevant Information: Querying Your Knowledge Base

Once your documents show a "Processed" status, you can start extracting the information you need for your research paper.

### Step 1: Navigate to the Retrieval Interface

1.  In the main navigation bar of the `LightRAG` WebUI, **click** on the tab labeled **"Retrieval"** (as per `lightrag_webui/src/locales/en.json`).
2.  This will **open** the query interface, which is likely a chat-style window (controlled by `lightrag_webui/src/features/RetrievalTesting.tsx`).

### Step 2: Formulating and Running Queries

1.  **Query Input:**
    *   You'll see an input box, typically at the bottom of the chat interface. The placeholder text might be "Enter your query (Support prefix: /<Query Mode>)" (from `lightrag_webui/src/locales/en.json`: `"retrievePanel.retrieval.placeholder"`).
    *   **Action:** **Type** your research question or keywords into this box. For example: "What are the main arguments against Theory X discussed in these papers?" or "key findings on renewable energy adoption in Brazil."

2.  **Understanding and Selecting Query Modes:**
    *   `LightRAG` offers several query modes to tailor how it searches for information and synthesizes answers. These modes are defined in the `QueryRequest` model (`lightrag/api/routers/query_routes.py`) and are selectable in the UI (`lightrag_webui/src/components/retrieval/QuerySettings.tsx`).
    *   **Accessing Query Mode Settings:** Look for a **"Parameters"** section or a settings icon on the **"Retrieval"** page. This panel will contain a **"Query Mode"** dropdown.
    *   **Available Modes:**
        *   **`/naive`**: Performs a basic, straightforward search.
        *   **`/local`**: Focuses on context-dependent information, likely retrieving specific text chunks and entities directly related to the query terms.
        *   **`/global`**: Utilizes the broader knowledge graph, emphasizing relationships between entities across your entire document set.
        *   **`/hybrid`**: Combines aspects of both local and global retrieval. **This is the default mode if no prefix is specified** (as stated in `lightrag/api/README.md`).
        *   **`/mix`**: Integrates knowledge graph traversal with vector-based similarity search for comprehensive results.
        *   **`/bypass`**: Sends the query directly to the underlying Large Language Model (LLM) without performing any retrieval from your documents. This is generally not what you want for finding information *within* your research files.
    *   **Action:** You can either **select** the desired mode from the **"Query Mode"** dropdown in the UI settings or **type** the mode prefix directly into the chat input before your query (e.g., `/mix your question here`).

3.  **Adjusting Query Settings (Parameters Section):**
    *   The **"Parameters"** section (`QuerySettings.tsx`) allows you to fine-tune your queries:
        *   **"Response Format"**: **Choose** how the LLM should structure its answer (e.g., "Multiple Paragraphs," "Single Paragraph," "Bullet Points" - from `lightrag_webui/src/locales/en.json`).
        *   **"Top K Results"**: (Default: 60) **Set** the number of top relevant items (entities, relationships, or text chunks) `LightRAG` should retrieve to form the context for the LLM.
        *   **"Max Tokens for Text Unit / Global Context / Local Context"**: These settings control the maximum length of different types of context provided to the LLM. Defaults are usually around 4000 tokens.
        *   **"History Turns"**: (Default: 3) **Set** how many previous turns of your current conversation with `LightRAG` are included as context for the LLM, enabling follow-up questions.
        *   **"Stream Response"**: If checked, the LLM's response will appear token by token, which can feel more interactive for longer answers.
        *   **"User Prompt"**: This is a powerful feature. You can **enter** specific instructions here to guide the LLM on *how to format its answer* or *what aspects to emphasize*, separate from your main query content. For example: "Please summarize the findings and list the source documents for each point."

4.  **Executing the Query:**
    *   After **typing** your query and **adjusting** any settings, **click** the **"Send"** button (usually an icon like a paper airplane, labeled "Send" as per `lightrag_webui/src/locales/en.json`: `"retrievePanel.retrieval.send"`).
    *   **Expected Feedback:** `LightRAG` will process your query. If streaming is enabled, the assistant's response will appear incrementally in the chat window. Otherwise, you'll wait a moment for the complete response to be generated.

---

## Part 5: Utilizing Query Results for Your Paper & Referencing

This part explains how to use the information `LightRAG` provides and how it supports your citation needs.

### Step 1: Reviewing and Copying Responses

1.  **Response Display:** The LLM-generated answer will appear in the chat area, rendered by the `ChatMessage.tsx` component. This component supports Markdown formatting, code blocks, and can even display Mermaid diagrams if the LLM generates graph descriptions in that format.
2.  **Copying Information:**
    *   **Action:** Look for a **Copy** icon next to the assistant's message. **Click** it to copy the response text to your clipboard.
    *   **Purpose:** This allows you to easily transfer quotes, summaries, or key points into your research paper draft.

### Step 2: Referencing Your Sources with LightRAG

Properly citing your sources is critical. Here’s how `LightRAG` helps:

1.  **`LightRAG`'s Built-in Source Tracking:**
    *   The `lightrag/api/README.md` states: "`LightRAG` now supports citation functionality, enabling proper source attribution."
    *   The backend system (`lightrag/operate.py`) includes the `file_path` (and sometimes `created_at` timestamps) of the original documents when it constructs the context for the LLM. This means the LLM *has access* to the source file information when generating its response.

2.  **Obtaining Source Information for Your Citations:**
    *   **Direct UI Display of Sources:** The `LightRAG` WebUI's chat response area (`ChatMessage.tsx`) does **not** automatically display a list of source files or page numbers for every statement made by the LLM.
    *   **Strategy 1: Prompting the LLM for Sources:**
        *   **Action:** When you formulate your query, or by using the **"User Prompt"** field in the Query Settings, explicitly **ask** the LLM to identify its sources from the context it was given.
        *   **Example Query Addition:** "... For each point, please indicate the source document name."
        *   **Example User Prompt:** "Cite the source file for each key finding mentioned in your response."
        *   **Expected Outcome:** The LLM, having received `file_path` information in its context, *may* include these source file names in its generated answer. The success of this depends on the LLM's ability to follow such instructions.
    *   **Strategy 2: Using "Only Need Context" Mode (Most Reliable for Source Identification):**
        *   **Action:** In the Query Settings panel, **check** the box for **"Only Need Context"**. Then, **run** your query as usual.
        *   **Expected Outcome:** Instead of an LLM-generated summary or answer, `LightRAG` will display the raw retrieved context that *would have been sent* to the LLM. This raw context will include the text chunks, entities, and relationships, along with their associated metadata, which critically includes the `file_path`.
        *   **Purpose:** You can then directly see which document(s) contributed to the relevant information for your query and use these `file_path` details for your citations.

3.  **Source Granularity:**
    *   The documentation confirms that `file_path` is tracked and available.
    *   While specific page numbers for PDFs or precise section headers within documents are not explicitly guaranteed to be part of the metadata for *every* retrieved chunk across all file types, the source *file* itself will be identifiable.

4.  **Final Citation Formatting:**
    *   Once you have identified the relevant content and its source file path using `LightRAG`, you will still need to:
        1.  **Open** the original document to verify the context and gather full bibliographic details (author, year, title, etc.).
        2.  Manually **format** your citations according to your required academic style (e.g., APA, MLA, Chicago) in your word processor or using dedicated reference management software (like Zotero, Mendeley, EndNote).
    *   `LightRAG` excels at the *discovery* and *sourcing* of information from your vast collection, but it does not automate the final step of bibliographic formatting.

---

## Part 6: Advanced Exploration & Workflow Enhancement

Beyond basic querying, `LightRAG` offers features for deeper analysis and customization.

### Step 1: Exploring Connections with the Knowledge Graph

The Knowledge Graph (KG) provides a visual representation of the entities and relationships extracted from your documents. This can help you discover connections you might not have noticed.

1.  **Navigate to the Knowledge Graph Section:**
    *   In the main navigation bar, **click** on the **"Knowledge Graph"** tab. This will load the interactive 3D graph visualization interface (controlled by `lightrag_webui/src/features/GraphViewer.tsx`).

2.  **Interacting with the Graph:**
    *   **Select Query Label:** On the left sidebar, use the **"Label"** dropdown or search bar (`lightrag_webui/src/components/graph/GraphLabels.tsx`) to focus the graph. You can **select** an entity type (e.g., "person," "organization") or **search** for a specific entity name. Selecting `*` (asterisk) attempts to load all nodes (be mindful of the "Max Nodes" setting).
    *   **Refresh Graph Data vs. Layout:**
        *   To reload graph data after adding new files or making backend changes, **click** the **"Refresh"** button (circular arrow icon) next to the label selection in the **"Label"** section (`GraphLabels.tsx`).
        *   To visually re-arrange the currently displayed nodes, use the **"Layout Graph"** control (`lightrag_webui/src/components/graph/LayoutsControl.tsx`) to **select** and **apply** different layout algorithms (e.g., "Circular," "Force Directed").
    *   **Node Interaction:**
        *   **Hover** your mouse over nodes to highlight them.
        *   **Click** on a node to select it. This opens the **"Properties"** panel on the right (`lightrag_webui/src/components/graph/PropertiesView.tsx`).
    *   **Camera Controls:** Use **W, A, S, D** keys for panning, **Q** and **E** for up/down movement. **Hold** the **right mouse button** and **drag** to rotate the view. Use **"Zoom In"** / **"Zoom Out"** buttons or your mouse scroll wheel. **"Reset Zoom"** returns to the default view.
    *   **Search within Graph:** Use the graph-specific search bar ("Search nodes..." from `GraphSearch.tsx`) to find nodes in the current view.

3.  **Viewing and Editing Node/Relationship Properties:**
    *   When a node or edge is selected, the **"Properties"** panel displays its details: "ID," "Labels," "Degree," and other properties like "Description," "Name," "Type," "Source ID," "File Path," "Keywords," "Weight."
    *   The documentation suggests that you can **edit** these properties directly from this panel (as supported by `lightrag_webui/src/components/graph/EditablePropertyRow.tsx` and backend routes in `lightrag/api/routers/graph_routes.py`). This is useful for refining your knowledge graph.
    *   Buttons like **"Expand Node"** and **"Prune Node"** in the properties panel allow you to dynamically add or remove connected nodes from the visualization, helping you focus on specific subgraphs.

### Step 2: Entity Merging (Advanced Data Cleaning - Conceptual)

`LightRAG`'s core library supports merging multiple entities into a single target entity, automatically handling relationships (`rag.merge_entities()` in `lightrag.py`). This is useful for de-duplicating concepts.

*   **From the Web UI:** The provided documentation does **not** explicitly detail a direct "Merge Entities" button or feature within the Web UI. This functionality is primarily described as a Python function in the `LightRAG` Core.
*   **Conceptual Use:** If you identify duplicate entities, you would typically use the `merge_entities` function via the `LightRAG` Core API (e.g., in a Python script) or look for such features if they are added to the UI in future versions.

---

## Part 7: Maintaining Your LightRAG Instance & Data

### Step 1: Clearing Documents and Cache

For maintenance or to start fresh with a new set of documents:

1.  **Clear All Documents:**
    *   **Navigate** to the **"Documents"** tab.
    *   Look for the **"Clear"** button (often an eraser icon, as per `lightrag_webui/src/locales/en.json`: `"documentPanel.clearDocuments.button": "Clear"`).
    *   **Action:** Clicking this button opens a **"Clear Documents"** dialog (`lightrag_webui/src/components/documents/ClearDocumentsDialog.tsx`).
    *   **WARNING:** This action, as described in the UI text (`"documentPanel.clearDocuments.warning"`), "will permanently delete all documents and cannot be undone!" It removes all documents, entities, relationships, and files from the system. You will need to **type** `yes` in a confirmation box to proceed.
    *   **Purpose:** Use this if you want to completely reset your `LightRAG` instance and re-ingest a new set of documents.

2.  **Clear LLM Cache:**
    *   Within the **"Clear Documents"** dialog, there's also an option to **"Clear LLM cache"** (as per `lightrag_webui/src/locales/en.json`).
    *   **Purpose:** This clears `LightRAG`'s cache of responses from the Large Language Model (LLM) (e.g., from previous queries or entity extractions). This can be useful if you've changed LLM models or configurations and want to ensure fresh responses, without re-indexing all your documents. It does *not* delete your documents or the knowledge graph itself.

### Step 2: Exporting Your Knowledge Graph Data (Conceptual)

For your research paper, you might want to export the structured data from `LightRAG` for further analysis or to include as supplementary material.

*   The `lightrag/api/README.md` and `lightrag/lightrag.py` documentation mention an `export_data()` Python function in the `LightRAG` Core library, which supports exporting data to formats like CSV, Excel, Markdown, and plain text.
*   **From the Web UI:** The provided documentation for the WebUI components does **not** explicitly show a direct "Export Data" button or feature for the knowledge graph or document list. This functionality is primarily exposed via the `LightRAG` Core API.
*   **Conceptual Export Process (if no direct UI button):** If you need to export data and a direct UI button is not present, you would conceptually need to:
    1.  **Interact** with the underlying API endpoints. You can explore these via the Swagger UI, typically accessible at `http://localhost:9621/docs`.
    2.  Alternatively, **use** the `LightRAG` Core library programmatically in a Python script to call the `export_data` function.

---

## Part 8: Limitations and Important Notes

*   **Legacy `.doc` Files:** `LightRAG` (with default `Docker` setup) does **not** natively support legacy `.doc` files. You **must convert** these to `.docx`, text-searchable `.pdf`, or `.txt` before uploading.
*   **Image-Only PDFs:** For best results with PDF files, **ensure** they are text-searchable (i.e., contain actual selectable text, not just scanned images).
*   **Other File Formats:** While `LightRAG` lists many file extensions as supported (in `DocumentManager`), some (like RTF, ODT, EPUB, TEX) might require additional, non-default system libraries (e.g., `docling`) for full processing. If you encounter issues with these, **convert** them to more reliably supported formats like PDF, DOCX, or TXT.
*   **No Manual Folder Organization Needed:** `LightRAG` is designed to work with a flat collection of files in its input directory. You do not need to manually **sort** your files into subdirectories before uploading or scanning.
*   **Final Judgment Rests with User:** Always critically **review** the information retrieved by `LightRAG` and **consult** the original source document to ensure accuracy and proper context before using it in your research paper.

---

## Conclusion: Empowering Your Research

`LightRAG`, based on its documented features, offers a robust and user-friendly way to tackle your disorganized research files. By following this tutorial, you can:

*   Successfully **ingest and index** your mixed-format documents (after necessary conversions, especially for `.doc` files).
*   **Utilize** a powerful query interface with various modes to efficiently find specific information.
*   **Leverage** `LightRAG`'s **source tracking (`file_path`)** to support your referencing needs.
*   Optionally, **explore** your data visually through the **knowledge graph**.

This system has the potential to significantly reduce the time you spend sifting through documents, allowing you to focus more on the critical tasks of analyzing information and writing your paper. Remember to **consult** the `lightrag/api/README.md` and the UI tooltips (many are defined in `lightrag_webui/src/locales/en.json`) for quick reminders as you use the tool.

Good luck with your research!