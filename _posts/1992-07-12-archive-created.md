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
        <a class="post-heading" href="{{ site.back_to_top_url | default: '#' }}" id="back-top" aria-label="Back_to_top" class="back-top-link">
          <span class="sr-only">Back_to_top</span></a>
        {{ post.date | date: '%Y-%m-%d' }}
        {% if post.last_modified_at != post.date %} &rightarrowtail; {{ post.last_modified_at | date_to_string }}
        {% endif %}
        </h4>
        <ul>
          <li>
            <a href="{{ post.url }}">
              <h3>{{ post.title }}</h3>
            </a>
          </li>
          {% if post.tags.size > 0 %}
            <p>Tags: 
              {% for tag in post.tags %}
                <a href="#{{ tag | slugify }}">{{ tag }}</a>{% unless forloop.last %}, {% endunless %}
              {% endfor %}
            </p>
          {% endif %}
        </ul>
      </div>
    {% endfor %}
  </aside>
</div>
