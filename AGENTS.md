The AI ASSISTANT must ground its responses exclusively within the following data/information/knowledge:

````jekyll-garden-jekyll-garden.github.io
~~~
Directory structure:
└── jekyll-garden-jekyll-garden.github.io/
    ├── README.md
    ├── _config.yml
    ├── autocomplete.txt
    ├── blog.code-workspace
    ├── debug.yml
    ├── docker-compose.yml
    ├── Dockerfile
    ├── Gemfile
    ├── LICENSE
    ├── SearchData.json
    ├── _includes/
    │   ├── Backlinks.html
    │   ├── Content.html
    │   ├── Feed.html
    │   ├── Footer.html
    │   ├── Nav.html
    │   └── Search.html
    ├── _layouts/
    │   ├── Post.html
    │   └── Stylesheet.html
    ├── _notes/
    │   └── Public/
    │       ├── Customization.md
    │       ├── Deployment.md
    │       ├── Getting Started.md
    │       ├── Markdown Guide.md
    │       ├── Obsidian Setup.md
    │       ├── Theme Features.md
    │       └── Wiki Links.md
    ├── _posts/
    │   └── 2024-01-15-welcome-to-jekyll-garden.md
    ├── assets/
    │   ├── css/
    │   │   ├── fruity.css
    │   │   └── style.css
    │   └── js/
    │       └── Search.js
    ├── pages/
    │   ├── 404.md
    │   ├── about.md
    │   ├── blog.md
    │   ├── Credits.md
    │   ├── index.md
    │   └── notes.md
    └── utilities/
        └── Autocomplete.ts

================================================
FILE: README.md
================================================
# Jekyll Garden
![screenshot](https://github.com/user-attachments/assets/f5752b1a-eb11-4385-a2ad-09f0e698ad30)
A simple Jekyll theme that turns your Obsidian notes into a beautiful website. Perfect for sharing your thoughts and knowledge online. If you use Obsidian for note-taking, this theme makes it easy to publish your markdown files as a connected website with wiki-style links and full-text search.


### What it does

Jekyll Garden connects your notes together with simple `[[note title]]` links, just like in Obsidian. You can find any note quickly with the built-in search that works as you type. The design focuses on your content with a clean, minimal look that works great on phones, tablets, and computers. Choose between dark and light themes, and when you want to write traditional blog posts, you can do that too. The theme also supports mathematical expressions if you need to write equations.

## Getting Started

Getting started is straightforward. First, download this theme to your computer. Then edit the settings in the `_config.yml` file with your website information. Add your notes to the `_notes` folder, and finally deploy to GitHub Pages, Netlify, or any web hosting service.

## Basic Setup

Edit `_config.yml` with your information:

```yaml
title: "My Website"
heading: "Your Name"
description: "A brief description of your site"
url: "https://yoursite.com"
```

### Deployment Options

You can deploy your site to a subdomain (like `notes.yoursite.com`) or a subdirectory (like `yoursite.com/notes`):

**For subdomains:**
```yaml
url: "https://notes.yoursite.com"
baseurl: ""
```

**For subdirectories:**
```yaml
url: "https://yoursite.com"
baseurl: "/notes"
```

See `SUBDOMAIN_SETUP.md` for more details.

## Writing Notes

### Creating a Note

Each note is just a markdown file with a title. You write your content in markdown format, just like you would in Obsidian or any other markdown editor.

```yaml
---
title: "My First Note"
date: 2025-01-15
---
```

## Features

### Linking Notes Together
Connect your notes by using `[[note title]]` to link to other notes. This creates the same kind of connections you're used to in Obsidian, but now they work on your website too.


### Simple Linking
The linking system works just like Obsidian. Write `[[note title]]` and the links are created automatically. When you hover over a link, you'll see a preview of the connected note.

### Search
Finding content is easy with the built-in search. It searches through all your notes instantly as you type, looking at both titles and content to help you find exactly what you need.

### Backlinks
See which notes link to the current one you're reading. This helps you discover related content and explore the connections between your ideas, just like the backlinks feature in Obsidian.

### Math
If you need to write mathematical expressions, the theme supports it. Use `$x = y$` for inline math and `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$` for complex equations.

## How to Publishing Your Site

### GitHub Pages (Free)
GitHub Pages is the easiest way to get started. Upload your files to GitHub, enable GitHub Pages in the repository settings, and your site goes live automatically.

### Netlify (Free)
Netlify is another great option. Connect your GitHub repository to Netlify, and it will build and host your site. Every time you update your files, your site updates automatically.

### Local Testing
Test your site locally before publishing. Run `bundle install` to install dependencies, then `bundle exec jekyll serve` to start a local server and see your site in action.

### Customization
Change the look of your site by editing the `assets/css/style.css` file. You can modify colors, fonts, and other visual elements to match your preferences. If you want to customize the layout, you can modify files in the `_layouts/` folder. Add your own CSS and JavaScript as needed, but remember to keep it simple.

## Contributing
Found a bug or have an idea for improvement? Contributions are welcome. Fork the repository, make your changes, and submit a pull request.

## License

MIT License - use it freely for any project.



================================================
FILE: _config.yml
================================================
# Welcome to Jekyll!
#
# This config file is meant for settings that affect your whole blog, values
# which you are expected to set up once and rarely edit after that. If you find
# yourself editing this file very often, consider using Jekyll's data files
# feature for the data you need to update frequently.
#
# For technical reasons, this file is *NOT* reloaded automatically when you use
# 'bundle exec jekyll serve'. If you change this file, please restart the server process.
#
# If you need help with YAML syntax, here are some quick references for you: 
# https://learn-the-web.algonquindesign.ca/topics/markdown-yaml-cheat-sheet/#yaml
# https://learnxinyminutes.com/docs/yaml/
#
# Site settings
# These are used to personalize your new site. If you look in the HTML files,
# you will see them accessed via {{ site.title }}, {{ site.email }}, and so on.
# You can create any custom variable you would like, and they will be accessible
# in the templates via {{ site.myvariable }}.

# Jekyll Garden Configuration
# Optimized for actual template usage

# Preferences (controls template behavior)
preferences:
  homepage:
    enabled: false
  search:
    enabled: true
  backlinks:
    enabled: true
  pagepreview:
    enabled: true
  wiki_style_link:
    enabled: true

# Site Configuration
title: "Your Site Title"
heading: "Your Name"
description: "A brief description of your site"
url: "https://yoursite.com"
baseurl: ""

# Asset Configuration
apple_touch_icon: "/assets/img/profile.png"
css_file: "/assets/css/style.css"
ie_css: "/assets/css/ie-target.css"

# Menu Items
menu:
  - title: "Notes"
    url: "/notes"
  - title: "Blog"
    url: "/blog"
  - title: "About"
    url: "/about"

# Footer
footer:
  copyright: "© 2024 Your Name. Contents under CC-BY-NC"
  credits:
    enabled: true
    url: "/credits"
    text: "Credits"

# Collections
collections:
  notes:
    output: true
    permalink: /:collection/:name

# Defaults
defaults:
  - scope:
      path: ""
      type: "notes"
    values:
      layout: "Post"
      content-type: "notes"
      feed: "show"
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "Post"
      content-type: "post"
      feed: "show"
      permalink: /blog/:title/

# Plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap

# Private links (for broken wiki links)
privatelinks:
  title: "Private Note"
  msg: "This note hasn't been published yet."

# Math rendering
katex: true

# Exclude from processing
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor/bundle/
  - vendor/cache/
  - vendor/gems/
  - vendor/ruby/


================================================
FILE: autocomplete.txt
================================================
---
---

{%- for post in site.posts -%}
{{ post.title | strip_html | escape }}{% unless foorloop.last %};{% endunless %}
{%- endfor -%}



================================================
FILE: blog.code-workspace
================================================
{
	"folders": [
		{
			"path": "."
		}
	],
	"settings": {
		"browser-preview.startUrl": "localhost:4000",
		"editor.fontSize": 12,
		"editor.fontFamily": "'Source Code Pro', 'Fira Code', Consolas, 'Courier New', monospace"
	}
}


================================================
FILE: debug.yml
================================================
name: Jekyll-Garden [DEBUG MODE]
debug: true
baseurl: ""
url: http://127.0.0.1:4000


================================================
FILE: docker-compose.yml
================================================
version: "3"

networks:
  jekyll:
    external: false

services:
  garden:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: jekyll
    restart: always
    networks:
      - jekyll
    volumes:
      - ./_posts:/usr/src/app/_posts
      - ./_notes:/usr/src/app/_notes
      - ./assets:/usr/src/app/assets
      - ./pages:/usr/src/app/pages
    ports:
      - "4000:4000"




================================================
FILE: Dockerfile
================================================
FROM ruby:3.1.1-alpine3.15

RUN apk add --no-cache build-base nodejs-current

RUN gem install bundler

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]

EXPOSE 4000




================================================
FILE: Gemfile
================================================
source "https://rubygems.org"
# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
gem "jekyll", "~> 4.0.0"
# This is the default theme for new Jekyll sites. You may change this to anything you like.
# gem "minima", "~> 2.5"
# If you want to use GitHub Pages, remove the "gem "jekyll"" above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
# gem "github-pages", group: :jekyll_plugins
# If you have any plugins, put them here!
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.12"
  gem "jekyll-tidy"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
install_if -> { RUBY_PLATFORM =~ %r!mingw|mswin|java! } do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :install_if => Gem.win_platform?

gem 'jekyll-sitemap'
gem 'kramdown-math-katex'

gem "webrick", "~> 1.7"


