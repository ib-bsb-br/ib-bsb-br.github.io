---
layout: favicon
slug: archive-created
---
<h1 class="post-title">
  <a href="#bottom-of-page" aria-label="Go to bottom">{{ page.title | strip_html | strip }}</a>
</h1>
<div class="post-wrapper">
  <aside class="tagged-posts">
    {% assign sorted_posts = site.posts | sort: 'date' | reverse %}
    {% for post in sorted_posts %}
      <div class="search-link">
        <h4>
          <a class="post-heading" href="{{ site.back_to_top_url | default: '#' }}" id="back-to-top" aria-label="Back to top">
            <img src="{{ '/assets/gold.ico' | relative_url }}" alt="gold icon">
          </a>
          {{ post.date | date: '%Y-%m-%d' }}
        </h4>
        <ul>
          <li>
            <a href="{{ post.url }}">
              <h3>{{ post.title }}</h3>
            </a>
          </li>
        </ul>
      </div>
    {% endfor %}
  </aside>
</div>
