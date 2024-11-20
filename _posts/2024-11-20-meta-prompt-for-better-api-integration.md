---
tags: AI>LLM
info: aberto.
date: 2024-11-20
type: post
layout: post
published: true
slug: meta-prompt-for-better-api-integration
title: 'Meta-Prompt for Better API Integration'
---
URL Source: `https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/`

We recently published [Meta-Prompt](https://docs.jina.ai/), a single text file that outlines all of our API specifications. You can think of it as documentation for LLMs, and use it to automatically generate integrations of our APIs including Reader, Embeddings, Reranker, and more.

0:00

/1:44

![Image 1](https://jina-ai-gmbh.ghost.io/content/media/2024/11/meta-prompt-square-VEED_thumb.jpg)

It's as simple as copying and pasting our prompt into ChatGPT/Claude, or piping it into the [`llm`](https://github.com/simonw/llm) command as a system prompt, then adding your own prompt to specify what you want to build (which we do below). It's great if you want to use LLMs to quickly build apps that scrape the web, work with embeddings, or even full-blown RAG systems. All that with minimal hallucinations.

Let’s say you want to use an LLM to generate code that uses Jina’s APIs. Let’s ask GPT-4o to do just that:

0:00

/0:27

![Image 2](https://jina-ai-gmbh.ghost.io/content/media/2024/11/output_thumb.jpg)

Looks good, right? It’s got the `from jina import Client` and everything.

One small problem: The Jina package is in maintenance mode, and it is _not_ the way to access our APIs. Even if you _do_ install the Jina package, the generated program will crash when you try to run it:

0:00

/0:21

![Image 3](https://jina-ai-gmbh.ghost.io/content/media/2024/11/Screencast-from-2024-11-11-14-43-51_thumb.jpg)

So what? We can just ask GPT to search the web for Jina’s APIs, right? Here’s what we get:

0:00

/1:14

![Image 4](https://jina-ai-gmbh.ghost.io/content/media/2024/11/Screencast-from-2024-11-11-14-45-33_thumb.jpg)

However, if you look at the code it _doesn’t_ use all of the relevant Jina APIs. It very clearly didn’t find out that Reader is a thing, instead making us install [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to do the scraping. And, even when it _could_ (supposedly) do the scraping with BeautifulSoup, it didn’t accurately parse the response format for Jina Embeddings, leading to a crash:

0:00

/0:16

![Image 5](https://jina-ai-gmbh.ghost.io/content/media/2024/11/Screencast-from-2024-11-11-14-50-35--1-_thumb.jpg)

Yet, even if ChatGPT _could_ do it properly by searching, many other LLMs (like Claude) don’t currently support web search, severely limiting your options.

This is where Meta-Prompt shines. With Meta-Prompt, you can load all the context and specifications of Jina’s APIs into the LLM. This means the LLM can generate code that leverages Jina’s APIs directly, without hallucinations or unnecessary workarounds, giving you code that works _the first time_.

💡

Okay, __usually__ the first time. LLMs can be unpredictable, but as you can see below, things went well in our experiments.

To put the Meta-Prompt through its paces, we ran a few experiments and evaluated the results. Unless otherwise specified, we used [Claude-3.5-Sonnet](https://www.anthropic.com/news/claude-3-5-sonnet) as the LLM.

For all experiments, we specified relevant API keys (like `JINA_API_KEY` and `ANTHROPIC_API_KEY`) as environment variables before running the generated code.

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#experiment-1-verifying-statements-using-meta-prompt-in-chatgpt "Experiment 1: Verifying Statements Using Meta-Prompt in ChatGPT")Experiment 1: Verifying Statements Using Meta-Prompt in ChatGPT

We're writing this just after the US elections, where more disinformation than ever was flying around. How can we separate the signal from the noise in our feeds, and get just the good stuff with none of the lies?

Let's say we want to check whether a new UK law is accurately reported on [BBC.com](http://bbc.com/), specifically the claim:

> "The UK government has announced a new law that will require social media companies to verify the age of their users."

We can copy-paste the Meta-Prompt into ChatGPT, then type our own prompt to generate the code to do that, like:

```
Write the JavaScript code to check the validity
of the following statement on bbc.com: 

"The UK government has announced a new law 
that will require social media companies to 
verify the age of their users."
```

0:00

/0:35

![Image 6](https://jina-ai-gmbh.ghost.io/content/media/2024/11/grounding-chatgpt_thumb.jpg)

We can then run that with `node grounding.js` (after installing any prerequisite packages like [axios](https://www.npmjs.com/package/axios)). We get output like this, showing that the claim is true, along with sources:

0:00

/0:04

![Image 7](https://jina-ai-gmbh.ghost.io/content/media/2024/11/grounding-run-1_thumb.jpg)

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#experiment-2-visualizing-hacker-news-from-the-cli "Experiment 2: Visualizing Hacker News from the CLI")Experiment 2: Visualizing Hacker News from the CLI

If you’re more of a command line warrior, you can use Meta-Prompt from the CLI via cURL. First, you’ll need to install the `llm` Python package:

```
pip install llm
```

And then the Claude-3 plugin:

```
llm install llm-claude-3
```

For the last stage of setup, specify your Anthropic API key:

```
export ANTHROPIC_API_KEY=<your key>
```

Now, let’s write a prompt to visualize every sentence from the Hacker News front page:

```
grab every sentence from hackernews frontpage and 
visualize them in a 2d umap using matplotlib
```

We can [pipe](https://wizardzines.com/comics/bash-pipes/) this into the `llm` command with:

```
curl docs.jina.ai | llm -s "grab every sentence from hackernews frontpage and visualize them in a 2d umap using matplotlib" -m claude-3.5-sonnet
```

0:00

/0:24

![Image 8](https://jina-ai-gmbh.ghost.io/content/media/2024/11/Screencast-from-2024-11-11-11-23-03_thumb.jpg)

If we extract and and run the generated code, we get something like this:

0:00

/0:38

![Image 9](https://jina-ai-gmbh.ghost.io/content/media/2024/11/Screencast-from-2024-11-11-11-28-43_thumb.jpg)

💡

One current limitation (though I’m sure with some extra coding from the user there’s a way around it) is that you’ll need to install requirements manually. No `requirements.txt` is generated. In this case we needed [UMAP](https://umap-learn.readthedocs.io/en/latest/) and [Matplotlib](https://matplotlib.org/), though your mileage may vary.

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#experiment-3-building-a-simple-rag-system-with-json-storage "Experiment 3: Building a Simple RAG System with JSON Storage")Experiment 3: Building a Simple RAG System with JSON Storage

To push things even farther, let's create a simple RAG system. In my spare time I'm learning [SolidPython](https://github.com/jeff-dh/SolidPython) so we'll use the repo and wiki as a knowledge base. To keep things simple, we won't use a database, but rather just store the data in a JSON file.

Here's the prompt, stored in the file `prompt.txt`:

```
Create a simple RAG system using pages from these sources:

- repo: <https://github.com/jeff-dh/SolidPython>
- wiki: <https://github.com/jeff-dh/SolidPython/wiki> (and all the subpages)

Scrape no other pages.

Instead of using vector database, use JSON file

You can access an LLM with the CLI command: llm 'your prompt' -m claude-3.5-sonnet

After segmenting and indexing all the pages, present a prompt for the user to ask a
question. To answer the question, find the top three segments and pass them to the LLM
with the prompt:

--- prompt start ---
Based on these segments:

- {segment 1}
- {segment 2}
- {segment 3}

Answer the question: {question}
--- prompt end ---
```

As you can see, we can give the LLM additional tools by specifying them in the prompt. Without this, Claude often hallucinates a less optimal (or even broken) way to add the LLM to the RAG system.

Since this is a very long prompt (with plenty of punctuation that may break any pipe we run it in), we’ll use the text `$(cat prompt.txt)` rather than the prompt itself when we run our command:

```
curl docs.jina.ai/v4 | llm -s "$(cat prompt.txt)" -m claude-3.5-sonnet
```

0:00

/0:34

![Image 10](https://jina-ai-gmbh.ghost.io/content/media/2024/11/docsqa-claude_thumb.jpg)

Phew! That's a lot of output. But (like with the Hacker News example) it's a pain in the neck to extract and run the code from that big blob of text. Of course, there’s no problem that can’t be solved by just throwing more LLM at it, right? So let’s add another prompt to “de-blob” the original output:

```
leave just the code in this file, remove all surrounding explanatory text. 
do not wrap code in backticks, just return "pure code"
```

Now we add that to our command pipeline and run it:

```
curl docs.jina.ai/v4 | llm -s "$(cat prompt.txt)" -m claude-3.5-sonnet | llm -s 'leave just the code in this file, remove all surrounding explanatory text. do not wrap code in backticks, just return "pure code"' -m claude-3.5-sonnet > app.py
```

💡

Since we’re using `> app.py` at the end of our command to direct all output into a file, there’s nothing to show in a video.

We can then run that app with `python app.py` and we get our RAG program. As you can see, it can answer questions and maintain a working memory:

0:00

/0:34

![Image 11](https://jina-ai-gmbh.ghost.io/content/media/2024/11/docsqa-run_thumb.jpg)

💡

The first run of this took a little longer, since it had to segment and encode all the data. For subsequent runs it loaded that from a JSON file to save time and cost.

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#experiment-4-building-an-app-factory-with-meta-prompt "Experiment 4: Building an App Factory with Meta-Prompt")Experiment 4: Building an App Factory with Meta-Prompt

Now that we can generate scripts and apps non-interactively, we can easily automate an "app factory" - a script that iterates over prompts and produces Python scripts as output. You can get the app factory script in a [GitHub gist](https://gist.github.com/alexcg1/4150f2e7dfe0d635260c71d59324172b) for now:

[App Factory with Jina AI Meta-Prompt App Factory with Jina AI Meta-Prompt. GitHub Gist: instantly share code, notes, and snippets. ![Image 12](https://jina-ai-gmbh.ghost.io/content/images/icon/pinned-octocat-093da3e6fa40.svg)262588213843476 ![Image 13](https://jina-ai-gmbh.ghost.io/content/images/thumbnail/gist-og-image-54fd7dc0713e.png)](https://gist.github.com/alexcg1/4150f2e7dfe0d635260c71d59324172b)

What it does, in short, is:

*   Iterate through the `prompts` directory which contains (you guessed it) prompt files.
*   Pass the Meta-Prompt and each prompt text to Claude-3.5-Sonnet (via `llm`).
*   Take the output and pass that to Claude _again_, this time with the prompt telling it to just leave the code.
*   Write that to a file in the `apps` directory.

We'd show a demo, but there’s not much to see. It just logs which prompt filename it's working on, and otherwise operates silently with no interesting output to the screen.

💡

__Testing__ the apps it generates is another matter, one that I can't solve off the top of my head. In our experience, we often specify the data we want to use in our prompts, usually by passing an external URL to download with Reader. Yet sometimes the LLM hallucinates mock data, and the script runs without obvious issues — it just "lies" about what it's doing.

To take the app factory to the next level, you could go full [Factorio](https://www.notion.so/Meta-Prompt-LLM-Generated-Code-without-The-Hallucinations-333ad1ddc735470e83f987d7dd6a644f?pvs=21) and write _another_ script to generate app ideas and from there generate prompts to feed into the factory. We haven’t done that yet, but we leave it as an exercise for you, the reader.

We learned a lot from using Meta-Prompt, both about what to put in our own prompts and how different LLMs generate different output.

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#general-observations "General Observations")General Observations

*   **API Specialization**: Using task-specific APIs (e.g., [Google Books](https://developers.google.com/books) for book-related queries) ensures more consistent results than general-purpose search APIs, which can reduce token usage and improve reliability.
*   **Custom Prompts for Reusability**: For non-interactive setups, saving prompts as `.txt` files and piping them into the CLI enables efficient code-only outputs without extra explanatory text cluttering things up.
*   **Structured Output**: Storing outputs (usually in JSON format) and reloading them as needed saves tokens and streamlines tasks like generating embeddings, where token usage can be expensive.

### [](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#insights-from-using-different-llms "Insights from Using Different LLMs")Insights from Using Different LLMs

**GPT**

*   **Prompt Retention Issues**: GPT-4o sometimes loses details with lengthy instructions, leading to issues when it "forgets" key elements mid-discussion. This leads to a _lot_ of frustration when you have to remind it of simple things.
*   **API Integration Challenges**: In cases like integrating [Milvus Lite](https://milvus.io/docs/milvus_lite.md) with `jina-embeddings-v3`, even when we provide the Milvus Lite API instructions, GPT-4o fails completely and repeatedly, generating code that creates databases that lack the embeddings that the code just generated, making semantic search applications impossible.

**Claude**

*   **Code Output Limitations**: Claude-3.5 often produces scripts that appear complete but contain silent issues, like missing error handling or failing to account for missing API keys. Additionally, it sometimes falls back on pre-set examples rather than generating responses tailored to specific instructions.
*   **Silent Output**: With LLM-generated code it _really_ helps to have some logging of what's happening behind the scenes when you run the program, just to make sure the model didn't mess things up. Unless you directly specify to do so, apps created with Claude will often run silently, leaving you with no clue what’s happening.
*   **Interaction with CLI**: You need to clearly specify that CLI commands are _CLI_ commands. If you tell Claude it can use the `llm` command, often it will try to call a Python `llm()` function which doesn’t exist.
*   **Claude 3.5-Sonnet Is the Way to Go:** Claude-3.5-Haiku also seemed to work okay in initial tests, but Opus and Sonnet-3 just summarize the Jina API instructions, without taking into account the user prompt.

[](https://jina.ai/news/meta-prompt-for-better-jina-api-integration-and-codegen/#conclusion "Conclusion")Conclusion
-------------------------------------------------------------------------------------------------------------------

Using Meta-Prompt provides new ways to integrate Jina’s APIs with LLMs, allowing you to run experiments and build apps that work on the first try. No more crashes, missed API connections, or hallucinated functions — Meta-Prompt ensures the code generated is accurate and functional right out of the gate. Whether you’re verifying statements, generating embeddings, building a lightweight RAG system, or automating app creation, Meta-Prompt transforms natural language instructions into actionable, correct code, bypassing the typical back and forth with an LLM to get things that actually work.

Whether you’re copying Meta-Prompt into ChatGPT or using it with a custom LLM command, it offers a straightforward, reliable way to leverage Jina’s capabilities. Our experiments and insights show Meta-Prompt as a solid tool for robust integration into your projects.

If you’re ready to explore what Meta-Prompt can do, head to [docs.jina.ai](http://docs.jina.ai/) for the latest documentation and resources.