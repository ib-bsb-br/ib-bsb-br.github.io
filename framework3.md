# Framework3: Integrated GitHub Actions Framework for Jekyll Content Automation and Deployment

## Goal Statement
Build an enhanced GitHub Actions framework (framework3) that keeps the baseline deployment architecture from framework1 while integrating scheduled content-refresh, repository dispatch triggering, preprocessing, caching, and post-deploy automation patterns from raw_data.

## 1) Analysis of framework1 (baseline)

Framework1 is a focused **build-and-deploy** workflow for GitHub Pages with these core principles:

1. **Single responsibility flow**
   - One build job followed by one deploy job.
2. **GitHub Pages native deployment path**
   - Uses `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`.
3. **Jekyll-specific build with production environment**
   - Builds with `bundle exec jekyll build` and sets `JEKYLL_ENV=production`.
4. **Secure, least-necessary permissions**
   - `contents: read`, `pages: write`, `id-token: write`.
5. **Concurrency control for Pages**
   - Uses the `pages` concurrency group to avoid overlapping deployments.

This gives a stable deployment baseline but does not natively include content preprocessing, scheduled refreshes, dispatch orchestration, or post-deploy downstream automations.

## 2) Analysis and categorization of raw_data

Raw_data adds four major capability groups:

### A. Event-driven and scheduled content refresh
- Hourly and 6-hourly schedules for refreshing calendar/content files.
- Manual `workflow_dispatch` triggers.
- Python scripts (`events.py`, `tags.py`, `preprocess_posts.py`) update generated data.

### B. Workflow orchestration across events
- `repository_dispatch` (`trigger-jekyll`) to trigger a full pipeline from another workflow.
- `curl`-based dispatch job using tokenized auth.

### C. Content commit-before-build pattern
- Pre-build job commits generated files and pushes to `main`.
- Merge strategy (`-X ours`) attempts to reconcile with remote updates.

### D. Performance and output optimization
- Caching pip and Jekyll/site artifacts.
- Pagefind index generation and post-processing.
- Additional system dependencies (`sqlite3`) and Python package sets.
- Alternate deployment via `peaceiris/actions-gh-pages` with `gh-pages` branch and CNAME handling.
- Optional post-deploy job adding new post URLs to a spaced-inbox workflow.

## 3) Overlaps, gaps, and contradictions with framework1

### Overlaps
- Both systems center on GitHub Actions automation and Jekyll build/deploy.
- Both use concurrency controls and push/manual trigger concepts.

### Gaps in framework1 (filled by raw_data)
- No scheduled refresh in framework1.
- No preprocessing/commit stage before build.
- No search index post-build enhancements.
- No multi-trigger orchestration (`repository_dispatch`).
- No downstream post-deploy content processing.

### Contradictions to resolve
1. **Deployment mechanism mismatch**
   - Framework1 uses artifact-based GitHub Pages deploy actions.
   - Raw_data primarily uses `peaceiris/actions-gh-pages` to publish `_site`.
2. **Permission scope expansion**
   - Raw_data requires `contents: write` for automated commits.
3. **Complexity increase**
   - Added caching, dependency installs, and multiple jobs can reduce maintainability if unmanaged.

## 4) Hypothesis

If framework1 is extended with a staged content lifecycle (refresh -> preprocess -> commit -> build -> deploy -> post-deploy), then the resulting framework3 will preserve framework1 reliability while significantly improving automation depth, freshness of content, and operational flexibility.

## 5) Draft framework3