================================================
FILE: LICENSE
================================================
MIT License

Copyright (c) 2021 Jekyll-Garden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



================================================
FILE: SearchData.json
================================================
---
permalink: /SearchData.json
---

{
  {%- assign i = 0 -%}
  {%- for note in site.notes -%}

    "{{ i }}": {
       "doc":  {{ note.title | strip_html | escape | jsonify }},
       "title": {{ note.title | strip_html | escape | jsonify }},
       "content": {{ note.content | replace: '</h', ' . </h' | replace: '<hr', ' . <hr' | replace: '</p', ' . </p' | replace: '<ul', ' . <ul' | replace: '</ul', ' . </ul' | replace: '<ol', ' . <ol' | replace: '</ol', ' . </ol' | replace: '</tr', ' . </tr' | replace: '<li', ' | <li' | replace: '</li', ' | </li' | replace: '</td', ' | </td' | replace: '<td', ' | <td' | replace: '</th', ' | </th' | replace: '<th', ' | <th' | strip_html | remove: 'Table of contents' | normalize_whitespace | replace: '. . .', '.' | replace: '. .', '.' | replace: '| |', '|' | append: ' ' | strip_html | strip_newline | strip | escape | jsonify }},
       "url": "{{ site.baseurl }}{{ note.url }}"
    }{%- unless forloop.last -%},{%- endunless -%}{%- assign i = i | plus: 1 -%}
    
  {% endfor %}
}


