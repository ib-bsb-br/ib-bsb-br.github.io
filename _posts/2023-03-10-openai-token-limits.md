---
title: OpenAI Token Limits
date: 2023-03-10 00:00:00 -03:00
categories:
- Tutorial
tags:
- AI
comment: github.com/Ighina/DeepTiling
info: aberto.
type: post
layout: post
sha: 
---

How to Get Around OpenAI GPT-3 Token Limits
Python Developer’s Guide to OpenAI GPT-3 API
UPDATED: The article includes the ChatGPT API option (model=”gpt-3.5-turbo”).

If you are reading this article, you have encountered the token limits of OpenAI’s GPT-3 models. The limits for various models are provided here.


https://platform.openai.com/docs/models/gpt-3
To overcome this limitation, OpenAI offers a great example with the Summarizing Books with Human Feedback (https://openai.com/blog/summarizing-books/) solution as provided below.

The original text is divided into sections, and each section is summarized.
Section summaries are summarized again into higher-level summaries.
The summarizing process continues until a complete summary is achieved.
I faced a similar issue while working on the article “Creating Meeting Minutes using OpenAI GPT-3 API” because most meeting transcripts exceed 4,000 tokens.

This, like everything, has many different ways to be completed. For now, I am providing three options:

NLTK (Natural Language Toolkit). Token count using this option does not match OpenAI tokenizer, but the difference is nominal.
Transformers. Token count using this option matches OpenAI tokenizer.
Tiktoken. Token count using this option matches OpenAI tokenizer and is faster than Transformers.
NLTK
NLTK is a leading platform for building Python programs to work with human language data. This code was developed using Google Colab, but you can use any IDE of your choice. Some codes are specific to Goole Colab, though.

Prerequisites
The following are prerequisites for this tutorial:

Python Package: nltk (Natural Language Toolkit)
Python Package: openai
Install Python Packages
%%writefile requirements.txt
openai
nltk
%pip install -r requirements.txt
Import Python Packages
import platform
import os
import openai
import os

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

print('Python: ', platform.python_version())
print('re: ', re.__version__)
print('nltk: ', nltk.__version__)

(Optional) Count the Number of Tokens
OpenAI GPT-3 is limited to 4,001 tokens per request, encompassing both the request (i.e., prompt) and response. We will be determining the number of tokens present in the meeting transcript.

def count_tokens(filename):
    with open(filename, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    return len(tokens)
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"
token_count = count_tokens(filename)
print(f"Number of tokens: {token_count}")

(Optional for the second block of code) Break up the Meeting Transcript into chunks of 2,000 tokens with an overlap of 100 tokens
We will be dividing the meeting transcript into segments of 2,000 tokens, with an overlap of 100 tokens to avoid losing any information from the split.

def break_up_file(tokens, chunk_size, overlap_size):
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_file(tokens[chunk_size-overlap_size:], chunk_size, overlap_size)

def break_up_file_to_chunks(filename, chunk_size=2000, overlap_size=100):
    with open(filename, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    return list(break_up_file(tokens, chunk_size, overlap_size))
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

chunks = break_up_file_to_chunks(filename)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {len(chunk)} tokens")

Function to Convert the NLTK Tokenized Text to Non-Tokenized Text
We will need to convert the tokenized text from NLTK to non-tokenized text, as the OpenAI GPT-3 API does not handle tokenized text very well, which can result in a higher token count exceeding 2,000.

def convert_to_detokenized_text(tokenized_text):
    prompt_text = " ".join(tokenized_text)
    prompt_text = prompt_text.replace(" 's", "'s")
    return detokenized_text
Set OpenAI API Key
Set an environment variable called “OPEN_API_KEY” and assign a secret API key from OpenAI (https://beta.openai.com/account/api-keys).

os.environ["OPENAI_API_KEY"] = 'your openai api key'
openai.api_key = os.getenv("OPENAI_API_KEY")
Summarize the Meeting Transcript one chunk (of 2,000 tokens) at a time
Option 1: model=”text-davinci-003"

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):
    prompt_request = "Summarize this meeting transcript: " + convert_to_detokenized_text(chunks[i])
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["text"].strip())
Option 2: model=”gpt-3.5-turbo”

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):

    prompt_request = "Summarize this meeting transcript: " + convert_to_prompt_text(chunks[i])
    
    messages = [{"role": "system", "content": "This is text summarization."}]    
    messages.append({"role": "user", "content": prompt_request})

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["message"]['content'].strip())
Consolidate the Meeting Transcript Summaries
prompt_request = "Consoloidate these meeting summaries: " + str(prompt_response)
response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
meeting_summary = response["choices"][0]["text"].strip()
print(meeting_summary)
Transformers
Transformers provides APIs and tools to easily download and train state-of-the-art pretrained models. This code was developed using Google Colab, but you can use any IDE of your choice. Some codes are specific to Goole Colab, though.

Prerequisites
The following are prerequisites for this tutorial:

Python Package: torch
Python Package: transformers
Python Package: openai
Install Python Packages
%%writefile requirements.txt
openai
torch
transformers
%pip install -r requirements.txt
Import Python Packages
import platform
import os
import openai

import torch
import transformers
from transformers import AutoTokenizer