```yaml
name: Framework3 - Integrated Jekyll Content + Deployment Pipeline

on:
  push:
    branches: ["main"]
  workflow_dispatch:
  repository_dispatch:
    types: [trigger-jekyll]
  schedule:
    - cron: '0 */6 * * *'

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  refresh-content:
    name: Refresh and Preprocess Content
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - name: Install preprocessing dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install requests icalendar datetime pyyaml
      - name: Run refresh scripts
        env:
          CALENDAR_URL: ${{ secrets.CALENDAR_URL }}
          CALENDAR_USER: ${{ secrets.CALENDAR_USER }}
          CALENDAR_PASS: ${{ secrets.CALENDAR_PASS }}
        run: |
          python tags.py
          python events.py
          python preprocess_posts.py
      - name: Commit generated updates (if any)
        run: |
          git config --local user.email "actions@github.com"
          git config --local user.name "GitHub Actions"
          git add --all
          if ! git diff-index --quiet HEAD; then
            git commit -m "chore: refresh generated content [skip ci]"
            git push origin HEAD:main
          fi

  build:
    name: Build Jekyll Site
    runs-on: ubuntu-latest
    needs: refresh-content
    steps:
      - uses: actions/checkout@v6
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true
      - uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - uses: actions/cache@v5
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: ${{ runner.os }}-pip-
      - uses: actions/cache@v5
        with:
          path: _site
          key: jekyll-site-${{ github.sha }}
          restore-keys: jekyll-site-
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5
      - name: Build with Jekyll
        env:
          JEKYLL_ENV: production
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
      - name: Generate and adjust search index
        run: |
          npx -y pagefind --site _site --output-path _site/pagefind
          python modify-pagefind-ui.py
      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4

  post-deploy-automation:
    name: Optional Post-deploy Actions
    runs-on: ubuntu-latest
    needs: deploy
    if: github.event_name == 'push' && !contains(github.event.head_commit.message, '[skip ci]')
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - name: Example downstream integration
        run: |
          python script.py --no-review
          python review_load.py data.db
```

## 6) Framework3 evaluation

### Coherence
- Preserves framework1 ordering (build before deploy).
- Adds upstream refresh and optional downstream automation as explicit stages.

### Completeness
- Covers all trigger modes seen in raw_data: push, manual, schedule, repository_dispatch.
- Includes content generation, build optimization, search indexing, and deploy.

### Clarity
- Job names map to lifecycle phases.
- Secrets are consumed only in refresh-related steps.

### Practicality
- Uses caching and conditional commits to reduce redundant work.
- Maintains single deployment gate via `needs` dependencies.

### Comparison against established variants in provided data
- Compared to framework1: framework3 is broader and lifecycle-driven.
- Compared to raw_data `jekyll.yml`: framework3 keeps the robust Pages artifact deployment semantics from framework1 while integrating raw_data automation extensions.

## 7) Finalized framework3 (refined integration strategy)

### Core design rule
Retain framework1 as the **deployment backbone**, and layer raw_data features around it in three rings:

1. **Pre-build ring**: refresh, preprocess, and commit generated content.
2. **Build ring**: Jekyll build + index generation + artifact upload.
3. **Post-deploy ring**: optional downstream automation (e.g., inbox/review tasks).

### Key improvements over framework1
1. Trigger expansion: `schedule` + `repository_dispatch` + `workflow_dispatch` + `push`.
2. Data freshness: automated Python-based content regeneration before build.
3. Search quality: integrated Pagefind generation and UI post-processing.
4. Operational efficiency: dependency/site caching.
5. Extensibility: explicit post-deploy job for future automations.

## 8) Conclusion

The hypothesis is supported: framework3 successfully integrates raw_data into framework1 without losing framework1's identifiable structure. Framework3 is more comprehensive, better suited for continuously updated content, and still anchored in a clear build/deploy backbone.

## 9) Limitations and future development

### Current limitations
- More moving parts increase maintenance burden.
- Automated commit flows can create merge complexity.
- Additional dependencies (Python + system packages) increase CI runtime variance.

### Next actionable steps
1. Introduce path-based change detection to skip unnecessary jobs.
2. Add guarded retries for network-dependent content fetches.
3. Split reusable logic into composite actions.
4. Add CI validation job for generated artifacts before deploy.
5. Add observability summaries (job outputs + deployment metadata).

### Research/development opportunities
- Evaluate when to use artifact deployment vs branch deployment per repository constraints.
- Benchmark cache strategies for Jekyll + Python hybrid pipelines.
- Formalize conflict-resolution strategy for auto-commit workflows in high-change repos.