================================================
FILE: _includes/Backlinks.html
================================================
{%- assign link_count = 0 -%}
{%- assign wiki_link_title = '[' | append: page.title | append: ']' -%}
{%- for note in site.notes -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
                {%- assign link_count = link_count | plus:1 -%}
            {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{%- for note in site.posts -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
                {%- assign link_count = link_count | plus:1 -%}
            {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{%- for note in site.pages -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
                {%- assign link_count = link_count | plus:1 -%}
            {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{%- if link_count > 0 -%}
{%- assign wiki_link_title = '[' | append: page.title | append: ']' -%}
{%- assign display_class = 'hide' -%}
{%- if site.preferences.backlinks.enabled -%}
{%- assign display_class = 'show' -%}
{%- endif -%}
<div class="links-section {{display_class}}" id="jekyll-seamless-backlinks">
    <h6>Links to this note</h6>
    <ul class="links-grid">
        {%- for note in site.notes -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
            <li><a href="{{ site.baseurl }}{{note.url}}">{{ note.title }}</a></li>
            {%- endif -%}
        {%- endif -%}
        {%- endfor -%}
        {%- for note in site.posts -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
            <li><a href="{{ site.baseurl }}{{note.url}}">{{ note.title }}</a></li>
            {%- endif -%}
        {%- endif -%}
        {%- endfor -%}
        {%- for note in site.pages -%}
        {%- if note.url != page.url -%}
            {%- if note.content contains wiki_link_title -%}
            <li><a href="{{ site.baseurl }}{{note.url}}">{{ note.title }}</a></li>
            {%- endif -%}
        {%- endif -%}
        {%- endfor -%}
    </ul>
</div>
{%- endif -%}



================================================
FILE: _includes/Content.html
================================================
<div class="content">
    {{ content | markdownify }}
</div>

<script>
// Process wiki links after page load, excluding code blocks
document.addEventListener('DOMContentLoaded', function() {
    const contentDiv = document.querySelector('.content');
    if (!contentDiv) return;
    
    // Get all available notes for link resolution
    const availableNotes = [
        {%- for note in site.notes -%}
            {
                title: "{{ note.title | escape }}",
                url: "{{ site.baseurl }}{{ note.url }}",
                excerpt: "{{ note.content | strip_html | normalize_whitespace | truncatewords: 20 | escape }}"
            }{%- unless forloop.last -%},{%- endunless -%}
        {%- endfor -%}
    ];
    
    // Function to find note by title (case-insensitive)
    function findNoteByTitle(title) {
        return availableNotes.find(note => 
            note.title.toLowerCase() === title.toLowerCase()
        );
    }
    
    // Function to process wiki links in text nodes only
    function processWikiLinks(node) {
        if (node.nodeType === Node.TEXT_NODE) {
            // Only process text nodes that are not inside code elements
            let parent = node.parentElement;
            while (parent) {
                if (parent.tagName === 'CODE' || parent.tagName === 'PRE' || 
                    parent.classList.contains('highlighter-rouge') || 
                    parent.classList.contains('highlight')) {
                    return; // Skip if inside code
                }
                parent = parent.parentElement;
            }
            
            // Process wiki links in this text node
            const text = node.textContent;
            const wikiLinkRegex = /\[\[([^\]]+)\]\]/g;
            let match;
            let lastIndex = 0;
            const fragments = [];
            
            while ((match = wikiLinkRegex.exec(text)) !== null) {
                // Add text before the match
                if (match.index > lastIndex) {
                    fragments.push(document.createTextNode(text.slice(lastIndex, match.index)));
                }
                
                const linkText = match[1];
                const linkSpan = document.createElement('span');
                
                // Check if it's an external link (contains ::)
                if (linkText.includes('::')) {
                    const [title, url] = linkText.split('::');
                    const link = document.createElement('a');
                    link.href = url;
                    link.target = '_blank';
                    link.rel = 'noopener';
                    link.textContent = title;
                    linkSpan.appendChild(link);
                } else {
                    // Internal link - try to find the note
                    const foundNote = findNoteByTitle(linkText);
                    const link = document.createElement('a');
                    
                    if (foundNote) {
                        link.href = foundNote.url;
                        link.textContent = linkText;
                        link.className = 'wiki-link';
                        
                        // Add hover preview functionality
                        link.addEventListener('mouseenter', function() {
                            showPreview(this, foundNote.title, foundNote.excerpt);
                        });
                        
                        link.addEventListener('mouseleave', function() {
                            hidePreview();
                        });
                    } else {
                        // Note doesn't exist - create a placeholder
                        link.href = 'javascript:void(0)';
                        link.textContent = linkText;
                        link.className = 'stale-link';
                        link.title = 'Note not found: ' + linkText;
                    }
                    
                    linkSpan.appendChild(link);
                }
                
                fragments.push(linkSpan);
                lastIndex = match.index + match[0].length;
            }
            
            // Add remaining text
            if (lastIndex < text.length) {
                fragments.push(document.createTextNode(text.slice(lastIndex)));
            }
            
            // Replace the text node with fragments if we found wiki links
            if (fragments.length > 0) {
                const parent = node.parentNode;
                fragments.forEach(fragment => parent.insertBefore(fragment, node));
                parent.removeChild(node);
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // Recursively process child nodes
            const children = Array.from(node.childNodes);
            children.forEach(child => processWikiLinks(child));
        }
    }
    
    // Function to show hover preview
    function showPreview(link, title, excerpt) {
        // Remove any existing preview
        hidePreview();
        
        const preview = document.createElement('div');
        preview.className = 'link-preview';
        preview.innerHTML = `
            <div class="preview-content">
                <strong>${title}</strong>
                <p>${excerpt}</p>
            </div>
        `;
        
        document.body.appendChild(preview);
        
        // Position the preview near the link
        const rect = link.getBoundingClientRect();
        preview.style.position = 'fixed';
        preview.style.left = rect.left + 'px';
        preview.style.top = (rect.bottom + 5) + 'px';
        preview.style.zIndex = '1000';
    }
    
    // Function to hide hover preview
    function hidePreview() {
        const existingPreview = document.querySelector('.link-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
    }
    
    // Process all nodes in the content
    processWikiLinks(contentDiv);
});
</script> 


================================================
FILE: _includes/Feed.html
================================================
<!-- feed with filter-->
<div class="related-wrapper">
{% assign note_items = site.notes | sort: "date" | reverse %}
{% for note_items in note_items %}
    {%- if note_items.feed == "show" -%}
            <div class="notelist-feed">
                <a href="{{ site.baseurl }}{{note_items.url}}">
                    <p>{{ note_items.title }}</p>
                </a>
            </div>
    {%- endif -%}
{%- endfor -%}
</div>


================================================
FILE: _includes/Footer.html
================================================
<div class="footer">
  <div class="footer-left">
    <h6>
      {{ site.footer.copyright }}
      {%- if site.footer.credits.enabled -%}
          • <a href="{{ site.baseurl }}{{ site.footer.credits.url }}">{{ site.footer.credits.text }}</a>
      {%- endif -%}
    </h6>
  </div>
  <div class="footer-right">
    <button class="theme-toggle" aria-label="Toggle dark mode" title="Toggle dark mode">
      <svg viewBox="0 0 14 14" width="14" height="14" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <circle cx="7" cy="7" r="5"/>
      </svg>
    </button>
  </div>
</div>

<script>
  // Theme toggle
  const themeToggle = document.querySelector('.theme-toggle');
  const root = document.documentElement;
  const body = document.body;
  
  function setTheme(theme) {
    root.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }
  
  // Initial theme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    setTheme(savedTheme);
  }
  
  themeToggle.addEventListener('click', function() {
    root.classList.add('theme-transition');
    body.classList.add('theme-transition');
    
    const isDark = root.getAttribute('data-theme') === 'dark';
    setTheme(isDark ? 'light' : 'dark');
  });
</script>


================================================
FILE: _includes/Nav.html
================================================
<nav class="nav">
  <div class="nav-left">
    <a href="{{ site.baseurl }}/">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="8" width="16" height="16" rx="4" />
      </svg>
    </a>
  </div>
  
  <div class="nav-right">
    <div class="dropdown">
      <div class="hamburger">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 6H21M3 12H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="dropdown-menu">
        {%- if site.menu -%}
          {%- for item in site.menu -%}
            <a href="{{ site.baseurl }}{{ item.url }}">{{ item.title }}</a>
          {%- endfor -%}
        {%- else -%}
          <a href="{{ site.baseurl }}/">About</a>
          <a href="{{ site.baseurl }}/notes">Notes</a>
          <a href="{{ site.baseurl }}/about">About</a>
        {%- endif -%}
      </div>
    </div>
  </div>
</nav>

<script>
  const hamburger = document.querySelector('.hamburger');
  const dropdown = document.querySelector('.dropdown');
  
  hamburger.addEventListener('click', function(e) {
    e.stopPropagation();
    this.classList.toggle('active');
    dropdown.classList.toggle('active');
  });
  
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
      hamburger.classList.remove('active');
      dropdown.classList.remove('active');
    }
  });
</script>


================================================
FILE: _includes/Search.html
================================================
{%- if site.preferences.search.enabled -%}
    <!-- search bar -->
    <div class="search-container">
        <input class="search-input" type="text" placeholder="Search Notes..." id="search-input" autocomplete="off">
        <div id="search-results" class="search-results"></div>
    </div>
    <script type="text/javascript" src="{{ site.baseurl }}/assets/js/vendor/lunr.min.js"></script>
    <script src="{{ site.baseurl }}/assets/js/Search.js"></script>
{%- endif -%} 


================================================
FILE: _layouts/Post.html
================================================
<!DOCTYPE html>
<html lang="en">

<head>
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <meta content="{{ site.title | default: site.heading }}" property="og:site_name" />
    <meta content="{{ site.description | default: 'A Jekyll Garden site' }}" property="og:description">
    <meta content="{{ site.url }}/about/" property="article:author">
    {%- if site.og_image -%}
    <meta property="og:image" content="{{ site.baseurl }}{{ site.og_image }}">
    {%- endif -%}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    {%- if page.title -%}
    <meta content="{{ page.title }}" property="og:title">
    <meta content="article" property="og:type">
    <meta content="{{ site.url }}{{ page.url }}" property="og:url">
    {%- else -%}
    <meta content="website" property="og:type">
    <meta content="{{ site.url }}{{ page.url }}" property="og:url">
    {%- endif -%}

    <title>{%- if page.title -%}{{ page.title }} - {%- endif -%}{{ site.heading }}</title>
    <link rel="canonical" href="{{site.url}}{{page.url}}" />
    {%- if site.apple_touch_icon -%}
    <link rel="apple-touch-icon" href="{{ site.baseurl }}{{ site.apple_touch_icon }}">
    {%- endif -%}
    {%- if site.favicon -%}
    <link rel="icon" href="{{ site.baseurl }}{{ site.favicon }}" type="image/svg+xml" sizes="any" />
    {%- endif -%}
    {%- if site.css_file -%}
    <link href="{{ site.baseurl }}{{ site.css_file }}" rel="stylesheet" media="all" class="default" />
    {%- else -%}
    <link href="{{ site.baseurl }}/assets/css/style.css" rel="stylesheet" media="all" class="default" />
    {%- endif -%}
    {%- if site.katex -%}
    <link href="{{ site.baseurl }}/assets/css/vendor/Katex.css" rel="stylesheet" media="all" class="default" />
    {%- endif -%}

    <!--[if IE]>
        {%- if site.ie_css -%}
        <link href="{{ site.baseurl }}{{ site.ie_css }}" rel="stylesheet" type="text/css"/>
        {%- else -%}
        <link href="{{ site.baseurl }}/assets/css/ie-target.css" rel="stylesheet" type="text/css"/>
        {%- endif -%}
    <![endif]-->
    <!--<link href="/assets/css/prism.css" rel="stylesheet" />-->
    <link rel="alternate" type="application/rss+xml" href="{{ site.url }}/feed.xml">
</head>

<body>
    <div class="container">
        <div>
            {%- include Nav.html -%}
            
            <!-- Homepage Layout-->
            {%- if page.permalink == "/" -%}
                {%- if site.preferences.homepage.enabled -%}
                    <!--- Show content from index.md when homepage is enabled -->
                    {%- include Content.html -%}
                {%- else -%}
                    <!--- Show content from notes.md + search + feed when homepage is disabled -->
                    <h1>{{page.title}}</h1>
                    {%- include Content.html -%}
                    {%- include Search.html -%}
                    {%- include Feed.html -%}
                {%- endif -%}
            {%- endif -%}

            <!--- Notes Feed Layout-->
            {%- if page.permalink == "/notes" -%}
                <h1>{{page.title}}</h1>
                {%- include Content.html -%}
                {%- include Search.html -%}
                {%- include Feed.html -%}
            {%- endif -%}

            <!--- Notes Layout-->
            {%- if page.content-type == "notes" -%}
                <h1>{{page.title}}</h1>
                {%- include Content.html -%}
                {%- if site.preferences.backlinks.enabled -%}
                {%- include Backlinks.html -%}
                {%- endif -%}
            {%- endif -%}

             <!--- Post Layout-->
             {%- if page.content-type == "post"  -%}
                 <h1>{{page.title}}</h1>
                 {%- include Content.html -%}
                 {%- if site.preferences.backlinks.enabled -%}
                 {%- include Backlinks.html -%}
                 {%- endif -%}
             {%- endif -%}

            <!--- Static Page Layout-->
            {%- if page.content-type == "static" -%}
                <h1>{{page.title}}</h1>                        
                {%- include Content.html -%}
            {%- endif -%}
            
            <!--- Blog Feed Layout-->
            {%- if page.permalink == "/blog" -%}
                <div class="related-wrapper">
                {% assign post_items = site.posts | sort: "date" | reverse %}
                {% for post_items in post_items %}
                    {%- if post_items.feed == "show" -%}
                            <div class="notelist-feed">
                                <a href="{{ site.baseurl }}{{post_items.url}}">
                                    <p>{{ post_items.title }}</p>
                                </a>
                            </div>
                    {%- endif -%}
                {%- endfor -%}
                </div>
            {%- endif -%}

            {%- include Footer.html -%}
        </div>
    </div>
</body>
</html> 


================================================
FILE: _layouts/Stylesheet.html
================================================
---
layout: none
---
{{ content | scssify }}



================================================
FILE: _notes/Public/Customization.md
================================================
---
title: Customization
feed: show
date: 2024-01-15
---

You can customize your Jekyll Garden site by editing a few key files.

## Basic Settings

Edit `_config.yml` to change your site information:

```yaml
title: "My Digital Garden"
heading: "Your Name"
description: "A brief description of your site"
url: "https://yoursite.com"
```

## Menu Items

Add or change navigation menu items:

```yaml
menu:
  - title: "Notes"
    url: "/notes"
  - title: "About"
    url: "/about"
  - title: "Blog"
    url: "/blog"
```

## Theme Preferences

Control which features are enabled:

```yaml
preferences:
  homepage:
    enabled: true      # Show custom homepage
  search:
    enabled: true      # Enable search
  backlinks:
    enabled: true      # Show backlinks
```

## Colors and Fonts

Change the look by editing `assets/css/style.css`:

```css
:root {
  --primary-color: #007acc;
  --text-color: #333;
  --background-color: #fff;
  --font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}
```

## Dark Mode

The theme includes automatic dark mode support. Users can toggle between light and dark themes, and their preference is saved.

## Custom Fonts

Add custom fonts by importing them in the CSS:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

:root {
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

## Layout Changes

For advanced customization, you can modify files in the `_layouts/` folder. But remember to keep it simple - focus on content over complex styling.

## Tips

- Start with basic settings in `_config.yml`
- Test changes locally before deploying
- Keep customization minimal for better performance
- Use the [[Deployment]] guide when you're ready to publish

---

*Customization should enhance your content, not distract from it.* 


================================================
FILE: _notes/Public/Deployment.md
================================================
---
title: Deployment
feed: show
date: 2024-01-15
---

Once you've set up your Jekyll Garden site, here's how to publish it online.

## GitHub Pages (Free)

GitHub Pages is the easiest way to get started:

1. **Upload your files** to a GitHub repository
2. **Enable GitHub Pages** in repository settings
3. **Set source** to "Deploy from a branch"
4. **Choose your main branch** (usually `main` or `master`)

Your site will be available at `https://yourusername.github.io/repository-name`

## Netlify (Free)

Netlify offers automatic deployments:

1. **Connect your GitHub repository** to Netlify
2. **Set build command**: `bundle exec jekyll build`
3. **Set publish directory**: `_site`
4. **Deploy automatically** when you push changes

## Vercel (Free)

Vercel is another great option:

1. **Import your repository** to Vercel
2. **Framework preset**: Jekyll
3. **Deploy automatically** on every push

## Local Testing

Test your site before deploying:

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000` to see your site.

## Custom Domain

Add your own domain in `_config.yml`:

```yaml
url: "https://yourdomain.com"
```

Then configure your domain with your hosting provider.

## Tips

- **Test locally first**: Make sure everything works before deploying
- **Check your links**: Ensure all [[Wiki Links]] work correctly
- **Optimize images**: Compress images for faster loading
- **Use HTTPS**: Most hosting providers offer this automatically

## Troubleshooting

**Site not updating?**
- Check that your changes are pushed to the repository
- Verify the build completed successfully
- Clear your browser cache

**Broken links?**
- Ensure all note titles match exactly
- Check that notes have `feed: "show"` in front matter
- Rebuild your site after adding new notes

---

*Your digital garden is ready to share with the world!* 


================================================
FILE: _notes/Public/Getting Started.md
================================================
---
title: Getting Started
feed: show
date: 2024-01-15
---

Jekyll Garden makes it easy to turn your Obsidian notes into a website. Here's how to get started:

## Quick Setup

1. **Download this theme** to your computer
2. **Add your notes** to the `_notes` folder (each note is a markdown file)
3. **Edit `_config.yml`** to set your site's title and information
4. **Deploy** to GitHub Pages or Netlify

## Adding Your First Note

Create a new markdown file in the `_notes` folder:

```yaml
---
title: "My First Note"
date: 2024-01-15
feed: "show"
---
```

Then write your content using [[Wiki Links]] to connect to other notes.

## What's Next?

- Learn how to use [[Wiki Links]] to connect your notes
- See the [[Markdown Guide]] for formatting help
- Customize your site with the [[Customization]] guide
- Deploy your site using the [[Deployment]] instructions

## Tips

- **Start small**: Add a few notes first to see how it works
- **Use descriptive titles**: They become your URLs and link targets
- **Link liberally**: The more connections, the better your garden grows
- **Keep it simple**: Focus on content, not complex formatting

---

*Your digital garden is ready to grow! 🌱* 


================================================
FILE: _notes/Public/Markdown Guide.md
================================================
---
title: Markdown Guide
feed: show
date: 2024-01-15
---

This guide shows the essential markdown formatting you can use in your notes.

## Headings

```markdown
# Main heading
## Section heading
### Subsection heading
```

## Text Formatting

```markdown
*Italic text* or _italic text_
**Bold text** or __bold text__
`inline code`
~~strikethrough~~
```

## Lists

```markdown
- Unordered list item
- Another item
  - Nested item

1. Ordered list item
2. Another item
```

## Links

```markdown
[Link text](https://example.com)
[[Wiki link to another note]]
[[External link::https://example.com]]
```

## Code Blocks

```markdown
```javascript
function hello() {
    console.log("Hello, World!");
}
```
```

## Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
```

## Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Content  | Content  |
```

## Math (if enabled)

```markdown
Inline math: $x = y$
Block math: $$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$
```

## Images

```markdown
![Alt text](/assets/img/image.jpg)
```

## Horizontal Rules

```markdown
---
```

## Tips

- Use clear, descriptive headings
- Keep paragraphs short and focused
- Use [[Wiki Links]] to connect related notes
- Don't over-format - focus on readability

---

*This covers the most common markdown features you'll need for your notes.* 


================================================
FILE: _notes/Public/Obsidian Setup.md
================================================
---
title: Obsidian Setup
feed: show
date: 2024-01-15
---

Here's how to set up Jekyll Garden to work seamlessly with Obsidian.

## Use `_notes` as Your Vault

The simplest approach is to use the `_notes` folder as your Obsidian vault:

1. **Open Obsidian**
2. **Create a new vault** or open existing vault
3. **Set the vault location** to the `_notes` folder in your Jekyll Garden project

This way, all your notes are automatically part of your website.

## Front Matter Requirements

All notes must use the proper front matter format:

```yaml
---
title: "Your Note Title"
date: 2024-01-15
feed: "show"
---
```

The `feed: "show"` setting makes the note appear on your website. Use `feed: "hide"` for private notes.

## Git Ignore Setup

Add these folders to your `.gitignore` file:

```gitignore
# Obsidian settings
.obsidian/
.trash/

# Jekyll build files
_site/
.sass-cache/
.jekyll-cache/
```

## Private Notes

To keep some notes private (not published on your website):

1. **Create a folder** inside `_notes` (e.g., `_notes/Private/`)
2. **Add the folder to `.gitignore`**:
   ```gitignore
   _notes/Private/
   ```
3. **Set `feed: "hide"`** in the note's front matter

This way, private notes stay in your Obsidian vault but won't be synced to Git or built as pages in Jekyll.

## Workflow

1. **Write notes** in Obsidian using the `_notes` folder
2. **Use [[Wiki Links]]** to connect your notes
3. **Add proper front matter** to each note
4. **Commit and push** to publish changes
5. **Your website updates** automatically

## Tips

- **Keep Obsidian and Jekyll in sync**: The `_notes` folder is your single source of truth
- **Use descriptive titles**: They become your URLs and link targets
- **Test locally**: Run `bundle exec jekyll serve` to preview changes
- **Backup regularly**: Your notes are valuable - keep them safe

## External Resources

- [Obsidian Documentation](https://obsidian.md/help)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages](https://pages.github.com/)

---

*This setup gives you the best of both worlds: powerful note-taking in Obsidian and beautiful publishing with Jekyll Garden.* 


================================================
FILE: _notes/Public/Theme Features.md
================================================
---
title: Theme Features
feed: show
date: 2024-01-15
---

Jekyll Garden comes with several features that make it easy to create and navigate your digital garden.

## Wiki-Style Links
Connect your notes using `[[note title]]` syntax, just like in Obsidian. Links are created automatically and work seamlessly across your site.

## Full-Text Search
Find any note quickly with the built-in search feature. Search works across note titles and content, with results updating as you type.

## Automatic Backlinks
See which notes link to the current one. This helps you discover related content and explore connections between your ideas.

## Dark/Light Theme
Toggle between light and dark themes with a single click. Your preference is saved and remembered for future visits.

## Responsive Design
Your site looks great on all devices - phones, tablets, and computers. The design adapts automatically to different screen sizes.

## Math Support
Write mathematical expressions using KaTeX. Use `$x = y$` for inline math and `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$` for block equations.

## Blog Integration
Supports jekyll blog. Write chronological blog posts in the `_posts` folder and link them to your notes.


## Customizable
Easily customize colors, fonts, and layout by editing CSS variables. See the [[Customization]] guide for details.

---

*These features work together to create a powerful yet simple platform for sharing your knowledge.* 


================================================
FILE: _notes/Public/Wiki Links.md
================================================
---
title: Wiki Links
feed: show
date: 2024-01-15
---

Wiki links let you connect your notes using double brackets, like `[[Note Title]]`. This works exactly like linking notes in Obsidian.

## How to Use

Simply type `[[Note Title]]` in your note. If a note with that title exists, it becomes a clickable link. If not, you'll see a placeholder indicating the note doesn't exist yet.

You can also link to external websites: `[[Google::https://google.com]]`.

## Examples

```markdown
This note connects to [[Getting Started]] and [[Markdown Guide]].

For more information, check out [[Jekyll::https://jekyllrb.com]].
```

## Automatic Backlinks

When you create a wiki link to another note, that note automatically shows a "Backlinks" section. For example, if you visit [[Getting Started]], you'll see this note listed there because we linked to it.


## Troubleshooting

If a wiki link appears broken:
1. Check the exact spelling of the note title
2. Make sure the note exists in the `_notes` folder
3. Verify the note has `feed: "show"` in its front matter

---

*Wiki links transform your notes from isolated documents into a connected knowledge base.* 


================================================
FILE: _posts/2024-01-15-welcome-to-jekyll-garden.md
================================================
---
title: "Welcome to Jekyll Garden"
date: 2024-01-15
categories: [jekyll, digital-garden]
tags: [welcome, introduction]
---

Jekyll Garden is a thoughtfully minimal theme for Jekyll that transforms your Obsidian vault into a beautiful, interconnected website. It's designed for those who value clarity and focus, letting your notes and ideas shine without distraction.

## What Makes It Special

- **Obsidian Integration**: Use your existing Obsidian vault structure
- **Wiki-style Links**: Connect ideas with `[[note title]]` syntax
- **Clean Design**: Minimal, typography-focused layout
- **Fast Performance**: Static site generation for speed
- **Search Functionality**: Full-text search across all content

---

*Start building your own digital garden and see how your ideas connect and flourish over time.* 


================================================
FILE: assets/css/fruity.css
================================================

/*
Based on https://github.com/jwarby/jekyll-pygments-themes ; Theme Fruity.
Added variables to asssure all colors works with dark and light theme (partially it does)
Some color variables are from style.css
*/

html {
    --highlight-color-orange: #fb660a;
    --highlight-color-green: #008800;
    --highlight-color-red: #ff0007;
    --highlight-color-pink: #ff0086;
    --highlight-color-grey: #444444;
    --highlight-color-khaki: #817816;
    --highlight-color-comment-bg: #0f140f;
    --highlight-color-whitespace: #888888;
}

.highlight pre { background-color: var(--color-border-light); }
.highlight .hll { background-color: var(--color-border-light); }
.highlight .c { color: var(--highlight-color-green); font-style: italic; background-color: var(--color-border-light); } /* Comment */
.highlight .err { color: var(--color-text); } /* Error */
.highlight .g { color: var(--color-text); } /* Generic */
.highlight .k { color: var(--highlight-color-orange); font-weight: bold } /* Keyword */
.highlight .l { color: var(--color-text); } /* Literal */
.highlight .n { color: var(--color-text); } /* Name */
.highlight .o { color: var(--color-text); } /* Operator */
.highlight .x { color: var(--color-text); } /* Other */
.highlight .p { color: var(--color-text); } /* Punctuation */
.highlight .cm { color: var(--highlight-color-green); font-style: italic; background-color: var(--highlight-color-comment-bg) } /* Comment.Multiline */
.highlight .cp { color: var(--highlight-color-red); font-weight: bold; font-style: italic; background-color: var(--highlight-color-comment-bg) } /* Comment.Preproc */
.highlight .c1 { color: var(--highlight-color-green); font-style: italic; background-color: var(--highlight-color-comment-bg) } /* Comment.Single */
.highlight .cs { color: var(--highlight-color-green); font-style: italic; background-color: var(--highlight-color-comment-bg)} /* Comment.Special */
.highlight .gd { color: var(--color-text); } /* Generic.Deleted */
.highlight .ge { color: var(--color-text); } /* Generic.Emph */
.highlight .gr { color: var(--color-text); } /* Generic.Error */
.highlight .gh { color: var(--color-text);; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: var(--color-text); } /* Generic.Inserted */
.highlight .go { color: var(--highlight-color-grey); background-color: var(--highlight-color-comment-bg)} /* Generic.Output */
.highlight .gp { color: var(--color-text); } /* Generic.Prompt */
.highlight .gs { color: var(--color-text); } /* Generic.Strong */
.highlight .gu { color: var(--color-text);; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: var(--color-text); } /* Generic.Traceback */
.highlight .kc { color: var(--highlight-color-orange); font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: var(--highlight-color-orange); font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: var(--highlight-color-orange); font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: var(--highlight-color-orange) } /* Keyword.Pseudo */
.highlight .kr { color: var(--highlight-color-orange); font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: var(--highlight-color-khaki); font-weight: bold } /* Keyword.Type */
.highlight .ld { color: var(--color-text); } /* Literal.Date */
.highlight .m { color: var(--color-text-link); font-weight: bold } /* Literal.Number */
.highlight .s { color: var(--color-text-link) } /* Literal.String */
.highlight .na { color: var(--highlight-color-pink); font-weight: bold } /* Name.Attribute */
.highlight .nb { color: var(--color-text); } /* Name.Builtin */
.highlight .nc { color: var(--color-text); } /* Name.Class */
.highlight .no { color: var(--color-text-link) } /* Name.Constant */
.highlight .nd { color: var(--color-text); } /* Name.Decorator */
.highlight .ni { color: var(--color-text); } /* Name.Entity */
.highlight .ne { color: var(--color-text); } /* Name.Exception */
.highlight .nf { color: var(--highlight-color-pink); font-weight: bold } /* Name.Function */
.highlight .nl { color: var(--color-text); } /* Name.Label */
.highlight .nn { color: var(--color-text); } /* Name.Namespace */
.highlight .nx { color: var(--color-text); } /* Name.Other */
.highlight .py { color: var(--color-text); } /* Name.Property */
.highlight .nt { color: var(--highlight-color-orange); font-weight: bold } /* Name.Tag */
.highlight .nv { color: var(--highlight-color-orange) } /* Name.Variable */
.highlight .ow { color: var(--color-text); } /* Operator.Word */
.highlight .w { color: var( --highlight-color-whitespace); } /* Text.Whitespace NOT SURE */
.highlight .mf { color: var(--color-text-link); font-weight: bold } /* Literal.Number.Float */
.highlight .mh { color: var(--color-text-link); font-weight: bold } /* Literal.Number.Hex */
.highlight .mi { color: var(--color-text-link); font-weight: bold } /* Literal.Number.Integer */
.highlight .mo { color: var(--color-text-link); font-weight: bold } /* Literal.Number.Oct */
.highlight .sb { color: var(--color-text-link) } /* Literal.String.Backtick */
.highlight .sc { color: var(--color-text-link) } /* Literal.String.Char */
.highlight .sd { color: var(--color-text-link) } /* Literal.String.Doc */
.highlight .s2 { color: var(--color-text-link) } /* Literal.String.Double */
.highlight .se { color: var(--color-text-link) } /* Literal.String.Escape */
.highlight .sh { color: var(--color-text-link) } /* Literal.String.Heredoc */
.highlight .si { color: var(--color-text-link) } /* Literal.String.Interpol */
.highlight .sx { color: var(--color-text-link) } /* Literal.String.Other */
.highlight .sr { color: var(--color-text-link) } /* Literal.String.Regex */
.highlight .s1 { color: var(--color-text-link) } /* Literal.String.Single */
.highlight .ss { color: var(--color-text-link) } /* Literal.String.Symbol */
.highlight .bp { color: var(--color-text); } /* Name.Builtin.Pseudo */
.highlight .vc { color: var(--highlight-color-orange) } /* Name.Variable.Class */
.highlight .vg { color: var(--highlight-color-orange) } /* Name.Variable.Global */
.highlight .vi { color: var(--highlight-color-orange) } /* Name.Variable.Instance */
.highlight .il { color: var(--color-text-link); font-weight: bold } /* Literal.Number.Integer.Long */


================================================
FILE: assets/css/style.css
================================================
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

:root {
  --bg: rgb(255, 252, 240);
  --bg2: rgb(242, 240, 229);
  --text: #6f6e69;
  --title: #343331;
  --brand: rgb(58, 169, 159);
  --border: rgb(230, 228, 217);
  
  --font: "Inter", sans-serif;
  --weight-medium: 400;
  --weight-bold: 600;
  
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2rem;
  --space-xl: 3rem;
  
  --max-width: 48rem;
  --line-height: 1.5;
  
  /* 5-level typography scale (1rem = 15px) */
  --scale-xs: 0.8rem;     /* 12px */
  --scale-sm: 0.933rem;   /* 14px */
  --scale-base: 1rem;     /* 15px */
  --scale-lg: 1.2rem;     /* 18px */
  --scale-xl: 1.4rem;     /* 21px */
}

/* Dark theme variables */
[data-theme="dark"] {
  --bg: #18181c;
  --bg2: #23232a;
  --text: #d6d6d6;
  --title: #fff;
  --brand: #3ac9b0;
  --border: #33343a;
}

/* smooth transition on theme switching */
html.theme-transition,
body.theme-transition {
  transition: background 0.3s, color 0.3s;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 15px;
}

body {
  font-family: var(--font);
  font-weight: var(--weight-medium);
  line-height: var(--line-height);
  color: var(--text);
  background: var(--bg);
  font-size: var(--scale-base);
}

.container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: var(--space-xl);
}

.container > div {
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-xl) var(--space-xl);
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-xl);
}

.nav-left a {
  text-decoration: none;
}

.logo {
  width: 32px;
  height: 32px;
  display: block;
}

.dropdown {
  position: relative;
}

.hamburger {
  cursor: pointer;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--title);
}

.hamburger svg {
  transition: transform 0.3s ease;
}

.hamburger.active svg {
  transform: rotate(90deg);
}

.dropdown-menu {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  background: var(--bg);
  border-top: 1px solid var(--border);
  padding: var(--space-sm);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1001;
}

.dropdown.active .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu a {
  display: block;
  padding: var(--space-sm);
  color: var(--text);
  text-decoration: none;
  transition: 0.3s ease;
  border-radius: 0.5rem;
  font-size: var(--scale-base);
}

.dropdown-menu a:hover {
  color: var(--brand);
  background: var(--bg2);
}

@media (min-width: 768px) {
  .dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    left: auto;
    width: 200px;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
  }
  
  .dropdown-menu a {
    padding: 0.75rem 1rem;
    font-size: var(--scale-base);
  }
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font);
  color: var(--title);
  margin-bottom: var(--space-sm);
  line-height: 1.5;
}

h1 {
  font-size: clamp(1.2rem, 4vw, 1.4rem);
  font-weight: var(--weight-bold);
  margin-bottom: var(--space-lg);
}

h2 {
  font-size: clamp(1.1rem, 3vw, 1.2rem);
  font-weight: var(--weight-bold);
  margin-top: var(--space-xl);
  margin-bottom: var(--space-md);
}

h3 {
  font-size: clamp(1rem, 2vw, 1.2rem);
  font-weight: var(--weight-bold);
  margin-top: var(--space-lg);
  margin-bottom: var(--space-sm);
}

h4, h5, h6 { 
  font-size: var(--scale-base); 
  font-weight: var(--weight-bold);
}

p {
  font-size: var(--scale-base); 
  margin-bottom: var(--space-md);
  color: var(--text);
  line-height: 1.7;
  font-weight: 400;
}

a {
  color: var(--text);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
}

a:hover {
  color: var(--brand);
}

.btn {
  padding: 0.6rem 1.2rem;
  border-radius: 0.2rem;
  color: var(--bg);
  background: var(--title);
  transition: background 0.2s;
  text-decoration: none;
  font-size: var(--scale-sm);
  text-align: center;
  display: inline-block;
  margin-right: var(--space-sm);
  border: none;
  font-weight: 500;
  letter-spacing: 0.025em;
}

.btn:hover {
  background: var(--text);
  color: var(--bg);
}

.note-list-sec {
  margin-top: var(--space-xl);
}

.note-list-sec h3 {
  margin-top: 0;
}

.note-list {
  list-style: none;
}

.note-list li {
  border-bottom: 1px solid var(--border);
  padding: var(--space-xs) 0;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.note-list > li:first-child {
  border-top: 1px solid var(--border);
}

.note-title {
  font-size: var(--scale-base);
  font-weight: var(--weight-medium);
  color: var(--title);
}

.note-title a {
  text-decoration: none;
  color: var(--title);
}

.note-title a:hover {
  color: var(--brand);
}

.links-section {
  margin-top: var(--space-xl);
  margin-bottom: var(--space-lg);
}

.links-section h6 {
  color: var(--title);
  font-size: var(--scale-sm);
  font-weight: var(--weight-medium);
  margin-bottom: var(--space-sm);
}

.links-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-sm);
  list-style: none;
  margin-bottom: 0;
  padding-left: 0;
}

.links-grid li {
  padding-bottom: var(--space-xs);
  border-bottom: 1px solid;
  color: var(--border);
}

.links-grid a {
  color: var(--text);
  text-decoration: none;
  font-size: var(--scale-sm);
  line-height: 1.5;
}

.links-grid a:hover {
  color: var(--brand);
}

@media (max-width: 520px) {
  .links-grid {
    grid-template-columns: 1fr;
  }
}

.footer {
  margin-top: var(--space-xl);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer h6 {
  color: var(--title);
  font-size: var(--scale-xs);
  font-weight: 400;
  letter-spacing: 0.01em;
}

.footer-left {
  text-align: left;
}

.footer-right {
  flex: 1;
  text-align: right;
}

.theme-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  color: var(--text);
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  margin: 0;
  transition: color 0.3s;
}

.theme-toggle:hover {
  color: var(--brand);
}

.theme-toggle svg {
  display: block;
  width: 14px;
  height: 14px;
}

/* Markdown Support */
blockquote {
  border-left: 4px solid var(--brand);
  padding-left: var(--space-md);
  margin: var(--space-lg) 0;
  font-style: italic;
  color: var(--text);
  line-height: 1.6;
  background: var(--bg2);
  padding: var(--space-md);
  border-radius: 0.25rem;
}

code {
  background: var(--bg2);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  color: var(--text);
}

pre {
  background: var(--bg2);
  padding: var(--space-md);
  border-radius: 0.5rem;
  overflow-x: auto;
  margin: var(--space-lg) 0;
  border: 1px solid var(--border);
}

pre code {
  background: none;
  padding: 0;
  border-radius: 0;
  font-size: 0.875rem;
  line-height: 1.5;
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: var(--space-xl) 0;
}

ul, ol {
  margin-bottom: var(--space-md);
  padding-left: var(--space-lg);
}

li {
  margin-bottom: var(--space-xs);
  line-height: 1.6;
}

strong {
  font-weight: 600;
}

em {
  font-style: italic;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--space-lg) 0;
  font-size: 0.875rem;
}

th, td {
  padding: var(--space-sm) var(--space-md);
  text-align: left;
  border-bottom: 1px solid var(--border);
}

th {
  font-weight: 600;
  color: var(--title);
  background: var(--bg2);
}

td {
  background: var(--bg);
  color: var(--text);
}

/* Search styles - modernized */
.search-container {
  margin-bottom: var(--space-lg);
  position: relative;
}

.search-input {
  width: 100%;
  padding: var(--space-sm);
  border: 1px solid var(--border);
  border-radius: 0.25rem;
  font-size: var(--scale-base);
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
}

.search-input:focus {
  outline: none;
  border-color: var(--brand);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg);
  max-height: 300px;
  overflow-y: auto;
  z-index: 999;
  display: none;
}

.search-active .search-results {
  display: block;
  border: 1px solid var(--border);
  border-top: none;
  border-radius: 0 0 0.25rem 0.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-results-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.search-results-list-item {
  margin: 0;
}

.search-result {
  display: block;
  padding: var(--space-xs);
  text-decoration: none;
  color: var(--text);
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--border);
  line-height: 1.5;
}

.search-result:last-child {
  border-bottom: none;
}

.search-result:hover {
  background: var(--bg2);
  color: var(--brand);
}

.search-result-title {
  color: var(--title);
  font-weight: var(--weight-bold);
  margin-bottom: var(--space-sm);
  font-size: var(--scale-base);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.search-result-doc {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.search-result-doc-title {
  font-weight: var(--weight-bold);
  color: var(--title);
}

.search-result-previews {
  margin-top: var(--space-xs);
}

.search-result-preview {
  color: var(--text);
  font-size: var(--scale-sm);
  line-height: 1.4;
  margin-bottom: var(--space-xs);
  opacity: 0.8;
}

.search-result-highlight {
  background: var(--brand);
  color: var(--bg);
  padding: 0 2px;
  border-radius: 2px;
  font-weight: var(--weight-bold);
}

.search-no-result {
  color: var(--text);
  font-style: italic;
  padding: var(--space-md);
  text-align: center;
}

/* Feed styles */
.notelist-feed {
  border-bottom: 1px solid var(--border);
  padding: var(--space-sm) 0;
  transition: background 0.3s ease;
}

.notelist-feed:hover {
  background: var(--bg2);
}

.notelist-feed a {
  text-decoration: none;
  color: inherit;
}

.notelist-feed p {
  color: var(--title);
  margin-bottom: 0;
  font-size: var(--scale-base);
  font-weight: var(--weight-medium);
}

.list-feed {
  border-bottom: 1px solid var(--border);
  padding: var(--space-sm) 0;
}

.list-feed a {
  text-decoration: none;
  color: var(--title);
  transition: color 0.3s ease;
}

.list-feed a:hover {
  color: var(--brand);
}

/* Hide/show classes for backlinks */
.hide {
  display: none;
}

.show {
  display: block;
}

/* Tooltip styles */
.tooltip {
  position: relative;
  display: inline;
}

.tooltip .right {
  width: 300px;
  padding: 0.5rem 0.75rem;
  font-size: var(--scale-xs);
  line-height: 1.3;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 150%;
  z-index: 1;
  background-color: var(--bg2);
  color: var(--text);
  border-radius: 6px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s;
  text-align: left;
}

.tooltip:hover .right {
  opacity: 1;
  visibility: visible;
}

.tooltip .right .tooltip-excerpt {
  color: var(--text);
  line-height: 1.3;
  font-size: var(--scale-xs);
  display: block;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 280px;
}

.stale-link {
  color: var(--text) !important;
  opacity: 0.6;
  cursor: not-allowed;
}

.wiki-link {
  color: var(--brand);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.wiki-link:hover {
  border-bottom-color: var(--brand);
}

.link-preview {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: var(--space-sm);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  max-width: 300px;
  font-size: var(--scale-sm);
  line-height: 1.4;
}

.preview-content strong {
  color: var(--title);
  display: block;
  margin-bottom: var(--space-xs);
}

.preview-content p {
  color: var(--text);
  margin: 0;
  opacity: 0.8;
  font-size: 0.875rem;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .container {
    padding-top: var(--space-md);
  }
  
  .container > div {
    padding: 0 var(--space-md) var(--space-md);
  }
  
  .nav {
    margin-bottom: var(--space-lg);
  }
  
  h1 {
    font-size: var(--scale-lg);
  }
  
  h2 {
    font-size: var(--scale-base);
  }
  
  h3 {
    font-size: var(--scale-base);
  }
}

@media (max-width: 520px) {
  .container {
    padding-top: var(--space-sm);
  }
  
  .container > div {
    padding: 0 var(--space-sm) var(--space-sm);
  }
  
  .btn {
    display: block;
    margin-bottom: var(--space-sm);
  }
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: var(--space-md) 0;
}

p a[href^="http://"], p a[href^="https://"],
li a[href^="http://"], li a[href^="https://"] {
  position: relative;
}
p a[href^="http://"]:after, p a[href^="https://"]:after,
li a[href^="http://"]:after, li a[href^="https://"]:after {
  content: '';
  display: inline-block;
  width: 1em;
  height: 1em;
  margin-left: 0.25em;
  vertical-align: text-top;
  background: url('data:image/svg+xml;utf8,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2024%2024%22%20fill=%22none%22%20stroke=%22%23555%22%20stroke-width=%222%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cpath%20d=%22M5%2019L19%205M5%205h14v14%22/%3E%3C/svg%3E') no-repeat center center;
  background-size: 1em 1em;
  opacity: 0.7;
}


================================================
FILE: assets/js/Search.js
================================================
// Copyright (c) 2020-2024 Jekyll Garden. Credits: Raghuveer S

/********************************************************************************************
 * 
 * MIT License
 * 
 * Copyright (c) 2020 Raghuveer S
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * 
 * 
 * File: Search.js
 * Author: Raghuveer S
 * 
 * Preface: I take loads of inspiration from just-the-docs to implement this.
 * This can be easily ported to suit your needs. There is very little project specific stuff
 * in this.
 * 
 * How to customize this for your own project:
 * --------------------------------------------
 * 1. Lunr takes json fields for indexing, so create a json file with all the fields
 *      you want searched by Lunr. For eg. In my case, it is title, content, url for my 
 *      blog posts.
 *      Note: In this project, the json gets automatically generated. (SEE: search-data.json)
 * 2. Change the field names below accordingly. (SEE: this.field)
 * 3. Create a HTML Page with an input box(with id='search-input') and a div beneath it
 *     with id='search-results'. Also, don't forget to embed this script using the script
 *     tag.
 * 4. You are good to go. If you need additional customization you can change the boost 
 *      values, layout, colors etc by tinkering with the correponding parts of the code.
 *********************************************************************************************/

 (function (sj) {
    "use strict";

    sj.addEvent = function(el, type, handler) {
      if (el.attachEvent) el.attachEvent('on'+type, handler); else el.addEventListener(type, handler);
    }
    sj.removeEvent = function(el, type, handler) {
      if (el.detachEvent) el.detachEvent('on'+type, handler); else el.removeEventListener(type, handler);
    }
    sj.onReady = function(ready) {
      // in case the document is already rendered
      if (document.readyState!='loading') ready();
      // modern browsers
      else if (document.addEventListener) document.addEventListener('DOMContentLoaded', ready);
      // IE <= 8
      else document.attachEvent('onreadystatechange', function(){
          if (document.readyState=='complete') ready();
      });
    }

    
    async function getSearchData(dataUrl) {
        let response = await fetch(dataUrl);
        let responseText = response.text();
        return responseText;
    }

    function searchInit() {
        var dataUrl = "/SearchData.json";

        getSearchData(dataUrl)
            .then(function(responseText) {
            var docs = JSON.parse(responseText);

            lunr.tokenizer.separator = /[\s/]+/;

            var index = lunr(function(){
                this.ref('id');
                this.field('title', {boost: 500});
                this.field('content', {boost: 1});
                this.field('url');
                this.metadataWhitelist = ['position']

                for (var i in docs) {
                    this.add({
                        id: i,
                        title: docs[i].title,
                        content: docs[i].content,
                        url: docs[i].url
                    });
                }
            });
            searchLoaded(index, docs);
        }).catch(function(err) {
            console.warn("Error processing the search-data for lunrjs",err);
        });
    }

    function searchLoaded(index, docs) {
        var index = index;
        var docs = docs;
        var searchInput = document.getElementById('search-input');
        var searchResults = document.getElementById('search-results');
        var currentInput;
        var currentSearchIndex = 0;

        function showSearch() {
            document.documentElement.classList.add('search-active');
        }

        function hideSearch() {
            document.documentElement.classList.remove('search-active');
        }

        function update() {
            currentSearchIndex++;

            var input = searchInput.value;
            if (input === '') {
                hideSearch();
            } else {
                showSearch();
                window.scroll(0, -1);
                setTimeout(function() { window.scroll(0, 0);}, 0);
            }

            if (input === currentInput) {
                return;
            }

            currentInput = input;
            searchResults.innerHTML = '';
            if (input === '') {
                return;
            }

            var results = index.query(function (query) {
                var tokens = lunr.tokenizer(input)
               query.term(tokens, {
                 boost: 10
               });
               query.term(tokens, {
                 wildcard: lunr.Query.wildcard.TRAILING
               });
            });

            if ((results.length == 0) && (input.length > 2)) {
                var tokens = lunr.tokenizer(input).filter(function(token, i){
                   return token.str.length < 20; 
                })

                if (tokens.length > 0) {
                    results = index.query(function (query){
                        query.term(tokens, {
                            editDistance: Math.round(Math.sqrt(input.length / 2 - 1))
                        });
                    });
                }
            }

            if (results.length == 0) {
                var noResultsDiv = document.createElement('div');
                noResultsDiv.classList.add('search-no-result');
                noResultsDiv.innerText = 'No results found';
                searchResults.appendChild(noResultsDiv);
            } else {
                var resultsList = document.createElement('ul');
                resultsList.classList.add('search-results-list');
                searchResults.appendChild(resultsList);

                addResults(resultsList, results, 0, 10, 100, currentSearchIndex);
            }

            function addResults(resultsList, results, start, batchSize, batchMillis, searchIndex) {
                if (searchIndex != currentSearchIndex) {
                    return;
                }
                for (var i = start; i < (start + batchSize); i++) {
                    if (i == results.length) {
                        return;
                    }
                    addResult(resultsList, results[i]);
                }
                setTimeout(function() {
                    addResults(resultsList, results, start + batchSize, batchSize, batchMillis, searchIndex);
                }, batchMillis);
            }

            function addResult(resultsList, result) {
                
                var doc = docs[result.ref];
                var resultsListItem = document.createElement('li');
                resultsListItem.classList.add('search-results-list-item');
                resultsList.appendChild(resultsListItem);

                var resultLink = document.createElement('a');
                resultLink.classList.add('search-result');
                resultLink.setAttribute('href', doc.url);
                resultsListItem.appendChild(resultLink);

                var resultTitle = document.createElement('div');
                resultTitle.classList.add('search-result-title');
                resultLink.appendChild(resultTitle);

                var resultDocTitle = document.createElement('div');
                resultDocTitle.classList.add('search-result-doc-title');
                resultDocTitle.innerHTML = doc.doc;
                resultTitle.appendChild(resultDocTitle);
                var resultDocOrSection = resultDocTitle;
                
                if (doc.doc != doc.title) {
                    
                    resultDoc.classList.add('search-result-doc-parent');
                    var resultSection = document.createElement('div');
                    resultSection.classList.add('search-result-section');
                    resultSection.innerHTML = doc.title;
                    resultTitle.appendChild(resultSection);
                    resultDocOrSection = resultSection;
                }


                
                var metadata = result.matchData.metadata;
                var titlePositions = [];
                var contentPositions = [];
                for (var j in metadata) {
                    var meta = metadata[j];
                    if (meta.title) {
                        var positions = meta.title.position;
                        for (var k in positions) {
                            titlePositions.push(positions[k]);
                        }
                    }

                    if (meta.content) {
                        var positions = meta.content.position;
                        for(var k in positions) {
                            var position = positions[k];
                            var previewStart = position[0];
                            var previewEnd = position[0] + position[1];
                            var ellipsesBefore = true;
                            var ellipsesAfter = true;
                            for (var k = 0; k < 3; k++) {
                                var nextSpace = doc.content.lastIndexOf(' ', previewStart - 2);
                                var nextDot = doc.content.lastIndexOf('. ', previewStart - 2);
                                if ((nextDot >= 0) && (nextDot > nextSpace)) {
                                    previewStart = nextDot + 1;
                                    ellipsesBefore = false;
                                    break;
                                }
                                if (nextSpace < 0) {
                                    previewStart = 0;
                                    ellipsesBefore = false;
                                    break;
                                }
                                previewStart = nextSpace + 1;
                            }

                            for (var k = 0; k < 3; k++) {
                                var nextSpace = doc.content.indexOf(' ', previewEnd + 1);
                                var nextDot = doc.content.indexOf('. ', previewEnd + 1);
                                if ((nextDot >= 0) && (nextDot < nextSpace)) {
                                    previewEnd = nextDot;
                                    ellipsesAfter = false;
                                    break;
                                }
                                if (nextSpace < 0) {
                                    previewEnd = doc.content.length;
                                    ellipsesAfter = false;
                                    break;
                                }
                                previewEnd = nextSpace;
                            }

                            contentPositions.push({
                                highlight: position,
                                previewStart: previewStart, previewEnd: previewEnd,
                                ellipsesBefore: ellipsesBefore, ellipsesAfter: ellipsesAfter
                            });
                        }
                    }
                }
                if (titlePositions.length > 0) {
                    titlePositions.sort(function(p1, p2){ return p1[0] - p2[0] });
                    resultDocOrSection.innerHTML = '';
                    addHighlightedText(resultDocOrSection, doc.title, 0, doc.title.length, titlePositions);
                }

                if (contentPositions.length > 0) {
                    contentPositions.sort(function(p1, p2){ return p1.highlight[0] - p2.highlight[0] });
                    var contentPosition = contentPositions[0];
                    var previewPosition = {
                        highlight: [contentPosition.highlight],
                        previewStart: contentPosition.previewStart, previewEnd: contentPosition.previewEnd,
                        ellipsesBefore: contentPosition.ellipsesBefore, ellipsesAfter: contentPosition.ellipsesAfter
                    };
                    var previewPositions = [previewPosition];
                    for (var j = 1; j < contentPositions.length; j++) {
                        contentPosition = contentPositions[j];
                        if (previewPosition.previewEnd < contentPosition.previewStart) {
                            previewPosition = {
                            highlight: [contentPosition.highlight],
                            previewStart: contentPosition.previewStart, previewEnd: contentPosition.previewEnd,
                            ellipsesBefore: contentPosition.ellipsesBefore, ellipsesAfter: contentPosition.ellipsesAfter
                            }
                            previewPositions.push(previewPosition);
                        } else {
                            previewPosition.highlight.push(contentPosition.highlight);
                            previewPosition.previewEnd = contentPosition.previewEnd;
                            previewPosition.ellipsesAfter = contentPosition.ellipsesAfter;
                        }
                    }

                    var resultPreviews = document.createElement('div');
                    resultPreviews.classList.add('search-result-previews');
                    resultLink.appendChild(resultPreviews);

                    var content = doc.content;
                    
                    for (var j = 0; j < Math.min(previewPositions.length, 2); j++) {
                        var position = previewPositions[j];
                        var resultPreview = document.createElement('div');
                        resultPreview.classList.add('search-result-preview');
                        resultPreviews.appendChild(resultPreview);

                        if (position.ellipsesBefore) {
                            resultPreview.appendChild(document.createTextNode('... '));
                        }
                        addHighlightedText(resultPreview, content, position.previewStart, position.previewEnd, position.highlight);
                        if (position.ellipsesAfter) {
                            resultPreview.appendChild(document.createTextNode(' ...'));
                        }
                    }
                }
            }

            function addHighlightedText(parent, text, start, end, positions) {
                var index = start;
                for (var i in positions) {
                    var position = positions[i];
                    var span = document.createElement('span');
                    span.innerHTML = text.substring(index, position[0]);
                    parent.appendChild(span);
                    index = position[0] + position[1];
                    var highlight = document.createElement('span');
                    highlight.classList.add('search-result-highlight');
                    highlight.innerHTML = text.substring(position[0], index);
                    parent.appendChild(highlight);
                }
                var span = document.createElement('span');
                span.innerHTML = text.substring(index, end);
                parent.appendChild(span);
            }
        }
        
        sj.addEvent(searchInput, 'focus', function(){
            setTimeout(update, 0);
        });

        sj.addEvent(searchInput, 'keyup', function(e){
            switch (e.keyCode) {
            case 27: // When esc key is pressed, hide the results and clear the field
                let searchInput = document.getElementById("search-input");
                searchInput.value = "";
                searchInput.blur();
                hideSearch();
                break;
            case 38: // arrow up
            case 40: // arrow down
            case 13: // enter
                e.preventDefault();
                return;
            }
            update();
        });

        sj.addEvent(searchInput, 'keydown', function(e){
            switch (e.keyCode) {
            case 38: // arrow up
                e.preventDefault();
                var active = document.querySelector('.search-result.active');
                if (active) {
                    active.classList.remove('active');
                    if (active.parentElement.previousSibling) {
                        var previous = active.parentElement.previousSibling.querySelector('.search-result');
                        previous.classList.add('active');
                        previous.scrollIntoView(false);
                    }
                }
                return;
            case 40: // arrow down
                e.preventDefault();
                var active = document.querySelector('.search-result.active');
                if (active) {
                    if (active.parentElement.nextSibling) {
                        var next = active.parentElement.nextSibling.querySelector('.search-result');
                        active.classList.remove('active');
                        next.classList.add('active');
                        next.scrollIntoView(false);
                    }
                } else {
                var next = document.querySelector('.search-result');
                    if (next) {
                        next.classList.add('active');
                    }
                }
                return;
            case 13: // enter
                e.preventDefault();
                var active = document.querySelector('.search-result.active');
                if (active) {
                active.click();
                } else {
                var first = document.querySelector('.search-result');
                if (first) {
                    first.click();
                }
                }
                return;
            }
        });

        sj.addEvent(document, 'click', function(e){
            if (e.target != searchInput) {
            hideSearch();
            }
        });

    }

    function searchInitListener() {
      document.onkeyup = function (e) {
        var evt = window.event || e;
        let searchInput = document.getElementById("search-input");
        let key = evt.keyCode || evt.which;
        if (e.shiftKey && key == 83) {
          searchInput.focus();
        }
      };
    }


    sj.onReady(function(){
        searchInitListener();
        searchInit();
    });
})(window.sj = window.sj || {});






================================================
FILE: pages/404.md
================================================
---
permalink: /404.html
layout: Post
content-type: static
title: Page Not Found
---

# 404 - Page Not Found

The page you're looking for doesn't exist.

Please check the URL and try again.

---

*Don't worry, even the best digital gardens have a few dead ends. The important thing is to keep exploring! 🌱*


================================================
FILE: pages/about.md
================================================
---
title: "About"
layout: Post
content-type: "static"
permalink: /about
---

# About

Jekyll Garden is a clean, minimal Jekyll theme designed to make publishing your Obsidian vault as a static website incredibly easy. It bridges the gap between private knowledge management and public sharing, allowing you to create a digital garden where your notes are interconnected through wiki-style links and easily discoverable through search. 


================================================
FILE: pages/blog.md
================================================
---
title: "Blog"
layout: Post
permalink: /blog
content-type: "static"
---

Browse all published blog posts. These are chronological, time-sensitive posts alongside the evergreen digital garden notes. 


================================================
FILE: pages/Credits.md
================================================
---
title: "Credits"
layout: Post
permalink: /credits
content-type: "static"
---

# Credits and Acknowledgments

Jekyll Garden wouldn't exist without the contributions of many talented developers and designers. Here's who made it possible:

## Development and Inspiration

The foundation of Jekyll Garden comes from the work of several key individuals. **[Raghuveer](https://github.com/rgvr)** created the [Simply Jekyll theme](https://github.com/rgvr/simply-jekyll) that served as the foundation for this project, providing the initial structure and design principles. **[Santosh Thottingal](https://github.com/santhoshtr)** introduced the concept of Digital Gardens and inspired the wiki-linking approach that makes Jekyll Garden unique.

The development involved several contributors who brought their expertise to different aspects. **[Asim K T](https://github.com/asimkt)** coded the base HTML structure and implemented the core Jekyll Garden functionality. **[Ershad](https://github.com/ershad)** provided invaluable help with Jekyll and Ruby development. **[Anish](https://github.com/anishsheela)** contributed JavaScript improvements and bug fixes. **[Puttalu](https://github.com/aashiks)** provided OrgMode expertise and guidance.

The **[Team Obsidian](https://obsidian.md/)** deserves special recognition for creating the amazing markdown-based knowledge management tool that inspired the wiki-link syntax we use throughout the theme.

## Technologies

- **Highlight themes** from [Jekyll Pygment Themes](https://github.com/jwarby/jekyll-pygments-themes)
- **[Jekyll](https://jekyllrb.com/)** - The static site generator that powers everything
- **[Lunr.js](https://lunrjs.com/)** - Client-side search functionality
- **[KaTeX](https://katex.org/)** - Math expression rendering
- **[Inter font](https://rsms.me/inter/)** - Typography by Rasmus Andersson

---

*Jekyll Garden is open source and welcomes contributions. If you'd like to help improve the theme, please visit the [GitHub repository](https://github.com/Jekyll-Garden/jekyll-garden.github.io).*


================================================
FILE: pages/index.md
================================================
---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: Post
permalink: /
title: Jekyll Garden
---

Jekyll Garden is a simple theme that turns your Obsidian notes into a beautiful website. If you use Obsidian for note-taking, this theme makes it easy to publish your markdown files as a connected website with wiki-style links and full-text search.

Start by reading [[Getting Started]] to set up your own Jekyll Garden. Learn how to use [[Wiki Links]] to connect your notes, explore the [[Markdown Guide]] for formatting, and customize your site with the [[Customization]] guide. When you're ready to share your notes online, follow the [[Deployment]] instructions.


================================================
FILE: pages/notes.md
================================================
---
title: Notes
layout: Post
permalink: /notes
---

Browse all published notes in your digital garden. Notes are organized by connections, not chronology. Click any note to explore its links and context.


================================================
FILE: utilities/Autocomplete.ts
================================================
// Copyright (c) 2020-2024 Jekyll Garden. Credits: Raghuveer S

/************************************************************************************************
 * 
 * MIT License
 * 
 * Copyright (c) 2020 Raghuveer S
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 * 
 * 
 * Author@Raghuveer S, 2019
 * This is a plugin that I use with VS Code to enable autocompletion of 
 * filenames when using wiki-style link syntax "[["
 * 
 * How to use this file:
 * ---------------------
 * Disclaimer: This is not a published plugin i.e., it is not present in the VS Code Marketplace.
 *    1. Create a VSCode Plugin template using Yeoman. (This can be googled, it's a very simple step)
 *    2. Now open the template folder that you created.
 *    3. Copy this file to the 'src' folder inside the template folder and rename it to 'extension.ts'. 
 *        If there is already a file by that name in the 'src', just replace it with this.
 *    4. Now copy the entire template folder to C:/Users/<UserName>/.vscode/
 *    5. Restart vscode and you should now find that when you are working with 'simply jekyll' posts,
 *        you have autocompletion ready to fire.
**************************************************************************************************/

import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
	const provider = new IncludeCompletionProvider();
	context.subscriptions.push(vscode.languages.registerCompletionItemProvider('markdown', provider, '['));
}



class IncludeCompletionProvider implements vscode.CompletionItemProvider, vscode.Disposable {
	private titles: string[] = [];
	private watcher: vscode.FileSystemWatcher;
	
	constructor() {
		this.updateTitles();

		this.watcher = vscode.workspace.createFileSystemWatcher("**/_site/Autocomplete.txt");
		this.watcher.onDidCreate(()=> this.updateTitles());
		this.watcher.onDidChange(()=> this.updateTitles());
		this.watcher.onDidDelete(()=> this.updateTitles());
	}

	public dispose() {
		this.watcher.dispose();
	}

	public provideCompletionItems (document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken) {
		let linePrefix = document.lineAt(position).text.substr(0, position.character);
		if (!linePrefix.endsWith('[[')) {
				return undefined;
		}

		let completionItemArray: vscode.CompletionItem[] = [];

		for (let entry of this.titles) {
			completionItemArray.push(new vscode.CompletionItem(entry, vscode.CompletionItemKind.Text));
		}

		return completionItemArray;
	}

	private async updateTitles() {
		if (!vscode.workspace.workspaceFolders) {
			return undefined;
		}

		const folderUri = vscode.workspace.workspaceFolders[0].uri;
		const fileUri = folderUri.with({ path: path.posix.join(folderUri.path, '_site/autocomplete.txt') });

		let titles = <string[]> undefined;

		const readData =  await vscode.workspace.fs.readFile(fileUri);
		titles = Buffer.from(readData).toString('utf8').split(";");

		this.titles = titles;
	}


}


~~~
````

So, your tasks, as the AI ASSISTANT, are all the necessary and sufficient ones to properly extract from the above given referenced `jekyll-garden-jekyll-garden.github.io/` repository source-code the following features and capabilities in order to coherently, seamsless and organically enclose these extracted features and capabilities within this jekyll static site of mine located at `https://github.com/ib-bsb-br/ib-bsb-br.github.io`:

```features-and-capabilities
- Disregard the implementation of the 'search' feature, my jekyll static site already leverage 'pagefind' for that.

- Disregard the implementation of the 'frontmatter' variable named `feed` (The feed: "show" setting makes the note appear on your website. Use feed: "hide" for private notes.).

- Implement 'backlinks' and 'automatic backlinks' bidirectionally.

- Instead of using the `_notes` folde location, use my `_posts` folder location.

- Enclose the `backlinks`, the `Links to this note` - for each related markdown file enclosed within my `_posts` folder - within my already defined location for `ref`, which I configured at `https://github.com/ib-bsb-br/ib-bsb-br.github.io/raw/refs/heads/main/preprocess_posts.py` for `bibref` reffered elements.
```
