---
tags: scripts>powershell, estudos
info: aberto.
date: 2025-01-04
type: post
layout: post
published: true
slug: doc2plan-to-jekyll-markdown-via-powershell
title: 'doc2plan to jekyll markdown via PowerShell'
---
{% codeblock powershell %}
Param(
    [Parameter(Mandatory = $true)]
    [string]$JsonFilePath,
    [Parameter(Mandatory = $true)]
    [string]$OutputMarkdownPath
)

# Function to adjust heading levels
function Adjust-Headings {
    Param(
        [string]$content,
        [int]$levelOffset
    )
    if ([string]::IsNullOrEmpty($content)) {
        return ''
    }

    $lines = $content -split "`n"
    $adjustedLines = foreach ($line in $lines) {
        if ($line -match '^(#{1,6})') {
            $hashes = $Matches[1]
            $newLevel = [Math]::Min($hashes.Length + $levelOffset, 6)
            $restOfLine = $line.Substring($hashes.Length)
            ('#' * $newLevel) + $restOfLine
        } else {
            $line
        }
    }
    return ($adjustedLines -join "`n")
}

# Function to process topics recursively
function Process-Topic {
    Param(
        [psobject]$topic,
        [int]$headingLevel
    )

    $output = ""

    try {
        # Sanitize the title to remove markdown formatting
        $title = $topic.title -replace '^[#*\-\s]*', ''   # Remove leading #, *, -, spaces
        $title = $title.Trim('*').Trim()                  # Remove asterisks and extra spaces

        # Create the heading for the topic
        $headingHashes = '#' * $headingLevel
        $output += "`n$headingHashes $title`n`n"

        $content = $topic.content

        if ([string]::IsNullOrEmpty($content)) {
            $adjustedContent = ''  # Set to empty string if content is null or empty
        }
        else {
            # Adjust content headings
            $adjustedContent = Adjust-Headings -content $content -levelOffset ($headingLevel - 1)
        }

        $output += $adjustedContent + "`n"

        # Process children recursively
        if ($topic.children -and $topic.children.Count -gt 0) {
            foreach ($child in $topic.children) {
                $childOutput = Process-Topic -topic $child -headingLevel ($headingLevel + 1)
                $output += $childOutput
            }
        }
    }
    catch {
        Write-Error "Error processing topic '$($topic.title)': $_"
    }

    return $output
}

# Main script execution
try {
    # Read the JSON data
    $JsonData = Get-Content -Raw -Path $JsonFilePath | ConvertFrom-Json

    # Initialize output content
    $markdownContent = ""

    # Create front matter
    $frontMatter = "---`n"
    $frontMatter += "title: '$($JsonData.name)'`n"
    $frontMatter += "layout: default`n"
    $frontMatter += "---`n`n"

    $markdownContent += $frontMatter

    # Include keyTopics if available
    if ($JsonData.keyTopics) {
        $keyTopicsContent = Adjust-Headings -content $JsonData.keyTopics -levelOffset 0
        $markdownContent += $keyTopicsContent + "`n"
    }

    # Process chapters
    $chapters = $JsonData.chapters
    foreach ($chapter in $chapters) {
        # Sanitize chapter name
        $chapterName = $chapter.name -replace '^[#*\-\s]*', ''   # Remove leading #, *, -, spaces
        $chapterName = $chapterName.Trim('*').Trim()             # Remove asterisks and extra spaces

        $markdownContent += "`n## $chapterName`n`n"

        # Adjust headings in chapter content if needed (if chapter has content)
        if ($chapter.content) {
            $adjustedChapterContent = Adjust-Headings -content $chapter.content -levelOffset 1
            $markdownContent += $adjustedChapterContent + "`n"
        }

        # Process topics within the chapter
        if ($chapter.topics) {
            foreach ($topic in $chapter.topics) {
                $topicOutput = Process-Topic -topic $topic -headingLevel 3
                $markdownContent += $topicOutput
            }
        }
    }

    # Write the combined markdown content to the output file
    Set-Content -Path $OutputMarkdownPath -Value $markdownContent -Encoding UTF8

    Write-Host "Markdown file has been created at $OutputMarkdownPath"
}
catch {
    Write-Error "An error occurred: $_"
}
{% endcodeblock %}