print('Python: ', platform.python_version())
print('re: ', re.__version__)
print('torch: ', torch.__version__)
print('transformers: ', transformers.__version__)

(Optional) Count the Number of Tokens
OpenAI GPT-3 is limited to 4,001 tokens per request, encompassing both the request (i.e., prompt) and response. We will be determining the number of tokens present in the meeting transcript.

def count_tokens(filename):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
    num_tokens = input_ids.shape[1]
    return num_tokens
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"
token_count = count_tokens(filename)
print(f"Number of tokens: {token_count}")

(Optional for the second block of code) Break up text into chunks of 2000 tokens with an overlap of 100 tokens
We will be breaking up the text into chunks of 2,000 tokens with an overlapping 100 tokens to ensure any information is not lost from breaking up the text.

def break_up_file_to_chunks(filename, chunk_size=2000, overlap=100):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    tokens = tokenizer.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

chunks = break_up_file_to_chunks(filename)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {len(chunk)} tokens")

Set OpenAI API Key
Set an environment variable called “OPEN_API_KEY” and assign a secret API key from OpenAI (https://beta.openai.com/account/api-keys).

os.environ["OPENAI_API_KEY"] = 'paste your openai api key here'
openai.api_key = os.getenv("OPENAI_API_KEY")
Summarize the text one chunk at a time
Option 1: model=”text-davinci-003"

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []

tokenizer = AutoTokenizer.from_pretrained("gpt2")

chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):

    prompt_request = "Summarize this meeting transcript: " + tokenizer.decode(chunks[i])
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["text"].strip())
Option 2: model=”gpt-3.5-turbo”

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []

tokenizer = AutoTokenizer.from_pretrained("gpt2")

chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):

    prompt_request = "Summarize this meeting transcript: " + tokenizer.decode(chunks[i])

    messages = [{"role": "system", "content": "This is text summarization."}]    
    messages.append({"role": "user", "content": prompt_request})

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["message"]['content'].strip())
Consolidate the summaries
prompt_request = "Consoloidate these meeting summaries: " + str(prompt_response)
response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
Summary of summaries
meeting_summary = response["choices"][0]["text"].strip()
print(meeting_summary)
Tiktoken
tiktoken is a fast BPE tokeniser for use with OpenAI’s models. This code was developed using Google Colab, but you can use any IDE of your choice. Some codes are specific to Goole Colab, though.

Prerequisites
The following are prerequisites for this tutorial:

Python Package: tiktoken
Python Package: openai
Install Python Packages
%%writefile requirements.txt
openai
tiktoken
%pip install -r requirements.txt
Import Python Packages
import platform
import os
import openai
import tiktoken

print('Python: ', platform.python_version())
(Optional) Count the Number of Tokens
OpenAI GPT-3 is limited to 4,001 tokens per request, encompassing both the request (i.e., prompt) and response. We will be determining the number of tokens present in the meeting transcript.

def count_tokens(filename):
    encoding = tiktoken.get_encoding("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    input_ids = encoding.encode(text)
    num_tokens = len(input_ids)
    return num_tokens
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

num_tokens = count_tokens(filename=filename)
print("Number of tokens:  ", num_tokens)

(Optional for the second block of code) Break up text into chunks of 2000 tokens with an overlap of 100 tokens
We will be breaking up the text into chunks of 2,000 tokens with an overlapping 100 tokens to ensure any information is not lost from breaking up the text.

def break_up_file_to_chunks(filename, chunk_size=2000, overlap=100):

    encoding = tiktoken.get_encoding("gpt2")
    with open(filename, 'r') as f:
        text = f.read()

    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks
filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

chunks = break_up_file_to_chunks(filename)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i}: {len(chunk)} tokens")

Set OpenAI API Key
Set an environment variable called “OPEN_API_KEY” and assign a secret API key from OpenAI (https://beta.openai.com/account/api-keys).

os.environ["OPENAI_API_KEY"] = 'paste your openai api key here'
openai.api_key = os.getenv("OPENAI_API_KEY")
Summarize the text one chunk at a time
Option 1: model=”text-davinci-003"

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []

encoding = tiktoken.get_encoding("gpt2")
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):
    prompt_request = "Summarize this meeting transcript: " + encoding.decode(chunks[i])

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt_request,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["text"].strip())
Option 2: model=”gpt-3.5-turbo”

filename = "/content/drive/MyDrive/Colab Notebooks/minutes/data/Round_22_Online_Kickoff_Meeting.txt"

prompt_response = []

encoding = tiktoken.get_encoding("gpt2")
chunks = break_up_file_to_chunks(filename)

for i, chunk in enumerate(chunks):

    prompt_request = "Summarize this meeting transcript: " + encoding.decode(chunks[i])
    messages = [{"role": "system", "content": "This is text summarization."}]    
    messages.append({"role": "user", "content": prompt_request})

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=.5,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
    )
    
    prompt_response.append(response["choices"][0]["message"]['content'].strip())
Consolidate the summaries
prompt_request = "Consoloidate these meeting summaries: " + str(prompt_response)

response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_request,
        temperature=.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
Summary of Summaries
meeting_summary = response["choices"][0]["text"].strip()
print(meeting_summary)
I hope you have enjoyed this tutorial. If you have any questions or comments, please provide them here.
