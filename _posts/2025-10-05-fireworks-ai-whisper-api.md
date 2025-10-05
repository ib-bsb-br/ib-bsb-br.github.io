---
tags: [scratchpad]
info: aberto.
date: 2025-10-05
type: post
layout: post
published: true
slug: fireworks-ai-whisper-api
title: 'Fireworks AI - Whisper API'
---
bibref https://fireworks.ai/models/fireworks/whisper-v3-turbo

Whisper V3 Turbo API & Playground | Fireworks AI

===============

[Join the **Fireworks Startups Program** and unlock credits, expert support, and community to scale fast. Join here](https://fireworks.ai/startup-program)

[![Image 3: Fireworks Logo](https://cdn.sanity.io/images/pv37i0yn/production/2095949f01e1cf9cf0841096b67d547d9dbfba2e-215x24.svg)](https://fireworks.ai/)

*             Platform  
*             Models  
*             Developers  
*   [Pricing](https://fireworks.ai/pricing)
*             Partners  
*             Resources  
*             Company  

[Log In](https://fireworks.ai/login)[Get Started](https://fireworks.ai/signup)

![Image 4: OpenAi Logo MArk](https://cdn.sanity.io/images/pv37i0yn/production/f549e0e24c286535bc06df0b0310d270183469e8-40x40.svg)

Whisper V3 Turbo
================

Whisper large-v3-turbo is a finetuned version of a pruned Whisper large-v3. In other words, it's the exact same model, except that the number of decoding layers have reduced from 32 to 4. As a result, the model is way faster, at the expense of a minor quality degradation.

[Try Model](https://app.fireworks.ai/playground?model=accounts/fireworks/models/whisper-v3-turbo)

Fireworks Features
------------------

### Serverless

Immediately run model on pre-configured GPUs and pay-per-token

[Learn More](https://docs.fireworks.ai/getting-started/quickstart)

### On-demand Deployment

On-demand deployments give you dedicated GPUs for Whisper V3 Turbo using Fireworks' reliable, high-performance system with no rate limits.

[Learn More](https://fireworks.ai/docs/guides/ondemand-deployments)

Whisper V3 Turbo FAQs
---------------------

### What is Whisper V3 Turbo and who developed it?

### What applications and use-cases does Whisper V3 Turbo excel at?

### What is the maximum context length for Whisper V3 Turbo?

### What is the usable context window?

### What are known failure modes of Whisper V3 Turbo?

### How many parameters does Whisper V3 Turbo have?

### What license governs commercial use of Whisper V3 Turbo?

Info & Pricing
--------------

### Provider

OpenAI

### Model Type

Audio

### Serverless

Available

### Pricing Per Minute

$0.0009

* * *

![Image 5: Fireworks Logo](https://cdn.sanity.io/images/pv37i0yn/production/2095949f01e1cf9cf0841096b67d547d9dbfba2e-215x24.svg)

### Platform

[AI Native](https://fireworks.ai/ai-native)[Enterprise](https://fireworks.ai/enterprise)[Customers](https://fireworks.ai/customers)

### Use Cases

[Code Assistance](https://fireworks.ai/usecases/code-assistance)[Conversational AI](https://fireworks.ai/conversational-ai)[Agentic Systems](https://fireworks.ai/usecases/agentic-systems)[Search](https://fireworks.ai/usecases/search)[Multimedia](https://fireworks.ai/usecases/multimedia)[Enterprise RAG](https://fireworks.ai/usecases/enterprise-rag)

### Developers

[Model Library](https://fireworks.ai/models)[Docs](https://docs.fireworks.ai/getting-started/introduction)[CLI](https://docs.fireworks.ai/tools-sdks/firectl/firectl)[API](https://docs.fireworks.ai/api-reference/introduction)[Changelog](https://docs.fireworks.ai/updates/changelog)

### Pricing

[Serverless](https://fireworks.ai/pricing#serverless-pricing)[On-Demand](https://fireworks.ai/pricing#on-demand-pricing)[Fine Tuning](https://fireworks.ai/pricing#fine-tuning-pricing)[Enterprise](https://fireworks.ai/contact-reserved)

### Partners

[Cloud and Infrastructure](https://fireworks.ai/partners#cloud-infra)[Consulting and Services](https://fireworks.ai/partners#consulting)[Technology](https://fireworks.ai/partners#technology)[Fireworks for Startups](https://fireworks.ai/startup-program)

### Resources

[Blog](https://fireworks.ai/blog)[Demos](https://demos.fireworks.ai/)[Cookbooks](https://docs.fireworks.ai/examples/introduction)

### Company

[Leadership](https://fireworks.ai/team)[Investors](https://fireworks.ai/team#investors)[Careers](https://job-boards.greenhouse.io/fireworksai)[Trust Center](https://trust.fireworks.ai/)

© 2025 Fireworks AI, Inc. All rights reserved.

[](https://x.com/FireworksAI_HQ)[](https://www.youtube.com/@fireworksai)[](https://www.linkedin.com/company/fireworks-ai)[](https://discord.gg/fireworks)

--

# Transcribe audio

<CardGroup cols={1}>
  <Card title="Try notebook" icon="rocket" href="https://colab.research.google.com/github/fw-ai/cookbook/blob/main/learn/audio/audio_prerecorded_speech_to_text/audio_prerecorded_speech_to_text.ipynb">
    Send a sample audio to get a transcription.
  </Card>
</CardGroup>

### Request

##### (multi-part form)

<ParamField query="file" type="file | string" required>
  The input audio file to transcribe or an URL to the public audio file.

  Max audio file size is 1 GB, there is no limit for audio duration. Common file formats such as mp3, flac, and wav are supported. Note that the audio will be resampled to 16kHz, downmixed to mono, and reformatted to 16-bit signed little-endian format before transcription. Pre-converting the file before sending it to the API can improve runtime performance.
</ParamField>

<ParamField query="model" type="string" default="whisper-v3" optional>
  String name of the ASR model to use. Can be one of `whisper-v3` or `whisper-v3-turbo`. Please use the following serverless endpoints:

  * [https://audio-prod.us-virginia-1.direct.fireworks.ai](https://audio-prod.us-virginia-1.direct.fireworks.ai) (for `whisper-v3`);
  * [https://audio-turbo.us-virginia-1.direct.fireworks.ai](https://audio-turbo.us-virginia-1.direct.fireworks.ai) (for `whisper-v3-turbo`);
</ParamField>

<ParamField query="vad_model" type="string" default="silero" optional>
  String name of the voice activity detection (VAD) model to use. Can be one of `silero`, or `whisperx-pyannet`.
</ParamField>

<ParamField query="alignment_model" type="string" default="mms_fa" optional>
  String name of the alignment model to use. Currently supported:

  * `mms_fa` optimal accuracy for multilingual speech.
  * `tdnn_ffn` optimal accuracy for English-only speech.
  * `gentle` best accuracy for English-only speech (requires a dedicated endpoint, contact us at <a href="mailto:inquiries@fireworks.ai">[inquiries@fireworks.ai](mailto:inquiries@fireworks.ai)</a>).
</ParamField>

<ParamField query="language" type="string | null" optional>
  The target language for transcription. See the [Supported Languages](#supported-languages) section below for a complete list of available languages.
</ParamField>

<ParamField query="prompt" type="string | null" optional>
  The input prompt that the model will use when generating the transcription. Can be used to specify custom words or specify the style of the transcription. E.g. `Um, here's, uh, what was recorded.` will make the model to include the filler words into the transcription.
</ParamField>

<ParamField query="temperature" type="float | list[float]" default="0">
  Sampling temperature to use when decoding text tokens during transcription. Alternatively, fallback decoding can be enabled by passing a list of temperatures like `0.0,0.2,0.4,0.6,0.8,1.0`. This can help to improve performance.
</ParamField>

<ParamField query="response_format" type="string" default="json">
  The format in which to return the response. Can be one of `json`, `text`, `srt`, `verbose_json`, or `vtt`.
</ParamField>

<ParamField query="timestamp_granularities" type="string | list[string]" optional>
  The timestamp granularities to populate for this transcription. `response_format` must be set `verbose_json` to use timestamp granularities. Either or both of these options are supported. Can be one of `word`, `segment`, or `word,segment`. If not present, defaults to `segment`.
</ParamField>

<ParamField query="diarize" type="string" optional>
  Whether to get speaker diarization for the transcription. Can be one of `true`, or `false`. If not present, defaults to `false`.

  Enabling diarization also requires other fields to hold specific values:

  1. `response_format` must be set `verbose_json`.
  2. `timestamp_granularities` must include `word` to use diarization.
</ParamField>

<ParamField query="min_speakers" type="int" optional>
  The minimum number of speakers to detect for diarization. `diarize` must be set `true` to use `min_speakers`. If not present, defaults to `1`.
</ParamField>

<ParamField query="max_speakers" type="int" optional>
  The maximum number of speakers to detect for diarization. `diarize` must be set `true` to use `max_speakers`. If not present, defaults to `inf`.
</ParamField>

<ParamField query="preprocessing" type="string" optional>
  Audio preprocessing mode. Currently supported:

  * `none` to skip audio preprocessing.
  * `dynamic` for arbitrary audio content with variable loudness.
  * `soft_dynamic` for speech intense recording such as podcasts and voice-overs.
  * `bass_dynamic` for boosting lower frequencies;
</ParamField>

### Response

<Tabs>
  <Tab title="json/text/srt/vtt">
    <ResponseField name="text" type="string" required />
  </Tab>

  <Tab title="verbose_json">
    <ResponseField name="task" type="string" default="transcribe" required>
      The task which was performed. Either `transcribe` or `translate`.
    </ResponseField>

    <ResponseField name="language" type="string" required>
      The language of the transcribed/translated text.
    </ResponseField>

    <ResponseField name="duration" type="number" required>
      The duration of the transcribed/translated audio, in seconds.
    </ResponseField>

    <ResponseField name="text" type="string" required>
      The transcribed/translated text.
    </ResponseField>

    <ResponseField name="words" type="object[] | null" optional>
      Extracted words and their corresponding timestamps.

      <Expandable title="Word properties">
        <ResponseField name="word" type="string" required>
          The text content of the word.
        </ResponseField>

        <ResponseField name="language" type="string" required>
          The language of the word.
        </ResponseField>

        <ResponseField name="probability" type="number" required>
          The probability of the word.
        </ResponseField>

        <ResponseField name="hallucination_score" type="number" required>
          The hallucination score of the word.
        </ResponseField>

        <ResponseField name="start" type="number" required>
          Start time of the word in seconds.
        </ResponseField>

        <ResponseField name="end" type="number" required>
          End time of the word in seconds.
        </ResponseField>

        <ResponseField name="speaker_id" type="string" optional>
          Speaker label for the word.
        </ResponseField>
      </Expandable>
    </ResponseField>

    <ResponseField name="segments" type="object[] | null" optional>
      Segments of the transcribed/translated text and their corresponding details.

      <Expandable title="Segment properties (partial)">
        <ResponseField name="id" type="number" required>
          The id of the segment.
        </ResponseField>

        <ResponseField name="text" type="string" required>
          The text content of the segment.
        </ResponseField>

        <ResponseField name="start" type="number" required>
          Start time of the segment in seconds.
        </ResponseField>

        <ResponseField name="end" type="number" required>
          End time of the segment in seconds.
        </ResponseField>

        <ResponseField name="speaker_id" type="string" optional>
          Speaker label for the segment.
        </ResponseField>

        <ResponseField name="words" type="object[] | null" optional>
          Extracted words in the segment.
        </ResponseField>
      </Expandable>
    </ResponseField>
  </Tab>
</Tabs>

<RequestExample>
  ```curl curl

  # Download audio file
  curl -L -o "audio.flac" "https://tinyurl.com/4997djsh"

  # Make request
  curl -X POST "https://audio-prod.us-virginia-1.direct.fireworks.ai/v1/audio/transcriptions" \
  -H "Authorization: <FIREWORKS_API_KEY>" \
  -F "file=@audio.flac"
  ```

  ```python fireworks sdk
  !pip install fireworks-ai requests python-dotenv

  from fireworks.client.audio import AudioInference
  import requests
  import os
  from dotenv import load_dotenv
  import time

  # Create a .env file with your API key
  load_dotenv()


  # Download audio sample
  audio = requests.get("https://tinyurl.com/4cb74vas").content

  # Prepare client
  client = AudioInference(
      model="whisper-v3",
      base_url="https://audio-prod.us-virginia-1.direct.fireworks.ai",
      # Or for the turbo version
      # model="whisper-v3-turbo",
      # base_url="https://audio-turbo.us-virginia-1.direct.fireworks.ai",
      api_key=os.getenv("FIREWORKS_API_KEY"),
  )

  # Make request
  start = time.time()
  r = await client.transcribe_async(audio=audio)
  print(f"Took: {(time.time() - start):.3f}s. Text: '{r.text}'")
  ```

  ```python Python (openai sdk)
  !pip install openai requests python-dotenv

  from openai import OpenAI
  import os
  import requests
  from dotenv import load_dotenv

  load_dotenv()

  client = OpenAI(
      base_url="https://audio-prod.us-virginia-1.direct.fireworks.ai/v1",
      api_key=os.getenv("FIREWORKS_API_KEY")
      )
  audio_file= requests.get("https://tinyurl.com/4cb74vas").content
  transcription = client.audio.transcriptions.create(
      model="whisper-v3",
      file=audio_file
  )
  print(transcription.text)
  ```
</RequestExample>

### Supported Languages

The following languages are supported for transcription:

<Accordion title="Language Code & Name">
  | Language Code | Language Name       |
  | ------------- | ------------------- |
  | en            | English             |
  | zh            | Chinese             |
  | de            | German              |
  | es            | Spanish             |
  | ru            | Russian             |
  | ko            | Korean              |
  | fr            | French              |
  | ja            | Japanese            |
  | pt            | Portuguese          |
  | tr            | Turkish             |
  | pl            | Polish              |
  | ca            | Catalan             |
  | nl            | Dutch               |
  | ar            | Arabic              |
  | sv            | Swedish             |
  | it            | Italian             |
  | id            | Indonesian          |
  | hi            | Hindi               |
  | fi            | Finnish             |
  | vi            | Vietnamese          |
  | he            | Hebrew              |
  | uk            | Ukrainian           |
  | el            | Greek               |
  | ms            | Malay               |
  | cs            | Czech               |
  | ro            | Romanian            |
  | da            | Danish              |
  | hu            | Hungarian           |
  | ta            | Tamil               |
  | no            | Norwegian           |
  | th            | Thai                |
  | ur            | Urdu                |
  | hr            | Croatian            |
  | bg            | Bulgarian           |
  | lt            | Lithuanian          |
  | la            | Latin               |
  | mi            | Maori               |
  | ml            | Malayalam           |
  | cy            | Welsh               |
  | sk            | Slovak              |
  | te            | Telugu              |
  | fa            | Persian             |
  | lv            | Latvian             |
  | bn            | Bengali             |
  | sr            | Serbian             |
  | az            | Azerbaijani         |
  | sl            | Slovenian           |
  | kn            | Kannada             |
  | et            | Estonian            |
  | mk            | Macedonian          |
  | br            | Breton              |
  | eu            | Basque              |
  | is            | Icelandic           |
  | hy            | Armenian            |
  | ne            | Nepali              |
  | mn            | Mongolian           |
  | bs            | Bosnian             |
  | kk            | Kazakh              |
  | sq            | Albanian            |
  | sw            | Swahili             |
  | gl            | Galician            |
  | mr            | Marathi             |
  | pa            | Punjabi             |
  | si            | Sinhala             |
  | km            | Khmer               |
  | sn            | Shona               |
  | yo            | Yoruba              |
  | so            | Somali              |
  | af            | Afrikaans           |
  | oc            | Occitan             |
  | ka            | Georgian            |
  | be            | Belarusian          |
  | tg            | Tajik               |
  | sd            | Sindhi              |
  | gu            | Gujarati            |
  | am            | Amharic             |
  | yi            | Yiddish             |
  | lo            | Lao                 |
  | uz            | Uzbek               |
  | fo            | Faroese             |
  | ht            | Haitian Creole      |
  | ps            | Pashto              |
  | tk            | Turkmen             |
  | nn            | Nynorsk             |
  | mt            | Maltese             |
  | sa            | Sanskrit            |
  | lb            | Luxembourgish       |
  | my            | Myanmar             |
  | bo            | Tibetan             |
  | tl            | Tagalog             |
  | mg            | Malagasy            |
  | as            | Assamese            |
  | tt            | Tatar               |
  | haw           | Hawaiian            |
  | ln            | Lingala             |
  | ha            | Hausa               |
  | ba            | Bashkir             |
  | jw            | Javanese            |
  | su            | Sundanese           |
  | yue           | Cantonese           |
  | zh-hant       | Traditional Chinese |
  | zh-hans       | Simplified Chinese  |
</Accordion>


--

# Create Batch Request

<CardGroup cols={1}>
  <Card title="Try notebook" icon="rocket" href="https://colab.research.google.com/github/fw-ai/cookbook/blob/main/learn/batch-api/batch_api.ipynb">
    Create a batch request for our audio transcription service
  </Card>
</CardGroup>

### Headers

<ParamField header="Authorization" type="string" required>
  Your Fireworks API key, e.g. `Authorization=FIREWORKS_API_KEY`. Alternatively, can be provided as a query param.
</ParamField>

### Path Parameters

<ParamField query="path" type="string" required>
  The relative route of the target API operation (e.g. `"v1/audio/transcriptions"`, `"v1/audio/translations"`). This should correspond to a valid route supported by the backend service.
</ParamField>

### Query Parameters

<ParamField query="endpoint_id" type="string" required>
  Identifies the target backend service or model to handle the request. Currently supported:

  * `audio-prod`: [https://audio-prod.us-virginia-1.direct.fireworks.ai](https://audio-prod.us-virginia-1.direct.fireworks.ai)
  * `audio-turbo`: [https://audio-turbo.us-virginia-1.direct.fireworks.ai](https://audio-turbo.us-virginia-1.direct.fireworks.ai)
</ParamField>

### Body

Request body fields vary depending on the selected `endpoint_id` and `path`.

The request body must conform to the schema defined by the corresponding synchronous API.\
For example, transcription requests typically accept fields such as `model`, `diarize`, and `response_format`.\
Refer to the relevant synchronous API for required fields:

* [Transcribe audio](https://docs.fireworks.ai/api-reference/audio-transcriptions)
* [Translate audio](https://docs.fireworks.ai/api-reference/audio-translations)

### Response

<Tabs>
  <Tab title="json">
    <ResponseField name="status" type="string" required>
      The status of the batch request submission.\
      A value of `"submitted"` indicates the batch request was accepted and queued for processing.
    </ResponseField>

    <ResponseField name="batch_id" type="string" required>
      A unique identifier assigned to the batch job.
      This ID can be used to check job status or retrieve results later.
    </ResponseField>

    <ResponseField name="account_id" type="string" required>
      The unique identifier of the account associated with the batch job.
    </ResponseField>

    <ResponseField name="endpoint_id" type="string" required>
      The backend service selected to process the request.\
      This typically matches the `endpoint_id` used during submission.
    </ResponseField>

    <ResponseField name="message" type="string" optional>
      A human-readable message describing the result of the submission.\
      Typically `"Request submitted successfully"` if accepted.
    </ResponseField>
  </Tab>
</Tabs>

<RequestExample>
  ```curl curl

  # Download audio file
  curl -L -o "audio.flac" "https://tinyurl.com/4997djsh"

  # Make request
  curl -X POST "https://audio-batch.link.fireworks.ai/v1/audio/transcriptions?endpoint_id=audio-prod" \
  -H "Authorization: <FIREWORKS_API_KEY>" \
  -F "file=@audio.flac"
  ```

  ```python python
  !pip install requests

  import os
  import requests

  # input API key and download audio
  api_key = "<FIREWORKS_API_KEY>"
  audio = requests.get("https://tinyurl.com/4cb74vas").content

  # Prepare request data
  url = "https://audio-batch.link.fireworks.ai/v1/audio/transcriptions?endpoint_id=audio-prod"
  headers = {"Authorization": api_key}
  payload = {
      "model": "whisper-v3",
      "response_format": "json"
  }
  files = {"file": ("audio.flac", audio, "audio/flac")}

  # Send request
  response = requests.post(url, headers=headers, data=payload, files=files)
  print(response.text)
  ```
</RequestExample>

To check the status of your batch request, use the [Check Batch Status](https://docs.fireworks.ai/api-reference/get-batch-status) endpoint with the returned `batch_id`.

--

# Check Batch Status

This endpoint allows you to check the current status of a previously submitted batch request, and retrieve the final result if available.

<CardGroup cols={1}>
  <Card title="Try notebook" icon="rocket" href="https://colab.research.google.com/github/fw-ai/cookbook/blob/main/learn/batch-api/batch_api.ipynb">
    Check status of your batch request
  </Card>
</CardGroup>

### Headers

<ParamField header="Authorization" type="string" required>
  Your Fireworks API key. e.g. `Authorization=FIREWORKS_API_KEY`. Alternatively, can be provided as a query param.
</ParamField>

### Path Parameters

<ParamField query="account_id" type="string" required>
  The identifier of your Fireworks account. Must match the account used when the batch request was submitted.
</ParamField>

<ParamField query="batch_id" type="string" required>
  The unique identifier of the batch job to check.\
  This should match the `batch_id` returned when the batch request was originally submitted.
</ParamField>

### Response

The response includes the status of the batch job and, if completed, the final result.

<Tabs>
  <Tab title="json">
    <ResponseField name="status" type="string" required>
      The status of the batch job at the time of the request.\
      Possible values include `"completed"` and `"processing"`.
    </ResponseField>

    <ResponseField name="batch_id" type="string" required>
      The unique identifier of the batch job whose status is being retrieved.\
      This ID matches the one provided in the original request.
    </ResponseField>

    <ResponseField name="message" type="string" optional>
      A human-readable message describing the current state of the batch job.\
      This field is typically `null` when the job has completed successfully.
    </ResponseField>

    <ResponseField name="content_type" type="string" optional>
      The original content type of the response body.\
      This value can be used to determine how to parse the string in the `body` field.
    </ResponseField>

    <ResponseField name="body" type="string" optional>
      The serialized result of the batch job, this field is only present when `status` is `"completed"`.\
      The format of this string depends on the `content_type` field and may vary across endpoints.\
      Clients should use `content_type` to determine how to parse or interpret the value.
    </ResponseField>
  </Tab>
</Tabs>

<RequestExample>
  ```curl curl
  # Make request
  curl -X GET "https://audio-batch.link.fireworks.ai/v1/accounts/{account_id}/batch_job/{batch_id}" \
  -H "Authorization: <FIREWORKS_API_KEY>"
  ```

  ```python python
  !pip install requests

  import os
  import requests

  # Input api key and path parameters
  api_key = "<FIREWORKS_API_KEY>"
  account_id = "<ACCOUNT_ID>"
  batch_id = "<BATCH_ID>"

  # Send request
  url = f"https://audio-batch.link.fireworks.ai/v1/accounts/{account_id}/batch_job/{batch_id}"
  headers = {"Authorization": api_key}

  response = requests.get(url, headers=headers)
  print(response.text)
  ```
</RequestExample>