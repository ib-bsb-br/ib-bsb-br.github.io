---
tags:
  - scripts>powershell, software>windows
info: aberto.
date: 2024-09-12
type: post
layout: post
published: true
slug: urls-list-text-scraper
title: 'URLs list text scraper'
---

Reference: `https://github.com/kitsuyui/scraper`

To download the text content of multiple URLs from a list on Windows 11, we'll create a PowerShell script that's more robust and flexible than the previously suggested batch file. This approach leverages PowerShell's strengths and provides better error handling and output formatting.

1. First, ensure you have `scraper.exe` set up:
   - Download the latest Windows executable from https://github.com/kitsuyui/scraper/releases/latest
   - Rename it to `scraper.exe` and place it in a directory that's in your system PATH

2. Create a file named `scraper-config.json` with the following content:
   ```json
   [
     {"type": "xpath", "label": "BodyText", "query": "//body//text()"}
   ]
   ```

3. Create a text file named `urls.txt` with one URL per line:
   ```
   https://example.com
   https://another-example.com
   https://third-example.com
   ```

4. Create a new file named `Scrape-Urls.ps1` with the following PowerShell script:

   ```powershell
   # Scrape-Urls.ps1
   param(
       [string]$UrlFile = "urls.txt",
       [string]$ConfigFile = "scraper-config.json",
       [string]$OutputDir = "scraped_content"
   )

   # Ensure the output directory exists
   New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

   # Read URLs from file
   $urls = Get-Content $UrlFile

   foreach ($url in $urls) {
       try {
           Write-Host "Processing: $url"
           
           # Generate a safe filename
           $filename = ($url -replace "https?://", "" -replace "[^a-zA-Z0-9]+", "_") + ".txt"
           $outputPath = Join-Path $OutputDir $filename

           # Download and scrape content
           $content = Invoke-WebRequest -Uri $url -UseBasicParsing | Select-Object -ExpandProperty Content
           $scrapedContent = $content | & scraper -c $ConfigFile | ConvertFrom-Json

           # Extract text from JSON and save
           $bodyText = $scrapedContent | Where-Object { $_.label -eq "BodyText" } | Select-Object -ExpandProperty results
           $bodyText -join " " | Out-File -FilePath $outputPath

           Write-Host "Saved to: $outputPath"
       }
       catch {
           Write-Host "Error processing $url : $_" -ForegroundColor Red
       }
       Write-Host
   }

   Write-Host "All URLs processed." -ForegroundColor Green
   ```

5. Open PowerShell and navigate to the directory containing your script and files.

6. Run the script:
   ```powershell
   .\Scrape-Urls.ps1
   ```

This improved solution offers several advantages:

- It uses PowerShell, which is more powerful and flexible than batch scripts on Windows.
- It includes error handling to manage issues with individual URLs without stopping the entire process.
- It creates a separate output directory for scraped content, keeping things organized.
- It generates safe filenames based on the URLs, avoiding potential naming conflicts or invalid characters.
- It extracts the actual text content from the JSON output, providing clean text files.
- It's more customizable, allowing you to specify different input files, config files, or output directories.

Additional notes:

1. This script respects rate limiting by processing URLs sequentially. For a large number of URLs, consider adding a delay between requests.

2. Some websites may block or behave differently with automated requests. You might need to add user-agent headers or other modifications for certain sites:

   ```powershell
   $headers = @{
       "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
   }
   $content = Invoke-WebRequest -Uri $url -UseBasicParsing -Headers $headers | Select-Object -ExpandProperty Content
   ```

3. Always ensure you have permission to scrape the websites you're targeting and that you're complying with their terms of service and robots.txt files.

4. For very large lists of URLs, consider implementing parallel processing or breaking the list into smaller batches to improve efficiency.

5. You may want to add more robust URL validation and error checking, depending on your specific needs and the reliability of your URL list.