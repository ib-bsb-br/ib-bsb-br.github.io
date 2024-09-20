---
title: tampermonkey dify hit-testing [script]
date: 2024-02-18 00:00:00 -03:00
categories:
- Code
tags:
- scripts
comment: https://cloud.dify.ai/
info: fechado.
type: post
layout: post
---

```
// ==UserScript==
// @name         Delayed API Request and Download for Multiple Queries
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Automatically make API requests for multiple queries with delays and download responses
// @match        https://cloud.dify.ai/datasets/2ca8dd6b-6c29-4d0d-86e0-2219d8f84a6d/hitTesting
// @grant        GM_download
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    // Define the API endpoint
    const apiEndpoint = "https://cloud.dify.ai/console/api/datasets/2ca8dd6b-6c29-4d0d-86e0-2219d8f84a6d/hit-testing";

    // Define the headers and body of the request
    const headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Bearer <!-- placeholder -->",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    };

    // Define your queries
    const queries = [
        {"content": "<!-- placeholder -->"},
        {"content": "<!-- placeholder -->"}
    ];

    // Function to make the API request and download the response
    function makeApiRequestAndDownload(query, index) {
        const body = JSON.stringify({
            "query": query.content, // Adjusted to use the "content" key
            "retrieval_model": {
            "search_method": "hybrid_search",
            "reranking_enable": false,
            "reranking_model": {
                "reranking_provider_name": "cohere",
                "reranking_model_name": "rerank-english-v2.0"
            },
            "top_k": 10,
            "score_threshold_enabled": false,
            "score_threshold": 0.33
        }
        });

        GM_xmlhttpRequest({
            method: "POST",
            url: apiEndpoint,
            headers: headers,
            data: body,
            onload: function(response) {
                const filename = `api-response-${index}.json`;
                const blob = new Blob([response.responseText], {type: "application/json"});
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            }
        });
    }

    // Iterate over each query with a delay
    queries.forEach((query, index) => {
        setTimeout(() => {
            makeApiRequestAndDownload(query, index);
        }, 7000 * index); // 7000 ms delay between each request
    });
})();
```
