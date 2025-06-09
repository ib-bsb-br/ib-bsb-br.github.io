---
date: 2024-07-13
tags: [github>jekyll]
comment: 
info: fechado.
type: post
layout: post
---
{% raw %}
Github Actions workflow to ensure the new gems are installed and locked in Gemfile.lock

`.github/workflows/update_gemfile_lock.yml`:

```
name: Update Gemfile.lock

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  update-gemfile-lock:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          persist-credentials: true   # ensure GITHUB_TOKEN is available for push

      - name: Set up Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3.4'

      - name: Disable Bundler Frozen Mode
        run: bundle config set frozen false

      - name: Install Bundler
        run: gem install bundler

      - name: Update & Commit Gemfile.lock
        run: |
          bundle update ffi
          bundle install

          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'

          git add Gemfile.lock

          # Only commit & push if there are staged changes
          if git diff --staged --quiet; then
            echo "✔︎ No changes to Gemfile.lock; skipping commit and push."
          else
            git commit -m 'Update Gemfile.lock'
            git push
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
{% endraw %}
