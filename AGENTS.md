The ASSISTANT must ground its responses exclusively within the following data/information/knowledge:

````https://github.com/sylhare/Simple-Jekyll-Search
~~~
<purpose>This file contains a packed representation of the entire repository&apos;s contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.</purpose><file_format>The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Repository files, each consisting of:
  - File path as an attribute
  - Full contents of the file</file_format><usage_guidelines>- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.</usage_guidelines><notes>- Some files may have been excluded based on .gitignore rules and Repomix&apos;s configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been formatted for parsing in xml style
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)</notes><directory_structure>.github/
  workflows/
    cypress.yml
    main.yml
  dependabot.yml
cypress/
  e2e/
    keyboard-input.cy.ts
    search-state-persistence.cy.ts
    simple-jekyll-search.cy.ts
  support/
    commands.ts
    e2e.ts
    index.ts
  tsconfig.json
dest/
  simple-jekyll-search.js
  simple-jekyll-search.min.js
docs/
  _includes/
    footer.html
    head.html
    header.html
    search.html
  _layouts/
    default.html
    page.html
    post.html
  _plugins/
    simple_search_filter_cn.rb
    simple_search_filter.rb
  _posts/
    2014-11-01-welcome-to-jekyll.md
    2014-11-02-test.md
    2025-04-22-technical-example.md
  _sass/
    _base.scss
    _custom.scss
    _layout.scss
    _syntax-highlighting.scss
    jekyll-simple-search.scss
  assets/
    css/
      main.scss
    data/
      search.json
    js/
      simple-jekyll-search.min.js
  _config.yml
  Gemfile
  get-started.md
  index.html
  Wiki.md
scripts/
  kill-jekyll.js
  stamp.js
  start-jekyll.js
src/
  middleware/
    highlighting.ts
    highlightMiddleware.ts
  SearchStrategies/
    search/
      findFuzzyMatches.ts
      findLevenshteinMatches.ts
      findLiteralMatches.ts
      findWildcardMatches.ts
    HybridSearchStrategy.ts
    SearchStrategy.ts
    StrategyFactory.ts
    types.ts
  types/
    global.d.ts
  utils/
    default.ts
    types.ts
  index.ts
  JSONLoader.ts
  OptionsValidator.ts
  Repository.ts
  SimpleJekyllSearch.ts
  Templater.ts
  utils.ts
tests/
  middleware/
    highlighting.test.ts
    highlightMiddleware.test.ts
  SearchStrategies/
    findFuzzyMatches.test.ts
    findLevenshteinMatches.test.ts
    findLiteralMatches.test.ts
    findWildcardMatches.test.ts
    HybridSearchStrategy.test.ts
    SearchStrategy.test.ts
    StrategyFactory.test.ts
  OptionsValidator.test.ts
  Repository.test.ts
  SimpleJekyllSearch.test.ts
  Templater.test.ts
  utils.test.ts
.gitignore
CONTRIBUTING.md
cypress.config.ts
eslint.config.js
LICENSE.md
package.json
README.md
tsconfig.json
vite.config.ts</directory_structure><files>This section contains the contents of the repository&apos;s files.<file path=".github/workflows/cypress.yml">name: Cypress Tests
on: [push]
jobs:
  cypress:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chrome, firefox]
    steps:
      - uses: actions/checkout@v6
      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: &apos;24&apos;
          cache: &apos;yarn&apos;
      - name: Install dependencies
        run: yarn install --frozen-lockfile
      - name: Build application
        run: yarn run build
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: &apos;3.2&apos;
          bundler-cache: true
      - name: Install Jekyll dependencies
        run: |
          cd docs
          bundle install
      - name: Build Jekyll site
        run: |
          cd docs
          bundle exec jekyll build
      - name: Run Cypress on ${{ matrix.browser }}
        shell: bash
        run: |
          set -o pipefail
          node scripts/start-jekyll.js &amp;
          JEKYLL_PID=$!

          sleep 8

          yarn cypress run --browser ${{ matrix.browser }}
          CYPRESS_EXIT_CODE=$?

          node scripts/kill-jekyll.js || true

          if kill -0 $JEKYLL_PID 2&gt;/dev/null; then
            kill $JEKYLL_PID || true
          fi

          exit $CYPRESS_EXIT_CODE</file><file path=".github/workflows/main.yml">name: Simple-Jekyll-Search
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Setup Node.js
        uses: actions/setup-node@v6
        with:
          node-version: &apos;24&apos;
          cache: &apos;yarn&apos;
      - name: Install dependencies
        run: yarn install --frozen-lockfile
      - name: Run unit tests
        run: yarn run test:unit
      - name: Build application
        run: yarn run build</file><file path=".github/dependabot.yml">version: 2
updates:
  - package-ecosystem: &quot;npm&quot;
    directory: &quot;/&quot;
    schedule:
      interval: &quot;monthly&quot;
    open-pull-requests-limit: 10
    commit-message:
      prefix: &quot;chore&quot;
    labels:
      - &quot;dependencies&quot;
      - &quot;javascript&quot;
      - &quot;typescript&quot;
    groups:
      typescript:
        patterns:
          - &quot;@types/*&quot;
          - &quot;typescript&quot;
          - &quot;@typescript-eslint/*&quot;
        update-types:
          - &quot;minor&quot;
          - &quot;patch&quot;
      testing:
        patterns:
          - &quot;vitest*&quot;
          - &quot;@vitest/*&quot;
          - &quot;cypress&quot;
          - &quot;jsdom&quot;
        update-types:
          - &quot;minor&quot;
          - &quot;patch&quot;
      build-tools:
        patterns:
          - &quot;vite*&quot;
          - &quot;terser&quot;
          - &quot;eslint*&quot;
        update-types:
          - &quot;minor&quot;
          - &quot;patch&quot;
    allow:
      - dependency-type: &quot;development&quot;

  - package-ecosystem: &quot;github-actions&quot;
    directory: &quot;/&quot;
    schedule:
      interval: &quot;monthly&quot;
    open-pull-requests-limit: 5
    commit-message:
      prefix: &quot;ci&quot;
    labels:
      - &quot;dependencies&quot;
      - &quot;github-actions&quot;</file><file path="cypress/e2e/keyboard-input.cy.ts">describe(&apos;Keyboard Input&apos;, () =&gt; {
  beforeEach(() =&gt; {
    cy.visit(&apos;/&apos;);
  });

  it(&apos;should trigger search on non-whitelisted keys&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;).type(&apos;a&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
  });

  it(&apos;should not trigger search on whitelisted keys&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;).type(&apos;{enter}&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;be.empty&apos;);
    cy.get(&apos;#search-input&apos;).type(&apos;{uparrow}&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;be.empty&apos;);
    cy.get(&apos;#search-input&apos;).type(&apos;{shift}&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;be.empty&apos;);
  });

  it(&apos;should trigger search after typing non-whitelisted keys&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;)
      .type(&apos;{shift}&apos;)
      .type(&apos;test&apos;)
      .type(&apos;{enter}&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
  });
});</file><file path="cypress/e2e/search-state-persistence.cy.ts">describe(&apos;Search State Persistence (Cross-Browser)&apos;, () =&gt; {
  const STORAGE_KEY = &apos;sjs-search-state&apos;;

  beforeEach(() =&gt; {
    cy.visit(&apos;/&apos;);
    cy.window().then(win =&gt; win.sessionStorage.clear());
  });

  describe(&apos;sessionStorage integration&apos;, () =&gt; {
    it(&apos;stores search state with correct structure&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;Lorem&apos;);
      cy.window().then(win =&gt; {
        const stored = win.sessionStorage.getItem(STORAGE_KEY);
        expect(stored).to.not.be.null;
        const state = JSON.parse(stored!);
        expect(state.query).to.equal(&apos;Lorem&apos;);
        expect(state.timestamp).to.be.a(&apos;number&apos;);
        expect(state.path).to.equal(&apos;/Simple-Jekyll-Search/&apos;);
      });
    });

    it(&apos;restores from sessionStorage when input is empty (Firefox scenario)&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          query: &apos;Lorem ipsum&apos;,
          timestamp: Date.now(),
          path: &apos;/Simple-Jekyll-Search/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;Lorem ipsum&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
    });

    it(&apos;clears storage when search is cleared&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;Lorem&apos;);
      cy.window().then(win =&gt; {
        expect(win.sessionStorage.getItem(STORAGE_KEY)).to.not.be.null;
      });
      cy.get(&apos;#search-input&apos;).clear();
      cy.get(&apos;#search-input&apos;).type(&apos; &apos;).clear();
      cy.wait(200);
      cy.window().then(win =&gt; {
        expect(win.sessionStorage.getItem(STORAGE_KEY)).to.be.null;
      });
    });
  });

  describe(&apos;edge cases - corrupted/stale storage&apos;, () =&gt; {
    it(&apos;handles corrupted JSON gracefully&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, &apos;{broken json&apos;);
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.empty&apos;);
      cy.get(&apos;#search-input&apos;).type(&apos;test&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
      cy.get(&apos;#search-input&apos;).clear();
      cy.window().should(win =&gt; {
        expect(win.sessionStorage.getItem(STORAGE_KEY)).to.be.null;
      });
    });

    it(&apos;ignores stale data (&gt;30 min old)&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          query: &apos;old query&apos;,
          timestamp: Date.now() - (31 * 60 * 1000),
          path: &apos;/Simple-Jekyll-Search/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.empty&apos;);
      cy.get(&apos;#search-input&apos;).type(&apos;test&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
      cy.get(&apos;#search-input&apos;).clear();
      cy.window().should(win =&gt; {
        expect(win.sessionStorage.getItem(STORAGE_KEY)).to.be.null;
      });
    });

    it(&apos;ignores storage from different page path&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          query: &apos;other page query&apos;,
          timestamp: Date.now(),
          path: &apos;/different-page/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;&apos;);
      cy.get(&apos;#search-input&apos;).type(&apos;test&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
      cy.get(&apos;#search-input&apos;).clear();
      cy.window().should(win =&gt; {
        expect(win.sessionStorage.getItem(STORAGE_KEY)).to.be.null;
      });
    });

    it(&apos;handles missing query field&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          timestamp: Date.now(),
          path: &apos;/Simple-Jekyll-Search/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;&apos;);
    });

    it(&apos;handles non-string query field&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          query: 12345,
          timestamp: Date.now(),
          path: &apos;/Simple-Jekyll-Search/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;&apos;);
    });
  });

  describe(&apos;back navigation flow&apos;, () =&gt; {
    it(&apos;preserves search input and results after navigating back from a result link&apos;, () =&gt; {
      const searchQuery = &apos;Lorem ipsum&apos;;
      cy.get(&apos;#search-input&apos;).type(searchQuery);
      cy.get(&apos;#results-container&apos;)
        .should(&apos;be.visible&apos;)
        .contains(&apos;This is just a test&apos;)
        .should(&apos;exist&apos;);
      cy.get(&apos;#results-container&apos;).invoke(&apos;html&apos;).as(&apos;originalResults&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;This is just a test&apos;)
        .click();
      cy.url().should(&apos;include&apos;, &apos;?query=Lorem%20ipsum&apos;);
      cy.url().should(&apos;not.eq&apos;, Cypress.config().baseUrl + &apos;/&apos;);
      cy.go(&apos;back&apos;);
      cy.url().should(&apos;include&apos;, &apos;/Simple-Jekyll-Search&apos;);
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, searchQuery);
      cy.get(&apos;#results-container&apos;)
        .should(&apos;be.visible&apos;)
        .should(&apos;not.be.empty&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;This is just a test&apos;)
        .should(&apos;exist&apos;);
    });

    it(&apos;preserves highlighted search results after navigating back&apos;, () =&gt; {
      const searchQuery = &apos;Lorem&apos;;
      cy.get(&apos;#search-input&apos;).type(searchQuery);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;).should(&apos;exist&apos;);
      cy.get(&apos;#results-container a&apos;)
        .first()
        .click();
      cy.go(&apos;back&apos;);
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, searchQuery);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;).should(&apos;exist&apos;);
    });
  });

  describe(&apos;data within valid threshold&apos;, () =&gt; {
    it(&apos;restores data that is 29 minutes old&apos;, () =&gt; {
      cy.window().then(win =&gt; {
        win.sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
          query: &apos;Lorem&apos;,
          timestamp: Date.now() - (29 * 60 * 1000),
          path: &apos;/Simple-Jekyll-Search/&apos;
        }));
      });
      cy.reload();
      cy.get(&apos;#search-input&apos;).should(&apos;have.value&apos;, &apos;Lorem&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;not.be.empty&apos;);
    });
  });
});</file><file path="cypress/e2e/simple-jekyll-search.cy.ts">describe(&apos;Simple Jekyll Search&apos;, () =&gt; {
  beforeEach(() =&gt; {
    cy.visit(&apos;/&apos;);
  });

  it(&apos;Searching a Post&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;).type(&apos;This&apos;);
    cy.get(&apos;#results-container&apos;).contains(&apos;This is just a test&apos;);
  });

  it(&apos;Searching a Post follows link with query&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;).type(&apos;Lorem ipsum&apos;);
    cy.get(&apos;#results-container&apos;)
      .contains(&apos;This is just a test&apos;)
      .should(&apos;have.length&apos;, 1)
      .click();
    cy.url().should(&apos;include&apos;, &apos;?query=Lorem%20ipsum&apos;);
  });

  it(&apos;No results found&apos;, () =&gt; {
    cy.get(&apos;#search-input&apos;).type(&apos;xyzabc123notfound&apos;);
    cy.get(&apos;#results-container&apos;).should(&apos;contain&apos;, &apos;No results found&apos;);
  });

  describe(&apos;Search Functionality Edge cases&apos;, () =&gt; {
    it(&apos;Searches for &quot;sed -i hostname&quot;&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;sed -i hostname&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;Technical Example&apos;)
        .should(&apos;exist&apos;);
    });

    it(&apos;Searches for &quot;New York&quot;&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;New York&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;Technical Example&apos;)
        .should(&apos;exist&apos;);
    });

    it(&apos;Searches for special characters&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;~!@#$%^&amp;&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;Technical Example&apos;)
        .should(&apos;exist&apos;);
    });
  });

  describe(&apos;Hybrid Strategy with Highlighting&apos;, () =&gt; {
    it(&apos;should use literal search and highlight exact matches&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;Lorem&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.visible&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;This is just a test&apos;)
        .should(&apos;exist&apos;);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;)
        .should(&apos;exist&apos;)
        .should(&apos;have.css&apos;, &apos;background-color&apos;, &apos;rgb(255, 255, 0)&apos;);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;)
        .filter(&apos;:contains(&quot;Lorem&quot;)&apos;)
        .should(&apos;have.length.at.least&apos;, 1);
    });

    it(&apos;should use literal search for multi-word queries and highlight&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;Lorem ipsum&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.visible&apos;);
      cy.get(&apos;#results-container&apos;)
        .contains(&apos;This is just a test&apos;)
        .should(&apos;exist&apos;);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;).should(&apos;have.length.at.least&apos;, 1);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;)
        .filter(&apos;:contains(&quot;Lorem&quot;)&apos;)
        .should(&apos;exist&apos;);
    });

    it(&apos;should handle different search patterns with hybrid strategy&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;)
        .clear()
        .type(&apos;ipsum&apos;);
      cy.get(&apos;#results-container li&apos;).should(&apos;have.length.at.least&apos;, 1);
      cy.get(&apos;#results-container&apos;).should(&apos;contain.text&apos;, &apos;ipsum&apos;);
    });

    it(&apos;should handle partial matches with hybrid strategy&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;)
        .clear()
        .type(&apos;technical&apos;);
      cy.get(&apos;#results-container li&apos;).should(&apos;have.length.at.least&apos;, 1);
      cy.get(&apos;#results-container&apos;).should(&apos;contain.text&apos;, &apos;Technical&apos;);
    });

    it(&apos;should escape HTML in search results&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;sed&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.visible&apos;);
      cy.get(&apos;#results-container .search-desc&apos;)
        .should(&apos;exist&apos;)
        .and(&apos;not.contain&apos;, &apos;&lt;script&gt;&apos;);
    });

    it(&apos;should highlight matches, preserve valid URLs, and navigate correctly&apos;, () =&gt; {
      cy.get(&apos;#search-input&apos;).type(&apos;test&apos;);
      cy.get(&apos;#results-container&apos;).should(&apos;be.visible&apos;);
      cy.get(&apos;#results-container .search-desc .search-highlight&apos;).should(&apos;have.length.at.least&apos;, 1);
      cy.get(&apos;#results-container a&apos;)
        .contains(&apos;This is just a test&apos;)
        .should(&apos;have.attr&apos;, &apos;href&apos;)
        .and(&apos;match&apos;, /\/2014\/11\/02\/test\.html\?query=test/);
      cy.get(&apos;#results-container a&apos;)
        .contains(&apos;This is just a test&apos;)
        .click();
      cy.url().should(&apos;include&apos;, &apos;/2014/11/02/test.html&apos;);
      cy.url().should(&apos;include&apos;, &apos;?query=test&apos;);
    });
  });
});</file><file path="cypress/support/commands.ts">/**
 * Custom Cypress commands.
 * @see https://on.cypress.io/custom-commands
 */</file><file path="cypress/support/e2e.ts">// Import commands.js using ES2015 syntax:
import &apos;./commands&apos;;

// Hide XHR requests from command log
const app = window.top as Window &amp; typeof globalThis;
if (app) {
  app.console.log = () =&gt; {};
}</file><file path="cypress/support/index.ts">/**
 * Cypress support file - loaded automatically before test files.
 * @see https://on.cypress.io/configuration
 */
import &apos;./commands&apos;;</file><file path="cypress/tsconfig.json">{
  &quot;compilerOptions&quot;: {
    &quot;target&quot;: &quot;es2020&quot;,
    &quot;module&quot;: &quot;es2020&quot;,
    &quot;lib&quot;: [&quot;es2020&quot;, &quot;dom&quot;],
    &quot;types&quot;: [&quot;cypress&quot;, &quot;node&quot;],
    &quot;moduleResolution&quot;: &quot;bundler&quot;,
    &quot;allowJs&quot;: true,
    &quot;esModuleInterop&quot;: true,
    &quot;strict&quot;: true,
    &quot;skipLibCheck&quot;: true,
    &quot;isolatedModules&quot;: true,
    &quot;noEmit&quot;: true
  },
  &quot;include&quot;: [&quot;**/*.ts&quot;]
}</file><file path="dest/simple-jekyll-search.js">(function(global, factory) {
  typeof exports === &quot;object&quot; &amp;&amp; typeof module !== &quot;undefined&quot; ? factory(exports) : typeof define === &quot;function&quot; &amp;&amp; define.amd ? define([&quot;exports&quot;], factory) : (global = typeof globalThis !== &quot;undefined&quot; ? globalThis : global || self, factory(global.SimpleJekyllSearch = {}));
})(this, (function(exports2) {
  &quot;use strict&quot;;
  function load(location, callback) {
    const xhr = getXHR();
    xhr.open(&quot;GET&quot;, location, true);
    xhr.onreadystatechange = createStateChangeListener(xhr, callback);
    xhr.send();
  }
  function createStateChangeListener(xhr, callback) {
    return function() {
      if (xhr.readyState === 4 &amp;&amp; xhr.status === 200) {
        try {
          callback(null, JSON.parse(xhr.responseText));
        } catch (err) {
          callback(err instanceof Error ? err : new Error(String(err)), null);
        }
      }
    };
  }
  function getXHR() {
    return window.XMLHttpRequest ? new window.XMLHttpRequest() : new window.ActiveXObject(&quot;Microsoft.XMLHTTP&quot;);
  }
  class OptionsValidator {
    constructor(params) {
      if (!this.validateParams(params)) {
        throw new Error(&quot;-- OptionsValidator: required options missing&quot;);
      }
      this.requiredOptions = params.required;
    }
    getRequiredOptions() {
      return this.requiredOptions;
    }
    validate(parameters) {
      const errors = [];
      this.requiredOptions.forEach((requiredOptionName) =&gt; {
        if (typeof parameters[requiredOptionName] === &quot;undefined&quot;) {
          errors.push(requiredOptionName);
        }
      });
      return errors;
    }
    validateParams(params) {
      if (!params) {
        return false;
      }
      return typeof params.required !== &quot;undefined&quot; &amp;&amp; Array.isArray(params.required);
    }
  }
  function findLiteralMatches(text, criteria) {
    const lowerText = text.trim().toLowerCase();
    const pattern = criteria.endsWith(&quot; &quot;) ? [criteria.toLowerCase()] : criteria.trim().toLowerCase().split(&quot; &quot;);
    const wordsFound = pattern.filter((word) =&gt; lowerText.indexOf(word) &gt;= 0).length;
    if (wordsFound !== pattern.length) {
      return [];
    }
    const matches = [];
    for (const word of pattern) {
      if (!word || word.length === 0) continue;
      let startIndex = 0;
      while ((startIndex = lowerText.indexOf(word, startIndex)) !== -1) {
        matches.push({
          start: startIndex,
          end: startIndex + word.length,
          text: text.substring(startIndex, startIndex + word.length),
          type: &quot;exact&quot;
        });
        startIndex += word.length;
      }
    }
    return matches;
  }
  function findFuzzyMatches(text, criteria) {
    criteria = criteria.trimEnd();
    if (criteria.length === 0) return [];
    const lowerText = text.toLowerCase();
    const lowerCriteria = criteria.toLowerCase();
    let textIndex = 0;
    let criteriaIndex = 0;
    const matchedIndices = [];
    while (textIndex &lt; text.length &amp;&amp; criteriaIndex &lt; criteria.length) {
      if (lowerText[textIndex] === lowerCriteria[criteriaIndex]) {
        matchedIndices.push(textIndex);
        criteriaIndex++;
      }
      textIndex++;
    }
    if (criteriaIndex !== criteria.length) {
      return [];
    }
    if (matchedIndices.length === 0) {
      return [];
    }
    const start = matchedIndices[0];
    const end = matchedIndices[matchedIndices.length - 1] + 1;
    return [{
      start,
      end,
      text: text.substring(start, end),
      type: &quot;fuzzy&quot;
    }];
  }
  function findWildcardMatches(text, pattern, config = {}) {
    const regexPattern = pattern.replace(/\*/g, buildWildcardFragment(config));
    const regex = new RegExp(regexPattern, &quot;gi&quot;);
    const matches = [];
    let match;
    while ((match = regex.exec(text)) !== null) {
      matches.push({
        start: match.index,
        end: match.index + match[0].length,
        text: match[0],
        type: &quot;wildcard&quot;
      });
      if (regex.lastIndex === match.index) {
        regex.lastIndex++;
      }
    }
    return matches;
  }
  function buildWildcardFragment(config) {
    const maxSpaces = normalizeMaxSpaces(config.maxSpaces);
    if (maxSpaces === 0) {
      return &quot;[^ ]*&quot;;
    }
    if (maxSpaces === Infinity) {
      return &quot;[^ ]*(?: [^ ]*)*&quot;;
    }
    return `[^ ]*(?: [^ ]*){0,${maxSpaces}}`;
  }
  function normalizeMaxSpaces(value) {
    if (typeof value !== &quot;number&quot; || Number.isNaN(value) || value &lt;= 0) {
      return 0;
    }
    if (!Number.isFinite(value)) {
      return Infinity;
    }
    return Math.floor(value);
  }
  class SearchStrategy {
    constructor(findMatchesFunction) {
      this.findMatchesFunction = findMatchesFunction;
    }
    matches(text, criteria) {
      if (text === null || text.trim() === &quot;&quot; || !criteria) {
        return false;
      }
      const matchInfo = this.findMatchesFunction(text, criteria);
      return matchInfo.length &gt; 0;
    }
    findMatches(text, criteria) {
      if (text === null || text.trim() === &quot;&quot; || !criteria) {
        return [];
      }
      return this.findMatchesFunction(text, criteria);
    }
  }
  const LiteralSearchStrategy = new SearchStrategy(
    findLiteralMatches
  );
  const FuzzySearchStrategy = new SearchStrategy(
    (text, criteria) =&gt; {
      const fuzzyMatches = findFuzzyMatches(text, criteria);
      if (fuzzyMatches.length &gt; 0) {
        return fuzzyMatches;
      }
      return findLiteralMatches(text, criteria);
    }
  );
  class WildcardSearchStrategy extends SearchStrategy {
    constructor(config = {}) {
      const normalizedConfig = { ...config };
      super((text, criteria) =&gt; {
        const wildcardMatches = findWildcardMatches(text, criteria, normalizedConfig);
        if (wildcardMatches.length &gt; 0) {
          return wildcardMatches;
        }
        return findLiteralMatches(text, criteria);
      });
      this.config = normalizedConfig;
    }
    getConfig() {
      return { ...this.config };
    }
  }
  new WildcardSearchStrategy();
  class HybridSearchStrategy extends SearchStrategy {
    constructor(config = {}) {
      super((text, criteria) =&gt; {
        return this.hybridFind(text, criteria);
      });
      this.config = {
        ...config,
        preferFuzzy: config.preferFuzzy ?? false,
        wildcardPriority: config.wildcardPriority ?? true,
        minFuzzyLength: config.minFuzzyLength ?? 4,
        maxExtraFuzzyChars: config.maxExtraFuzzyChars ?? 2,
        maxSpaces: config.maxSpaces ?? 1
      };
    }
    hybridFind(text, criteria) {
      if (this.config.wildcardPriority &amp;&amp; criteria.includes(&quot;*&quot;)) {
        const wildcardMatches = findWildcardMatches(text, criteria, this.config);
        if (wildcardMatches.length &gt; 0) return wildcardMatches;
      }
      if (criteria.includes(&quot; &quot;) || criteria.length &lt; this.config.minFuzzyLength) {
        const literalMatches = findLiteralMatches(text, criteria);
        if (literalMatches.length &gt; 0) return literalMatches;
      }
      if (this.config.preferFuzzy || criteria.length &gt;= this.config.minFuzzyLength) {
        const fuzzyMatches = findFuzzyMatches(text, criteria);
        if (fuzzyMatches.length &gt; 0) {
          const constrainedMatches = this.applyFuzzyConstraints(fuzzyMatches, criteria);
          if (constrainedMatches.length &gt; 0) return constrainedMatches;
        }
      }
      return findLiteralMatches(text, criteria);
    }
    applyFuzzyConstraints(matches, criteria) {
      const limit = this.config.maxExtraFuzzyChars;
      if (!Number.isFinite(limit) || limit &lt; 0) {
        return matches;
      }
      const normalizedCriteriaLength = this.normalizeLength(criteria);
      if (normalizedCriteriaLength === 0) {
        return matches;
      }
      return matches.filter((match) =&gt; {
        const normalizedMatchLength = this.normalizeLength(match.text);
        const extraChars = Math.max(0, normalizedMatchLength - normalizedCriteriaLength);
        return extraChars &lt;= limit;
      });
    }
    normalizeLength(value) {
      return value.replace(/\s+/g, &quot;&quot;).length;
    }
  }
  const DefaultHybridSearchStrategy = new HybridSearchStrategy();
  class StrategyFactory {
    static create(config = { type: &quot;literal&quot; }) {
      const { options: options2 } = config;
      const type = this.isValidStrategy(config.type) ? config.type : &quot;literal&quot;;
      switch (type) {
        case &quot;literal&quot;:
          return LiteralSearchStrategy;
        case &quot;fuzzy&quot;:
          return FuzzySearchStrategy;
        case &quot;wildcard&quot;:
          return new WildcardSearchStrategy(options2);
        case &quot;hybrid&quot;:
          return new HybridSearchStrategy(options2);
        default:
          return LiteralSearchStrategy;
      }
    }
    static getAvailableStrategies() {
      return [&quot;literal&quot;, &quot;fuzzy&quot;, &quot;wildcard&quot;, &quot;hybrid&quot;];
    }
    static isValidStrategy(type) {
      return this.getAvailableStrategies().includes(type);
    }
  }
  function merge(target, source) {
    return { ...target, ...source };
  }
  function isJSON(json) {
    return Array.isArray(json) || json !== null &amp;&amp; typeof json === &quot;object&quot;;
  }
  function NoSort() {
    return 0;
  }
  function isObject(obj) {
    return Boolean(obj) &amp;&amp; Object.prototype.toString.call(obj) === &quot;[object Object]&quot;;
  }
  const DEFAULT_OPTIONS = {
    searchInput: null,
    resultsContainer: null,
    json: [],
    success: function() {
    },
    searchResultTemplate: &apos;&lt;li&gt;&lt;a href=&quot;{url}&quot; title=&quot;{desc}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,
    templateMiddleware: (_prop, _value, _template) =&gt; void 0,
    sortMiddleware: NoSort,
    noResultsText: &quot;No results found&quot;,
    limit: 10,
    strategy: &quot;literal&quot;,
    debounceTime: null,
    exclude: [],
    onSearch: () =&gt; {
    },
    onError: (error) =&gt; console.error(&quot;SimpleJekyllSearch error:&quot;, error),
    fuzzy: false
    // Deprecated, use strategy: &apos;fuzzy&apos; instead
  };
  const REQUIRED_OPTIONS = [&quot;searchInput&quot;, &quot;resultsContainer&quot;, &quot;json&quot;];
  const WHITELISTED_KEYS = /* @__PURE__ */ new Set([
    &quot;Enter&quot;,
    &quot;Shift&quot;,
    &quot;CapsLock&quot;,
    &quot;ArrowLeft&quot;,
    &quot;ArrowUp&quot;,
    &quot;ArrowRight&quot;,
    &quot;ArrowDown&quot;,
    &quot;Meta&quot;
  ]);
  class Repository {
    constructor(initialOptions = {}) {
      this.data = [];
      this.excludePatterns = [];
      this.setOptions(initialOptions);
    }
    put(input) {
      if (isObject(input)) {
        return this.addObject(input);
      }
      if (Array.isArray(input)) {
        return this.addArray(input);
      }
      return void 0;
    }
    clear() {
      this.data.length = 0;
      return this.data;
    }
    search(criteria) {
      if (!criteria) {
        return [];
      }
      const matches = this.findMatches(this.data, criteria).sort(this.options.sortMiddleware);
      return matches.map((item) =&gt; ({ ...item }));
    }
    setOptions(newOptions) {
      let strategyConfig = this.normalizeStrategyOption(newOptions?.strategy ?? DEFAULT_OPTIONS.strategy);
      if (newOptions?.fuzzy &amp;&amp; !newOptions?.strategy) {
        console.warn(&apos;[Simple Jekyll Search] Warning: fuzzy option is deprecated. Use strategy: &quot;fuzzy&quot; instead.&apos;);
        strategyConfig = { type: &quot;fuzzy&quot; };
      }
      const exclude = newOptions?.exclude || DEFAULT_OPTIONS.exclude;
      this.excludePatterns = exclude.map((pattern) =&gt; new RegExp(pattern));
      this.options = {
        limit: newOptions?.limit || DEFAULT_OPTIONS.limit,
        searchStrategy: this.searchStrategy(strategyConfig),
        sortMiddleware: newOptions?.sortMiddleware || DEFAULT_OPTIONS.sortMiddleware,
        exclude,
        strategy: strategyConfig
      };
    }
    addObject(obj) {
      this.data.push(obj);
      return this.data;
    }
    addArray(arr) {
      const added = [];
      this.clear();
      for (const item of arr) {
        if (isObject(item)) {
          added.push(this.addObject(item)[0]);
        }
      }
      return added;
    }
    findMatches(data, criteria) {
      const matches = [];
      for (let i = 0; i &lt; data.length &amp;&amp; matches.length &lt; this.options.limit; i++) {
        const match = this.findMatchesInObject(data[i], criteria);
        if (match) {
          matches.push(match);
        }
      }
      return matches;
    }
    findMatchesInObject(obj, criteria) {
      let hasMatch = false;
      const result = { ...obj };
      result._matchInfo = {};
      for (const key in obj) {
        if (!this.isExcluded(obj[key]) &amp;&amp; this.options.searchStrategy.matches(obj[key], criteria)) {
          hasMatch = true;
          if (this.options.searchStrategy.findMatches) {
            const matchInfo = this.options.searchStrategy.findMatches(obj[key], criteria);
            if (matchInfo &amp;&amp; matchInfo.length &gt; 0) {
              result._matchInfo[key] = matchInfo;
            }
          }
        }
      }
      return hasMatch ? result : void 0;
    }
    isExcluded(term) {
      const termStr = String(term);
      return this.excludePatterns.some((regex) =&gt; regex.test(termStr));
    }
    searchStrategy(strategy) {
      if (!strategy?.type || !StrategyFactory.isValidStrategy(strategy.type)) {
        return LiteralSearchStrategy;
      }
      return StrategyFactory.create(strategy);
    }
    normalizeStrategyOption(strategy) {
      if (!strategy) {
        return this.getDefaultStrategyConfig();
      }
      return typeof strategy === &quot;string&quot; ? { type: strategy } : strategy;
    }
    getDefaultStrategyConfig() {
      const defaultStrategy = DEFAULT_OPTIONS.strategy;
      {
        return { type: defaultStrategy };
      }
    }
  }
  const options = {
    pattern: /\{(.*?)\}/g,
    template: &quot;&quot;,
    middleware: function() {
      return void 0;
    }
  };
  function setOptions(_options) {
    if (_options.pattern) {
      options.pattern = _options.pattern;
    }
    if (_options.template) {
      options.template = _options.template;
    }
    if (typeof _options.middleware === &quot;function&quot;) {
      options.middleware = _options.middleware;
    }
  }
  function compile(data, query) {
    return options.template.replace(options.pattern, function(match, prop) {
      const matchInfo = data._matchInfo?.[prop];
      if (matchInfo &amp;&amp; matchInfo.length &gt; 0 &amp;&amp; query) {
        const value2 = options.middleware(prop, data[prop], options.template, query, matchInfo);
        if (typeof value2 !== &quot;undefined&quot;) {
          return value2;
        }
      }
      if (query) {
        const value2 = options.middleware(prop, data[prop], options.template, query);
        if (typeof value2 !== &quot;undefined&quot;) {
          return value2;
        }
      }
      const value = options.middleware(prop, data[prop], options.template);
      if (typeof value !== &quot;undefined&quot;) {
        return value;
      }
      return data[prop] || match;
    });
  }
  let SimpleJekyllSearch$1 = class SimpleJekyllSearch {
    constructor() {
      this.debounceTimerHandle = null;
      this.eventHandler = null;
      this.pageShowHandler = null;
      this.pendingRequest = null;
      this.isInitialized = false;
      this.STORAGE_KEY = &quot;sjs-search-state&quot;;
      this.options = { ...DEFAULT_OPTIONS };
      this.repository = new Repository();
      this.optionsValidator = new OptionsValidator({
        required: REQUIRED_OPTIONS
      });
    }
    debounce(func, delayMillis) {
      if (delayMillis) {
        if (this.debounceTimerHandle) {
          clearTimeout(this.debounceTimerHandle);
        }
        this.debounceTimerHandle = setTimeout(func, delayMillis);
      } else {
        func();
      }
    }
    throwError(message) {
      throw new Error(`SimpleJekyllSearch --- ${message}`);
    }
    emptyResultsContainer() {
      this.options.resultsContainer.innerHTML = &quot;&quot;;
    }
    initWithJSON(json) {
      this.repository.put(json);
      this.registerInput();
    }
    initWithURL(url) {
      load(url, (err, json) =&gt; {
        if (err) {
          this.throwError(`Failed to load JSON from ${url}: ${err.message}`);
        }
        this.initWithJSON(json);
      });
    }
    registerInput() {
      this.eventHandler = (e) =&gt; {
        try {
          const inputEvent = e;
          if (!WHITELISTED_KEYS.has(inputEvent.key)) {
            this.emptyResultsContainer();
            this.debounce(() =&gt; {
              try {
                this.search(e.target.value);
              } catch (searchError) {
                console.error(&quot;Search error:&quot;, searchError);
                this.options.onError?.(searchError);
              }
            }, this.options.debounceTime ?? null);
          }
        } catch (error) {
          console.error(&quot;Input handler error:&quot;, error);
          this.options.onError?.(error);
        }
      };
      this.options.searchInput.addEventListener(&quot;input&quot;, this.eventHandler);
      this.pageShowHandler = () =&gt; {
        this.restoreSearchState();
      };
      window.addEventListener(&quot;pageshow&quot;, this.pageShowHandler);
      this.restoreSearchState();
    }
    saveSearchState(query) {
      if (!query?.trim()) {
        this.clearSearchState();
        return;
      }
      try {
        const state = {
          query: query.trim(),
          timestamp: Date.now(),
          path: window.location.pathname
        };
        sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(state));
      } catch {
      }
    }
    getStoredSearchState() {
      try {
        const raw = sessionStorage.getItem(this.STORAGE_KEY);
        if (!raw) return null;
        const state = JSON.parse(raw);
        if (typeof state?.query !== &quot;string&quot;) return null;
        const MAX_AGE_MS = 30 * 60 * 1e3;
        if (Date.now() - state.timestamp &gt; MAX_AGE_MS) {
          this.clearSearchState();
          return null;
        }
        if (state.path &amp;&amp; state.path !== window.location.pathname) {
          this.clearSearchState();
          return null;
        }
        return state.query;
      } catch {
        this.clearSearchState();
        return null;
      }
    }
    clearSearchState() {
      try {
        sessionStorage.removeItem(this.STORAGE_KEY);
      } catch {
      }
    }
    restoreSearchState() {
      const hasExistingResults = this.options.resultsContainer.children.length &gt; 0;
      if (hasExistingResults) return;
      let query = this.options.searchInput.value?.trim();
      if (!query) {
        query = this.getStoredSearchState() || &quot;&quot;;
      }
      if (query.length &gt; 0) {
        this.options.searchInput.value = query;
        this.search(query);
      }
    }
    search(query) {
      if (query?.trim().length &gt; 0) {
        this.saveSearchState(query);
        this.emptyResultsContainer();
        const results = this.repository.search(query);
        this.render(results, query);
        this.options.onSearch?.();
      } else {
        this.clearSearchState();
      }
    }
    render(results, query) {
      if (results.length === 0) {
        this.options.resultsContainer.insertAdjacentHTML(&quot;beforeend&quot;, this.options.noResultsText);
        return;
      }
      const fragment = document.createDocumentFragment();
      results.forEach((result) =&gt; {
        result.query = query;
        const div = document.createElement(&quot;div&quot;);
        div.innerHTML = compile(result, query);
        fragment.appendChild(div);
      });
      this.options.resultsContainer.appendChild(fragment);
    }
    destroy() {
      if (this.eventHandler) {
        this.options.searchInput.removeEventListener(&quot;input&quot;, this.eventHandler);
        this.eventHandler = null;
      }
      if (this.pageShowHandler) {
        window.removeEventListener(&quot;pageshow&quot;, this.pageShowHandler);
        this.pageShowHandler = null;
      }
      if (this.debounceTimerHandle) {
        clearTimeout(this.debounceTimerHandle);
        this.debounceTimerHandle = null;
      }
      this.clearSearchState();
    }
    init(_options) {
      const errors = this.optionsValidator.validate(_options);
      if (errors.length &gt; 0) {
        this.throwError(`Missing required options: ${REQUIRED_OPTIONS.join(&quot;, &quot;)}`);
      }
      this.options = merge(this.options, _options);
      setOptions({
        template: this.options.searchResultTemplate,
        middleware: this.options.templateMiddleware
      });
      this.repository.setOptions({
        limit: this.options.limit,
        sortMiddleware: this.options.sortMiddleware,
        strategy: this.options.strategy,
        exclude: this.options.exclude
      });
      if (isJSON(this.options.json)) {
        this.initWithJSON(this.options.json);
      } else {
        this.initWithURL(this.options.json);
      }
      const rv = {
        search: this.search.bind(this),
        destroy: this.destroy.bind(this)
      };
      this.options.success?.call(rv);
      return rv;
    }
  };
  function escapeHtml(text) {
    const map = {
      &quot;&amp;&quot;: &quot;&amp;amp;&quot;,
      &quot;&lt;&quot;: &quot;&amp;lt;&quot;,
      &quot;&gt;&quot;: &quot;&amp;gt;&quot;,
      &apos;&quot;&apos;: &quot;&amp;quot;&quot;,
      &quot;&apos;&quot;: &quot;&amp;#039;&quot;
    };
    return text.replace(/[&amp;&lt;&gt;&quot;&apos;]/g, (m) =&gt; map[m]);
  }
  function mergeOverlappingMatches(matches) {
    if (matches.length === 0) return [];
    const sorted = [...matches].sort((a, b) =&gt; a.start - b.start);
    const merged = [{ ...sorted[0] }];
    for (let i = 1; i &lt; sorted.length; i++) {
      const current = sorted[i];
      const last = merged[merged.length - 1];
      if (current.start &lt;= last.end) {
        last.end = Math.max(last.end, current.end);
      } else {
        merged.push({ ...current });
      }
    }
    return merged;
  }
  function highlightWithMatchInfo(text, matchInfo, options2 = {}) {
    if (!text || matchInfo.length === 0) {
      return escapeHtml(text);
    }
    const className = options2.className || &quot;search-highlight&quot;;
    const maxLength = options2.maxLength;
    const mergedMatches = mergeOverlappingMatches(matchInfo);
    let result = &quot;&quot;;
    let lastIndex = 0;
    for (const match of mergedMatches) {
      result += escapeHtml(text.substring(lastIndex, match.start));
      result += `&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(text.substring(match.start, match.end))}&lt;/span&gt;`;
      lastIndex = match.end;
    }
    result += escapeHtml(text.substring(lastIndex));
    if (maxLength &amp;&amp; result.length &gt; maxLength) {
      result = truncateAroundMatches(text, mergedMatches, maxLength, options2.contextLength || 30, className);
    }
    return result;
  }
  function truncateAroundMatches(text, matches, maxLength, contextLength, className) {
    if (matches.length === 0) {
      const truncated = text.substring(0, maxLength - 3);
      return escapeHtml(truncated) + &quot;...&quot;;
    }
    const firstMatch = matches[0];
    const start = Math.max(0, firstMatch.start - contextLength);
    const end = Math.min(text.length, firstMatch.end + contextLength);
    let result = &quot;&quot;;
    if (start &gt; 0) {
      result += &quot;...&quot;;
    }
    const snippet = text.substring(start, end);
    const adjustedMatches = matches.filter((m) =&gt; m.start &lt; end &amp;&amp; m.end &gt; start).map((m) =&gt; ({
      ...m,
      start: Math.max(0, m.start - start),
      end: Math.min(snippet.length, m.end - start)
    }));
    let lastIndex = 0;
    for (const match of adjustedMatches) {
      result += escapeHtml(snippet.substring(lastIndex, match.start));
      result += `&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(snippet.substring(match.start, match.end))}&lt;/span&gt;`;
      lastIndex = match.end;
    }
    result += escapeHtml(snippet.substring(lastIndex));
    if (end &lt; text.length) {
      result += &quot;...&quot;;
    }
    return result;
  }
  const DEFAULT_TRUNCATE_FIELDS = [&quot;content&quot;, &quot;desc&quot;, &quot;description&quot;];
  const DEFAULT_NO_HIGHLIGHT_FIELDS = [&quot;url&quot;, &quot;link&quot;, &quot;href&quot;, &quot;query&quot;];
  function createHighlightTemplateMiddleware(options2 = {}) {
    const highlightOptions = {
      className: options2.className || &quot;search-highlight&quot;,
      maxLength: options2.maxLength,
      contextLength: options2.contextLength || 30
    };
    const truncateFields = options2.truncateFields || DEFAULT_TRUNCATE_FIELDS;
    const noHighlightFields = options2.noHighlightFields || DEFAULT_NO_HIGHLIGHT_FIELDS;
    return function(prop, value, _template, query, matchInfo) {
      if (typeof value !== &quot;string&quot;) {
        return void 0;
      }
      if (noHighlightFields.includes(prop)) {
        return void 0;
      }
      const shouldTruncate = truncateFields.includes(prop);
      if (matchInfo &amp;&amp; matchInfo.length &gt; 0 &amp;&amp; query) {
        const fieldOptions = {
          ...highlightOptions,
          maxLength: shouldTruncate ? highlightOptions.maxLength : void 0
        };
        const highlighted = highlightWithMatchInfo(value, matchInfo, fieldOptions);
        return highlighted !== value ? highlighted : void 0;
      }
      if (shouldTruncate &amp;&amp; highlightOptions.maxLength &amp;&amp; value.length &gt; highlightOptions.maxLength) {
        return escapeHtml(value.substring(0, highlightOptions.maxLength - 3) + &quot;...&quot;);
      }
      return void 0;
    };
  }
  function defaultHighlightMiddleware(prop, value, template, query, matchInfo) {
    const middleware = createHighlightTemplateMiddleware();
    return middleware(prop, value, template, query, matchInfo);
  }
  function SimpleJekyllSearch(options2) {
    const instance = new SimpleJekyllSearch$1();
    return instance.init(options2);
  }
  if (typeof window !== &quot;undefined&quot;) {
    window.SimpleJekyllSearch = SimpleJekyllSearch;
    window.createHighlightTemplateMiddleware = createHighlightTemplateMiddleware;
  }
  exports2.DefaultHybridSearchStrategy = DefaultHybridSearchStrategy;
  exports2.HybridSearchStrategy = HybridSearchStrategy;
  exports2.StrategyFactory = StrategyFactory;
  exports2.createHighlightTemplateMiddleware = createHighlightTemplateMiddleware;
  exports2.default = SimpleJekyllSearch;
  exports2.defaultHighlightMiddleware = defaultHighlightMiddleware;
  exports2.escapeHtml = escapeHtml;
  exports2.highlightWithMatchInfo = highlightWithMatchInfo;
  exports2.mergeOverlappingMatches = mergeOverlappingMatches;
  Object.defineProperties(exports2, { __esModule: { value: true }, [Symbol.toStringTag]: { value: &quot;Module&quot; } });
}));</file><file path="dest/simple-jekyll-search.min.js">/*!
  * Simple-Jekyll-Search v2.1.1
  * Copyright 2015-2022, Christian Fei
  * Copyright 2025-2026, Sylhare
  * Licensed under the MIT License.
  */
(function(global,factory){typeof exports===&quot;object&quot;&amp;&amp;typeof module!==&quot;undefined&quot;?factory(exports):typeof define===&quot;function&quot;&amp;&amp;define.amd?define([&quot;exports&quot;],factory):(global=typeof globalThis!==&quot;undefined&quot;?globalThis:global||self,factory(global.SimpleJekyllSearch={}))})(this,function(exports2){&quot;use strict&quot;;function load(location,callback){const xhr=getXHR();xhr.open(&quot;GET&quot;,location,true);xhr.onreadystatechange=createStateChangeListener(xhr,callback);xhr.send()}function createStateChangeListener(xhr,callback){return function(){if(xhr.readyState===4&amp;&amp;xhr.status===200){try{callback(null,JSON.parse(xhr.responseText))}catch(err){callback(err instanceof Error?err:new Error(String(err)),null)}}}}function getXHR(){return window.XMLHttpRequest?new window.XMLHttpRequest:new window.ActiveXObject(&quot;Microsoft.XMLHTTP&quot;)}class OptionsValidator{constructor(params){if(!this.validateParams(params)){throw new Error(&quot;-- OptionsValidator: required options missing&quot;)}this.requiredOptions=params.required}getRequiredOptions(){return this.requiredOptions}validate(parameters){const errors=[];this.requiredOptions.forEach(requiredOptionName=&gt;{if(typeof parameters[requiredOptionName]===&quot;undefined&quot;){errors.push(requiredOptionName)}});return errors}validateParams(params){if(!params){return false}return typeof params.required!==&quot;undefined&quot;&amp;&amp;Array.isArray(params.required)}}function findLiteralMatches(text,criteria){const lowerText=text.trim().toLowerCase();const pattern=criteria.endsWith(&quot; &quot;)?[criteria.toLowerCase()]:criteria.trim().toLowerCase().split(&quot; &quot;);const wordsFound=pattern.filter(word=&gt;lowerText.indexOf(word)&gt;=0).length;if(wordsFound!==pattern.length){return[]}const matches=[];for(const word of pattern){if(!word||word.length===0)continue;let startIndex=0;while((startIndex=lowerText.indexOf(word,startIndex))!==-1){matches.push({start:startIndex,end:startIndex+word.length,text:text.substring(startIndex,startIndex+word.length),type:&quot;exact&quot;});startIndex+=word.length}}return matches}function findFuzzyMatches(text,criteria){criteria=criteria.trimEnd();if(criteria.length===0)return[];const lowerText=text.toLowerCase();const lowerCriteria=criteria.toLowerCase();let textIndex=0;let criteriaIndex=0;const matchedIndices=[];while(textIndex&lt;text.length&amp;&amp;criteriaIndex&lt;criteria.length){if(lowerText[textIndex]===lowerCriteria[criteriaIndex]){matchedIndices.push(textIndex);criteriaIndex++}textIndex++}if(criteriaIndex!==criteria.length){return[]}if(matchedIndices.length===0){return[]}const start=matchedIndices[0];const end=matchedIndices[matchedIndices.length-1]+1;return[{start:start,end:end,text:text.substring(start,end),type:&quot;fuzzy&quot;}]}function findWildcardMatches(text,pattern,config={}){const regexPattern=pattern.replace(/\*/g,buildWildcardFragment(config));const regex=new RegExp(regexPattern,&quot;gi&quot;);const matches=[];let match;while((match=regex.exec(text))!==null){matches.push({start:match.index,end:match.index+match[0].length,text:match[0],type:&quot;wildcard&quot;});if(regex.lastIndex===match.index){regex.lastIndex++}}return matches}function buildWildcardFragment(config){const maxSpaces=normalizeMaxSpaces(config.maxSpaces);if(maxSpaces===0){return&quot;[^ ]*&quot;}if(maxSpaces===Infinity){return&quot;[^ ]*(?: [^ ]*)*&quot;}return`[^ ]*(?: [^ ]*){0,${maxSpaces}}`}function normalizeMaxSpaces(value){if(typeof value!==&quot;number&quot;||Number.isNaN(value)||value&lt;=0){return 0}if(!Number.isFinite(value)){return Infinity}return Math.floor(value)}class SearchStrategy{constructor(findMatchesFunction){this.findMatchesFunction=findMatchesFunction}matches(text,criteria){if(text===null||text.trim()===&quot;&quot;||!criteria){return false}const matchInfo=this.findMatchesFunction(text,criteria);return matchInfo.length&gt;0}findMatches(text,criteria){if(text===null||text.trim()===&quot;&quot;||!criteria){return[]}return this.findMatchesFunction(text,criteria)}}const LiteralSearchStrategy=new SearchStrategy(findLiteralMatches);const FuzzySearchStrategy=new SearchStrategy((text,criteria)=&gt;{const fuzzyMatches=findFuzzyMatches(text,criteria);if(fuzzyMatches.length&gt;0){return fuzzyMatches}return findLiteralMatches(text,criteria)});class WildcardSearchStrategy extends SearchStrategy{constructor(config={}){const normalizedConfig={...config};super((text,criteria)=&gt;{const wildcardMatches=findWildcardMatches(text,criteria,normalizedConfig);if(wildcardMatches.length&gt;0){return wildcardMatches}return findLiteralMatches(text,criteria)});this.config=normalizedConfig}getConfig(){return{...this.config}}}new WildcardSearchStrategy;class HybridSearchStrategy extends SearchStrategy{constructor(config={}){super((text,criteria)=&gt;this.hybridFind(text,criteria));this.config={...config,preferFuzzy:config.preferFuzzy??false,wildcardPriority:config.wildcardPriority??true,minFuzzyLength:config.minFuzzyLength??4,maxExtraFuzzyChars:config.maxExtraFuzzyChars??2,maxSpaces:config.maxSpaces??1}}hybridFind(text,criteria){if(this.config.wildcardPriority&amp;&amp;criteria.includes(&quot;*&quot;)){const wildcardMatches=findWildcardMatches(text,criteria,this.config);if(wildcardMatches.length&gt;0)return wildcardMatches}if(criteria.includes(&quot; &quot;)||criteria.length&lt;this.config.minFuzzyLength){const literalMatches=findLiteralMatches(text,criteria);if(literalMatches.length&gt;0)return literalMatches}if(this.config.preferFuzzy||criteria.length&gt;=this.config.minFuzzyLength){const fuzzyMatches=findFuzzyMatches(text,criteria);if(fuzzyMatches.length&gt;0){const constrainedMatches=this.applyFuzzyConstraints(fuzzyMatches,criteria);if(constrainedMatches.length&gt;0)return constrainedMatches}}return findLiteralMatches(text,criteria)}applyFuzzyConstraints(matches,criteria){const limit=this.config.maxExtraFuzzyChars;if(!Number.isFinite(limit)||limit&lt;0){return matches}const normalizedCriteriaLength=this.normalizeLength(criteria);if(normalizedCriteriaLength===0){return matches}return matches.filter(match=&gt;{const normalizedMatchLength=this.normalizeLength(match.text);const extraChars=Math.max(0,normalizedMatchLength-normalizedCriteriaLength);return extraChars&lt;=limit})}normalizeLength(value){return value.replace(/\s+/g,&quot;&quot;).length}}const DefaultHybridSearchStrategy=new HybridSearchStrategy;class StrategyFactory{static create(config={type:&quot;literal&quot;}){const{options:options2}=config;const type=this.isValidStrategy(config.type)?config.type:&quot;literal&quot;;switch(type){case&quot;literal&quot;:return LiteralSearchStrategy;case&quot;fuzzy&quot;:return FuzzySearchStrategy;case&quot;wildcard&quot;:return new WildcardSearchStrategy(options2);case&quot;hybrid&quot;:return new HybridSearchStrategy(options2);default:return LiteralSearchStrategy}}static getAvailableStrategies(){return[&quot;literal&quot;,&quot;fuzzy&quot;,&quot;wildcard&quot;,&quot;hybrid&quot;]}static isValidStrategy(type){return this.getAvailableStrategies().includes(type)}}function merge(target,source){return{...target,...source}}function isJSON(json){return Array.isArray(json)||json!==null&amp;&amp;typeof json===&quot;object&quot;}function NoSort(){return 0}function isObject(obj){return Boolean(obj)&amp;&amp;Object.prototype.toString.call(obj)===&quot;[object Object]&quot;}const DEFAULT_OPTIONS={searchInput:null,resultsContainer:null,json:[],success:function(){},searchResultTemplate:&apos;&lt;li&gt;&lt;a href=&quot;{url}&quot; title=&quot;{desc}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,templateMiddleware:(_prop,_value,_template)=&gt;void 0,sortMiddleware:NoSort,noResultsText:&quot;No results found&quot;,limit:10,strategy:&quot;literal&quot;,debounceTime:null,exclude:[],onSearch:()=&gt;{},onError:error=&gt;console.error(&quot;SimpleJekyllSearch error:&quot;,error),fuzzy:false};const REQUIRED_OPTIONS=[&quot;searchInput&quot;,&quot;resultsContainer&quot;,&quot;json&quot;];const WHITELISTED_KEYS=new Set([&quot;Enter&quot;,&quot;Shift&quot;,&quot;CapsLock&quot;,&quot;ArrowLeft&quot;,&quot;ArrowUp&quot;,&quot;ArrowRight&quot;,&quot;ArrowDown&quot;,&quot;Meta&quot;]);class Repository{constructor(initialOptions={}){this.data=[];this.excludePatterns=[];this.setOptions(initialOptions)}put(input){if(isObject(input)){return this.addObject(input)}if(Array.isArray(input)){return this.addArray(input)}return void 0}clear(){this.data.length=0;return this.data}search(criteria){if(!criteria){return[]}const matches=this.findMatches(this.data,criteria).sort(this.options.sortMiddleware);return matches.map(item=&gt;({...item}))}setOptions(newOptions){let strategyConfig=this.normalizeStrategyOption(newOptions?.strategy??DEFAULT_OPTIONS.strategy);if(newOptions?.fuzzy&amp;&amp;!newOptions?.strategy){console.warn(&apos;[Simple Jekyll Search] Warning: fuzzy option is deprecated. Use strategy: &quot;fuzzy&quot; instead.&apos;);strategyConfig={type:&quot;fuzzy&quot;}}const exclude=newOptions?.exclude||DEFAULT_OPTIONS.exclude;this.excludePatterns=exclude.map(pattern=&gt;new RegExp(pattern));this.options={limit:newOptions?.limit||DEFAULT_OPTIONS.limit,searchStrategy:this.searchStrategy(strategyConfig),sortMiddleware:newOptions?.sortMiddleware||DEFAULT_OPTIONS.sortMiddleware,exclude:exclude,strategy:strategyConfig}}addObject(obj){this.data.push(obj);return this.data}addArray(arr){const added=[];this.clear();for(const item of arr){if(isObject(item)){added.push(this.addObject(item)[0])}}return added}findMatches(data,criteria){const matches=[];for(let i=0;i&lt;data.length&amp;&amp;matches.length&lt;this.options.limit;i++){const match=this.findMatchesInObject(data[i],criteria);if(match){matches.push(match)}}return matches}findMatchesInObject(obj,criteria){let hasMatch=false;const result={...obj};result._matchInfo={};for(const key in obj){if(!this.isExcluded(obj[key])&amp;&amp;this.options.searchStrategy.matches(obj[key],criteria)){hasMatch=true;if(this.options.searchStrategy.findMatches){const matchInfo=this.options.searchStrategy.findMatches(obj[key],criteria);if(matchInfo&amp;&amp;matchInfo.length&gt;0){result._matchInfo[key]=matchInfo}}}}return hasMatch?result:void 0}isExcluded(term){const termStr=String(term);return this.excludePatterns.some(regex=&gt;regex.test(termStr))}searchStrategy(strategy){if(!strategy?.type||!StrategyFactory.isValidStrategy(strategy.type)){return LiteralSearchStrategy}return StrategyFactory.create(strategy)}normalizeStrategyOption(strategy){if(!strategy){return this.getDefaultStrategyConfig()}return typeof strategy===&quot;string&quot;?{type:strategy}:strategy}getDefaultStrategyConfig(){const defaultStrategy=DEFAULT_OPTIONS.strategy;{return{type:defaultStrategy}}}}const options={pattern:/\{(.*?)\}/g,template:&quot;&quot;,middleware:function(){return void 0}};function setOptions(_options){if(_options.pattern){options.pattern=_options.pattern}if(_options.template){options.template=_options.template}if(typeof _options.middleware===&quot;function&quot;){options.middleware=_options.middleware}}function compile(data,query){return options.template.replace(options.pattern,function(match,prop){const matchInfo=data._matchInfo?.[prop];if(matchInfo&amp;&amp;matchInfo.length&gt;0&amp;&amp;query){const value2=options.middleware(prop,data[prop],options.template,query,matchInfo);if(typeof value2!==&quot;undefined&quot;){return value2}}if(query){const value2=options.middleware(prop,data[prop],options.template,query);if(typeof value2!==&quot;undefined&quot;){return value2}}const value=options.middleware(prop,data[prop],options.template);if(typeof value!==&quot;undefined&quot;){return value}return data[prop]||match})}let SimpleJekyllSearch$1=class SimpleJekyllSearch{constructor(){this.debounceTimerHandle=null;this.eventHandler=null;this.pageShowHandler=null;this.pendingRequest=null;this.isInitialized=false;this.STORAGE_KEY=&quot;sjs-search-state&quot;;this.options={...DEFAULT_OPTIONS};this.repository=new Repository;this.optionsValidator=new OptionsValidator({required:REQUIRED_OPTIONS})}debounce(func,delayMillis){if(delayMillis){if(this.debounceTimerHandle){clearTimeout(this.debounceTimerHandle)}this.debounceTimerHandle=setTimeout(func,delayMillis)}else{func()}}throwError(message){throw new Error(`SimpleJekyllSearch --- ${message}`)}emptyResultsContainer(){this.options.resultsContainer.innerHTML=&quot;&quot;}initWithJSON(json){this.repository.put(json);this.registerInput()}initWithURL(url){load(url,(err,json)=&gt;{if(err){this.throwError(`Failed to load JSON from ${url}: ${err.message}`)}this.initWithJSON(json)})}registerInput(){this.eventHandler=e=&gt;{try{const inputEvent=e;if(!WHITELISTED_KEYS.has(inputEvent.key)){this.emptyResultsContainer();this.debounce(()=&gt;{try{this.search(e.target.value)}catch(searchError){console.error(&quot;Search error:&quot;,searchError);this.options.onError?.(searchError)}},this.options.debounceTime??null)}}catch(error){console.error(&quot;Input handler error:&quot;,error);this.options.onError?.(error)}};this.options.searchInput.addEventListener(&quot;input&quot;,this.eventHandler);this.pageShowHandler=()=&gt;{this.restoreSearchState()};window.addEventListener(&quot;pageshow&quot;,this.pageShowHandler);this.restoreSearchState()}saveSearchState(query){if(!query?.trim()){this.clearSearchState();return}try{const state={query:query.trim(),timestamp:Date.now(),path:window.location.pathname};sessionStorage.setItem(this.STORAGE_KEY,JSON.stringify(state))}catch{}}getStoredSearchState(){try{const raw=sessionStorage.getItem(this.STORAGE_KEY);if(!raw)return null;const state=JSON.parse(raw);if(typeof state?.query!==&quot;string&quot;)return null;const MAX_AGE_MS=30*60*1e3;if(Date.now()-state.timestamp&gt;MAX_AGE_MS){this.clearSearchState();return null}if(state.path&amp;&amp;state.path!==window.location.pathname){this.clearSearchState();return null}return state.query}catch{this.clearSearchState();return null}}clearSearchState(){try{sessionStorage.removeItem(this.STORAGE_KEY)}catch{}}restoreSearchState(){const hasExistingResults=this.options.resultsContainer.children.length&gt;0;if(hasExistingResults)return;let query=this.options.searchInput.value?.trim();if(!query){query=this.getStoredSearchState()||&quot;&quot;}if(query.length&gt;0){this.options.searchInput.value=query;this.search(query)}}search(query){if(query?.trim().length&gt;0){this.saveSearchState(query);this.emptyResultsContainer();const results=this.repository.search(query);this.render(results,query);this.options.onSearch?.()}else{this.clearSearchState()}}render(results,query){if(results.length===0){this.options.resultsContainer.insertAdjacentHTML(&quot;beforeend&quot;,this.options.noResultsText);return}const fragment=document.createDocumentFragment();results.forEach(result=&gt;{result.query=query;const div=document.createElement(&quot;div&quot;);div.innerHTML=compile(result,query);fragment.appendChild(div)});this.options.resultsContainer.appendChild(fragment)}destroy(){if(this.eventHandler){this.options.searchInput.removeEventListener(&quot;input&quot;,this.eventHandler);this.eventHandler=null}if(this.pageShowHandler){window.removeEventListener(&quot;pageshow&quot;,this.pageShowHandler);this.pageShowHandler=null}if(this.debounceTimerHandle){clearTimeout(this.debounceTimerHandle);this.debounceTimerHandle=null}this.clearSearchState()}init(_options){const errors=this.optionsValidator.validate(_options);if(errors.length&gt;0){this.throwError(`Missing required options: ${REQUIRED_OPTIONS.join(&quot;, &quot;)}`)}this.options=merge(this.options,_options);setOptions({template:this.options.searchResultTemplate,middleware:this.options.templateMiddleware});this.repository.setOptions({limit:this.options.limit,sortMiddleware:this.options.sortMiddleware,strategy:this.options.strategy,exclude:this.options.exclude});if(isJSON(this.options.json)){this.initWithJSON(this.options.json)}else{this.initWithURL(this.options.json)}const rv={search:this.search.bind(this),destroy:this.destroy.bind(this)};this.options.success?.call(rv);return rv}};function escapeHtml(text){const map={&quot;&amp;&quot;:&quot;&amp;amp;&quot;,&quot;&lt;&quot;:&quot;&amp;lt;&quot;,&quot;&gt;&quot;:&quot;&amp;gt;&quot;,&apos;&quot;&apos;:&quot;&amp;quot;&quot;,&quot;&apos;&quot;:&quot;&amp;#039;&quot;};return text.replace(/[&amp;&lt;&gt;&quot;&apos;]/g,m=&gt;map[m])}function mergeOverlappingMatches(matches){if(matches.length===0)return[];const sorted=[...matches].sort((a,b)=&gt;a.start-b.start);const merged=[{...sorted[0]}];for(let i=1;i&lt;sorted.length;i++){const current=sorted[i];const last=merged[merged.length-1];if(current.start&lt;=last.end){last.end=Math.max(last.end,current.end)}else{merged.push({...current})}}return merged}function highlightWithMatchInfo(text,matchInfo,options2={}){if(!text||matchInfo.length===0){return escapeHtml(text)}const className=options2.className||&quot;search-highlight&quot;;const maxLength=options2.maxLength;const mergedMatches=mergeOverlappingMatches(matchInfo);let result=&quot;&quot;;let lastIndex=0;for(const match of mergedMatches){result+=escapeHtml(text.substring(lastIndex,match.start));result+=`&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(text.substring(match.start,match.end))}&lt;/span&gt;`;lastIndex=match.end}result+=escapeHtml(text.substring(lastIndex));if(maxLength&amp;&amp;result.length&gt;maxLength){result=truncateAroundMatches(text,mergedMatches,maxLength,options2.contextLength||30,className)}return result}function truncateAroundMatches(text,matches,maxLength,contextLength,className){if(matches.length===0){const truncated=text.substring(0,maxLength-3);return escapeHtml(truncated)+&quot;...&quot;}const firstMatch=matches[0];const start=Math.max(0,firstMatch.start-contextLength);const end=Math.min(text.length,firstMatch.end+contextLength);let result=&quot;&quot;;if(start&gt;0){result+=&quot;...&quot;}const snippet=text.substring(start,end);const adjustedMatches=matches.filter(m=&gt;m.start&lt;end&amp;&amp;m.end&gt;start).map(m=&gt;({...m,start:Math.max(0,m.start-start),end:Math.min(snippet.length,m.end-start)}));let lastIndex=0;for(const match of adjustedMatches){result+=escapeHtml(snippet.substring(lastIndex,match.start));result+=`&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(snippet.substring(match.start,match.end))}&lt;/span&gt;`;lastIndex=match.end}result+=escapeHtml(snippet.substring(lastIndex));if(end&lt;text.length){result+=&quot;...&quot;}return result}const DEFAULT_TRUNCATE_FIELDS=[&quot;content&quot;,&quot;desc&quot;,&quot;description&quot;];const DEFAULT_NO_HIGHLIGHT_FIELDS=[&quot;url&quot;,&quot;link&quot;,&quot;href&quot;,&quot;query&quot;];function createHighlightTemplateMiddleware(options2={}){const highlightOptions={className:options2.className||&quot;search-highlight&quot;,maxLength:options2.maxLength,contextLength:options2.contextLength||30};const truncateFields=options2.truncateFields||DEFAULT_TRUNCATE_FIELDS;const noHighlightFields=options2.noHighlightFields||DEFAULT_NO_HIGHLIGHT_FIELDS;return function(prop,value,_template,query,matchInfo){if(typeof value!==&quot;string&quot;){return void 0}if(noHighlightFields.includes(prop)){return void 0}const shouldTruncate=truncateFields.includes(prop);if(matchInfo&amp;&amp;matchInfo.length&gt;0&amp;&amp;query){const fieldOptions={...highlightOptions,maxLength:shouldTruncate?highlightOptions.maxLength:void 0};const highlighted=highlightWithMatchInfo(value,matchInfo,fieldOptions);return highlighted!==value?highlighted:void 0}if(shouldTruncate&amp;&amp;highlightOptions.maxLength&amp;&amp;value.length&gt;highlightOptions.maxLength){return escapeHtml(value.substring(0,highlightOptions.maxLength-3)+&quot;...&quot;)}return void 0}}function defaultHighlightMiddleware(prop,value,template,query,matchInfo){const middleware=createHighlightTemplateMiddleware();return middleware(prop,value,template,query,matchInfo)}function SimpleJekyllSearch(options2){const instance=new SimpleJekyllSearch$1;return instance.init(options2)}if(typeof window!==&quot;undefined&quot;){window.SimpleJekyllSearch=SimpleJekyllSearch;window.createHighlightTemplateMiddleware=createHighlightTemplateMiddleware}exports2.DefaultHybridSearchStrategy=DefaultHybridSearchStrategy;exports2.HybridSearchStrategy=HybridSearchStrategy;exports2.StrategyFactory=StrategyFactory;exports2.createHighlightTemplateMiddleware=createHighlightTemplateMiddleware;exports2.default=SimpleJekyllSearch;exports2.defaultHighlightMiddleware=defaultHighlightMiddleware;exports2.escapeHtml=escapeHtml;exports2.highlightWithMatchInfo=highlightWithMatchInfo;exports2.mergeOverlappingMatches=mergeOverlappingMatches;Object.defineProperties(exports2,{__esModule:{value:true},[Symbol.toStringTag]:{value:&quot;Module&quot;}})});</file><file path="docs/_includes/footer.html">&lt;footer class=&quot;site-footer&quot;&gt;

  &lt;div class=&quot;wrapper&quot;&gt;

    &lt;div class=&quot;footer-col-wrapper&quot;&gt;
      &lt;div class=&quot;footer-col  footer-col-1&quot;&gt;
        &lt;ul class=&quot;contact-list&quot;&gt;
          &lt;li&gt;{{ site.title }}&lt;/li&gt;
          &lt;li&gt;&lt;p class=&quot;rss-subscribe&quot;&gt;subscribe &lt;a href=&quot;{{ &quot;/feed.xml&quot; | prepend: site.baseurl }}&quot;&gt;via RSS&lt;/a&gt;&lt;/p&gt;&lt;/li&gt;
          &lt;li&gt;&lt;a href=&quot;mailto:{{ site.email }}&quot;&gt;{{ site.email }}&lt;/a&gt;&lt;/li&gt;
        &lt;/ul&gt;
      &lt;/div&gt;

      &lt;div class=&quot;footer-col  footer-col-2&quot;&gt;
        &lt;ul class=&quot;social-media-list&quot;&gt;
          {% if site.github_username %}
          &lt;li&gt;
            &lt;a href=&quot;https://github.com/{{ site.github_username }}&quot;&gt;
              &lt;span class=&quot;icon  icon--github&quot;&gt;
                &lt;svg viewBox=&quot;0 0 16 16&quot;&gt;
                  &lt;path fill=&quot;#828282&quot; d=&quot;M7.999,0.431c-4.285,0-7.76,3.474-7.76,7.761 c0,3.428,2.223,6.337,5.307,7.363c0.388,0.071,0.53-0.168,0.53-0.374c0-0.184-0.007-0.672-0.01-1.32 c-2.159,0.469-2.614-1.04-2.614-1.04c-0.353-0.896-0.862-1.135-0.862-1.135c-0.705-0.481,0.053-0.472,0.053-0.472 c0.779,0.055,1.189,0.8,1.189,0.8c0.692,1.186,1.816,0.843,2.258,0.645c0.071-0.502,0.271-0.843,0.493-1.037 C4.86,11.425,3.049,10.76,3.049,7.786c0-0.847,0.302-1.54,0.799-2.082C3.768,5.507,3.501,4.718,3.924,3.65 c0,0,0.652-0.209,2.134,0.796C6.677,4.273,7.34,4.187,8,4.184c0.659,0.003,1.323,0.089,1.943,0.261 c1.482-1.004,2.132-0.796,2.132-0.796c0.423,1.068,0.157,1.857,0.077,2.054c0.497,0.542,0.798,1.235,0.798,2.082 c0,2.981-1.814,3.637-3.543,3.829c0.279,0.24,0.527,0.713,0.527,1.437c0,1.037-0.01,1.874-0.01,2.129 c0,0.208,0.14,0.449,0.534,0.373c3.081-1.028,5.302-3.935,5.302-7.362C15.76,3.906,12.285,0.431,7.999,0.431z&quot;/&gt;
                &lt;/svg&gt;
              &lt;/span&gt;

              &lt;span class=&quot;username&quot;&gt;{{ site.github_username }}&lt;/span&gt;
            &lt;/a&gt;
          &lt;/li&gt;
          {% endif %}

          {% if site.twitter_username %}
          &lt;li&gt;
            &lt;a href=&quot;https://twitter.com/{{ site.twitter_username }}&quot;&gt;
              &lt;span class=&quot;icon  icon--twitter&quot;&gt;
                &lt;svg viewBox=&quot;0 0 16 16&quot;&gt;
                  &lt;path fill=&quot;#828282&quot; d=&quot;M15.969,3.058c-0.586,0.26-1.217,0.436-1.878,0.515c0.675-0.405,1.194-1.045,1.438-1.809
                  c-0.632,0.375-1.332,0.647-2.076,0.793c-0.596-0.636-1.446-1.033-2.387-1.033c-1.806,0-3.27,1.464-3.27,3.27 c0,0.256,0.029,0.506,0.085,0.745C5.163,5.404,2.753,4.102,1.14,2.124C0.859,2.607,0.698,3.168,0.698,3.767 c0,1.134,0.577,2.135,1.455,2.722C1.616,6.472,1.112,6.325,0.671,6.08c0,0.014,0,0.027,0,0.041c0,1.584,1.127,2.906,2.623,3.206 C3.02,9.402,2.731,9.442,2.433,9.442c-0.211,0-0.416-0.021-0.615-0.059c0.416,1.299,1.624,2.245,3.055,2.271 c-1.119,0.877-2.529,1.4-4.061,1.4c-0.264,0-0.524-0.015-0.78-0.046c1.447,0.928,3.166,1.469,5.013,1.469 c6.015,0,9.304-4.983,9.304-9.304c0-0.142-0.003-0.283-0.009-0.423C14.976,4.29,15.531,3.714,15.969,3.058z&quot;/&gt;
                &lt;/svg&gt;
              &lt;/span&gt;

              &lt;span class=&quot;username&quot;&gt;{{ site.twitter_username }}&lt;/span&gt;
            &lt;/a&gt;
          &lt;/li&gt;
          {% endif %}
        &lt;/ul&gt;
      &lt;/div&gt;

      &lt;div class=&quot;footer-col  footer-col-3&quot;&gt;
        &lt;p class=&quot;text&quot;&gt;{{ site.description }}&lt;/p&gt;
      &lt;/div&gt;
    &lt;/div&gt;

  &lt;/div&gt;

&lt;/footer&gt;</file><file path="docs/_includes/head.html">&lt;head&gt;
    &lt;meta charset=&quot;utf-8&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width initial-scale=1&quot;&gt;
    &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge&quot;&gt;

    &lt;title&gt;{% if page.title %}{{ page.title }}{% else %}{{ site.title }}{% endif %}&lt;/title&gt;
    &lt;meta name=&quot;description&quot; content=&quot;{{ site.description }}&quot;&gt;

    &lt;link rel=&quot;stylesheet&quot; href=&quot;{{ &apos;/assets/css/main.css&apos; | prepend: site.baseurl }}&quot;&gt;
    &lt;link rel=&quot;canonical&quot; href=&quot;{{ page.url | replace:&apos;index.html&apos;,&apos;&apos; | prepend: site.baseurl | prepend: site.url }}&quot;&gt;
&lt;/head&gt;</file><file path="docs/_includes/header.html">&lt;header class=&quot;site-header&quot;&gt;

  &lt;div class=&quot;wrapper&quot;&gt;

    &lt;a class=&quot;site-title&quot; href=&quot;{{ site.baseurl }}/&quot;&gt;{{ site.title }}&lt;/a&gt;

    &lt;nav class=&quot;site-nav&quot;&gt;
      &lt;a href=&quot;#&quot; class=&quot;menu-icon&quot;&gt;
        &lt;svg viewBox=&quot;0 0 18 15&quot;&gt;
          &lt;path fill=&quot;#424242&quot; d=&quot;M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.031C17.335,0,18,0.665,18,1.484L18,1.484z&quot;/&gt;
          &lt;path fill=&quot;#424242&quot; d=&quot;M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0c0-0.82,0.665-1.484,1.484-1.484 h15.031C17.335,6.031,18,6.696,18,7.516L18,7.516z&quot;/&gt;
          &lt;path fill=&quot;#424242&quot; d=&quot;M18,13.516C18,14.335,17.335,15,16.516,15H1.484C0.665,15,0,14.335,0,13.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.031C17.335,12.031,18,12.696,18,13.516L18,13.516z&quot;/&gt;
        &lt;/svg&gt;
      &lt;/a&gt;

      &lt;div class=&quot;trigger&quot;&gt;
        {% for page in site.pages %}
          {% if page.title %}
          &lt;a class=&quot;page-link&quot; href=&quot;{{ page.url | prepend: site.baseurl }}&quot;&gt;{{ page.title }}&lt;/a&gt;
          {% endif %}
        {% endfor %}
      &lt;/div&gt;
    &lt;/nav&gt;

  &lt;/div&gt;

&lt;/header&gt;</file><file path="docs/_includes/search.html">&lt;div&gt;
  &lt;div id=&quot;search-demo-container&quot;&gt;
    &lt;input type=&quot;search&quot; id=&quot;search-input&quot; placeholder=&quot;search...&quot;&gt;
    &lt;ul id=&quot;results-container&quot;&gt;&lt;/ul&gt;
  &lt;/div&gt;

  &lt;script src=&quot;{{ &apos;/assets/js/simple-jekyll-search.min.js&apos; | relative_url }}?v={{ site.time | date: &apos;%s&apos; }}&quot;&gt;&lt;/script&gt;

  &lt;script&gt;
    var highlightMiddleware = window.createHighlightTemplateMiddleware({
      className: &apos;search-highlight&apos;,
      maxLength: 200
    });

    window.simpleJekyllSearch = new SimpleJekyllSearch({
      searchInput: document.getElementById(&apos;search-input&apos;),
      resultsContainer: document.getElementById(&apos;results-container&apos;),
      json: &apos;{{ &quot;/assets/data/search.json&quot; | relative_url }}&apos;,
      searchResultTemplate: &apos;&lt;li&gt;&lt;a href=&quot;{url}?query={query}&quot;&gt;{title}&lt;/a&gt;&lt;p class=&quot;search-tags&quot;&gt;{tags}&lt;/p&gt;&lt;p class=&quot;search-desc&quot;&gt;{content}&lt;/p&gt;&lt;/li&gt;&apos;,
      templateMiddleware: highlightMiddleware,
      noResultsText: &apos;No results found&apos;,
      limit: 10,
      strategy: &apos;hybrid&apos;,
      exclude: [&apos;Welcome&apos;],
    });
  &lt;/script&gt;

&lt;/div&gt;</file><file path="docs/_layouts/default.html">&lt;!doctype html&gt;
&lt;html lang=&quot;en&quot;&gt;

  {% include head.html %}

  &lt;body&gt;

    {% include header.html %}

    &lt;div class=&quot;page-content&quot;&gt;
      &lt;div class=&quot;wrapper&quot;&gt;
        {{ content }}
      &lt;/div&gt;
    &lt;/div&gt;

    {% include footer.html %}

  &lt;/body&gt;

&lt;/html&gt;</file><file path="docs/_layouts/page.html">---
layout: default
---
&lt;div class=&quot;post&quot;&gt;

  &lt;header class=&quot;post-header&quot;&gt;
    &lt;h1 class=&quot;post-title&quot;&gt;{{ page.title }}&lt;/h1&gt;
  &lt;/header&gt;

  &lt;article class=&quot;post-content&quot;&gt;
    {{ content }}
  &lt;/article&gt;

&lt;/div&gt;</file><file path="docs/_layouts/post.html">---
layout: default
---
&lt;div class=&quot;post&quot;&gt;

  &lt;header class=&quot;post-header&quot;&gt;
    &lt;h1 class=&quot;post-title&quot;&gt;{{ page.title }}&lt;/h1&gt;
    &lt;p class=&quot;post-meta&quot;&gt;{{ page.date | date: &quot;%b %-d, %Y&quot; }}{% if page.author %} • {{ page.author }}{% endif %}{% if page.meta %} • {{ page.meta }}{% endif %}&lt;/p&gt;
  &lt;/header&gt;

  &lt;article class=&quot;post-content&quot;&gt;
    {{ content }}
  &lt;/article&gt;

&lt;/div&gt;</file><file path="docs/_plugins/simple_search_filter_cn.rb"># encoding: utf-8
# frozen_string_literal: true

# Same as `simple_search_filter.rb`, but with additional adapted for Chinese characters
# Example usage in a Jekyll template:
#   {{ some_variable | remove_chars_cn }}
#
# This will remove the following characters from `some_variable`:
#   - Backslashes (\) are replaced with `&amp;#92;`
#   - Tabs (\t) are replaced with four spaces
#   - The following characters are removed: @, $, %, &amp;, &quot;, {, }
#
# Not compatible with GitHub page unless pre-built
module Jekyll
  module CharFilter
    def remove_chars_cn(input)
      input.gsub! &apos;\\&apos;, &apos;&amp;#92;&apos;
      input.gsub! /\t/, &apos;    &apos;
      input.gsub! &apos;@&apos;, &apos;&apos;
      input.gsub! &apos;$&apos;, &apos;&apos;
      input.gsub! &apos;%&apos;, &apos;&apos;
      input.gsub! &apos;&amp;&apos;, &apos;&apos;
      input.gsub! &apos;&quot;&apos;, &apos;&apos;
      input.gsub! &apos;{&apos;, &apos;&apos;
      input.gsub! &apos;}&apos;, &apos;&apos;
      input
    end
  end
end

# Registers the `remove_chars_cn` filter for use in Jekyll templates.
Liquid::Template.register_filter(Jekyll::CharFilter)</file><file path="docs/_plugins/simple_search_filter.rb"># encoding: utf-8
# frozen_string_literal: true

# Example usage in a Jekyll template:
#   {{ some_variable | remove_chars }}
#
# This will:
#   - Replace backslashes (\) with `&amp;#92;`
#   - Replace tabs (\t) with four spaces
#   - Remove control characters and extended ASCII characters
#
# Not compatible with GitHub Pages unless pre-built
module Jekyll
  module CharFilter
    def remove_chars(input)
      input.gsub! &apos;\\&apos;,&apos;&amp;#92;&apos;
      input.gsub! /\t/, &apos;    &apos;
      input.strip_control_and_extended_characters
    end
  end
end

Liquid::Template.register_filter(Jekyll::CharFilter)

# This ensures the resulting string contains only printable ASCII characters.
class String
  def strip_control_and_extended_characters()
    chars.each_with_object(&quot;&quot;) do |char, str|
      str &lt;&lt; char if char.ascii_only? and char.ord.between?(32,126)
    end
  end
end</file><file path="docs/_posts/2014-11-01-welcome-to-jekyll.md">---
layout: post
title: &quot;Welcome to Jekyll!&quot;
date: 2014-11-01 20:07:22
categories: [ jekyll ]
tags: [ jekyll, ruby, getting-started ]
---

You’ll find this post in your `_posts` directory.
Go ahead and edit it and re-build the site to see your changes.
You can rebuild the site in many different ways, but the most common way is to run `jekyll serve --watch`,
which launches a web server and auto-regenerates your site when a file is updated.

To add new posts,
simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the
necessary front matter.
Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
puts &quot;Hi, #{name}&quot;
end
print_hi(&apos;Tom&apos;)

# =&gt; prints &apos;Hi, Tom&apos; to STDOUT.

{% endhighlight %}

Check out the [Jekyll docs][jekyll] for more info on how to get the most out of Jekyll.
File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh].
If you have questions, you can ask them on [Jekyll’s dedicated Help repository][jekyll-help].

[jekyll]:      http://jekyllrb.com
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-help]: https://github.com/jekyll/jekyll-help</file><file path="docs/_posts/2014-11-02-test.md">---
layout: post
title: &quot;This is just a test&quot;
date: 2014-11-02 20:07:22
categories: [ search ]
tags: [ test, javascript, code ]
---

Lorem ipsum just some test.

This post is designed to test the search functionality. 
Try searching for keywords like **&quot;Lorem&quot;**, **&quot;code snippets&quot;**, or **&quot;upDown&quot;** to see how the search behaves.

Here’s a code example to test:

```js
function upDown(input) {
  const result = input
          .split(&apos;&apos;)
          .map((char, index) =&gt; index % 2 === 0 ? char.toUpperCase() : char.toLowerCase())
          .join(&apos;&apos;);
  console.log(`result: ${result}`);
  return result;
}

upDown(&apos;SearchTest123&apos;);
// Output: &quot;SeArChTeSt123&quot;
```

That&apos;s it!</file><file path="docs/_posts/2025-04-22-technical-example.md">---
layout: post
title: &quot;Technical Example&quot;
date: 2025-04-22 10:00:00
categories: [ search, tutorial ]
tags: [ regex, json, bash, code ]
---

This is an article with more technical content to test the search functionality.

A command with some regex and special characters:

```bash
grep -E -o &quot;[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}&quot; file.txt
sed &apos;s/^[ \t]*//;s/[ \t]*$//&apos; file.txt
sed -i &apos;s/\&quot;hostname\&quot;\:.*$/\&quot;hostname\&quot;\: \&quot;new-hostname\&quot;/&apos; config.json
```

A JSON object to test:

```json
{
  &quot;name&quot;: &quot;John Doe&quot;,
  &quot;age&quot;: 30,
  &quot;cities&quot;: [
    &quot;New York&quot;,
    &quot;Paris&quot;
  ],
  &quot;details&quot;: {
    &quot;height&quot;: 180,
    &quot;weight&quot;: 75
  }
}
```

Using highlight:

{% highlight terminal %}
...
Init4 = AT+CGDCONT=1,&quot;IP&quot;,&quot;internetmas&quot;,&quot;&quot;,0,0
...
{% endhighlight %}

A tricky string to test the search:

```text
This    is    a    test    with    irregular    spacing.
Special characters: ~!@#$%^&amp;*()_+`-={}|[]\:&quot;;&apos;&lt;&gt;?,./
Escape sequences: \n \t \r \\</file><file path="docs/_sass/_base.scss">@use &quot;sass:color&quot;;
@use &quot;custom&quot;;

/**
 * Reset some basic elements
 */
body, h1, h2, h3, h4, h5, h6,
p, blockquote, pre, hr,
dl, dd, ol, ul, figure {
    margin: 0;
    padding: 0;
}



/**
 * Basic styling
 */
body {
    font-family: $base-font-family;
    font-size: $base-font-size;
    line-height: $base-line-height;
    font-weight: 300;
    color: $text-color;
    background-color: $background-color;
    -webkit-text-size-adjust: 100%;
}



/**
 * Set `margin-bottom` to maintain vertical rhythm
 */
h1, h2, h3, h4, h5, h6,
p, blockquote, pre,
ul, ol, dl, figure {
    @include vertical-rhythm;
}

/**
 * Images
 */
img {
    max-width: 100%;
    vertical-align: middle;
}



/**
 * Figures
 */
figure &gt; img {
    display: block;
}

figcaption {
    font-size: $small-font-size;
}



/**
 * Lists
 */
ul, ol {
    margin-left: $spacing-unit;
}

li {
    &gt; ul,
    &gt; ol {
         margin-bottom: 0;
    }
}



/**
 * Headings
 */
h1, h2, h3, h4, h5, h6 {
    font-weight: 300;
}



/**
 * Links
 */
a {
    color: $brand-color;
    text-decoration: none;

    &amp;:visited {
        color: #5a96e8;
    }

    &amp;:hover {
        color: $text-color;
        text-decoration: underline;
    }
}



/**
 * Blockquotes
 */
blockquote {
    color: $grey-color;
    border-left: 4px solid $grey-color-light;
    padding-left: $spacing-unit-sm;
    font-size: 18px;
    letter-spacing: -1px;
    font-style: italic;

    &gt; :last-child {
        margin-bottom: 0;
    }
}



/**
 * Code formatting
 */
pre,
code {
    font-size: 15px;
    border: 1px solid $grey-color-light;
    border-radius: 3px;
    background-color: #eef;

    pre.highlight &amp; {
        background-color: unset;
    }
}

code {
    padding: 1px 5px;
}

pre {
    padding: 8px 12px;
    overflow-x: scroll;

    &gt; code {
        border: 0;
        padding-right: 0;
        padding-left: 0;
    }
}



/**
 * Wrapper
 */
.wrapper {
    max-width: -webkit-calc(800px - (#{$spacing-unit} * 2));
    max-width:         calc(800px - (#{$spacing-unit} * 2));
    margin-right: auto;
    margin-left: auto;
    padding-right: $spacing-unit;
    padding-left: $spacing-unit;
    @include clearfix;

    @include media-query($on-laptop) {
        max-width: -webkit-calc(800px - (#{$spacing-unit}));
        max-width:         calc(800px - (#{$spacing-unit}));
        padding-right: $spacing-unit-sm;
        padding-left: $spacing-unit-sm;
    }
}


/**
 * Icons
 */
.icon {

    &gt; svg {
        display: inline-block;
        width: 16px;
        height: 16px;
        vertical-align: middle;

        path {
            fill: $grey-color;
        }
    }
}</file><file path="docs/_sass/_custom.scss">@charset &quot;utf-8&quot;;
@use &quot;sass:color&quot;;

// Our variables
$base-font-family: Helvetica, Arial, sans-serif;
$base-font-size:   16px;
$small-font-size:  14px;
$base-line-height: 1.5;

$spacing-unit:     30px;
$spacing-unit-sm:  15px;

$text-color:       #111;
$background-color: #fdfdfd;
$brand-color:      #2a7ae2;

$grey-color:       #828282;
$grey-color-light:  #d1d1d1;
$grey-color-dark:  #3e3e3e;

$on-palm:          600px;
$on-laptop:        800px;

@mixin media-query($device) {
  @media screen and (max-width: $device) {
    @content;
  }
}

@mixin clearfix {
  &amp;:after {
    content: &quot;&quot;;
    display: table;
    clear: both;
  }
}

@mixin vertical-rhythm {
  margin-bottom: $spacing-unit-sm;
}

#results-container {
  margin-top: $spacing-unit;
}

#search-demo-container {
  max-width: 40em;
  padding: 1em;
  margin: 3em auto;
  border: 1px solid lightgrey;
}

#search-input {
  display: inline-block;
  padding: .5em;
  width: 100%;
  font-size: 0.8em;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

.info-text {
  margin-top: 20px;
}

.search-highlight {
  background-color: #ffff00;
  font-weight: bold;
  padding: 0 2px;
}

.search-desc {
  font-size: 0.9em;
  color: $grey-color-dark;
  margin: 0.3em 0;
}

.search-tags {
  font-size: 0.8em;
  color: $grey-color;
  margin: 0.2em 0;
  
  &amp;:empty {
    display: none;
  }
  
  &amp;:not(:empty)::before {
    content: &quot;Tags: &quot;;
    font-weight: 500;
  }
}</file><file path="docs/_sass/_layout.scss">@use &quot;custom&quot;;

/**
 * Site header
 */
.site-header {
    border-top: 5px solid $grey-color-dark;
    border-bottom: 1px solid $grey-color-light;
    min-height: 56px;

    // Positioning context for the mobile navigation icon
    position: relative;
}

.site-title {
    font-size: 26px;
    line-height: 56px;
    letter-spacing: -1px;
    margin-bottom: 0;
    float: left;

    &amp;,
    &amp;:visited {
        color: $grey-color-dark;
    }
}

.site-nav {
    float: right;
    line-height: 56px;

    .menu-icon {
        display: none;
    }

    .page-link {
        color: $text-color;
        line-height: $base-line-height;

        // Gaps between nav items, but not on the first one
        &amp;:not(:first-child) {
            margin-left: 20px;
        }
    }

    @include media-query($on-palm) {
        position: absolute;
        top: 9px;
        right: 30px;
        background-color: $background-color;
        border: 1px solid $grey-color-light;
        border-radius: 5px;
        text-align: right;

        .menu-icon {
            display: block;
            float: right;
            width: 36px;
            height: 26px;
            line-height: 0;
            padding-top: 10px;
            text-align: center;

            &gt; svg {
                width: 18px;
                height: 15px;

                path {
                    fill: $grey-color-dark;
                }
            }
        }

        .trigger {
            clear: both;
            display: none;
        }

        &amp;:hover .trigger {
            display: block;
            padding-bottom: 5px;
        }

        .page-link {
            display: block;
            padding: 5px 10px;
        }
    }
}



/**
 * Site footer
 */
.site-footer {
    border-top: 1px solid $grey-color-light;
    padding: $spacing-unit 0;
}

.footer-heading {
    font-size: 18px;
    margin-bottom: $spacing-unit-sm;
}

.contact-list,
.social-media-list {
    list-style: none;
    margin-left: 0;
}

.footer-col-wrapper {
    font-size: 15px;
    color: $grey-color;
    margin-left: -($spacing-unit-sm);
    @include clearfix;
}

.footer-col {
    float: left;
    margin-bottom: $spacing-unit-sm;
    padding-left: $spacing-unit-sm;
}

.footer-col-1 {
    width: -webkit-calc(35% - (#{$spacing-unit} / 2));
    width:         calc(35% - (#{$spacing-unit} / 2));
}

.footer-col-2 {
    width: -webkit-calc(20% - (#{$spacing-unit} / 2));
    width:         calc(20% - (#{$spacing-unit} / 2));
}

.footer-col-3 {
    width: -webkit-calc(45% - (#{$spacing-unit} / 2));
    width:         calc(45% - (#{$spacing-unit} / 2));
}

@include media-query($on-laptop) {
    .footer-col-1,
    .footer-col-2 {
        width: -webkit-calc(50% - (#{$spacing-unit} / 2));
        width:         calc(50% - (#{$spacing-unit} / 2));
    }

    .footer-col-3 {
        width: -webkit-calc(100% - (#{$spacing-unit} / 2));
        width:         calc(100% - (#{$spacing-unit} / 2));
    }
}

@include media-query($on-palm) {
    .footer-col {
        float: none;
        width: -webkit-calc(100% - (#{$spacing-unit} / 2));
        width:         calc(100% - (#{$spacing-unit} / 2));
    }
}



/**
 * Page content
 */
.page-content {
    padding: $spacing-unit 0;
}

.page-heading {
    font-size: 20px;
}

.post-list {
    margin-left: 0;
    list-style: none;

    &gt; li {
        margin-bottom: $spacing-unit;
    }
}

.post-meta {
    font-size: $small-font-size;
    color: $grey-color;
}

.post-link {
    display: block;
    font-size: 24px;
}



/**
 * Posts
 */
.post-header {
    margin-bottom: $spacing-unit;
}

.post-title {
    font-size: 42px;
    letter-spacing: -1px;
    line-height: 1;

    @include media-query($on-laptop) {
        font-size: 36px;
    }
}

.post-content {
    margin-bottom: $spacing-unit;

    h2 {
        font-size: 32px;

        @include media-query($on-laptop) {
            font-size: 28px;
        }
    }

    h3 {
        font-size: 26px;

        @include media-query($on-laptop) {
            font-size: 22px;
        }
    }

    h4 {
        font-size: 20px;

        @include media-query($on-laptop) {
            font-size: 18px;
        }
    }
}</file><file path="docs/_sass/_syntax-highlighting.scss">@use &quot;custom&quot;;

/**
 * Syntax highlighting styles
 */
.highlight {
    background: #f5f5f5;
    @include vertical-rhythm;

    .c     { color: #998; font-style: italic } // Comment
    .err   { color: #a61717; background-color: #e3d2d2 } // Error
    .k     { font-weight: bold } // Keyword
    .o     { font-weight: bold } // Operator
    .cm    { color: #998; font-style: italic } // Comment.Multiline
    .cp    { color: #999; font-weight: bold } // Comment.Preproc
    .c1    { color: #998; font-style: italic } // Comment.Single
    .cs    { color: #999; font-weight: bold; font-style: italic } // Comment.Special
    .gd    { color: #000; background-color: #fdd } // Generic.Deleted
    .gd .x { color: #000; background-color: #faa } // Generic.Deleted.Specific
    .ge    { font-style: italic } // Generic.Emph
    .gr    { color: #a00 } // Generic.Error
    .gh    { color: #999 } // Generic.Heading
    .gi    { color: #000; background-color: #dfd } // Generic.Inserted
    .gi .x { color: #000; background-color: #afa } // Generic.Inserted.Specific
    .go    { color: #888 } // Generic.Output
    .gp    { color: #555 } // Generic.Prompt
    .gs    { font-weight: bold } // Generic.Strong
    .gu    { color: #aaa } // Generic.Subheading
    .gt    { color: #a00 } // Generic.Traceback
    .kc    { font-weight: bold } // Keyword.Constant
    .kd    { font-weight: bold } // Keyword.Declaration
    .kp    { font-weight: bold } // Keyword.Pseudo
    .kr    { font-weight: bold } // Keyword.Reserved
    .kt    { color: #458; font-weight: bold } // Keyword.Type
    .m     { color: #099 } // Literal.Number
    .s     { color: #d14 } // Literal.String
    .na    { color: #008080 } // Name.Attribute
    .nb    { color: #0086B3 } // Name.Builtin
    .nc    { color: #458; font-weight: bold } // Name.Class
    .no    { color: #008080 } // Name.Constant
    .ni    { color: #800080 } // Name.Entity
    .ne    { color: #900; font-weight: bold } // Name.Exception
    .nf    { color: #900; font-weight: bold } // Name.Function
    .nn    { color: #555 } // Name.Namespace
    .nt    { color: #000080 } // Name.Tag
    .nv    { color: #008080 } // Name.Variable
    .ow    { font-weight: bold } // Operator.Word
    .w     { color: #bbb } // Text.Whitespace
    .mf    { color: #099 } // Literal.Number.Float
    .mh    { color: #099 } // Literal.Number.Hex
    .mi    { color: #099 } // Literal.Number.Integer
    .mo    { color: #099 } // Literal.Number.Oct
    .sb    { color: #d14 } // Literal.String.Backtick
    .sc    { color: #d14 } // Literal.String.Char
    .sd    { color: #d14 } // Literal.String.Doc
    .s2    { color: #d14 } // Literal.String.Double
    .se    { color: #d14 } // Literal.String.Escape
    .sh    { color: #d14 } // Literal.String.Heredoc
    .si    { color: #d14 } // Literal.String.Interpol
    .sx    { color: #d14 } // Literal.String.Other
    .sr    { color: #009926 } // Literal.String.Regex
    .s1    { color: #d14 } // Literal.String.Single
    .ss    { color: #990073 } // Literal.String.Symbol
    .bp    { color: #999 } // Name.Builtin.Pseudo
    .vc    { color: #008080 } // Name.Variable.Class
    .vg    { color: #008080 } // Name.Variable.Global
    .vi    { color: #008080 } // Name.Variable.Instance
    .il    { color: #099 } // Literal.Number.Integer.Long
}</file><file path="docs/_sass/jekyll-simple-search.scss">@import &quot;custom&quot;;
@import &quot;base&quot;;
@import &quot;layout&quot;;
@import &quot;syntax-highlighting&quot;;</file><file path="docs/assets/css/main.scss">---
---

@import &apos;jekyll-simple-search&apos;;</file><file path="docs/assets/data/search.json">---
layout: none
---
[
  {% for post in site.posts %}
    {
      &quot;title&quot;    : &quot;{{ post.title | escape }}&quot;,
      &quot;category&quot; : &quot;{{ post.category }}&quot;,
      &quot;tags&quot;     : &quot;{{ post.tags | join: &apos;, &apos; }}&quot;,
      &quot;url&quot;      : &quot;{{ post.url | relative_url }}&quot;,
      &quot;date&quot;     : &quot;{{ post.date }}&quot;,
      &quot;content&quot;  : {{ post.content | strip_html | strip_newlines | strip | escape | jsonify }}
    } {% unless forloop.last %},{% endunless %}
  {% endfor %}
]</file><file path="docs/assets/js/simple-jekyll-search.min.js">/*!
  * Simple-Jekyll-Search v2.1.1
  * Copyright 2015-2022, Christian Fei
  * Copyright 2025-2026, Sylhare
  * Licensed under the MIT License.
  */
(function(global,factory){typeof exports===&quot;object&quot;&amp;&amp;typeof module!==&quot;undefined&quot;?factory(exports):typeof define===&quot;function&quot;&amp;&amp;define.amd?define([&quot;exports&quot;],factory):(global=typeof globalThis!==&quot;undefined&quot;?globalThis:global||self,factory(global.SimpleJekyllSearch={}))})(this,function(exports2){&quot;use strict&quot;;function load(location,callback){const xhr=getXHR();xhr.open(&quot;GET&quot;,location,true);xhr.onreadystatechange=createStateChangeListener(xhr,callback);xhr.send()}function createStateChangeListener(xhr,callback){return function(){if(xhr.readyState===4&amp;&amp;xhr.status===200){try{callback(null,JSON.parse(xhr.responseText))}catch(err){callback(err instanceof Error?err:new Error(String(err)),null)}}}}function getXHR(){return window.XMLHttpRequest?new window.XMLHttpRequest:new window.ActiveXObject(&quot;Microsoft.XMLHTTP&quot;)}class OptionsValidator{constructor(params){if(!this.validateParams(params)){throw new Error(&quot;-- OptionsValidator: required options missing&quot;)}this.requiredOptions=params.required}getRequiredOptions(){return this.requiredOptions}validate(parameters){const errors=[];this.requiredOptions.forEach(requiredOptionName=&gt;{if(typeof parameters[requiredOptionName]===&quot;undefined&quot;){errors.push(requiredOptionName)}});return errors}validateParams(params){if(!params){return false}return typeof params.required!==&quot;undefined&quot;&amp;&amp;Array.isArray(params.required)}}function findLiteralMatches(text,criteria){const lowerText=text.trim().toLowerCase();const pattern=criteria.endsWith(&quot; &quot;)?[criteria.toLowerCase()]:criteria.trim().toLowerCase().split(&quot; &quot;);const wordsFound=pattern.filter(word=&gt;lowerText.indexOf(word)&gt;=0).length;if(wordsFound!==pattern.length){return[]}const matches=[];for(const word of pattern){if(!word||word.length===0)continue;let startIndex=0;while((startIndex=lowerText.indexOf(word,startIndex))!==-1){matches.push({start:startIndex,end:startIndex+word.length,text:text.substring(startIndex,startIndex+word.length),type:&quot;exact&quot;});startIndex+=word.length}}return matches}function findFuzzyMatches(text,criteria){criteria=criteria.trimEnd();if(criteria.length===0)return[];const lowerText=text.toLowerCase();const lowerCriteria=criteria.toLowerCase();let textIndex=0;let criteriaIndex=0;const matchedIndices=[];while(textIndex&lt;text.length&amp;&amp;criteriaIndex&lt;criteria.length){if(lowerText[textIndex]===lowerCriteria[criteriaIndex]){matchedIndices.push(textIndex);criteriaIndex++}textIndex++}if(criteriaIndex!==criteria.length){return[]}if(matchedIndices.length===0){return[]}const start=matchedIndices[0];const end=matchedIndices[matchedIndices.length-1]+1;return[{start:start,end:end,text:text.substring(start,end),type:&quot;fuzzy&quot;}]}function findWildcardMatches(text,pattern,config={}){const regexPattern=pattern.replace(/\*/g,buildWildcardFragment(config));const regex=new RegExp(regexPattern,&quot;gi&quot;);const matches=[];let match;while((match=regex.exec(text))!==null){matches.push({start:match.index,end:match.index+match[0].length,text:match[0],type:&quot;wildcard&quot;});if(regex.lastIndex===match.index){regex.lastIndex++}}return matches}function buildWildcardFragment(config){const maxSpaces=normalizeMaxSpaces(config.maxSpaces);if(maxSpaces===0){return&quot;[^ ]*&quot;}if(maxSpaces===Infinity){return&quot;[^ ]*(?: [^ ]*)*&quot;}return`[^ ]*(?: [^ ]*){0,${maxSpaces}}`}function normalizeMaxSpaces(value){if(typeof value!==&quot;number&quot;||Number.isNaN(value)||value&lt;=0){return 0}if(!Number.isFinite(value)){return Infinity}return Math.floor(value)}class SearchStrategy{constructor(findMatchesFunction){this.findMatchesFunction=findMatchesFunction}matches(text,criteria){if(text===null||text.trim()===&quot;&quot;||!criteria){return false}const matchInfo=this.findMatchesFunction(text,criteria);return matchInfo.length&gt;0}findMatches(text,criteria){if(text===null||text.trim()===&quot;&quot;||!criteria){return[]}return this.findMatchesFunction(text,criteria)}}const LiteralSearchStrategy=new SearchStrategy(findLiteralMatches);const FuzzySearchStrategy=new SearchStrategy((text,criteria)=&gt;{const fuzzyMatches=findFuzzyMatches(text,criteria);if(fuzzyMatches.length&gt;0){return fuzzyMatches}return findLiteralMatches(text,criteria)});class WildcardSearchStrategy extends SearchStrategy{constructor(config={}){const normalizedConfig={...config};super((text,criteria)=&gt;{const wildcardMatches=findWildcardMatches(text,criteria,normalizedConfig);if(wildcardMatches.length&gt;0){return wildcardMatches}return findLiteralMatches(text,criteria)});this.config=normalizedConfig}getConfig(){return{...this.config}}}new WildcardSearchStrategy;class HybridSearchStrategy extends SearchStrategy{constructor(config={}){super((text,criteria)=&gt;this.hybridFind(text,criteria));this.config={...config,preferFuzzy:config.preferFuzzy??false,wildcardPriority:config.wildcardPriority??true,minFuzzyLength:config.minFuzzyLength??4,maxExtraFuzzyChars:config.maxExtraFuzzyChars??2,maxSpaces:config.maxSpaces??1}}hybridFind(text,criteria){if(this.config.wildcardPriority&amp;&amp;criteria.includes(&quot;*&quot;)){const wildcardMatches=findWildcardMatches(text,criteria,this.config);if(wildcardMatches.length&gt;0)return wildcardMatches}if(criteria.includes(&quot; &quot;)||criteria.length&lt;this.config.minFuzzyLength){const literalMatches=findLiteralMatches(text,criteria);if(literalMatches.length&gt;0)return literalMatches}if(this.config.preferFuzzy||criteria.length&gt;=this.config.minFuzzyLength){const fuzzyMatches=findFuzzyMatches(text,criteria);if(fuzzyMatches.length&gt;0){const constrainedMatches=this.applyFuzzyConstraints(fuzzyMatches,criteria);if(constrainedMatches.length&gt;0)return constrainedMatches}}return findLiteralMatches(text,criteria)}applyFuzzyConstraints(matches,criteria){const limit=this.config.maxExtraFuzzyChars;if(!Number.isFinite(limit)||limit&lt;0){return matches}const normalizedCriteriaLength=this.normalizeLength(criteria);if(normalizedCriteriaLength===0){return matches}return matches.filter(match=&gt;{const normalizedMatchLength=this.normalizeLength(match.text);const extraChars=Math.max(0,normalizedMatchLength-normalizedCriteriaLength);return extraChars&lt;=limit})}normalizeLength(value){return value.replace(/\s+/g,&quot;&quot;).length}}const DefaultHybridSearchStrategy=new HybridSearchStrategy;class StrategyFactory{static create(config={type:&quot;literal&quot;}){const{options:options2}=config;const type=this.isValidStrategy(config.type)?config.type:&quot;literal&quot;;switch(type){case&quot;literal&quot;:return LiteralSearchStrategy;case&quot;fuzzy&quot;:return FuzzySearchStrategy;case&quot;wildcard&quot;:return new WildcardSearchStrategy(options2);case&quot;hybrid&quot;:return new HybridSearchStrategy(options2);default:return LiteralSearchStrategy}}static getAvailableStrategies(){return[&quot;literal&quot;,&quot;fuzzy&quot;,&quot;wildcard&quot;,&quot;hybrid&quot;]}static isValidStrategy(type){return this.getAvailableStrategies().includes(type)}}function merge(target,source){return{...target,...source}}function isJSON(json){return Array.isArray(json)||json!==null&amp;&amp;typeof json===&quot;object&quot;}function NoSort(){return 0}function isObject(obj){return Boolean(obj)&amp;&amp;Object.prototype.toString.call(obj)===&quot;[object Object]&quot;}const DEFAULT_OPTIONS={searchInput:null,resultsContainer:null,json:[],success:function(){},searchResultTemplate:&apos;&lt;li&gt;&lt;a href=&quot;{url}&quot; title=&quot;{desc}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,templateMiddleware:(_prop,_value,_template)=&gt;void 0,sortMiddleware:NoSort,noResultsText:&quot;No results found&quot;,limit:10,strategy:&quot;literal&quot;,debounceTime:null,exclude:[],onSearch:()=&gt;{},onError:error=&gt;console.error(&quot;SimpleJekyllSearch error:&quot;,error),fuzzy:false};const REQUIRED_OPTIONS=[&quot;searchInput&quot;,&quot;resultsContainer&quot;,&quot;json&quot;];const WHITELISTED_KEYS=new Set([&quot;Enter&quot;,&quot;Shift&quot;,&quot;CapsLock&quot;,&quot;ArrowLeft&quot;,&quot;ArrowUp&quot;,&quot;ArrowRight&quot;,&quot;ArrowDown&quot;,&quot;Meta&quot;]);class Repository{constructor(initialOptions={}){this.data=[];this.excludePatterns=[];this.setOptions(initialOptions)}put(input){if(isObject(input)){return this.addObject(input)}if(Array.isArray(input)){return this.addArray(input)}return void 0}clear(){this.data.length=0;return this.data}search(criteria){if(!criteria){return[]}const matches=this.findMatches(this.data,criteria).sort(this.options.sortMiddleware);return matches.map(item=&gt;({...item}))}setOptions(newOptions){let strategyConfig=this.normalizeStrategyOption(newOptions?.strategy??DEFAULT_OPTIONS.strategy);if(newOptions?.fuzzy&amp;&amp;!newOptions?.strategy){console.warn(&apos;[Simple Jekyll Search] Warning: fuzzy option is deprecated. Use strategy: &quot;fuzzy&quot; instead.&apos;);strategyConfig={type:&quot;fuzzy&quot;}}const exclude=newOptions?.exclude||DEFAULT_OPTIONS.exclude;this.excludePatterns=exclude.map(pattern=&gt;new RegExp(pattern));this.options={limit:newOptions?.limit||DEFAULT_OPTIONS.limit,searchStrategy:this.searchStrategy(strategyConfig),sortMiddleware:newOptions?.sortMiddleware||DEFAULT_OPTIONS.sortMiddleware,exclude:exclude,strategy:strategyConfig}}addObject(obj){this.data.push(obj);return this.data}addArray(arr){const added=[];this.clear();for(const item of arr){if(isObject(item)){added.push(this.addObject(item)[0])}}return added}findMatches(data,criteria){const matches=[];for(let i=0;i&lt;data.length&amp;&amp;matches.length&lt;this.options.limit;i++){const match=this.findMatchesInObject(data[i],criteria);if(match){matches.push(match)}}return matches}findMatchesInObject(obj,criteria){let hasMatch=false;const result={...obj};result._matchInfo={};for(const key in obj){if(!this.isExcluded(obj[key])&amp;&amp;this.options.searchStrategy.matches(obj[key],criteria)){hasMatch=true;if(this.options.searchStrategy.findMatches){const matchInfo=this.options.searchStrategy.findMatches(obj[key],criteria);if(matchInfo&amp;&amp;matchInfo.length&gt;0){result._matchInfo[key]=matchInfo}}}}return hasMatch?result:void 0}isExcluded(term){const termStr=String(term);return this.excludePatterns.some(regex=&gt;regex.test(termStr))}searchStrategy(strategy){if(!strategy?.type||!StrategyFactory.isValidStrategy(strategy.type)){return LiteralSearchStrategy}return StrategyFactory.create(strategy)}normalizeStrategyOption(strategy){if(!strategy){return this.getDefaultStrategyConfig()}return typeof strategy===&quot;string&quot;?{type:strategy}:strategy}getDefaultStrategyConfig(){const defaultStrategy=DEFAULT_OPTIONS.strategy;{return{type:defaultStrategy}}}}const options={pattern:/\{(.*?)\}/g,template:&quot;&quot;,middleware:function(){return void 0}};function setOptions(_options){if(_options.pattern){options.pattern=_options.pattern}if(_options.template){options.template=_options.template}if(typeof _options.middleware===&quot;function&quot;){options.middleware=_options.middleware}}function compile(data,query){return options.template.replace(options.pattern,function(match,prop){const matchInfo=data._matchInfo?.[prop];if(matchInfo&amp;&amp;matchInfo.length&gt;0&amp;&amp;query){const value2=options.middleware(prop,data[prop],options.template,query,matchInfo);if(typeof value2!==&quot;undefined&quot;){return value2}}if(query){const value2=options.middleware(prop,data[prop],options.template,query);if(typeof value2!==&quot;undefined&quot;){return value2}}const value=options.middleware(prop,data[prop],options.template);if(typeof value!==&quot;undefined&quot;){return value}return data[prop]||match})}let SimpleJekyllSearch$1=class SimpleJekyllSearch{constructor(){this.debounceTimerHandle=null;this.eventHandler=null;this.pageShowHandler=null;this.pendingRequest=null;this.isInitialized=false;this.STORAGE_KEY=&quot;sjs-search-state&quot;;this.options={...DEFAULT_OPTIONS};this.repository=new Repository;this.optionsValidator=new OptionsValidator({required:REQUIRED_OPTIONS})}debounce(func,delayMillis){if(delayMillis){if(this.debounceTimerHandle){clearTimeout(this.debounceTimerHandle)}this.debounceTimerHandle=setTimeout(func,delayMillis)}else{func()}}throwError(message){throw new Error(`SimpleJekyllSearch --- ${message}`)}emptyResultsContainer(){this.options.resultsContainer.innerHTML=&quot;&quot;}initWithJSON(json){this.repository.put(json);this.registerInput()}initWithURL(url){load(url,(err,json)=&gt;{if(err){this.throwError(`Failed to load JSON from ${url}: ${err.message}`)}this.initWithJSON(json)})}registerInput(){this.eventHandler=e=&gt;{try{const inputEvent=e;if(!WHITELISTED_KEYS.has(inputEvent.key)){this.emptyResultsContainer();this.debounce(()=&gt;{try{this.search(e.target.value)}catch(searchError){console.error(&quot;Search error:&quot;,searchError);this.options.onError?.(searchError)}},this.options.debounceTime??null)}}catch(error){console.error(&quot;Input handler error:&quot;,error);this.options.onError?.(error)}};this.options.searchInput.addEventListener(&quot;input&quot;,this.eventHandler);this.pageShowHandler=()=&gt;{this.restoreSearchState()};window.addEventListener(&quot;pageshow&quot;,this.pageShowHandler);this.restoreSearchState()}saveSearchState(query){if(!query?.trim()){this.clearSearchState();return}try{const state={query:query.trim(),timestamp:Date.now(),path:window.location.pathname};sessionStorage.setItem(this.STORAGE_KEY,JSON.stringify(state))}catch{}}getStoredSearchState(){try{const raw=sessionStorage.getItem(this.STORAGE_KEY);if(!raw)return null;const state=JSON.parse(raw);if(typeof state?.query!==&quot;string&quot;)return null;const MAX_AGE_MS=30*60*1e3;if(Date.now()-state.timestamp&gt;MAX_AGE_MS){this.clearSearchState();return null}if(state.path&amp;&amp;state.path!==window.location.pathname){this.clearSearchState();return null}return state.query}catch{this.clearSearchState();return null}}clearSearchState(){try{sessionStorage.removeItem(this.STORAGE_KEY)}catch{}}restoreSearchState(){const hasExistingResults=this.options.resultsContainer.children.length&gt;0;if(hasExistingResults)return;let query=this.options.searchInput.value?.trim();if(!query){query=this.getStoredSearchState()||&quot;&quot;}if(query.length&gt;0){this.options.searchInput.value=query;this.search(query)}}search(query){if(query?.trim().length&gt;0){this.saveSearchState(query);this.emptyResultsContainer();const results=this.repository.search(query);this.render(results,query);this.options.onSearch?.()}else{this.clearSearchState()}}render(results,query){if(results.length===0){this.options.resultsContainer.insertAdjacentHTML(&quot;beforeend&quot;,this.options.noResultsText);return}const fragment=document.createDocumentFragment();results.forEach(result=&gt;{result.query=query;const div=document.createElement(&quot;div&quot;);div.innerHTML=compile(result,query);fragment.appendChild(div)});this.options.resultsContainer.appendChild(fragment)}destroy(){if(this.eventHandler){this.options.searchInput.removeEventListener(&quot;input&quot;,this.eventHandler);this.eventHandler=null}if(this.pageShowHandler){window.removeEventListener(&quot;pageshow&quot;,this.pageShowHandler);this.pageShowHandler=null}if(this.debounceTimerHandle){clearTimeout(this.debounceTimerHandle);this.debounceTimerHandle=null}this.clearSearchState()}init(_options){const errors=this.optionsValidator.validate(_options);if(errors.length&gt;0){this.throwError(`Missing required options: ${REQUIRED_OPTIONS.join(&quot;, &quot;)}`)}this.options=merge(this.options,_options);setOptions({template:this.options.searchResultTemplate,middleware:this.options.templateMiddleware});this.repository.setOptions({limit:this.options.limit,sortMiddleware:this.options.sortMiddleware,strategy:this.options.strategy,exclude:this.options.exclude});if(isJSON(this.options.json)){this.initWithJSON(this.options.json)}else{this.initWithURL(this.options.json)}const rv={search:this.search.bind(this),destroy:this.destroy.bind(this)};this.options.success?.call(rv);return rv}};function escapeHtml(text){const map={&quot;&amp;&quot;:&quot;&amp;amp;&quot;,&quot;&lt;&quot;:&quot;&amp;lt;&quot;,&quot;&gt;&quot;:&quot;&amp;gt;&quot;,&apos;&quot;&apos;:&quot;&amp;quot;&quot;,&quot;&apos;&quot;:&quot;&amp;#039;&quot;};return text.replace(/[&amp;&lt;&gt;&quot;&apos;]/g,m=&gt;map[m])}function mergeOverlappingMatches(matches){if(matches.length===0)return[];const sorted=[...matches].sort((a,b)=&gt;a.start-b.start);const merged=[{...sorted[0]}];for(let i=1;i&lt;sorted.length;i++){const current=sorted[i];const last=merged[merged.length-1];if(current.start&lt;=last.end){last.end=Math.max(last.end,current.end)}else{merged.push({...current})}}return merged}function highlightWithMatchInfo(text,matchInfo,options2={}){if(!text||matchInfo.length===0){return escapeHtml(text)}const className=options2.className||&quot;search-highlight&quot;;const maxLength=options2.maxLength;const mergedMatches=mergeOverlappingMatches(matchInfo);let result=&quot;&quot;;let lastIndex=0;for(const match of mergedMatches){result+=escapeHtml(text.substring(lastIndex,match.start));result+=`&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(text.substring(match.start,match.end))}&lt;/span&gt;`;lastIndex=match.end}result+=escapeHtml(text.substring(lastIndex));if(maxLength&amp;&amp;result.length&gt;maxLength){result=truncateAroundMatches(text,mergedMatches,maxLength,options2.contextLength||30,className)}return result}function truncateAroundMatches(text,matches,maxLength,contextLength,className){if(matches.length===0){const truncated=text.substring(0,maxLength-3);return escapeHtml(truncated)+&quot;...&quot;}const firstMatch=matches[0];const start=Math.max(0,firstMatch.start-contextLength);const end=Math.min(text.length,firstMatch.end+contextLength);let result=&quot;&quot;;if(start&gt;0){result+=&quot;...&quot;}const snippet=text.substring(start,end);const adjustedMatches=matches.filter(m=&gt;m.start&lt;end&amp;&amp;m.end&gt;start).map(m=&gt;({...m,start:Math.max(0,m.start-start),end:Math.min(snippet.length,m.end-start)}));let lastIndex=0;for(const match of adjustedMatches){result+=escapeHtml(snippet.substring(lastIndex,match.start));result+=`&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(snippet.substring(match.start,match.end))}&lt;/span&gt;`;lastIndex=match.end}result+=escapeHtml(snippet.substring(lastIndex));if(end&lt;text.length){result+=&quot;...&quot;}return result}const DEFAULT_TRUNCATE_FIELDS=[&quot;content&quot;,&quot;desc&quot;,&quot;description&quot;];const DEFAULT_NO_HIGHLIGHT_FIELDS=[&quot;url&quot;,&quot;link&quot;,&quot;href&quot;,&quot;query&quot;];function createHighlightTemplateMiddleware(options2={}){const highlightOptions={className:options2.className||&quot;search-highlight&quot;,maxLength:options2.maxLength,contextLength:options2.contextLength||30};const truncateFields=options2.truncateFields||DEFAULT_TRUNCATE_FIELDS;const noHighlightFields=options2.noHighlightFields||DEFAULT_NO_HIGHLIGHT_FIELDS;return function(prop,value,_template,query,matchInfo){if(typeof value!==&quot;string&quot;){return void 0}if(noHighlightFields.includes(prop)){return void 0}const shouldTruncate=truncateFields.includes(prop);if(matchInfo&amp;&amp;matchInfo.length&gt;0&amp;&amp;query){const fieldOptions={...highlightOptions,maxLength:shouldTruncate?highlightOptions.maxLength:void 0};const highlighted=highlightWithMatchInfo(value,matchInfo,fieldOptions);return highlighted!==value?highlighted:void 0}if(shouldTruncate&amp;&amp;highlightOptions.maxLength&amp;&amp;value.length&gt;highlightOptions.maxLength){return escapeHtml(value.substring(0,highlightOptions.maxLength-3)+&quot;...&quot;)}return void 0}}function defaultHighlightMiddleware(prop,value,template,query,matchInfo){const middleware=createHighlightTemplateMiddleware();return middleware(prop,value,template,query,matchInfo)}function SimpleJekyllSearch(options2){const instance=new SimpleJekyllSearch$1;return instance.init(options2)}if(typeof window!==&quot;undefined&quot;){window.SimpleJekyllSearch=SimpleJekyllSearch;window.createHighlightTemplateMiddleware=createHighlightTemplateMiddleware}exports2.DefaultHybridSearchStrategy=DefaultHybridSearchStrategy;exports2.HybridSearchStrategy=HybridSearchStrategy;exports2.StrategyFactory=StrategyFactory;exports2.createHighlightTemplateMiddleware=createHighlightTemplateMiddleware;exports2.default=SimpleJekyllSearch;exports2.defaultHighlightMiddleware=defaultHighlightMiddleware;exports2.escapeHtml=escapeHtml;exports2.highlightWithMatchInfo=highlightWithMatchInfo;exports2.mergeOverlappingMatches=mergeOverlappingMatches;Object.defineProperties(exports2,{__esModule:{value:true},[Symbol.toStringTag]:{value:&quot;Module&quot;}})});</file><file path="docs/_config.yml"># Site settings
title: Simple Jekyll Search
email: your-email@domain.com
description: A simple search solution for Jekyll sites
baseurl: &quot;/Simple-Jekyll-Search&quot;
url: &quot;https://sylhare.github.io&quot;

# Build settings
markdown: kramdown
encoding: utf-8
sass:
  style: compressed

# Exclude from processing
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor/bundle/
  - vendor/cache/
  - vendor/gems/
  - vendor/ruby/</file><file path="docs/Gemfile">source &quot;https://rubygems.org&quot;

gem &apos;github-pages&apos;, group: :jekyll_plugins</file><file path="docs/get-started.md">---
layout: page
title: Get Started
permalink: /about/
---

This is a jekyll theme inspired by [jekyll-new](github.com/jglovier/jekyll-new) (jekyll 2.0&apos;s default theme),
to showcase the jekyll-simple-search library.

### Create `search.json`

Place the following code in a file called `search.json` in your Jekyll blog. 
(It&apos;s hosted [here]({{ &quot;/assets/data/search.json&quot; | relative_url }}) or in https://github.com/sylhare/Simple-Jekyll-Search/tree/docs/assets/data)

This file will be used as a small data source to perform the searches on the client side:

{% raw %}
```liquid
---
layout: none
---
[
  {% for post in site.posts %}
    {
      &quot;title&quot;    : &quot;{{ post.title | escape }}&quot;,
      &quot;category&quot; : &quot;{{ post.category }}&quot;,
      &quot;tags&quot;     : &quot;{{ post.tags | join: &apos;, &apos; }}&quot;,
      &quot;url&quot;      : &quot;{{ site.baseurl }}{{ post.url }}&quot;,
      &quot;date&quot;     : &quot;{{ post.date }}&quot;
    } {% unless forloop.last %},{% endunless %}
  {% endfor %}
]
```
{% endraw %}

### Add the search bar

SimpleJekyllSearch needs two `DOM` elements to work:

- a search input field
- a result container to display the results

{% raw %}
```html
&lt;div id=&quot;search-demo-container&quot;&gt;
  &lt;input type=&quot;search&quot; id=&quot;search-input&quot; placeholder=&quot;search...&quot;&gt;
  &lt;ul id=&quot;results-container&quot;&gt;&lt;/ul&gt;
&lt;/div&gt;
```
{% endraw %}

### Add the script

Customize SimpleJekyllSearch by passing in your configuration options:

{% raw %}
```html
&lt;script src=&quot;{{ &apos;/assets/js/simple-jekyll-search.min.js&apos; | prepend: site.baseurl }}&quot;&gt;&lt;/script&gt;

&lt;script&gt;
  window.simpleJekyllSearch = new SimpleJekyllSearch({
    searchInput: document.getElementById(&apos;search-input&apos;),
    resultsContainer: document.getElementById(&apos;results-container&apos;),
    json: &apos;{{ &quot;/assets/data/search.json&quot; | relative_url }}&apos;,
    searchResultTemplate: &apos;&lt;li&gt;&lt;a href=&quot;{url}?query={query}&quot; title=&quot;{desc}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,
    noResultsText: &apos;No results found&apos;,
    limit: 10,
    strategy: &apos;fuzzy&apos;,
    exclude: [&apos;Welcome&apos;]
  })
&lt;/script&gt;
```
{% endraw %}</file><file path="docs/index.html">---
layout: default
---

&lt;div class=&quot;home&quot;&gt;

  &lt;h1 class=&quot;page-heading&quot;&gt;Welcome to the Documentation&lt;/h1&gt;

  &lt;div class=&quot;info-text&quot;&gt;
    &lt;p&gt;
      Simple Jekyll Search is a lightweight search solution for Jekyll sites.
      &lt;a href=&quot;/get-started&quot; class=&quot;get-started-link&quot;&gt;Get Started&lt;/a&gt; or visit the
      &lt;a href=&quot;/wiki&quot; class=&quot;wiki-link&quot;&gt;Wiki&lt;/a&gt; for troubleshooting and more information.
    &lt;/p&gt;
    &lt;p&gt;Try out the search bar below to see it in action!&lt;/p&gt;
  &lt;/div&gt;

  {% include search.html %}

  &lt;h1 class=&quot;page-heading&quot;&gt;Posts&lt;/h1&gt;

  &lt;div&gt;
    &lt;p&gt;The posts hosted in this example blog.&lt;/p&gt;
  &lt;/div&gt;

  &lt;ul class=&quot;post-list&quot;&gt;
    {% for post in site.posts %}
      &lt;li&gt;
        &lt;span class=&quot;post-meta&quot;&gt;{{ post.date | date: &quot;%b %-d, %Y&quot; }}&lt;/span&gt;

        &lt;h2&gt;
          &lt;a class=&quot;post-link&quot; href=&quot;{{ post.url | prepend: site.baseurl }}&quot;&gt;{{ post.title }}&lt;/a&gt;
        &lt;/h2&gt;
      &lt;/li&gt;
    {% endfor %}
  &lt;/ul&gt;

&lt;/div&gt;</file><file path="docs/Wiki.md">---
layout: page
title: Wiki
permalink: /wiki/
---

For question and troubleshooting Simple Jekyll Search. 

## If search isn&apos;t working due to invalid JSON

- There is a filter plugin in the _plugins folder which should remove most characters that cause invalid JSON.
  To use it, add the simple_search_filter.rb file to your _plugins folder, and use `remove_chars` as a filter.

For example, in search.json, replace:

{% raw %}
```liquid
&quot;content&quot;: &quot;{{ page.content | strip_html | strip_newlines }}&quot;
```
{% endraw %}

with

{% raw %}
```liquid
&quot;content&quot;: &quot;{{ page.content | strip_html | strip_newlines | remove_chars | escape }}&quot;
```
{% endraw %}
If this doesn&apos;t work when using GitHub pages you can try `jsonify` to make sure the content is json compatible:

{% raw %}
```liquid
&quot;content&quot;: {{ page.content | jsonify }}
```
{% endraw %}

&gt; Note: you don&apos;t need to use quotes `&quot;` in this since `jsonify` automatically inserts them.


## Enabling full-text search

The &quot;full-text&quot; search as to look in the content of the post and not just the title,
as well as the pages.
You could also add another loop for the collections.
Replace `search.json` with the following code:

{% raw %}
```liquid
---
layout: none
---
[
  {% for post in site.posts %}
  {
    &quot;title&quot;    : &quot;{{ post.title | escape }}&quot;,
    &quot;category&quot; : &quot;{{ post.category }}&quot;,
    &quot;tags&quot;     : &quot;{{ post.tags | join: &apos;, &apos; }}&quot;,
    &quot;url&quot;      : &quot;{{ site.baseurl }}{{ post.url }}&quot;,
    &quot;date&quot;     : &quot;{{ post.date }}&quot;,
    &quot;content&quot;  : {{ post.content | strip_html | strip_newlines | jsonify }}
  } {% unless forloop.last %},{% endunless %}
  {% endfor %}
  ,
  {% for page in site.pages %}
  {
    {% if page.title != nil %}
    &quot;title&quot;    : &quot;{{ page.title | escape }}&quot;,
    &quot;category&quot; : &quot;{{ page.category }}&quot;,
    &quot;tags&quot;     : &quot;{{ page.tags | join: &apos;, &apos; }}&quot;,
    &quot;url&quot;      : &quot;{{ site.baseurl }}{{ page.url }}&quot;,
    &quot;date&quot;     : &quot;{{ page.date }}&quot;,
    &quot;content&quot;  : {{ post.content | strip_html | strip_newlines | jsonify }}
      {% endif %}
  } {% unless forloop.last %},{% endunless %}
  {% endfor %}
]
```
{% endraw %}</file><file path="scripts/kill-jekyll.js">import { exec } from &apos;child_process&apos;;

exec(&apos;pkill -f &quot;jekyll&quot; || true&apos;, (error, stdout, stderr) =&gt; {
  if (error) {
    console.log(&apos;No Jekyll processes found or could not kill.&apos;);
  } else {
    console.log(&apos;Jekyll processes terminated successfully.&apos;);
  }
  process.exit(0);
});</file><file path="scripts/stamp.js">&apos;use strict&apos;

import { readFileSync } from &apos;fs&apos;
import { fileURLToPath } from &apos;url&apos;
import { dirname, join } from &apos;path&apos;

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const year = new Date().getFullYear()
const packageJson = JSON.parse(readFileSync(join(__dirname, &apos;..&apos;, &apos;package.json&apos;), &apos;utf8&apos;))

const stampTop =
`/*!
  * Simple-Jekyll-Search v${packageJson.version}
  * Copyright 2015-2022, Christian Fei
  * Copyright 2025-${year}, Sylhare
  * Licensed under the MIT License.
  */
`

let input = &apos;&apos;
process.stdin.on(&apos;data&apos;, chunk =&gt; {
  input += chunk
})

process.stdin.on(&apos;end&apos;, () =&gt; {
  const output = stampTop + input
  process.stdout.write(output)
})</file><file path="scripts/start-jekyll.js">import { spawn, exec } from &apos;child_process&apos;;

console.log(&apos;Checking for processes on port 4000...&apos;);

// Kill any process using port 4000
exec(&apos;lsof -ti:4000 | xargs kill -9 2&gt;/dev/null || true&apos;, (error, stdout, stderr) =&gt; {
  if (stdout) {
    console.log(&apos;Killed process on port 4000&apos;);
  } else {
    console.log(&apos;No process found on port 4000&apos;);
  }
  
  console.log(&apos;Starting Jekyll server in detached mode...&apos;);
  
  const jekyllProcess = spawn(&apos;bundle&apos;, [&apos;exec&apos;, &apos;jekyll&apos;, &apos;serve&apos;, &apos;--detach&apos;], {
    cwd: &apos;docs&apos;,
    stdio: &apos;inherit&apos;,
    shell: true,
    env: {
      ...process.env,
      LANG: &apos;en_US.UTF-8&apos;,
      LC_ALL: &apos;en_US.UTF-8&apos;,
      LC_CTYPE: &apos;en_US.UTF-8&apos;
    }
  });
  
  jekyllProcess.on(&apos;error&apos;, (error) =&gt; {
    console.error(&apos;Error starting Jekyll server:&apos;, error.message);
    process.exit(1);
  });
  
  jekyllProcess.on(&apos;close&apos;, (code) =&gt; {
    if (code === 0) {
      console.log(&apos;Jekyll server started successfully!&apos;);
    } else {
      console.error(`Jekyll server exited with code ${code}`);
    }
    process.exit(code);
  });
});</file><file path="src/middleware/highlighting.ts">import { MatchInfo } from &apos;../SearchStrategies/types&apos;;

export interface HighlightOptions {
  className?: string;
  maxLength?: number;
  contextLength?: number;
}

export function escapeHtml(text: string): string {
  const map: Record&lt;string, string&gt; = {
    &apos;&amp;&apos;: &apos;&amp;amp;&apos;,
    &apos;&lt;&apos;: &apos;&amp;lt;&apos;,
    &apos;&gt;&apos;: &apos;&amp;gt;&apos;,
    &apos;&quot;&apos;: &apos;&amp;quot;&apos;,
    &quot;&apos;&quot;: &apos;&amp;#039;&apos;
  };
  return text.replace(/[&amp;&lt;&gt;&quot;&apos;]/g, m =&gt; map[m]);
}

export function mergeOverlappingMatches(matches: MatchInfo[]): MatchInfo[] {
  if (matches.length === 0) return [];
  
  const sorted = [...matches].sort((a, b) =&gt; a.start - b.start);
  const merged: MatchInfo[] = [{ ...sorted[0] }];
  
  for (let i = 1; i &lt; sorted.length; i++) {
    const current = sorted[i];
    const last = merged[merged.length - 1];
    
    if (current.start &lt;= last.end) {
      last.end = Math.max(last.end, current.end);
    } else {
      merged.push({ ...current });
    }
  }
  
  return merged;
}

export function highlightWithMatchInfo(
  text: string, 
  matchInfo: MatchInfo[], 
  options: HighlightOptions = {}
): string {
  if (!text || matchInfo.length === 0) {
    return escapeHtml(text);
  }
  
  const className = options.className || &apos;search-highlight&apos;;
  const maxLength = options.maxLength;
  
  const mergedMatches = mergeOverlappingMatches(matchInfo);
  
  let result = &apos;&apos;;
  let lastIndex = 0;
  
  for (const match of mergedMatches) {
    result += escapeHtml(text.substring(lastIndex, match.start));
    result += `&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(text.substring(match.start, match.end))}&lt;/span&gt;`;
    lastIndex = match.end;
  }
  
  result += escapeHtml(text.substring(lastIndex));
  
  if (maxLength &amp;&amp; result.length &gt; maxLength) {
    result = truncateAroundMatches(text, mergedMatches, maxLength, options.contextLength || 30, className);
  }
  
  return result;
}

function truncateAroundMatches(
  text: string,
  matches: MatchInfo[],
  maxLength: number,
  contextLength: number,
  className: string
): string {
  if (matches.length === 0) {
    const truncated = text.substring(0, maxLength - 3);
    return escapeHtml(truncated) + &apos;...&apos;;
  }
  
  const firstMatch = matches[0];
  const start = Math.max(0, firstMatch.start - contextLength);
  const end = Math.min(text.length, firstMatch.end + contextLength);
  
  let result = &apos;&apos;;
  
  if (start &gt; 0) {
    result += &apos;...&apos;;
  }
  
  const snippet = text.substring(start, end);
  const adjustedMatches = matches
    .filter(m =&gt; m.start &lt; end &amp;&amp; m.end &gt; start)
    .map(m =&gt; ({
      ...m,
      start: Math.max(0, m.start - start),
      end: Math.min(snippet.length, m.end - start)
    }));
  
  let lastIndex = 0;
  for (const match of adjustedMatches) {
    result += escapeHtml(snippet.substring(lastIndex, match.start));
    result += `&lt;span class=&quot;${className}&quot;&gt;${escapeHtml(snippet.substring(match.start, match.end))}&lt;/span&gt;`;
    lastIndex = match.end;
  }
  result += escapeHtml(snippet.substring(lastIndex));
  
  if (end &lt; text.length) {
    result += &apos;...&apos;;
  }
  
  return result;
}</file><file path="src/middleware/highlightMiddleware.ts">import { MatchInfo } from &apos;../SearchStrategies/types&apos;;
import { highlightWithMatchInfo, HighlightOptions, escapeHtml } from &apos;./highlighting&apos;;

export interface HighlightMiddlewareOptions extends HighlightOptions {
  /**
   * Fields that should be truncated when exceeding maxLength.
   * @default [&apos;content&apos;, &apos;desc&apos;, &apos;description&apos;]
   */
  truncateFields?: string[];
  
  /**
   * Fields that should NOT be highlighted (e.g., fields used in URLs/attributes).
   * These fields will be left untouched to prevent breaking HTML structure.
   * @default [&apos;url&apos;, &apos;link&apos;, &apos;href&apos;, &apos;query&apos;]
   */
  noHighlightFields?: string[];
}

/** Fields that contain long content and should be truncated by default */
const DEFAULT_TRUNCATE_FIELDS = [&apos;content&apos;, &apos;desc&apos;, &apos;description&apos;];

/** Fields that should never be highlighted (used in HTML attributes) */
const DEFAULT_NO_HIGHLIGHT_FIELDS = [&apos;url&apos;, &apos;link&apos;, &apos;href&apos;, &apos;query&apos;];

/**
 * Creates a template middleware that highlights search matches and truncates long content.
 * 
 * When a field has match info, the matched text is wrapped in a highlight span.
 * Fields in `truncateFields` are truncated to `maxLength` even without matches.
 * 
 * @param options - Configuration options for highlighting and truncation
 * @returns A middleware function for use with SimpleJekyllSearch&apos;s templateMiddleware option
 */
export function createHighlightTemplateMiddleware(options: HighlightMiddlewareOptions = {}) {
  const highlightOptions: HighlightOptions = {
    className: options.className || &apos;search-highlight&apos;,
    maxLength: options.maxLength,
    contextLength: options.contextLength || 30
  };
  
  const truncateFields = options.truncateFields || DEFAULT_TRUNCATE_FIELDS;
  const noHighlightFields = options.noHighlightFields || DEFAULT_NO_HIGHLIGHT_FIELDS;

  return function(
    prop: string, 
    value: string, 
    _template: string, 
    query?: string, 
    matchInfo?: MatchInfo[]
  ): string | undefined {
    if (typeof value !== &apos;string&apos;) {
      return undefined;
    }

    if (noHighlightFields.includes(prop)) {
      return undefined;
    }

    const shouldTruncate = truncateFields.includes(prop);

    if (matchInfo &amp;&amp; matchInfo.length &gt; 0 &amp;&amp; query) {
      const fieldOptions: HighlightOptions = {
        ...highlightOptions,
        maxLength: shouldTruncate ? highlightOptions.maxLength : undefined
      };
      const highlighted = highlightWithMatchInfo(value, matchInfo, fieldOptions);
      return highlighted !== value ? highlighted : undefined;
    }
    
    if (shouldTruncate &amp;&amp; highlightOptions.maxLength &amp;&amp; value.length &gt; highlightOptions.maxLength) {
      return escapeHtml(value.substring(0, highlightOptions.maxLength - 3) + &apos;...&apos;);
    }
    
    return undefined;
  };
}

/**
 * Pre-configured highlight middleware with default options.
 * 
 * @param prop - The property name being rendered
 * @param value - The property value
 * @param template - The template string
 * @param query - The search query
 * @param matchInfo - Match position information for highlighting
 * @returns The highlighted/truncated value, or undefined to use original
 */
export function defaultHighlightMiddleware(
  prop: string, 
  value: string, 
  template: string, 
  query?: string, 
  matchInfo?: MatchInfo[]
): string | undefined {
  const middleware = createHighlightTemplateMiddleware();
  return middleware(prop, value, template, query, matchInfo);
}</file><file path="src/SearchStrategies/search/findFuzzyMatches.ts">import { MatchInfo } from &apos;../types&apos;;

/**
 * Finds fuzzy matches where characters appear in sequence (but not necessarily consecutively).
 * Returns a single match spanning from the first to last matched character.
 *
 * @param text - The text to search in
 * @param criteria - The search criteria
 * @returns Array with single MatchInfo if all characters found in sequence, empty array otherwise
 */
export function findFuzzyMatches(text: string, criteria: string): MatchInfo[] {
  criteria = criteria.trimEnd();
  if (criteria.length === 0) return [];

  const lowerText = text.toLowerCase();
  const lowerCriteria = criteria.toLowerCase();
  
  let textIndex = 0;
  let criteriaIndex = 0;
  const matchedIndices: number[] = [];
  
  while (textIndex &lt; text.length &amp;&amp; criteriaIndex &lt; criteria.length) {
    if (lowerText[textIndex] === lowerCriteria[criteriaIndex]) {
      matchedIndices.push(textIndex);
      criteriaIndex++;
    }
    textIndex++;
  }
  
  if (criteriaIndex !== criteria.length) {
    return [];
  }
  
  if (matchedIndices.length === 0) {
    return [];
  }
  
  const start = matchedIndices[0];
  const end = matchedIndices[matchedIndices.length - 1] + 1;
  
  return [{
    start,
    end,
    text: text.substring(start, end),
    type: &apos;fuzzy&apos;
  }];
}</file><file path="src/SearchStrategies/search/findLevenshteinMatches.ts">import { MatchInfo } from &apos;../types&apos;;

/**
 * Calculates the Levenshtein distance between two strings.
 *
 * The Levenshtein distance is a measure of the difference between two strings.
 * It is calculated as the minimum number of single-character edits (insertions, deletions, or substitutions)
 * required to change one string into the other.
 *
 * @param a - The first string
 * @param b - The second string
 * @returns The Levenshtein distance
 */
function levenshtein(a: string, b: string): number {
  const lenA = a.length;
  const lenB = b.length;
  const distanceMatrix: number[][] = Array.from({ length: lenA + 1 }, () =&gt; Array(lenB + 1).fill(0));

  for (let i = 0; i &lt;= lenA; i++) distanceMatrix[i][0] = i;
  for (let j = 0; j &lt;= lenB; j++) distanceMatrix[0][j] = j;

  for (let i = 1; i &lt;= lenA; i++) {
    for (let j = 1; j &lt;= lenB; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      distanceMatrix[i][j] = Math.min(
        distanceMatrix[i - 1][j] + 1,
        distanceMatrix[i][j - 1] + 1,
        distanceMatrix[i - 1][j - 1] + cost
      );
    }
  }

  return distanceMatrix[lenA][lenB];
}

/**
 * Finds matches based on Levenshtein distance (edit distance).
 * Returns a match if the similarity is &gt;= 30% (edit distance allows for typos).
 *
 * @param text - The text to search in
 * @param pattern - The pattern to search for
 * @returns Array with single MatchInfo if similarity threshold met, empty array otherwise
 */
export function findLevenshteinMatches(text: string, pattern: string): MatchInfo[] {
  const distance = levenshtein(pattern, text);
  const similarity = 1 - distance / Math.max(pattern.length, text.length);

  if (similarity &gt;= 0.3) {
    return [{
      start: 0,
      end: text.length,
      text: text,
      type: &apos;fuzzy&apos;
    }];
  }

  return [];
}</file><file path="src/SearchStrategies/search/findLiteralMatches.ts">import { MatchInfo } from &apos;../types&apos;;

/**
 * Finds all literal matches of a search criteria in the text.
 * Handles multi-word searches by splitting on spaces and finding each word.
 * All words must be present for a match.
 *
 * @param text - The text to search in
 * @param criteria - The search criteria (can be multi-word)
 * @returns Array of MatchInfo objects for each word found
 */
export function findLiteralMatches(text: string, criteria: string): MatchInfo[] {
  const lowerText = text.trim().toLowerCase();
  const pattern = criteria.endsWith(&apos; &apos;) 
    ? [criteria.toLowerCase()] 
    : criteria.trim().toLowerCase().split(&apos; &apos;);

  const wordsFound = pattern.filter((word: string) =&gt; lowerText.indexOf(word) &gt;= 0).length;
  
  if (wordsFound !== pattern.length) {
    return [];
  }

  const matches: MatchInfo[] = [];
  
  for (const word of pattern) {
    if (!word || word.length === 0) continue;
    
    let startIndex = 0;
    while ((startIndex = lowerText.indexOf(word, startIndex)) !== -1) {
      matches.push({
        start: startIndex,
        end: startIndex + word.length,
        text: text.substring(startIndex, startIndex + word.length),
        type: &apos;exact&apos;
      });
      startIndex += word.length;
    }
  }
  
  return matches;
}</file><file path="src/SearchStrategies/search/findWildcardMatches.ts">import { MatchInfo, WildcardConfig } from &apos;../types&apos;;

/**
 * Finds matches using wildcard patterns (* matches any non-space characters).
 * Uses regex to find all matching patterns in the text.
 * Wildcards stop at spaces by default - configure `maxSpaces` to span across words.
 *
 * @param text - The text to search in
 * @param pattern - The wildcard pattern (e.g., &quot;hel*&quot; matches &quot;hello&quot; but not &quot;hello world&quot;)
 * @param config - Optional wildcard configuration
 * @returns Array of MatchInfo objects for each wildcard match
 */
export function findWildcardMatches(text: string, pattern: string, config: WildcardConfig = {}): MatchInfo[] {
  const regexPattern = pattern.replace(/\*/g, buildWildcardFragment(config));
  const regex = new RegExp(regexPattern, &apos;gi&apos;);
  const matches: MatchInfo[] = [];
  
  let match;
  while ((match = regex.exec(text)) !== null) {
    matches.push({
      start: match.index,
      end: match.index + match[0].length,
      text: match[0],
      type: &apos;wildcard&apos;
    });
    
    if (regex.lastIndex === match.index) {
      regex.lastIndex++;
    }
  }
  
  return matches;
}

export function buildWildcardFragment(config: WildcardConfig): string {
  const maxSpaces = normalizeMaxSpaces(config.maxSpaces);
  if (maxSpaces === 0) {
    return &apos;[^ ]*&apos;;
  }

  if (maxSpaces === Infinity) {
    return &apos;[^ ]*(?: [^ ]*)*&apos;;
  }

  return `[^ ]*(?: [^ ]*){0,${maxSpaces}}`;
}

function normalizeMaxSpaces(value: number | undefined): number {
  if (typeof value !== &apos;number&apos; || Number.isNaN(value) || value &lt;= 0) {
    return 0;
  }

  if (!Number.isFinite(value)) {
    return Infinity;
  }

  return Math.floor(value);
}</file><file path="src/SearchStrategies/HybridSearchStrategy.ts">import { SearchStrategy, MatchInfo, StrategyOptions } from &apos;./types&apos;;
import { findLiteralMatches } from &apos;./search/findLiteralMatches&apos;;
import { findFuzzyMatches } from &apos;./search/findFuzzyMatches&apos;;
import { findWildcardMatches } from &apos;./search/findWildcardMatches&apos;;

type ResolvedHybridOptions = StrategyOptions &amp; Required&lt;Pick&lt;StrategyOptions, &apos;preferFuzzy&apos; | &apos;wildcardPriority&apos; | &apos;minFuzzyLength&apos; | &apos;maxExtraFuzzyChars&apos; | &apos;maxSpaces&apos;&gt;&gt;;

export class HybridSearchStrategy extends SearchStrategy {
  private config: Readonly&lt;ResolvedHybridOptions&gt;;

  constructor(config: StrategyOptions = {}) {
    super((text: string, criteria: string) =&gt; {
      return this.hybridFind(text, criteria);
    });
    
    this.config = {
      ...config,
      preferFuzzy: config.preferFuzzy ?? false,
      wildcardPriority: config.wildcardPriority ?? true,
      minFuzzyLength: config.minFuzzyLength ?? 4,
      maxExtraFuzzyChars: config.maxExtraFuzzyChars ?? 2,
      maxSpaces: config.maxSpaces ?? 1,
    };
  }

  private hybridFind(text: string, criteria: string): MatchInfo[] {
    if (this.config.wildcardPriority &amp;&amp; criteria.includes(&apos;*&apos;)) {
      const wildcardMatches = findWildcardMatches(text, criteria, this.config);
      if (wildcardMatches.length &gt; 0) return wildcardMatches;
    }

    if (criteria.includes(&apos; &apos;) || criteria.length &lt; this.config.minFuzzyLength) {
      const literalMatches = findLiteralMatches(text, criteria);
      if (literalMatches.length &gt; 0) return literalMatches;
    }

    if (this.config.preferFuzzy || criteria.length &gt;= this.config.minFuzzyLength) {
      const fuzzyMatches = findFuzzyMatches(text, criteria);
      if (fuzzyMatches.length &gt; 0) {
        const constrainedMatches = this.applyFuzzyConstraints(fuzzyMatches, criteria);
        if (constrainedMatches.length &gt; 0) return constrainedMatches;
      }
    }

    return findLiteralMatches(text, criteria);
  }

  private applyFuzzyConstraints(matches: MatchInfo[], criteria: string): MatchInfo[] {
    const limit = this.config.maxExtraFuzzyChars;
    if (!Number.isFinite(limit) || limit &lt; 0) {
      return matches;
    }

    const normalizedCriteriaLength = this.normalizeLength(criteria);
    if (normalizedCriteriaLength === 0) {
      return matches;
    }

    return matches.filter(match =&gt; {
      const normalizedMatchLength = this.normalizeLength(match.text);
      const extraChars = Math.max(0, normalizedMatchLength - normalizedCriteriaLength);
      return extraChars &lt;= limit;
    });
  }

  private normalizeLength(value: string): number {
    return value.replace(/\s+/g, &apos;&apos;).length;
  }
}

export const DefaultHybridSearchStrategy = new HybridSearchStrategy();</file><file path="src/SearchStrategies/SearchStrategy.ts">import { findLiteralMatches } from &apos;./search/findLiteralMatches&apos;;
import { findFuzzyMatches } from &apos;./search/findFuzzyMatches&apos;;
import { findWildcardMatches } from &apos;./search/findWildcardMatches&apos;;
import { SearchStrategy, WildcardConfig } from &apos;./types&apos;;

export const LiteralSearchStrategy = new SearchStrategy(
  findLiteralMatches
);

export const FuzzySearchStrategy = new SearchStrategy(
  (text: string, criteria: string) =&gt; {
    const fuzzyMatches = findFuzzyMatches(text, criteria);
    if (fuzzyMatches.length &gt; 0) {
      return fuzzyMatches;
    }
    return findLiteralMatches(text, criteria);
  }
);

export class WildcardSearchStrategy extends SearchStrategy {
  private readonly config: Readonly&lt;WildcardConfig&gt;;

  constructor(config: WildcardConfig = {}) {
    const normalizedConfig = { ...config };
    super((text: string, criteria: string) =&gt; {
      const wildcardMatches = findWildcardMatches(text, criteria, normalizedConfig);
      if (wildcardMatches.length &gt; 0) {
        return wildcardMatches;
      }
      return findLiteralMatches(text, criteria);
    });
    this.config = normalizedConfig;
  }

  getConfig(): Readonly&lt;WildcardConfig&gt; {
    return { ...this.config };
  }
}

export const DefaultWildcardSearchStrategy = new WildcardSearchStrategy();</file><file path="src/SearchStrategies/StrategyFactory.ts">import { SearchStrategy, StrategyConfig } from &apos;./types&apos;;
import { LiteralSearchStrategy, FuzzySearchStrategy, WildcardSearchStrategy } from &apos;./SearchStrategy&apos;;
import { HybridSearchStrategy } from &apos;./HybridSearchStrategy&apos;;

export type StrategyType = &apos;literal&apos; | &apos;fuzzy&apos; | &apos;wildcard&apos; | &apos;hybrid&apos;;

export class StrategyFactory {
  static create(config: StrategyConfig = { type: &apos;literal&apos; }): SearchStrategy {
    const { options } = config;
    const type = this.isValidStrategy(config.type) ? config.type : &apos;literal&apos;;

    switch (type) {
      case &apos;literal&apos;:
        return LiteralSearchStrategy;
      
      case &apos;fuzzy&apos;:
        return FuzzySearchStrategy;
      
      case &apos;wildcard&apos;:
        return new WildcardSearchStrategy(options);
      
      case &apos;hybrid&apos;:
        return new HybridSearchStrategy(options);
      
      default:
        return LiteralSearchStrategy;
    }
  }

  static getAvailableStrategies(): StrategyType[] {
    return [&apos;literal&apos;, &apos;fuzzy&apos;, &apos;wildcard&apos;, &apos;hybrid&apos;];
  }

  static isValidStrategy(type: string): type is StrategyType {
    return this.getAvailableStrategies().includes(type as StrategyType);
  }
}</file><file path="src/SearchStrategies/types.ts">import type { StrategyType } from &apos;./StrategyFactory&apos;;

export interface MatchInfo {
  start: number;
  end: number;
  text: string;
  type: &apos;exact&apos; | &apos;fuzzy&apos; | &apos;wildcard&apos;;
}

export interface Matcher {
  matches(text: string | null, criteria: string): boolean;
  findMatches?(text: string | null, criteria: string): MatchInfo[];
}

export interface HybridConfig {
  preferFuzzy?: boolean;
  wildcardPriority?: boolean;
  minFuzzyLength?: number;
  /**
   * Maximum number of additional non-whitespace characters that a fuzzy match
   * is allowed to span beyond the query length. Set to a negative number or
   * Infinity to disable this guard.
   */
  maxExtraFuzzyChars?: number;
}

export interface WildcardOptions {
  /**
   * Maximum number of spaces a `*` wildcard is allowed to span within a single match.
   * Defaults to 0, which means wildcards stop at spaces.
   */
  maxSpaces?: number;
}

export type WildcardConfig = WildcardOptions;

export interface StrategyOptions extends HybridConfig, WildcardConfig {}

export interface StrategyConfig {
  type: StrategyType;
  options?: StrategyOptions;
}

export class SearchStrategy implements Matcher {
  private readonly findMatchesFunction: (text: string, criteria: string) =&gt; MatchInfo[];

  constructor(findMatchesFunction: (text: string, criteria: string) =&gt; MatchInfo[]) {
    this.findMatchesFunction = findMatchesFunction;
  }

  matches(text: string | null, criteria: string): boolean {
    if (text === null || text.trim() === &apos;&apos; || !criteria) {
      return false;
    }

    const matchInfo = this.findMatchesFunction(text, criteria);
    return matchInfo.length &gt; 0;
  }

  findMatches(text: string | null, criteria: string): MatchInfo[] {
    if (text === null || text.trim() === &apos;&apos; || !criteria) {
      return [];
    }

    return this.findMatchesFunction(text, criteria);
  }
}</file><file path="src/types/global.d.ts">import { SearchOptions, SimpleJekyllSearchInstance } from &apos;../utils/types&apos;;

declare global {
  interface Window {
    SimpleJekyllSearch: (options: SearchOptions) =&gt; SimpleJekyllSearchInstance;
  }
}</file><file path="src/utils/default.ts">import { NoSort } from &apos;../utils&apos;;
import { SearchOptions } from &apos;./types&apos;;

export const DEFAULT_OPTIONS: Required&lt;SearchOptions&gt; = {
  searchInput: null!,
  resultsContainer: null!,
  json: [],
  success: function(this: { search: (query: string) =&gt; void }) {},
  searchResultTemplate: &apos;&lt;li&gt;&lt;a href=&quot;{url}&quot; title=&quot;{desc}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,
  templateMiddleware: (_prop: string, _value: string, _template: string) =&gt; undefined,
  sortMiddleware: NoSort,
  noResultsText: &apos;No results found&apos;,
  limit: 10,
  strategy: &apos;literal&apos;,
  debounceTime: null,
  exclude: [],
  onSearch: () =&gt; {},
  onError: (error: Error) =&gt; console.error(&apos;SimpleJekyllSearch error:&apos;, error),
  fuzzy: false  // Deprecated, use strategy: &apos;fuzzy&apos; instead
};

export const REQUIRED_OPTIONS = [&apos;searchInput&apos;, &apos;resultsContainer&apos;, &apos;json&apos;];

export const WHITELISTED_KEYS = new Set([
  &apos;Enter&apos;, &apos;Shift&apos;, &apos;CapsLock&apos;, &apos;ArrowLeft&apos;, &apos;ArrowUp&apos;, &apos;ArrowRight&apos;, &apos;ArrowDown&apos;, &apos;Meta&apos;,
]);</file><file path="src/utils/types.ts">import { Matcher, StrategyConfig } from &apos;../SearchStrategies/types&apos;;
import { StrategyType } from &apos;../SearchStrategies/StrategyFactory&apos;;

export interface SearchResult {
  url: string;
  title: string;
  desc: string;
  query?: string;
}

export interface SearchData {
  url: string;
  title: string;
  category?: string;
  tags?: string;
  date?: string;
  content?: string;
}

export interface RepositoryOptions {
  /** @deprecated Use strategy instead (e.g. `strategy: &apos;fuzzy&apos;`) */
  fuzzy?: boolean;
  strategy?: StrategyType | StrategyConfig;
  limit?: number;
  searchStrategy?: Matcher;
  sortMiddleware?: (a: any, b: any) =&gt; number;
  exclude?: string[];
}

export interface RepositoryData {
  [key: string]: any;
  _matchInfo?: Record&lt;string, import(&apos;../SearchStrategies/types&apos;).MatchInfo[]&gt;;
}

export interface SearchOptions extends Omit&lt;RepositoryOptions, &apos;searchStrategy&apos;&gt; {
  searchInput: HTMLInputElement;
  resultsContainer: HTMLElement;
  json: SearchData[] | string;
  success?: (this: { search: (query: string) =&gt; void }) =&gt; void;
  searchResultTemplate?: string;
  templateMiddleware?: (
    prop: string, 
    value: string, 
    template: string, 
    query?: string, 
    matchInfo?: import(&apos;../SearchStrategies/types&apos;).MatchInfo[]
  ) =&gt; string | undefined;
  noResultsText?: string;
  debounceTime?: number | null;
  onSearch?: () =&gt; void;
  onError?: (error: Error) =&gt; void;
}

export interface SimpleJekyllSearchInstance {
  search: (query: string) =&gt; void;
  destroy: () =&gt; void;
}</file><file path="src/index.ts">import SimpleJekyllSearchClass from &apos;./SimpleJekyllSearch&apos;;
import { SearchOptions, SimpleJekyllSearchInstance } from &apos;./utils/types&apos;;
import { createHighlightTemplateMiddleware } from &apos;./middleware/highlightMiddleware&apos;;

function SimpleJekyllSearch(options: SearchOptions): SimpleJekyllSearchInstance {
  const instance = new SimpleJekyllSearchClass();
  return instance.init(options);
}

export default SimpleJekyllSearch;
export type { MatchInfo } from &apos;./SearchStrategies/types&apos;;
export type { HighlightOptions } from &apos;./middleware/highlighting&apos;;
export { highlightWithMatchInfo, escapeHtml, mergeOverlappingMatches } from &apos;./middleware/highlighting&apos;;
export { createHighlightTemplateMiddleware, defaultHighlightMiddleware } from &apos;./middleware/highlightMiddleware&apos;;

export { HybridSearchStrategy, DefaultHybridSearchStrategy } from &apos;./SearchStrategies/HybridSearchStrategy&apos;;
export type { HybridConfig } from &apos;./SearchStrategies/types&apos;;
export { StrategyFactory } from &apos;./SearchStrategies/StrategyFactory&apos;;
export type { StrategyType } from &apos;./SearchStrategies/StrategyFactory&apos;;

// Add to window if in browser environment
if (typeof window !== &apos;undefined&apos;) {
  (window as any).SimpleJekyllSearch = SimpleJekyllSearch;
  (window as any).createHighlightTemplateMiddleware = createHighlightTemplateMiddleware;
}</file><file path="src/JSONLoader.ts">interface XHR extends XMLHttpRequest {
  readyState: number;
  status: number;
  responseText: string;
}

interface WindowWithActiveX extends Window {
  ActiveXObject: new (type: string) =&gt; XHR;
}

type Callback = (error: Error | null, data: any) =&gt; void;

export function load(location: string, callback: Callback): void {
  const xhr = getXHR();
  xhr.open(&apos;GET&apos;, location, true);
  xhr.onreadystatechange = createStateChangeListener(xhr, callback);
  xhr.send();
}

function createStateChangeListener(xhr: XHR, callback: Callback): () =&gt; void {
  return function() {
    if (xhr.readyState === 4 &amp;&amp; xhr.status === 200) {
      try {
        callback(null, JSON.parse(xhr.responseText));
      } catch (err) {
        callback(err instanceof Error ? err : new Error(String(err)), null);
      }
    }
  };
}

function getXHR(): XHR {
  return window.XMLHttpRequest 
    ? new window.XMLHttpRequest() 
    : new ((window as unknown) as WindowWithActiveX).ActiveXObject(&apos;Microsoft.XMLHTTP&apos;);
}</file><file path="src/OptionsValidator.ts">interface ValidatorParams {
  required: string[];
}

interface ValidatorOptions {
  [key: string]: any;
}

export class OptionsValidator {
  private readonly requiredOptions: string[];

  constructor(params: ValidatorParams) {
    if (!this.validateParams(params)) {
      throw new Error(&apos;-- OptionsValidator: required options missing&apos;);
    }

    this.requiredOptions = params.required;
  }

  public getRequiredOptions(): string[] {
    return this.requiredOptions;
  }

  public validate(parameters: ValidatorOptions): string[] {
    const errors: string[] = [];
    this.requiredOptions.forEach((requiredOptionName: string) =&gt; {
      if (typeof parameters[requiredOptionName] === &apos;undefined&apos;) {
        errors.push(requiredOptionName);
      }
    });
    return errors;
  }

  private validateParams(params: ValidatorParams): boolean {
    if (!params) {
      return false;
    }
    return typeof params.required !== &apos;undefined&apos; &amp;&amp; Array.isArray(params.required);
  }
}</file><file path="src/Repository.ts">import { LiteralSearchStrategy } from &apos;./SearchStrategies/SearchStrategy&apos;;
import { Matcher, StrategyConfig } from &apos;./SearchStrategies/types&apos;;
import { StrategyFactory, StrategyType } from &apos;./SearchStrategies/StrategyFactory&apos;;
import { isObject } from &apos;./utils&apos;;
import { DEFAULT_OPTIONS } from &apos;./utils/default&apos;;
import { RepositoryData, RepositoryOptions } from &apos;./utils/types&apos;;

export class Repository {
  private data: RepositoryData[] = [];
  private options!: Required&lt;Omit&lt;RepositoryOptions, &apos;fuzzy&apos;&gt;&gt; &amp; Pick&lt;RepositoryOptions, &apos;fuzzy&apos;&gt;;
  private excludePatterns: RegExp[] = [];

  constructor(initialOptions: RepositoryOptions = {}) {
    this.setOptions(initialOptions);
  }

  public put(input: RepositoryData | RepositoryData[]): RepositoryData[] | undefined {
    if (isObject(input)) {
      return this.addObject(input);
    }
    if (Array.isArray(input)) {
      return this.addArray(input);
    }
    return undefined;
  }

  public clear(): RepositoryData[] {
    this.data.length = 0;
    return this.data;
  }

  public search(criteria: string): RepositoryData[] {
    if (!criteria) {
      return [];
    }
    const matches = this.findMatches(this.data, criteria).sort(this.options.sortMiddleware);
    return matches.map(item =&gt; ({ ...item }));
  }

  public setOptions(newOptions: RepositoryOptions): void {
    let strategyConfig = this.normalizeStrategyOption(newOptions?.strategy ?? DEFAULT_OPTIONS.strategy);
    
    if (newOptions?.fuzzy &amp;&amp; !newOptions?.strategy) {
      console.warn(&apos;[Simple Jekyll Search] Warning: fuzzy option is deprecated. Use strategy: &quot;fuzzy&quot; instead.&apos;);
      strategyConfig = { type: &apos;fuzzy&apos; };
    }
    
    const exclude = newOptions?.exclude || DEFAULT_OPTIONS.exclude;
    this.excludePatterns = exclude.map(pattern =&gt; new RegExp(pattern));
    this.options = {
      limit: newOptions?.limit || DEFAULT_OPTIONS.limit,
      searchStrategy: this.searchStrategy(strategyConfig),
      sortMiddleware: newOptions?.sortMiddleware || DEFAULT_OPTIONS.sortMiddleware,
      exclude: exclude,
      strategy: strategyConfig,
    };
  }

  private addObject(obj: RepositoryData): RepositoryData[] {
    this.data.push(obj);
    return this.data;
  }

  private addArray(arr: RepositoryData[]): RepositoryData[] {
    const added: RepositoryData[] = [];
    this.clear();
    for (const item of arr) {
      if (isObject(item)) {
        added.push(this.addObject(item)[0]);
      }
    }
    return added;
  }

  private findMatches(data: RepositoryData[], criteria: string): RepositoryData[] {
    const matches: RepositoryData[] = [];
    for (let i = 0; i &lt; data.length &amp;&amp; matches.length &lt; this.options.limit; i++) {
      const match = this.findMatchesInObject(data[i], criteria);
      if (match) {
        matches.push(match);
      }
    }
    return matches;
  }

  private findMatchesInObject(obj: RepositoryData, criteria: string): RepositoryData | undefined {
    let hasMatch = false;
    const result = { ...obj };
    result._matchInfo = {};

    for (const key in obj) {
      if (!this.isExcluded(obj[key]) &amp;&amp; this.options.searchStrategy.matches(obj[key], criteria)) {
        hasMatch = true;
        
        if (this.options.searchStrategy.findMatches) {
          const matchInfo = this.options.searchStrategy.findMatches(obj[key], criteria);
          if (matchInfo &amp;&amp; matchInfo.length &gt; 0) {
            result._matchInfo[key] = matchInfo;
          }
        }
      }
    }

    return hasMatch ? result : undefined;
  }

  private isExcluded(term: any): boolean {
    const termStr = String(term);
    return this.excludePatterns.some(regex =&gt; regex.test(termStr));
  }

  private searchStrategy(strategy: StrategyConfig): Matcher {
    if (!strategy?.type || !StrategyFactory.isValidStrategy(strategy.type)) {
      return LiteralSearchStrategy;
    }

    return StrategyFactory.create(strategy);
  }

  private normalizeStrategyOption(strategy?: StrategyType | StrategyConfig): StrategyConfig {
    if (!strategy) {
      return this.getDefaultStrategyConfig();
    }

    return typeof strategy === &apos;string&apos; ? { type: strategy } : strategy;
  }

  private getDefaultStrategyConfig(): StrategyConfig {
    const defaultStrategy = DEFAULT_OPTIONS.strategy;
    if (typeof defaultStrategy === &apos;string&apos;) {
      return { type: defaultStrategy };
    }
    return defaultStrategy;
  }
}</file><file path="src/SimpleJekyllSearch.ts">import { load as loadJSON } from &apos;./JSONLoader&apos;;
import { OptionsValidator } from &apos;./OptionsValidator&apos;;
import { Repository } from &apos;./Repository&apos;;
import { compile as compileTemplate, setOptions as setTemplaterOptions } from &apos;./Templater&apos;;
import { isJSON, merge } from &apos;./utils&apos;;
import { DEFAULT_OPTIONS, REQUIRED_OPTIONS, WHITELISTED_KEYS } from &apos;./utils/default&apos;;
import { SearchData, SearchOptions, SearchResult, SimpleJekyllSearchInstance } from &apos;./utils/types&apos;;

class SimpleJekyllSearch {
  private options: SearchOptions;
  private repository: Repository;
  private optionsValidator: OptionsValidator;
  private debounceTimerHandle: NodeJS.Timeout | null = null;
  private eventHandler: ((e: Event) =&gt; void) | null = null;
  private pageShowHandler: (() =&gt; void) | null = null;
  private pendingRequest: XMLHttpRequest | null = null;
  private isInitialized: boolean = false;
  private readonly STORAGE_KEY = &apos;sjs-search-state&apos;;

  constructor() {
    this.options = { ...DEFAULT_OPTIONS };
    this.repository = new Repository();
    this.optionsValidator = new OptionsValidator({
      required: REQUIRED_OPTIONS,
    });
  }

  private debounce(func: () =&gt; void, delayMillis: number | null): void {
    if (delayMillis) {
      if (this.debounceTimerHandle) {
        clearTimeout(this.debounceTimerHandle);
      }
      this.debounceTimerHandle = setTimeout(func, delayMillis);
    } else {
      func();
    }
  }

  private throwError(message: string): never {
    throw new Error(`SimpleJekyllSearch --- ${message}`);
  }

  private emptyResultsContainer(): void {
    this.options.resultsContainer.innerHTML = &apos;&apos;;
  }

  private initWithJSON(json: SearchData[]): void {
    this.repository.put(json);
    this.registerInput();
  }

  private initWithURL(url: string): void {
    loadJSON(url, (err, json) =&gt; {
      if (err) {
        this.throwError(`Failed to load JSON from ${url}: ${err.message}`);
      }
      this.initWithJSON(json);
    });
  }

  private registerInput(): void {
    this.eventHandler = (e: Event) =&gt; {
      try {
        const inputEvent = e as KeyboardEvent;
        if (!WHITELISTED_KEYS.has(inputEvent.key)) {
          this.emptyResultsContainer();
          this.debounce(() =&gt; {
            try {
              this.search((e.target as HTMLInputElement).value);
            } catch (searchError) {
              console.error(&apos;Search error:&apos;, searchError);
              this.options.onError?.(searchError as Error);
            }
          }, this.options.debounceTime ?? null);
        }
      } catch (error) {
        console.error(&apos;Input handler error:&apos;, error);
        this.options.onError?.(error as Error);
      }
    };
    
    this.options.searchInput.addEventListener(&apos;input&apos;, this.eventHandler);

    this.pageShowHandler = () =&gt; {
      this.restoreSearchState();
    };
    window.addEventListener(&apos;pageshow&apos;, this.pageShowHandler);

    this.restoreSearchState();
  }

  private saveSearchState(query: string): void {
    if (!query?.trim()) {
      this.clearSearchState();
      return;
    }
    try {
      const state = {
        query: query.trim(),
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(state));
    } catch {
    }
  }

  private getStoredSearchState(): string | null {
    try {
      const raw = sessionStorage.getItem(this.STORAGE_KEY);
      if (!raw) return null;

      const state = JSON.parse(raw);

      if (typeof state?.query !== &apos;string&apos;) return null;

      const MAX_AGE_MS = 30 * 60 * 1000;
      if (Date.now() - state.timestamp &gt; MAX_AGE_MS) {
        this.clearSearchState();
        return null;
      }

      if (state.path &amp;&amp; state.path !== window.location.pathname) {
        this.clearSearchState();
        return null;
      }

      return state.query;
    } catch {
      this.clearSearchState();
      return null;
    }
  }

  private clearSearchState(): void {
    try {
      sessionStorage.removeItem(this.STORAGE_KEY);
    } catch {
    }
  }

  private restoreSearchState(): void {
    const hasExistingResults = this.options.resultsContainer.children.length &gt; 0;
    if (hasExistingResults) return;

    let query = this.options.searchInput.value?.trim();

    if (!query) {
      query = this.getStoredSearchState() || &apos;&apos;;
    }

    if (query.length &gt; 0) {
      this.options.searchInput.value = query;
      this.search(query);
    }
  }

  public search(query: string): void {
    if (query?.trim().length &gt; 0) {
      this.saveSearchState(query);
      this.emptyResultsContainer();
      const results = this.repository.search(query) as SearchResult[];
      this.render(results, query);
      this.options.onSearch?.();
    } else {
      this.clearSearchState();
    }
  }

  private render(results: SearchResult[], query: string): void {
    if (results.length === 0) {
      this.options.resultsContainer.insertAdjacentHTML(&apos;beforeend&apos;, this.options.noResultsText!);
      return;
    }

    const fragment = document.createDocumentFragment();
    results.forEach(result =&gt; {
      result.query = query;
      const div = document.createElement(&apos;div&apos;);
      div.innerHTML = compileTemplate(result, query);
      fragment.appendChild(div);
    });

    this.options.resultsContainer.appendChild(fragment);
  }

  public destroy(): void {
    if (this.eventHandler) {
      this.options.searchInput.removeEventListener(&apos;input&apos;, this.eventHandler);
      this.eventHandler = null;
    }

    if (this.pageShowHandler) {
      window.removeEventListener(&apos;pageshow&apos;, this.pageShowHandler);
      this.pageShowHandler = null;
    }

    if (this.debounceTimerHandle) {
      clearTimeout(this.debounceTimerHandle);
      this.debounceTimerHandle = null;
    }

    this.clearSearchState();
  }

  public init(_options: SearchOptions): SimpleJekyllSearchInstance {
    const errors = this.optionsValidator.validate(_options);
    if (errors.length &gt; 0) {
      this.throwError(`Missing required options: ${REQUIRED_OPTIONS.join(&apos;, &apos;)}`);
    }

    this.options = merge&lt;SearchOptions&gt;(this.options, _options);

    setTemplaterOptions({
      template: this.options.searchResultTemplate,
      middleware: this.options.templateMiddleware,
    });

    this.repository.setOptions({
      limit: this.options.limit,
      sortMiddleware: this.options.sortMiddleware,
      strategy: this.options.strategy,
      exclude: this.options.exclude,
    });

    if (isJSON(this.options.json)) {
      this.initWithJSON(this.options.json as SearchData[]);
    } else {
      this.initWithURL(this.options.json as string);
    }

    const rv = {
      search: this.search.bind(this),
      destroy: this.destroy.bind(this),
    };

    this.options.success?.call(rv);
    return rv;
  }
}

export default SimpleJekyllSearch;</file><file path="src/Templater.ts">import { MatchInfo } from &apos;./SearchStrategies/types&apos;;

type MiddlewareFunction = (
  prop: string, 
  value: any, 
  template: string, 
  query?: string, 
  matchInfo?: MatchInfo[]
) =&gt; any;

interface TemplaterOptions {
  pattern?: RegExp;
  template?: string;
  middleware?: MiddlewareFunction;
}

interface Data {
  [key: string]: any;
  _matchInfo?: Record&lt;string, MatchInfo[]&gt;;
}

const options: TemplaterOptions &amp; { pattern: RegExp; template: string; middleware: MiddlewareFunction } = {
  pattern: /\{(.*?)\}/g,
  template: &apos;&apos;,
  middleware: function() { return undefined; }
};

export function setOptions(_options: TemplaterOptions): void {
  if (_options.pattern) {
    options.pattern = _options.pattern;
  }
  if (_options.template) {
    options.template = _options.template;
  }
  if (typeof _options.middleware === &apos;function&apos;) {
    options.middleware = _options.middleware;
  }
}

export function compile(data: Data, query?: string): string {
  return options.template.replace(options.pattern, function(match: string, prop: string) {
    const matchInfo = data._matchInfo?.[prop];
    
    if (matchInfo &amp;&amp; matchInfo.length &gt; 0 &amp;&amp; query) {
      const value = options.middleware(prop, data[prop], options.template, query, matchInfo);
      if (typeof value !== &apos;undefined&apos;) {
        return value;
      }
    }
    
    if (query) {
      const value = options.middleware(prop, data[prop], options.template, query);
      if (typeof value !== &apos;undefined&apos;) {
        return value;
      }
    }
    
    const value = options.middleware(prop, data[prop], options.template);
    if (typeof value !== &apos;undefined&apos;) {
      return value;
    }
    
    return data[prop] || match;
  });
}</file><file path="src/utils.ts">import { RepositoryData } from &apos;./utils/types&apos;;

export function merge&lt;T&gt;(target: T, source: Partial&lt;T&gt;): T {
  return { ...target, ...source } as T;
}

export function isJSON(json: any): boolean {
  return Array.isArray(json) || (json !== null &amp;&amp; typeof json === &apos;object&apos;);
}

export function NoSort(): number {
  return 0;
}

export function isObject(obj: any): obj is RepositoryData {
  return Boolean(obj) &amp;&amp; Object.prototype.toString.call(obj) === &apos;[object Object]&apos;;
}

export function clone&lt;T&gt;(input: T): T {
  if (input === null || typeof input !== &apos;object&apos;) {
    return input;
  }

  if (Array.isArray(input)) {
    return input.map(item =&gt; clone(item)) as unknown as T;
  }

  const output: Record&lt;string, any&gt; = {};
  for (const key in input) {
    if (Object.prototype.hasOwnProperty.call(input, key)) {
      output[key] = clone((input as Record&lt;string, any&gt;)[key]);
    }
  }

  return output as T;
}</file><file path="tests/middleware/highlighting.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { 
  escapeHtml, 
  mergeOverlappingMatches, 
  highlightWithMatchInfo 
} from &apos;../../src/middleware/highlighting&apos;;
import { MatchInfo } from &apos;../../src/SearchStrategies/types&apos;;

describe(&apos;escapeHtml&apos;, () =&gt; {
  it(&apos;should escape HTML special characters&apos;, () =&gt; {
    expect(escapeHtml(&apos;&lt;div&gt;&apos;)).toBe(&apos;&amp;lt;div&amp;gt;&apos;);
    expect(escapeHtml(&apos;&amp;&apos;)).toBe(&apos;&amp;amp;&apos;);
    expect(escapeHtml(&apos;&quot;hello&quot;&apos;)).toBe(&apos;&amp;quot;hello&amp;quot;&apos;);
    expect(escapeHtml(&quot;&apos;hello&apos;&quot;)).toBe(&apos;&amp;#039;hello&amp;#039;&apos;);
  });

  it(&apos;should handle mixed content&apos;, () =&gt; {
    expect(escapeHtml(&apos;&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;&apos;))
      .toBe(&apos;&amp;lt;script&amp;gt;alert(&amp;quot;XSS&amp;quot;)&amp;lt;/script&amp;gt;&apos;);
  });

  it(&apos;should handle empty string&apos;, () =&gt; {
    expect(escapeHtml(&apos;&apos;)).toBe(&apos;&apos;);
  });

  it(&apos;should not escape safe text&apos;, () =&gt; {
    expect(escapeHtml(&apos;hello world&apos;)).toBe(&apos;hello world&apos;);
  });
});

describe(&apos;mergeOverlappingMatches&apos;, () =&gt; {
  it(&apos;should return empty array for empty input&apos;, () =&gt; {
    expect(mergeOverlappingMatches([])).toEqual([]);
  });

  it(&apos;should return single match unchanged&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    expect(mergeOverlappingMatches(matches)).toEqual(matches);
  });

  it(&apos;should merge overlapping matches&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 3, end: 8, text: &apos;lo wo&apos;, type: &apos;exact&apos; }
    ];
    const result = mergeOverlappingMatches(matches);
    expect(result).toHaveLength(1);
    expect(result[0].start).toBe(0);
    expect(result[0].end).toBe(8);
  });

  it(&apos;should merge adjacent matches&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 5, end: 11, text: &apos; world&apos;, type: &apos;exact&apos; }
    ];
    const result = mergeOverlappingMatches(matches);
    expect(result).toHaveLength(1);
    expect(result[0].start).toBe(0);
    expect(result[0].end).toBe(11);
  });

  it(&apos;should keep separate non-overlapping matches&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 10, end: 15, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];
    const result = mergeOverlappingMatches(matches);
    expect(result).toHaveLength(2);
    expect(result[0].start).toBe(0);
    expect(result[0].end).toBe(5);
    expect(result[1].start).toBe(10);
    expect(result[1].end).toBe(15);
  });

  it(&apos;should handle unsorted matches&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 10, end: 15, text: &apos;world&apos;, type: &apos;exact&apos; },
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = mergeOverlappingMatches(matches);
    expect(result).toHaveLength(2);
    expect(result[0].start).toBe(0);
    expect(result[1].start).toBe(10);
  });

  it(&apos;should merge multiple overlapping matches&apos;, () =&gt; {
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 3, end: 8, text: &apos;lo wo&apos;, type: &apos;exact&apos; },
      { start: 6, end: 11, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];
    const result = mergeOverlappingMatches(matches);
    expect(result).toHaveLength(1);
    expect(result[0].start).toBe(0);
    expect(result[0].end).toBe(11);
  });
});

describe(&apos;highlightWithMatchInfo&apos;, () =&gt; {
  it(&apos;should return escaped text with no matches&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [];
    expect(highlightWithMatchInfo(text, matches)).toBe(&apos;hello world&apos;);
  });

  it(&apos;should highlight single match&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt; world&apos;);
  });

  it(&apos;should highlight multiple matches&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 6, end: 11, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt; &lt;span class=&quot;search-highlight&quot;&gt;world&lt;/span&gt;&apos;);
  });

  it(&apos;should use custom className&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches, { className: &apos;custom-highlight&apos; });
    expect(result).toBe(&apos;&lt;span class=&quot;custom-highlight&quot;&gt;hello&lt;/span&gt; world&apos;);
  });

  it(&apos;should escape HTML in text&apos;, () =&gt; {
    const text = &apos;&lt;div&gt;hello&lt;/div&gt;&apos;;
    const matches: MatchInfo[] = [
      { start: 5, end: 10, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&amp;lt;div&amp;gt;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&amp;lt;/div&amp;gt;&apos;);
  });

  it(&apos;should handle empty text&apos;, () =&gt; {
    const text = &apos;&apos;;
    const matches: MatchInfo[] = [];
    expect(highlightWithMatchInfo(text, matches)).toBe(&apos;&apos;);
  });

  it(&apos;should merge overlapping matches before highlighting&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 3, end: 8, text: &apos;lo wo&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello wo&lt;/span&gt;rld&apos;);
  });

  it(&apos;should truncate long text with maxLength option&apos;, () =&gt; {
    const text = &apos;This is a very long text that should be truncated when it exceeds the maximum length&apos;;
    const matches: MatchInfo[] = [
      { start: 10, end: 14, text: &apos;very&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches, { maxLength: 50, contextLength: 10 });
    expect(result.length).toBeLessThan(text.length);
    expect(result).toContain(&apos;very&apos;);
    expect(result).toContain(&apos;...&apos;);
  });

  it(&apos;should handle match at the beginning of text&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt; world&apos;);
  });

  it(&apos;should handle match at the end of text&apos;, () =&gt; {
    const text = &apos;hello world&apos;;
    const matches: MatchInfo[] = [
      { start: 6, end: 11, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;hello &lt;span class=&quot;search-highlight&quot;&gt;world&lt;/span&gt;&apos;);
  });

  it(&apos;should handle entire text as match&apos;, () =&gt; {
    const text = &apos;hello&apos;;
    const matches: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];
    const result = highlightWithMatchInfo(text, matches);
    expect(result).toBe(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
  });
});</file><file path="tests/middleware/highlightMiddleware.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { 
  createHighlightTemplateMiddleware, 
  defaultHighlightMiddleware 
} from &apos;../../src/middleware/highlightMiddleware&apos;;
import { MatchInfo } from &apos;../../src/SearchStrategies/types&apos;;

describe(&apos;createHighlightTemplateMiddleware&apos;, () =&gt; {
  it(&apos;should create a middleware function&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    expect(typeof middleware).toBe(&apos;function&apos;);
  });

  it(&apos;should highlight content field when matchInfo is provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
    expect(result).toContain(&apos;world&apos;);
  });

  it(&apos;should highlight desc field when matchInfo is provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 6, end: 11, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;desc&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{desc}&lt;/div&gt;&apos;, &apos;world&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;world&lt;/span&gt;&apos;);
  });

  it(&apos;should highlight description field when matchInfo is provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;description&apos;, &apos;test data&apos;, &apos;&lt;div&gt;{description}&lt;/div&gt;&apos;, &apos;test&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;test&lt;/span&gt;&apos;);
  });

  it(&apos;should highlight ANY field that has matchInfo (e.g., tags)&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 10, text: &apos;javascript&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;tags&apos;, &apos;javascript, react&apos;, &apos;&lt;div&gt;{tags}&lt;/div&gt;&apos;, &apos;javascript&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;javascript&lt;/span&gt;&apos;);
  });

  it(&apos;should highlight title field when matchInfo is provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;title&apos;, &apos;hello world post&apos;, &apos;&lt;div&gt;{title}&lt;/div&gt;&apos;, &apos;hello&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
  });

  it(&apos;should return undefined when query is not provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, undefined, matchInfo);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should return undefined when matchInfo is empty&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, []);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should return undefined when matchInfo is not provided&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, undefined);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should truncate long content even without matchInfo when maxLength is set&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware({
      maxLength: 50
    });
    const longText = &apos;This is a very long article that should be truncated. &apos;.repeat(10);

    const result = middleware(&apos;content&apos;, longText, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;other&apos;, undefined);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;...&apos;);
    expect(result!.length).toEqual(50);
  });

  it(&apos;should truncate content when match is on another field (title) but content is displayed&apos;, () =&gt; {    
    const middleware = createHighlightTemplateMiddleware({
      maxLength: 100
    });
    const longContent = &apos;This is a long article body that does not contain the search term. &apos;.repeat(20);

    const result = middleware(&apos;content&apos;, longContent, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, undefined);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;...&apos;);
    expect(result!.length).toEqual(100);
  });

  it(&apos;should return undefined when value is not a string&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 1, text: &apos;1&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, 123 as any, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;1&apos;, matchInfo);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should use custom className option&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware({
      className: &apos;custom-highlight&apos;
    });
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, matchInfo);
    
    expect(result).toContain(&apos;&lt;span class=&quot;custom-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
  });

  it(&apos;should respect maxLength option&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware({
      maxLength: 50
    });
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
    ];
    const longText = &apos;test this is a very long text that should be truncated because it exceeds the maximum allowed length&apos;;

    const result = middleware(&apos;content&apos;, longText, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;test&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;...&apos;);
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;test&lt;/span&gt;&apos;);
  });

  it(&apos;should handle multiple matches&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; },
      { start: 6, end: 11, text: &apos;world&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello world&apos;, matchInfo);
    
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;world&lt;/span&gt;&apos;);
  });

  it(&apos;should escape HTML in highlighted text&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 6, text: &apos;&lt;div&gt;test&lt;/div&gt;&apos;, type: &apos;exact&apos; }
    ];

    const result = middleware(&apos;content&apos;, &apos;&lt;div&gt;test&lt;/div&gt;&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;test&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).not.toContain(&apos;&lt;div&gt;test&lt;/div&gt;&apos;);
    expect(result).toContain(&apos;&amp;lt;&apos;);
    expect(result).toContain(&apos;&amp;gt;&apos;);
  });

  it(&apos;should return undefined when short content has no matches&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware();
    const matchInfo: MatchInfo[] = [];

    const result = middleware(&apos;content&apos;, &apos;no matches&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;test&apos;, matchInfo);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should NOT truncate non-truncateFields even when they are long&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware({
      maxLength: 20
    });
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 10, text: &apos;javascript&apos;, type: &apos;exact&apos; }
    ];
    const longTags = &apos;javascript, typescript, react, vue, angular, svelte, nextjs&apos;;

    const result = middleware(&apos;tags&apos;, longTags, &apos;&lt;div&gt;{tags}&lt;/div&gt;&apos;, &apos;javascript&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;javascript&lt;/span&gt;&apos;);
    expect(result).not.toContain(&apos;...&apos;);
    expect(result).toContain(&apos;svelte&apos;);
  });

  it(&apos;should allow custom truncateFields option&apos;, () =&gt; {
    const middleware = createHighlightTemplateMiddleware({
      maxLength: 30,
      truncateFields: [&apos;tags&apos;, &apos;content&apos;]
    });
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 10, text: &apos;javascript&apos;, type: &apos;exact&apos; }
    ];
    const longTags = &apos;javascript, typescript, react, vue, angular, svelte, nextjs&apos;;

    const result = middleware(&apos;tags&apos;, longTags, &apos;&lt;div&gt;{tags}&lt;/div&gt;&apos;, &apos;javascript&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;javascript&lt;/span&gt;&apos;);
    expect(result).toContain(&apos;...&apos;);
  });

  describe(&apos;noHighlightFields - preventing broken URLs&apos;, () =&gt; {
    it(&apos;should NOT highlight url field even when matchInfo is provided&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware();
      const matchInfo: MatchInfo[] = [
        { start: 14, end: 18, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const result = middleware(&apos;url&apos;, &apos;/2014/11/02/test.html&apos;, &apos;&lt;a href=&quot;{url}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      
      expect(result).toBeUndefined();
    });

    it(&apos;should NOT highlight link field even when matchInfo is provided&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware();
      const matchInfo: MatchInfo[] = [
        { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const result = middleware(&apos;link&apos;, &apos;test-page.html&apos;, &apos;&lt;a href=&quot;{link}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      
      expect(result).toBeUndefined();
    });

    it(&apos;should NOT highlight href field even when matchInfo is provided&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware();
      const matchInfo: MatchInfo[] = [
        { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const result = middleware(&apos;href&apos;, &apos;test.html&apos;, &apos;&lt;a href=&quot;{href}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      
      expect(result).toBeUndefined();
    });

    it(&apos;should NOT highlight query field even when matchInfo is provided&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware();
      const matchInfo: MatchInfo[] = [
        { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const result = middleware(&apos;query&apos;, &apos;test&apos;, &apos;&lt;a href=&quot;{url}?query={query}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      
      expect(result).toBeUndefined();
    });

    it(&apos;should still highlight title when url also matches&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware();
      const titleMatchInfo: MatchInfo[] = [
        { start: 15, end: 19, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const result = middleware(&apos;title&apos;, &apos;This is just a test&apos;, &apos;&lt;a href=&quot;{url}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, titleMatchInfo);
      
      expect(result).toBeDefined();
      expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;test&lt;/span&gt;&apos;);
    });

    it(&apos;should allow custom noHighlightFields option&apos;, () =&gt; {
      const middleware = createHighlightTemplateMiddleware({
        noHighlightFields: [&apos;customUrl&apos;, &apos;customLink&apos;]
      });
      const matchInfo: MatchInfo[] = [
        { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
      ];

      const urlResult = middleware(&apos;url&apos;, &apos;test.html&apos;, &apos;&lt;a href=&quot;{url}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      expect(urlResult).toBeDefined();
      expect(urlResult).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;test&lt;/span&gt;&apos;);

      const customResult = middleware(&apos;customUrl&apos;, &apos;test.html&apos;, &apos;&lt;a href=&quot;{customUrl}&quot;&gt;{title}&lt;/a&gt;&apos;, &apos;test&apos;, matchInfo);
      expect(customResult).toBeUndefined();
    });
  });
});

describe(&apos;defaultHighlightMiddleware&apos;, () =&gt; {
  it(&apos;should work as a pre-configured middleware&apos;, () =&gt; {
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = defaultHighlightMiddleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;hello&lt;/span&gt;&apos;);
  });

  it(&apos;should use default search-highlight class&apos;, () =&gt; {
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 4, text: &apos;test&apos;, type: &apos;exact&apos; }
    ];

    const result = defaultHighlightMiddleware(&apos;desc&apos;, &apos;test data&apos;, &apos;&lt;div&gt;{desc}&lt;/div&gt;&apos;, &apos;test&apos;, matchInfo);
    
    expect(result).toContain(&apos;class=&quot;search-highlight&quot;&apos;);
  });

  it(&apos;should highlight any field with matchInfo including title&apos;, () =&gt; {
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;title&apos;, type: &apos;exact&apos; }
    ];

    const result = defaultHighlightMiddleware(&apos;title&apos;, &apos;title text&apos;, &apos;&lt;div&gt;{title}&lt;/div&gt;&apos;, &apos;title&apos;, matchInfo);
    
    expect(result).toBeDefined();
    expect(result).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;title&lt;/span&gt;&apos;);
  });

  it(&apos;should return undefined without query&apos;, () =&gt; {
    const matchInfo: MatchInfo[] = [
      { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
    ];

    const result = defaultHighlightMiddleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, undefined, matchInfo);
    
    expect(result).toBeUndefined();
  });

  it(&apos;should return undefined without matchInfo for short content&apos;, () =&gt; {
    const result = defaultHighlightMiddleware(&apos;content&apos;, &apos;hello world&apos;, &apos;&lt;div&gt;{content}&lt;/div&gt;&apos;, &apos;hello&apos;, undefined);
    
    expect(result).toBeUndefined();
  });
});</file><file path="tests/SearchStrategies/findFuzzyMatches.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { findFuzzyMatches } from &apos;../../src/SearchStrategies/search/findFuzzyMatches&apos;;

describe(&apos;findFuzzyMatches&apos;, () =&gt; {
  it(&apos;matches exact strings&apos;, () =&gt; {
    const matches1 = findFuzzyMatches(&apos;hello&apos;, &apos;hello&apos;);
    expect(matches1).toHaveLength(1);
    expect(matches1[0].type).toBe(&apos;fuzzy&apos;);
    
    const matches2 = findFuzzyMatches(&apos;test&apos;, &apos;test&apos;);
    expect(matches2).toHaveLength(1);
    expect(matches2[0].type).toBe(&apos;fuzzy&apos;);
  });

  it(&apos;matches substrings&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;hello&apos;, &apos;hlo&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;test&apos;, &apos;tst&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;fuzzy&apos;, &apos;fzy&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;react&apos;, &apos;rct&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;what the heck&apos;, &apos;wth&apos;)).toHaveLength(1);
  });

  it(&apos;matches characters in sequence&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hw&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;a1b2c3&apos;, &apos;abc&apos;)).toHaveLength(1);
  });

  it(&apos;does not match out-of-sequence characters&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;abc&apos;, &apos;cba&apos;)).toEqual([]);
    expect(findFuzzyMatches(&apos;abcd&apos;, &apos;dc&apos;)).toEqual([]);
  });

  it(&apos;does not match words that don\&apos;t contain the search criteria&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;fuzzy&apos;, &apos;fzyyy&apos;)).toEqual([]);
    expect(findFuzzyMatches(&apos;react&apos;, &apos;angular&apos;)).toEqual([]);
    expect(findFuzzyMatches(&apos;what the heck&apos;, &apos;wth?&apos;)).toEqual([]);
  });

  it(&apos;is case insensitive&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;HELLO&apos;, &apos;hello&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;world&apos;, &apos;WORLD&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hEllO&apos;, &apos;HeLLo&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;Different Cases&apos;, &apos;dc&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;UPPERCASE&apos;, &apos;upprcs&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;lowercase&apos;, &apos;lc&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;DiFfErENt cASeS&apos;, &apos;dc&apos;)).toHaveLength(1);
  });

  it(&apos;handles special characters&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;hello!@#$&apos;, &apos;h!@#$&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;abc123xyz&apos;, &apos;123&apos;)).toHaveLength(1);
  });

  it(&apos;handles spaces correctly&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hw&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;h w&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hw &apos;)).toHaveLength(1);
  });

  it(&apos;matches characters in sequence&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hlo wld&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hw&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;hlowrd&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;wrld&apos;)).toHaveLength(1);
    expect(findFuzzyMatches(&apos;hello world&apos;, &apos;wh&apos;)).toEqual([]);
  });

  it(&apos;does not match when character frequency in the pattern exceeds the text&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;goggles&apos;, &apos;gggggggg&apos;)).toEqual([]);
    expect(findFuzzyMatches(&apos;aab&apos;, &apos;aaaa&apos;)).toEqual([]);
  });

  it(&apos;match ordered multiple words&apos;, () =&gt; {
    expect(findFuzzyMatches(&apos;Ola que tal&apos;, &apos;ola tal&apos;)).toHaveLength(1);
  });

  describe(&apos;original fuzzysearch test cases&apos;, () =&gt; {
    it(&apos;matches cartwheel test cases&apos;, () =&gt; {
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;car&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;cwhl&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;cwheel&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;cartwheel&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;cwheeel&apos;)).toEqual([]);
      expect(findFuzzyMatches(&apos;cartwheel&apos;, &apos;lw&apos;)).toEqual([]);
    });

    it(&apos;matches Chinese Unicode test cases&apos;, () =&gt; {
      expect(findFuzzyMatches(&apos;php语言&apos;, &apos;语言&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;php语言&apos;, &apos;hp语&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;Python开发者&apos;, &apos;Py开发&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;Python开发者&apos;, &apos;Py 开发&apos;)).toEqual([]);
      expect(findFuzzyMatches(&apos;爪哇开发进阶&apos;, &apos;爪哇进阶&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;非常简单的格式化工具&apos;, &apos;格式工具&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;学习正则表达式怎么学习&apos;, &apos;正则&apos;)).toHaveLength(1);
      expect(findFuzzyMatches(&apos;正则表达式怎么学习&apos;, &apos;学习正则&apos;)).toEqual([]);
    });
  });
});</file><file path="tests/SearchStrategies/findLevenshteinMatches.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { findLevenshteinMatches } from &apos;../../src/SearchStrategies/search/findLevenshteinMatches&apos;;

describe(&apos;findLevenshteinMatches&apos;, () =&gt; {
  it(&apos;should return matches for identical strings&apos;, () =&gt; {
    const matches = findLevenshteinMatches(&apos;hello&apos;, &apos;hello&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    expect(matches[0].text).toBe(&apos;hello&apos;);
  });

  it(&apos;should return matches for strings with small differences (substitutions)&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;kitten&apos;, &apos;sitting&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;flaw&apos;, &apos;lawn&apos;)).toHaveLength(1);
  });

  it(&apos;should return matches for strings with insertions&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;cat&apos;, &apos;cats&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;hello&apos;, &apos;helloo&apos;)).toHaveLength(1);
  });

  it(&apos;should return matches for strings with deletions&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;cats&apos;, &apos;cat&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;helloo&apos;, &apos;hello&apos;)).toHaveLength(1);
  });

  it(&apos;should return empty array for completely different strings (low similarity)&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;abc&apos;, &apos;xyz&apos;)).toEqual([]);
    expect(findLevenshteinMatches(&apos;abcd&apos;, &apos;wxyz&apos;)).toEqual([]);
  });

  it(&apos;should handle empty strings&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;&apos;, &apos;hello&apos;)).toEqual([]);
    expect(findLevenshteinMatches(&apos;hello&apos;, &apos;&apos;)).toEqual([]);
    expect(findLevenshteinMatches(&apos;&apos;, &apos;&apos;)).toEqual([]);
  });

  it(&apos;should handle single-character strings&apos;, () =&gt; {
    const matchesIdentical = findLevenshteinMatches(&apos;a&apos;, &apos;a&apos;);
    expect(matchesIdentical).toHaveLength(1);
    expect(matchesIdentical[0].text).toBe(&apos;a&apos;);

    expect(findLevenshteinMatches(&apos;a&apos;, &apos;b&apos;)).toEqual([]);
    expect(findLevenshteinMatches(&apos;a&apos;, &apos;&apos;)).toEqual([]);
  });

  it(&apos;should handle substitutions correctly&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;ab&apos;, &apos;ac&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;ac&apos;, &apos;bc&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;abc&apos;, &apos;axc&apos;)).toHaveLength(1);
  });

  it(&apos;should handle multiple operations&apos;, () =&gt; {
    expect(findLevenshteinMatches(&apos;example&apos;, &apos;samples&apos;)).toHaveLength(1);
    expect(findLevenshteinMatches(&apos;distance&apos;, &apos;eistancd&apos;)).toHaveLength(1);
  });

  it(&apos;should handle non-Latin characters&apos;, () =&gt; {
    const matches = findLevenshteinMatches(&apos;你好世界&apos;, &apos;你好&apos;);
    expect(matches).toHaveLength(1);
  });

  it(&apos;should respect similarity threshold of 30%&apos;, () =&gt; {
    const similarEnough = findLevenshteinMatches(&apos;back&apos;, &apos;book&apos;);
    expect(similarEnough).toHaveLength(1);
    
    const notSimilarEnough = findLevenshteinMatches(&apos;a&apos;, &apos;zzzzz&apos;);
    expect(notSimilarEnough).toEqual([]);
  });

  it(&apos;should return match info with correct structure&apos;, () =&gt; {
    const matches = findLevenshteinMatches(&apos;hello&apos;, &apos;helo&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0]).toMatchObject({
      start: 0,
      end: 5,
      text: &apos;hello&apos;,
      type: &apos;fuzzy&apos;
    });
  });
});</file><file path="tests/SearchStrategies/findLiteralMatches.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { findLiteralMatches } from &apos;../../src/SearchStrategies/search/findLiteralMatches&apos;;

describe(&apos;findLiteralMatches&apos;, () =&gt; {
  it(&apos;does not match a word that is partially contained in the search criteria when followed by a space&apos;, () =&gt; {
    expect(findLiteralMatches(&apos;this tasty tester text&apos;, &apos;test &apos;)).toEqual([]);
  });

  it(&apos;matches exact single word&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;hello world&apos;, &apos;hello&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].start).toBe(0);
    expect(matches[0].end).toBe(5);
    expect(matches[0].text).toBe(&apos;hello&apos;);
    expect(matches[0].type).toBe(&apos;exact&apos;);
  });

  it(&apos;matches multiple occurrences of the same word&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;hello world hello&apos;, &apos;hello&apos;);
    expect(matches).toHaveLength(2);
    expect(matches[0].start).toBe(0);
    expect(matches[0].end).toBe(5);
    expect(matches[1].start).toBe(12);
    expect(matches[1].end).toBe(17);
  });

  it(&apos;matches multi-word queries when all words present&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;hello amazing world&apos;, &apos;hello world&apos;);
    expect(matches.length).toBeGreaterThan(0);
    expect(matches.some(m =&gt; m.text === &apos;hello&apos;)).toBe(true);
    expect(matches.some(m =&gt; m.text === &apos;world&apos;)).toBe(true);
  });

  it(&apos;does not match when not all words are present&apos;, () =&gt; {
    expect(findLiteralMatches(&apos;hello world&apos;, &apos;hello missing&apos;)).toEqual([]);
  });

  it(&apos;is case insensitive&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;HELLO world&apos;, &apos;hello&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].text).toBe(&apos;HELLO&apos;);
  });

  it(&apos;handles empty or null inputs&apos;, () =&gt; {
    expect(findLiteralMatches(&apos;&apos;, &apos;test&apos;)).toEqual([]);
    expect(findLiteralMatches(&apos;test&apos;, &apos;&apos;)).toEqual([]);
  });

  it(&apos;matches substring within longer text&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;javascript is great&apos;, &apos;script&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].start).toBe(4);
    expect(matches[0].end).toBe(10);
  });

  it(&apos;handles special characters&apos;, () =&gt; {
    const matches = findLiteralMatches(&apos;hello@world.com&apos;, &apos;@world&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].text).toBe(&apos;@world&apos;);
  });
});</file><file path="tests/SearchStrategies/findWildcardMatches.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { findWildcardMatches, buildWildcardFragment } from &apos;../../src/SearchStrategies/search/findWildcardMatches&apos;;

describe(&apos;findWildcardMatches&apos;, () =&gt; {
  it(&apos;should return matches for exact matches&apos;, () =&gt; {
    const matches = findWildcardMatches(&apos;hello&apos;, &apos;hello&apos;);
    expect(matches).toHaveLength(1);
    expect(matches[0].type).toBe(&apos;wildcard&apos;);
  });

  it(&apos;should return matches for patterns with wildcards&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;hello&apos;, &apos;he*o&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;hello&apos;, &apos;he*o*&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;test&apos;, &apos;te*t&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;text&apos;, &apos;te*t&apos;)).toHaveLength(1);
  });

  it(&apos;should match within words but stop at spaces&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;hello amazing world&apos;, &apos;hello*world&apos;)).toHaveLength(0);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;hello*world&apos;)).toHaveLength(0);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;hello*&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;hello*&apos;)[0].text).toBe(&apos;hello&apos;);
  });

  it(&apos;should allow spaces when configured&apos;, () =&gt; {
    const matches = findWildcardMatches(&apos;hello world&apos;, &apos;hel*rld&apos;, { maxSpaces: 1 });
    expect(matches).toHaveLength(1);
    expect(matches[0].text).toBe(&apos;hello world&apos;);
  });

  it(&apos;should respect the maximum number of allowed spaces&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;hello brave new world&apos;, &apos;hel*rld&apos;, { maxSpaces: 2 })).toHaveLength(0);
    const matches = findWildcardMatches(&apos;hello brave new world&apos;, &apos;hel*rld&apos;, { maxSpaces: 3 });
    expect(matches).toHaveLength(1);
    expect(matches[0].text).toBe(&apos;hello brave new world&apos;);
  });

  it(&apos;should return empty array for non-matching wildcard patterns&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;world&apos;, &apos;h*o&apos;)).toEqual([]);
    expect(findWildcardMatches(&apos;xyz&apos;, &apos;abc&apos;)).toEqual([]);
  });

  it(&apos;should handle single-character patterns and texts&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;a&apos;, &apos;a&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;b&apos;, &apos;a&apos;)).toEqual([]);
    const starMatches = findWildcardMatches(&apos;a&apos;, &apos;*&apos;);
    expect(starMatches.length).toBeGreaterThanOrEqual(1);
  });

  it(&apos;should return empty array for a word not present in the text&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;missing&apos;)).toEqual([]);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;miss*&apos;)).toEqual([]);
  });

  it(&apos;should return match info with correct positions&apos;, () =&gt; {
    const matches = findWildcardMatches(&apos;hello&apos;, &apos;hello&apos;);
    expect(matches[0].start).toBe(0);
    expect(matches[0].end).toBe(5);
    expect(matches[0].text).toBe(&apos;hello&apos;);
  });

  it(&apos;should handle wildcards at beginning and end&apos;, () =&gt; {
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;*world&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;*world&apos;)[0].text).toBe(&apos;world&apos;);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;hello*&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;hello*&apos;)[0].text).toBe(&apos;hello&apos;);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;*llo wor*&apos;)).toHaveLength(1);
    expect(findWildcardMatches(&apos;hello world&apos;, &apos;*llo wor*&apos;)[0].text).toBe(&apos;hello world&apos;);
  });

  it(&apos;should stop at spaces and not match entire article&apos;, () =&gt; {
    const article = &apos;this is a test article with many words&apos;;
    const matches = findWildcardMatches(article, &apos;t*&apos;);
    expect(matches.length).toBeGreaterThanOrEqual(2);
    expect(matches[0].text).toBe(&apos;this&apos;);
    expect(matches[1].text).toBe(&apos;test&apos;);
    matches.forEach(match =&gt; {
      expect(match.text).not.toContain(&apos; &apos;);
    });
  });

  it(&apos;should allow unlimited spaces when configured with Infinity&apos;, () =&gt; {
    const matches = findWildcardMatches(&apos;hello this is a long world sequence&apos;, &apos;hel*rld&apos;, { maxSpaces: Infinity });
    expect(matches).toHaveLength(1);
    expect(matches[0].text).toBe(&apos;hello this is a long world&apos;);
  });
});

describe(&apos;buildWildcardFragment&apos;, () =&gt; {
  it(&apos;returns single-word pattern by default&apos;, () =&gt; {
    expect(buildWildcardFragment({})).toBe(&apos;[^ ]*&apos;);
  });

  it(&apos;allows configuring finite spaces&apos;, () =&gt; {
    expect(buildWildcardFragment({ maxSpaces: 2 })).toBe(&apos;[^ ]*(?: [^ ]*){0,2}&apos;);
  });

  it(&apos;normalizes values less than or equal to zero back to default&apos;, () =&gt; {
    expect(buildWildcardFragment({ maxSpaces: 0 })).toBe(&apos;[^ ]*&apos;);
    expect(buildWildcardFragment({ maxSpaces: -5 })).toBe(&apos;[^ ]*&apos;);
  });

  it(&apos;supports unlimited spaces with Infinity&apos;, () =&gt; {
    expect(buildWildcardFragment({ maxSpaces: Infinity })).toBe(&apos;[^ ]*(?: [^ ]*)*&apos;);
  });

  it(&apos;floors decimal inputs&apos;, () =&gt; {
    expect(buildWildcardFragment({ maxSpaces: 2.9 })).toBe(&apos;[^ ]*(?: [^ ]*){0,2}&apos;);
  });
});</file><file path="tests/SearchStrategies/HybridSearchStrategy.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { HybridSearchStrategy } from &apos;../../src/SearchStrategies/HybridSearchStrategy&apos;;

describe(&apos;HybridSearchStrategy&apos;, () =&gt; {
  describe(&apos;wildcard detection&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should use wildcard search when * is present&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello world&apos;, &apos;hel*&apos;);
      expect(matches).toHaveLength(1);
      expect(matches[0].type).toBe(&apos;wildcard&apos;);
      expect(matches[0].text).toBe(&apos;hello world&apos;);
    });

    it(&apos;should use wildcard search for multiple * patterns&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello amazing world&apos;, &apos;amaz*&apos;);
      expect(matches).toHaveLength(1);
      expect(matches[0].type).toBe(&apos;wildcard&apos;);
      expect(matches[0].text).toBe(&apos;amazing world&apos;);
    });

    it(&apos;should use wildcard search with maxSpaces: 0 to stop at word boundary&apos;, () =&gt; {
      const noSpaces = new HybridSearchStrategy({ maxSpaces: 0 });
      const matches = noSpaces.findMatches(&apos;hello world&apos;, &apos;hel*&apos;);
      expect(matches).toHaveLength(1);
      expect(matches[0].type).toBe(&apos;wildcard&apos;);
      expect(matches[0].text).toBe(&apos;hello&apos;);
    });

    it(&apos;should fall back to literal if wildcard has no match&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello world&apos;, &apos;xyz*abc&apos;);
      expect(matches).toEqual([]);
    });

    it(&apos;should match across one space by default (maxSpaces: 1)&apos;, () =&gt; {
      expect(strategy.matches(&apos;hello world&apos;, &apos;hel*rld&apos;)).toBe(true);
    });

    it(&apos;should respect wildcard maxSpaces: 0 to disable space spanning&apos;, () =&gt; {
      const noSpaces = new HybridSearchStrategy({ maxSpaces: 0 });
      expect(noSpaces.matches(&apos;hello world&apos;, &apos;hel*rld&apos;)).toBe(false);
    });

    it(&apos;should respect wildcard maxSpaces when provided and above 1&apos;, () =&gt; {
      const twoSpaces = new HybridSearchStrategy({ maxSpaces: 2 });
      expect(twoSpaces.matches(&apos;hello brave world&apos;, &apos;hel*rld&apos;)).toBe(true);
      expect(twoSpaces.matches(&apos;hello brave new world&apos;, &apos;hel*rld&apos;)).toBe(false);

      const threeSpaces = new HybridSearchStrategy({ maxSpaces: 3 });
      expect(threeSpaces.matches(&apos;hello brave new world&apos;, &apos;hel*rld&apos;)).toBe(true);
    });
  });

  describe(&apos;multi-word detection&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should use literal search for multi-word queries&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello amazing world&apos;, &apos;hello world&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;exact&apos;);
    });

    it(&apos;should find all words in multi-word search&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;test this amazing test&apos;, &apos;test amazing&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should not match if any word is missing&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello world&apos;, &apos;hello missing&apos;);
      expect(matches).toEqual([]);
    });
  });

  describe(&apos;fuzzy fallback&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should use fuzzy search for single-word queries &gt;= minFuzzyLength&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;testing&apos;, &apos;tsting&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    });

    it(&apos;should use fuzzy for long single words&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello&apos;, &apos;hllo&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    });
  });

  describe(&apos;fuzzy span constraints&apos;, () =&gt; {
    const longText = &apos;This is an article with more technical content to test the search functionality. A command with some regex and special characters.&apos;;

    it(&apos;rejects fuzzy matches that span too many extra characters by default&apos;, () =&gt; {
      const strategy = new HybridSearchStrategy();
      expect(strategy.findMatches(longText, &apos;high&apos;)).toEqual([]);
    });

    it(&apos;allows wider spans when explicitly configured&apos;, () =&gt; {
      const permissive = new HybridSearchStrategy({ maxExtraFuzzyChars: Infinity });
      const matches = permissive.findMatches(longText, &apos;high&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    });
  });

  describe(&apos;short query handling&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should use literal search for queries &lt; minFuzzyLength&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello&apos;, &apos;he&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;exact&apos;);
    });

    it(&apos;should use literal for 2-character queries&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;ab cd ef&apos;, &apos;ab&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });
  });

  describe(&apos;configuration&apos;, () =&gt; {
    it(&apos;should respect minFuzzyLength config&apos;, () =&gt; {
      const customStrategy = new HybridSearchStrategy({ minFuzzyLength: 5 });
      const matches = customStrategy.findMatches(&apos;test&apos;, &apos;test&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should respect preferFuzzy config&apos;, () =&gt; {
      const fuzzyPreferred = new HybridSearchStrategy({ preferFuzzy: true });
      const matches = fuzzyPreferred.findMatches(&apos;testing&apos;, &apos;tsting&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    });

    it(&apos;should respect wildcardPriority = false&apos;, () =&gt; {
      const noWildcardPriority = new HybridSearchStrategy({ wildcardPriority: false });
      const matches = noWildcardPriority.findMatches(&apos;hello world&apos;, &apos;hello&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should respect maxExtraFuzzyChars config&apos;, () =&gt; {
      const strict = new HybridSearchStrategy({ maxExtraFuzzyChars: 0, minFuzzyLength: 1 });
      expect(strict.findMatches(&apos;hello world&apos;, &apos;hw&apos;)).toEqual([]);

      const lenient = new HybridSearchStrategy({ maxExtraFuzzyChars: 10, minFuzzyLength: 1 });
      const matches = lenient.findMatches(&apos;hello world&apos;, &apos;hw&apos;);
      expect(matches.length).toBeGreaterThan(0);
      expect(matches[0].type).toBe(&apos;fuzzy&apos;);
    });

  });

  describe(&apos;fallback chain&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should fall back to literal when wildcard fails&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;hello world&apos;, &apos;world&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should fall back to literal when fuzzy fails&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;abc&apos;, &apos;xyz&apos;);
      expect(matches).toEqual([]);
    });

    it(&apos;should try all strategies in order&apos;, () =&gt; {
      const strategy = new HybridSearchStrategy();
      const matches = strategy.findMatches(&apos;hello world&apos;, &apos;hello&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });
  });

  describe(&apos;edge cases&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should handle empty strings&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;&apos;, &apos;test&apos;);
      expect(matches).toEqual([]);
    });

    it(&apos;should handle special characters&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;test@example.com&apos;, &apos;@example&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should handle unicode characters&apos;, () =&gt; {
      const matches = strategy.findMatches(&apos;你好世界&apos;, &apos;你好&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });
  });

  describe(&apos;matches() method&apos;, () =&gt; {
    const strategy = new HybridSearchStrategy();

    it(&apos;should return true for valid matches&apos;, () =&gt; {
      expect(strategy.matches(&apos;hello world&apos;, &apos;hello&apos;)).toBe(true);
      expect(strategy.matches(&apos;test&apos;, &apos;te*t&apos;)).toBe(true);
    });

    it(&apos;should return false for no matches&apos;, () =&gt; {
      expect(strategy.matches(&apos;hello&apos;, &apos;xyz&apos;)).toBe(false);
    });
  });
});</file><file path="tests/SearchStrategies/SearchStrategy.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import {
  FuzzySearchStrategy,
  LiteralSearchStrategy,
  DefaultWildcardSearchStrategy,
} from &apos;../../src/SearchStrategies/SearchStrategy&apos;;

describe.each([
  { name: &apos;LiteralSearchStrategy&apos;, strategy: LiteralSearchStrategy },
  { name: &apos;FuzzySearchStrategy&apos;, strategy: FuzzySearchStrategy },
  { name: &apos;WildcardSearchStrategy&apos;, strategy: DefaultWildcardSearchStrategy },
])(&apos;$name&apos;, ({ strategy }) =&gt; {
  it(&apos;matches a word that is contained in the search criteria (single words)&apos;, () =&gt; {
    expect(strategy.matches(&apos;hello world test search text&apos;, &apos;world&apos;)).toBe(true);
  });

  it(&apos;does not match if a word is not contained in the search criteria&apos;, () =&gt; {
    expect(strategy.matches(&apos;hello world test search text&apos;, &apos;hello my world&apos;)).toBe(false);
  });

  it(&apos;matches a word that is contained in the search criteria (multiple words)&apos;, () =&gt; {
    expect(strategy.matches(&apos;hello world test search text&apos;, &apos;hello text world&apos;)).toBe(true);
  });

  it(&apos;matches exact words when exact words with space in the search criteria&apos;, () =&gt; {
    expect(strategy.matches(&apos;hello world test search text&apos;, &apos;hello world &apos;)).toBe(true);
  });

  it(&apos;matches a word that is partially contained in the search criteria&apos;, () =&gt; {
    expect(strategy.matches(&apos;this tasty tester text&apos;, &apos;test&apos;)).toBe(true);
  });

  it(&apos;should handle empty strings correctly&apos;, () =&gt; {
    expect(strategy.matches(&apos;hello&apos;, &apos;&apos;)).toBe(false);
    expect(strategy.matches(&apos;&apos;, &apos;hello&apos;)).toBe(false);
    expect(strategy.matches(&apos;&apos;, &apos;&apos;)).toBe(false);
  });

  it(&apos;returns false when text is null&apos;, () =&gt; {
    expect(strategy.matches(null, &apos;criteria&apos;)).toBe(false);
  });
});</file><file path="tests/SearchStrategies/StrategyFactory.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { StrategyFactory } from &apos;../../src/SearchStrategies/StrategyFactory&apos;;
import { LiteralSearchStrategy, FuzzySearchStrategy, WildcardSearchStrategy, DefaultWildcardSearchStrategy } from &apos;../../src/SearchStrategies/SearchStrategy&apos;;
import { HybridSearchStrategy } from &apos;../../src/SearchStrategies/HybridSearchStrategy&apos;;

describe(&apos;StrategyFactory&apos;, () =&gt; {
  describe(&apos;create&apos;, () =&gt; {
    it(&apos;should create literal strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;literal&apos; });
      expect(strategy).toBe(LiteralSearchStrategy);
    });

    it(&apos;should create fuzzy strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;fuzzy&apos; });
      expect(strategy).toBe(FuzzySearchStrategy);
    });

    it(&apos;should create wildcard strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;wildcard&apos; });
      expect(strategy).toBeInstanceOf(WildcardSearchStrategy);
      expect(strategy).not.toBe(DefaultWildcardSearchStrategy);
      expect(strategy.matches(&apos;hello world&apos;, &apos;hel*&apos;)).toBe(true);
    });

    it(&apos;should create configurable wildcard strategy when options are provided&apos;, () =&gt; {
      const strategy = StrategyFactory.create({
        type: &apos;wildcard&apos;,
        options: { maxSpaces: 1 }
      });
      expect(strategy).not.toBe(DefaultWildcardSearchStrategy);
      expect(strategy.matches(&apos;hello world&apos;, &apos;hel*rld&apos;)).toBe(true);
      expect(DefaultWildcardSearchStrategy.matches(&apos;hello world&apos;, &apos;hel*rld&apos;)).toBe(false);
    });

    it(&apos;should create hybrid strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;hybrid&apos; });
      expect(strategy).toBeInstanceOf(HybridSearchStrategy);
    });

    it(&apos;should pass hybrid config&apos;, () =&gt; {
      const strategy = StrategyFactory.create({
        type: &apos;hybrid&apos;,
        options: { minFuzzyLength: 10 }
      });
      expect(strategy).toBeInstanceOf(HybridSearchStrategy);
      expect(strategy.findMatches(&apos;javascript&apos;, &apos;jvscrpt&apos;)).toEqual([]);
    });

    it(&apos;should forward wildcard options to hybrid strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({
        type: &apos;hybrid&apos;,
        options: { maxSpaces: 1 }
      }) as HybridSearchStrategy;

      expect(strategy.matches(&apos;hello world&apos;, &apos;hel*rld&apos;)).toBe(true);
    });
  });

  describe(&apos;error handling&apos;, () =&gt; {
    it(&apos;should default to literal for unknown type&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;unknown&apos; as any });
      expect(strategy).toBe(LiteralSearchStrategy);
    });
  });

  describe(&apos;getAvailableStrategies&apos;, () =&gt; {
    it(&apos;should return all available strategy types&apos;, () =&gt; {
      const strategies = StrategyFactory.getAvailableStrategies();
      expect(strategies).toContain(&apos;literal&apos;);
      expect(strategies).toContain(&apos;fuzzy&apos;);
      expect(strategies).toContain(&apos;wildcard&apos;);
      expect(strategies).toContain(&apos;hybrid&apos;);
      expect(strategies).toHaveLength(4);
    });
  });

  describe(&apos;isValidStrategy&apos;, () =&gt; {
    it(&apos;should return true for valid strategies&apos;, () =&gt; {
      expect(StrategyFactory.isValidStrategy(&apos;literal&apos;)).toBe(true);
      expect(StrategyFactory.isValidStrategy(&apos;fuzzy&apos;)).toBe(true);
      expect(StrategyFactory.isValidStrategy(&apos;wildcard&apos;)).toBe(true);
      expect(StrategyFactory.isValidStrategy(&apos;hybrid&apos;)).toBe(true);
    });

    it(&apos;should return false for invalid strategies&apos;, () =&gt; {
      expect(StrategyFactory.isValidStrategy(&apos;unknown&apos;)).toBe(false);
      expect(StrategyFactory.isValidStrategy(&apos;custom&apos;)).toBe(false);
      expect(StrategyFactory.isValidStrategy(&apos;&apos;)).toBe(false);
    });
  });

  describe(&apos;strategy functionality&apos;, () =&gt; {
    it(&apos;should create working literal strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;literal&apos; });
      expect(strategy.matches(&apos;hello world&apos;, &apos;hello&apos;)).toBe(true);
    });

    it(&apos;should create working fuzzy strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;fuzzy&apos; });
      const matches = strategy.findMatches(&apos;hello&apos;, &apos;hlo&apos;);
      expect(matches.length).toBeGreaterThan(0);
    });

    it(&apos;should create working wildcard strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;wildcard&apos; });
      expect(strategy.matches(&apos;hello world&apos;, &apos;hel*&apos;)).toBe(true);
    });

    it(&apos;should create working hybrid strategy&apos;, () =&gt; {
      const strategy = StrategyFactory.create({ type: &apos;hybrid&apos; });
      expect(strategy.matches(&apos;hello world&apos;, &apos;hello&apos;)).toBe(true);
      expect(strategy.matches(&apos;test&apos;, &apos;te*t&apos;)).toBe(true);
    });
  });
});</file><file path="tests/OptionsValidator.test.ts">import { describe, it, expect } from &apos;vitest&apos;;
import { OptionsValidator } from &apos;../src/OptionsValidator&apos;;

describe(&apos;OptionsValidator&apos;, () =&gt; {
  it(&apos;can be instanciated with options&apos;, () =&gt; {
    const requiredOptions = [&apos;foo&apos;, &apos;bar&apos;];
    const optionsValidator = new OptionsValidator({
      required: requiredOptions
    });

    expect(optionsValidator.getRequiredOptions()).toEqual(requiredOptions);
  });

  it(&apos;returns empty errors array for valid options&apos;, () =&gt; {
    const requiredOptions = [&apos;foo&apos;, &apos;bar&apos;];
    const optionsValidator = new OptionsValidator({
      required: requiredOptions
    });

    const errors = optionsValidator.validate({
      foo: &apos;&apos;,
      bar: &apos;&apos;
    });

    expect(errors.length).toBe(0);
  });

  it(&apos;returns array with errors for invalid options&apos;, () =&gt; {
    const requiredOptions = [&apos;foo&apos;, &apos;bar&apos;];
    const optionsValidator = new OptionsValidator({
      required: requiredOptions
    });

    const errors = optionsValidator.validate({
      foo: &apos;&apos;
    });

    expect(errors.length).toBe(1);
  });
});</file><file path="tests/Repository.test.ts">import { afterEach, beforeEach, describe, expect, it, vi } from &apos;vitest&apos;;
import { Repository } from &apos;../src/Repository&apos;;

interface TestElement {
  title: string;
  content: string;
}

const barElement: TestElement = { title: &apos;bar&apos;, content: &apos;bar&apos; };
const almostBarElement: TestElement = { title: &apos;almostbar&apos;, content: &apos;almostbar&apos; };
const loremElement: TestElement = { title: &apos;lorem&apos;, content: &apos;lorem ipsum&apos; };

const data: TestElement[] = [barElement, almostBarElement, loremElement];

describe(&apos;Repository&apos;, () =&gt; {
  let repository: Repository;

  beforeEach(() =&gt; {
    repository = new Repository();
    repository.put(data);
  });

  afterEach(() =&gt; {
    repository.clear();
  });

  it(&apos;finds a simple string&apos;, () =&gt; {
    const results = repository.search(&apos;bar&apos;);
    expect(results).toHaveLength(2);
    expect(results[0]).toMatchObject(barElement);
    expect(results[1]).toMatchObject(almostBarElement);
    expect(results[0]._matchInfo).toBeDefined();
  });

  it(&apos;limits the search results to one even if found more&apos;, () =&gt; {
    repository.setOptions({ limit: 1 });
    const results = repository.search(&apos;bar&apos;);
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject(barElement);
    expect(results[0]._matchInfo).toBeDefined();
  });

  it(&apos;finds a long string&apos;, () =&gt; {
    const results = repository.search(&apos;lorem ipsum&apos;);
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject(loremElement);
    expect(results[0]._matchInfo).toBeDefined();
  });

  it(&apos;[v1.x deprecated] fuzzy option still works via backward compatibility&apos;, () =&gt; {
    // Test backward compatibility: fuzzy: true should work and show warning
    const consoleWarnSpy = vi.spyOn(console, &apos;warn&apos;).mockImplementation(() =&gt; {});
    
    repository.setOptions({ fuzzy: true });
    const results = repository.search(&apos;lrm ism&apos;);
    
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject(loremElement);
    expect(results[0]._matchInfo).toBeDefined();
    expect(consoleWarnSpy).toHaveBeenCalledWith(&apos;[Simple Jekyll Search] Warning: fuzzy option is deprecated. Use strategy: &quot;fuzzy&quot; instead.&apos;);
    
    consoleWarnSpy.mockRestore();
  });

  it(&apos;finds a fuzzy string&apos;, () =&gt; {
    repository.setOptions({ strategy: &apos;fuzzy&apos; });
    const results = repository.search(&apos;lrm ism&apos;);
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject(loremElement);
    expect(results[0]._matchInfo).toBeDefined();
  });

  it(&apos;finds items using a wildcard pattern&apos;, () =&gt; {
    repository.setOptions({ strategy: &apos;wildcard&apos; });
    const results1 = repository.search(&apos;* ipsum&apos;);
    expect(results1).toHaveLength(1);
    expect(results1[0]).toMatchObject(loremElement);
    expect(results1[0]._matchInfo).toBeDefined();
    
    const results2 = repository.search(&apos;*bar&apos;);
    expect(results2).toHaveLength(2);
    expect(results2[0]).toMatchObject(barElement);
    expect(results2[1]).toMatchObject(almostBarElement);
  });

  it(&apos;respects wildcard spacing configuration via strategy object&apos;, () =&gt; {
    repository.put([{ title: &apos;foo&apos;, content: &apos;foo bar&apos; }]);
    repository.setOptions({ strategy: &apos;wildcard&apos; });
    expect(repository.search(&apos;foo*r&apos;)).toEqual([]);

    repository.setOptions({
      strategy: { type: &apos;wildcard&apos;, options: { maxSpaces: 1 } }
    });
    const configuredResults = repository.search(&apos;foo*r&apos;);
    expect(configuredResults).toHaveLength(1);
    expect(configuredResults[0]).toMatchObject({ title: &apos;foo&apos;, content: &apos;foo bar&apos; });
  });

  it(&apos;returns empty search results when an empty criteria is provided&apos;, () =&gt; {
    expect(repository.search(&apos;&apos;)).toEqual([]);
  });

  it(&apos;excludes items from search #1&apos;, () =&gt; {
    repository.setOptions({
      exclude: [&apos;almostbar&apos;],
    });
    expect(repository.search(&apos;almostbar&apos;)).toEqual([]);
  });

  it(&apos;sorts search results alphabetically by title&apos;, () =&gt; {
    repository.setOptions({
      sortMiddleware: (a: TestElement, b: TestElement) =&gt; {
        return a.title.localeCompare(b.title);
      },
    });
    const results = repository.search(&apos;r&apos;);
    expect(results).toHaveLength(3);
    expect(results[0]).toMatchObject(almostBarElement);
    expect(results[1]).toMatchObject(barElement);
    expect(results[2]).toMatchObject(loremElement);
  });

  it(&apos;uses default NoSort when no sortMiddleware provided&apos;, () =&gt; {
    const results = repository.search(&apos;r&apos;);
    expect(results).toHaveLength(3);
    expect(results[0]).toMatchObject(barElement);
    expect(results[1]).toMatchObject(almostBarElement);
    expect(results[2]).toMatchObject(loremElement);
  });

  it(&apos;demonstrates README example: custom sorting by section and caption&apos;, () =&gt; {
    const testData = [
      { section: &apos;Getting Started&apos;, caption: &apos;Installation&apos;, title: &apos;How to install&apos; },
      { section: &apos;API Reference&apos;, caption: &apos;Methods&apos;, title: &apos;Available methods&apos; },
      { section: &apos;Getting Started&apos;, caption: &apos;Configuration&apos;, title: &apos;How to configure&apos; },
      { section: &apos;API Reference&apos;, caption: &apos;Properties&apos;, title: &apos;Object properties&apos; }
    ];
    
    repository.put(testData);
    repository.setOptions({
      sortMiddleware: (a: any, b: any) =&gt; {
        const astr = String(a.section) + &quot;-&quot; + String(a.caption);
        const bstr = String(b.section) + &quot;-&quot; + String(b.caption);
        return astr.localeCompare(bstr);
      },
    });
    
    const results = repository.search(&apos;How&apos;);
    expect(results).toHaveLength(2);
    // Should be sorted by section first, then caption
    expect(results[0].section).toBe(&apos;Getting Started&apos;);
    expect(results[0].caption).toBe(&apos;Configuration&apos;);
    expect(results[1].section).toBe(&apos;Getting Started&apos;);
    expect(results[1].caption).toBe(&apos;Installation&apos;);
  });

  it(&apos;search results should be a clone and not a reference to repository data&apos;, () =&gt; {
    const query = &apos;Developer&apos;;
    const testData = [
      { name: &apos;Alice&apos;, role: &apos;Developer&apos; },
      { name: &apos;Bob&apos;, role: &apos;Designer&apos; }
    ];
    repository.put(testData);

    const results = repository.search(query);
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject({ name: &apos;Alice&apos;, role: &apos;Developer&apos; });

    (results as any[]).forEach(result =&gt; {
      result.role = &apos;Modified Role&apos;;
    });

    const originalData = repository.search(query);
    expect(originalData).toHaveLength(1);
    expect(originalData[0]).toMatchObject({ name: &apos;Alice&apos;, role: &apos;Developer&apos; });
  });

  it(&apos;demonstrates README sortMiddleware example exactly&apos;, () =&gt; {
    // This test matches the exact example from the README
    const testData = [
      { section: &apos;API Reference&apos;, caption: &apos;Properties&apos;, title: &apos;Object properties&apos; },
      { section: &apos;Getting Started&apos;, caption: &apos;Installation&apos;, title: &apos;How to install&apos; },
      { section: &apos;API Reference&apos;, caption: &apos;Methods&apos;, title: &apos;Available methods&apos; },
      { section: &apos;Getting Started&apos;, caption: &apos;Configuration&apos;, title: &apos;How to configure&apos; }
    ];
    
    repository.put(testData);
    repository.setOptions({
      sortMiddleware: function(a: any, b: any) {
        var astr = String(a.section) + &quot;-&quot; + String(a.caption);
        var bstr = String(b.section) + &quot;-&quot; + String(b.caption);
        return astr.localeCompare(bstr);
      },
    });
    
    const results = repository.search(&apos;a&apos;); // Search for &apos;a&apos; to get all results
    expect(results).toHaveLength(4);
    
    // Should be sorted by section first, then caption alphabetically
    expect(results[0].section).toBe(&apos;API Reference&apos;);
    expect(results[0].caption).toBe(&apos;Methods&apos;);
    expect(results[1].section).toBe(&apos;API Reference&apos;);
    expect(results[1].caption).toBe(&apos;Properties&apos;);
    expect(results[2].section).toBe(&apos;Getting Started&apos;);
    expect(results[2].caption).toBe(&apos;Configuration&apos;);
    expect(results[3].section).toBe(&apos;Getting Started&apos;);
    expect(results[3].caption).toBe(&apos;Installation&apos;);
  });
});</file><file path="tests/SimpleJekyllSearch.test.ts">import { afterEach, beforeEach, describe, expect, it, vi } from &apos;vitest&apos;;
import SimpleJekyllSearch from &apos;../src/SimpleJekyllSearch&apos;;
import { SearchData, SearchOptions } from &apos;../src/utils/types&apos;;
import { createHighlightTemplateMiddleware } from &apos;../src/middleware/highlightMiddleware&apos;;

describe(&apos;SimpleJekyllSearch&apos;, () =&gt; {
  let searchInstance: SimpleJekyllSearch;
  let mockOptions: SearchOptions;
  let mockSearchData: SearchData[];
  const STORAGE_KEY = &apos;sjs-search-state&apos;;

  beforeEach(() =&gt; {
    document.body.innerHTML = `
      &lt;input id=&quot;search-input&quot; type=&quot;text&quot; /&gt;
      &lt;div id=&quot;results-container&quot;&gt;&lt;/div&gt;
    `;

    searchInstance = new SimpleJekyllSearch();

    mockOptions = {
      searchInput: document.getElementById(&apos;search-input&apos;) as HTMLInputElement,
      resultsContainer: document.getElementById(&apos;results-container&apos;) as HTMLElement,
      json: [],
      searchResultTemplate: &apos;&lt;li&gt;{title}&lt;/li&gt;&apos;,
      noResultsText: &apos;No results found&apos;,
      debounceTime: 100,
    };

    mockSearchData = [
      { title: &apos;Test Post 1&apos;, url: &apos;/test1&apos;, category: &apos;test&apos;, tags: &apos;test1, test2&apos; },
      { title: &apos;Test Post 2&apos;, url: &apos;/test2&apos;, category: &apos;test&apos;, tags: &apos;test1, test2&apos; },
    ];

    sessionStorage.clear();
  });

  afterEach(() =&gt; {
    sessionStorage.clear();
  });

  describe(&apos;initialization&apos;, () =&gt; {
    it(&apos;should throw error when required options are missing&apos;, () =&gt; {
      const invalidOptions = {} as SearchOptions;
      expect(() =&gt; searchInstance.init(invalidOptions)).toThrow();
    });

    it(&apos;should initialize successfully with valid options&apos;, () =&gt; {
      const instance = searchInstance.init(mockOptions);
      expect(instance).toBeDefined();
      expect(instance.search).toBeDefined();
    });

    it(&apos;should initialize with JSON data&apos;, () =&gt; {
      const optionsWithJSON = { ...mockOptions, json: mockSearchData };
      const instance = searchInstance.init(optionsWithJSON);
      expect(instance).toBeDefined();
    });
  });

  describe(&apos;search functionality&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
    });

    it(&apos;should not search with empty query&apos;, () =&gt; {
      const resultsContainer = mockOptions.resultsContainer;
      searchInstance.search(&apos;&apos;);
      expect(resultsContainer.innerHTML).toBe(&apos;&apos;);
    });

    it(&apos;should search and render results&apos;, () =&gt; {
      const resultsContainer = mockOptions.resultsContainer;
      searchInstance.search(&apos;Test&apos;);
      expect(resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
    });

    it(&apos;should show no results text when no matches found&apos;, () =&gt; {
      const resultsContainer = mockOptions.resultsContainer;
      searchInstance.search(&apos;NonExistent&apos;);
      expect(resultsContainer.innerHTML).toContain(&apos;No results found&apos;);
    });
  });

  describe(&apos;keyboard input handling&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
    });

    it(&apos;should trigger search on non-whitelisted key input&apos;, async () =&gt; {
      const input = mockOptions.searchInput;
      const event = new KeyboardEvent(&apos;input&apos;, { key: &apos;t&apos; });
      input.value = &apos;Test&apos;;
      input.dispatchEvent(event);

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      expect(mockOptions.resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
      expect(input.value).toBe(&apos;Test&apos;);
    });

    it(&apos;should not trigger search on whitelisted key input&apos;, async () =&gt; {
      const input = mockOptions.searchInput;
      const event = new KeyboardEvent(&apos;input&apos;, { key: &apos;Enter&apos; });
      input.value = &apos;Test&apos;;
      input.dispatchEvent(event);

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      expect(mockOptions.resultsContainer.innerHTML).toBe(&apos;&apos;);
    });
  });

  describe(&apos;debounce functionality&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
    });

    it(&apos;should debounce multiple rapid inputs&apos;, async () =&gt; {
      const input = mockOptions.searchInput;
      const resultsContainer = mockOptions.resultsContainer;

      input.value = &apos;T&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;T&apos; }));

      input.value = &apos;Te&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;e&apos; }));

      input.value = &apos;Tes&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;s&apos; }));

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      expect(resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
    });
  });

  describe(&apos;search state restoration&apos;, () =&gt; {
    it(&apos;should restore search when input has value but results are empty&apos;, () =&gt; {
      const input = mockOptions.searchInput;
      const resultsContainer = mockOptions.resultsContainer;
      
      input.value = &apos;Test&apos;;
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
    });

    it(&apos;should not restore search when input is empty&apos;, () =&gt; {
      const input = mockOptions.searchInput;
      const resultsContainer = mockOptions.resultsContainer;
      
      input.value = &apos;&apos;;
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(resultsContainer.innerHTML).toBe(&apos;&apos;);
    });

    it(&apos;should not restore search when results already exist&apos;, () =&gt; {
      const input = mockOptions.searchInput;
      const resultsContainer = mockOptions.resultsContainer;
      
      resultsContainer.innerHTML = &apos;&lt;li&gt;Existing Result&lt;/li&gt;&apos;;
      input.value = &apos;Test&apos;;
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(resultsContainer.innerHTML).toBe(&apos;&lt;li&gt;Existing Result&lt;/li&gt;&apos;);
    });

    it(&apos;should not restore search when input has only whitespace&apos;, () =&gt; {
      const input = mockOptions.searchInput;
      const resultsContainer = mockOptions.resultsContainer;
      
      input.value = &apos;   &apos;;
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(resultsContainer.innerHTML).toBe(&apos;&apos;);
    });
  });

  describe(&apos;error handling&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
    });

    it(&apos;should call onError callback when provided&apos;, async () =&gt; {
      const onErrorSpy = vi.fn();
      const optionsWithErrorHandler = { ...mockOptions, onError: onErrorSpy };
      
      searchInstance.init(optionsWithErrorHandler);
      
      const input = mockOptions.searchInput;
      input.value = &apos;test&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;t&apos; }));

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      
      expect(onErrorSpy).not.toHaveBeenCalled();
    });

    it(&apos;should handle malformed search data gracefully&apos;, async () =&gt; {
      const onErrorSpy = vi.fn();
      const consoleErrorSpy = vi.spyOn(console, &apos;error&apos;).mockImplementation(() =&gt; {});
      
      const malformedData = [
        { title: &apos;Valid Post&apos;, url: &apos;/valid&apos; },
        { title: null, url: undefined },
        { title: &apos;Another Valid Post&apos;, url: &apos;/another&apos; }
      ];
      
      const optionsWithMalformedData = { 
        ...mockOptions, 
        json: malformedData as any,
        onError: onErrorSpy 
      };
      
      expect(() =&gt; searchInstance.init(optionsWithMalformedData)).not.toThrow();
      
      const input = mockOptions.searchInput;
      input.value = &apos;Valid&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;V&apos; }));

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      
      expect(onErrorSpy).toHaveBeenCalledWith(expect.any(Error));
      consoleErrorSpy.mockRestore();
    });

    it(&apos;should handle missing DOM elements gracefully&apos;, async () =&gt; {
      const onErrorSpy = vi.fn();
      const consoleErrorSpy = vi.spyOn(console, &apos;error&apos;).mockImplementation(() =&gt; {});
      
      const optionsWithMissingElement = { 
        ...mockOptions, 
        searchInput: null as any,
        onError: onErrorSpy 
      };
      
      expect(() =&gt; searchInstance.init(optionsWithMissingElement)).toThrow();
      consoleErrorSpy.mockRestore();
    });

    it(&apos;should use default error handler when onError not provided&apos;, async () =&gt; {
      const consoleErrorSpy = vi.spyOn(console, &apos;error&apos;).mockImplementation(() =&gt; {});
      
      searchInstance.init(mockOptions);
      
      const input = mockOptions.searchInput;
      input.value = &apos;test&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;t&apos; }));

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      
      expect(consoleErrorSpy).not.toHaveBeenCalled();
      consoleErrorSpy.mockRestore();
    });

    it(&apos;should handle invalid search queries gracefully&apos;, async () =&gt; {
      const onErrorSpy = vi.fn();
      const optionsWithErrorHandler = { ...mockOptions, onError: onErrorSpy };
      
      searchInstance.init(optionsWithErrorHandler);
      
      const input = mockOptions.searchInput;
      input.value = &apos;a&apos;.repeat(10000);
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;a&apos; }));

      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      
      expect(mockOptions.resultsContainer.innerHTML).toContain(&apos;No results found&apos;);
      expect(onErrorSpy).not.toHaveBeenCalled();
    });
  });

  describe(&apos;title highlighting with URL template&apos;, () =&gt; {
    it(&apos;should highlight title but not break URL when search term matches both&apos;, async () =&gt; {
      const highlightMiddleware = createHighlightTemplateMiddleware({
        className: &apos;search-highlight&apos;,
        maxLength: 200
      });

      const searchData: SearchData[] = [
        { 
          title: &apos;This is just a test&apos;, 
          url: &apos;/2014/11/02/test.html&apos;, 
          category: &apos;test&apos;, 
          tags: &apos;test1, test2&apos;,
          content: &apos;Some test content here&apos;
        }
      ];

      const optionsWithTemplate = {
        ...mockOptions,
        json: searchData,
        searchResultTemplate: &apos;&lt;li&gt;&lt;a href=&quot;{url}?query={query}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;,
        templateMiddleware: highlightMiddleware,
        strategy: &apos;hybrid&apos; as const
      };

      searchInstance.init(optionsWithTemplate);
      searchInstance.search(&apos;test&apos;);

      await new Promise(resolve =&gt; setTimeout(resolve, 50));

      const resultsContainer = mockOptions.resultsContainer;
      const link = resultsContainer.querySelector(&apos;a&apos;);

      expect(link).toBeTruthy();
      expect(link?.getAttribute(&apos;href&apos;)).toBe(&apos;/2014/11/02/test.html?query=test&apos;);
      expect(link?.innerHTML).toContain(&apos;&lt;span class=&quot;search-highlight&quot;&gt;test&lt;/span&gt;&apos;);
      expect(resultsContainer.innerHTML).not.toContain(&apos;href=&quot;/2014/11/02/&lt;span&apos;);
    });
  });

  describe(&apos;saveSearchState&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
    });

    it(&apos;stores valid JSON with query, timestamp, and path&apos;, () =&gt; {
      searchInstance.search(&apos;Test&apos;);
      
      const stored = sessionStorage.getItem(STORAGE_KEY);
      expect(stored).not.toBeNull();
      
      const state = JSON.parse(stored!);
      expect(state.query).toBe(&apos;Test&apos;);
      expect(state.timestamp).toBeTypeOf(&apos;number&apos;);
      expect(state.path).toBe(window.location.pathname);
    });

    it(&apos;clears storage when query is empty string&apos;, () =&gt; {
      searchInstance.search(&apos;Test&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
      
      searchInstance.search(&apos;&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;clears storage when query is whitespace only&apos;, () =&gt; {
      searchInstance.search(&apos;Test&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
      
      searchInstance.search(&apos;   &apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;trims query before storing&apos;, () =&gt; {
      searchInstance.search(&apos;  Test  &apos;);
      
      const stored = sessionStorage.getItem(STORAGE_KEY);
      const state = JSON.parse(stored!);
      expect(state.query).toBe(&apos;Test&apos;);
    });

    it(&apos;fails silently when sessionStorage is unavailable&apos;, () =&gt; {
      const originalSetItem = sessionStorage.setItem;
      sessionStorage.setItem = () =&gt; { throw new Error(&apos;Storage unavailable&apos;); };
      
      expect(() =&gt; searchInstance.search(&apos;Test&apos;)).not.toThrow();
      
      sessionStorage.setItem = originalSetItem;
    });

    it(&apos;fails silently when sessionStorage quota is exceeded&apos;, () =&gt; {
      const originalSetItem = sessionStorage.setItem;
      sessionStorage.setItem = () =&gt; { throw new DOMException(&apos;QuotaExceededError&apos;); };
      
      expect(() =&gt; searchInstance.search(&apos;Test&apos;)).not.toThrow();
      
      sessionStorage.setItem = originalSetItem;
    });
  });

  describe(&apos;getStoredSearchState&apos;, () =&gt; {
    it(&apos;returns query string for valid stored state&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;Test&apos;);
    });

    it(&apos;returns null when no state is stored&apos;, () =&gt; {
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
      expect(mockOptions.resultsContainer.innerHTML).toBe(&apos;&apos;);
    });

    it(&apos;returns null and clears for corrupted JSON&apos;, () =&gt; {
      sessionStorage.setItem(STORAGE_KEY, &apos;{broken json&apos;);
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;returns null and clears for missing query field&apos;, () =&gt; {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
        timestamp: Date.now(),
        path: window.location.pathname
      }));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
    });

    it(&apos;returns null and clears for non-string query field&apos;, () =&gt; {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
        query: 123,
        timestamp: Date.now(),
        path: window.location.pathname
      }));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
    });

    it(&apos;returns null and clears for stale data (&gt;30 min)&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now() - (31 * 60 * 1000), // 31 minutes ago
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;returns query for data within 30 min threshold&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now() - (29 * 60 * 1000), // 29 minutes ago
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;Test&apos;);
    });

    it(&apos;returns null and clears for different page path&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: &apos;/different-page/&apos;
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;returns query when path matches current location&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;Test&apos;);
    });

    it(&apos;fails silently when sessionStorage is unavailable&apos;, () =&gt; {
      const originalGetItem = sessionStorage.getItem;
      sessionStorage.getItem = () =&gt; { throw new Error(&apos;Storage unavailable&apos;); };
      
      mockOptions.json = mockSearchData;
      expect(() =&gt; searchInstance.init(mockOptions)).not.toThrow();
      
      sessionStorage.getItem = originalGetItem;
    });
  });

  describe(&apos;clearSearchState&apos;, () =&gt; {
    beforeEach(() =&gt; {
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
    });

    it(&apos;removes item from sessionStorage&apos;, () =&gt; {
      searchInstance.search(&apos;Test&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
      
      searchInstance.search(&apos;&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it(&apos;fails silently when sessionStorage is unavailable&apos;, () =&gt; {
      searchInstance.search(&apos;Test&apos;);
      
      const originalRemoveItem = sessionStorage.removeItem;
      sessionStorage.removeItem = () =&gt; { throw new Error(&apos;Storage unavailable&apos;); };
      
      expect(() =&gt; searchInstance.search(&apos;&apos;)).not.toThrow();
      
      sessionStorage.removeItem = originalRemoveItem;
    });
  });

  describe(&apos;restoreSearchState (with sessionStorage)&apos;, () =&gt; {
    it(&apos;does nothing when results already exist&apos;, () =&gt; {
      const resultsContainer = mockOptions.resultsContainer;
      resultsContainer.innerHTML = &apos;&lt;li&gt;Existing Result&lt;/li&gt;&apos;;
      
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(resultsContainer.innerHTML).toBe(&apos;&lt;li&gt;Existing Result&lt;/li&gt;&apos;);
    });

    it(&apos;uses browser-restored input value over storage&apos;, () =&gt; {
      const state = {
        query: &apos;StoredQuery&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;Test&apos;; // Browser restored this
      searchInstance.init(mockOptions);
      
      expect(mockOptions.resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
    });

    it(&apos;falls back to storage when input is empty&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;Test&apos;);
      expect(mockOptions.resultsContainer.innerHTML).toContain(&apos;Test Post&apos;);
    });

    it(&apos;syncs input value when restoring from storage&apos;, () =&gt; {
      const state = {
        query: &apos;Test&apos;,
        timestamp: Date.now(),
        path: window.location.pathname
      };
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;Test&apos;);
    });

    it(&apos;does nothing when both input and storage are empty&apos;, () =&gt; {
      mockOptions.json = mockSearchData;
      const input = mockOptions.searchInput;
      input.value = &apos;&apos;;
      searchInstance.init(mockOptions);
      
      expect(input.value).toBe(&apos;&apos;);
      expect(mockOptions.resultsContainer.innerHTML).toBe(&apos;&apos;);
    });
  });

  describe(&apos;registerInput&apos;, () =&gt; {
    it(&apos;adds input listener to searchInput&apos;, () =&gt; {
      const addEventListenerSpy = vi.spyOn(mockOptions.searchInput, &apos;addEventListener&apos;);
      
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(addEventListenerSpy).toHaveBeenCalledWith(&apos;input&apos;, expect.any(Function));
    });

    it(&apos;adds pageshow listener to window&apos;, () =&gt; {
      const addEventListenerSpy = vi.spyOn(window, &apos;addEventListener&apos;);
      
      mockOptions.json = mockSearchData;
      searchInstance.init(mockOptions);
      
      expect(addEventListenerSpy).toHaveBeenCalledWith(&apos;pageshow&apos;, expect.any(Function));
    });
  });

  describe(&apos;destroy&apos;, () =&gt; {
    it(&apos;removes input listener from searchInput&apos;, () =&gt; {
      mockOptions.json = mockSearchData;
      const instance = searchInstance.init(mockOptions);
      
      const removeEventListenerSpy = vi.spyOn(mockOptions.searchInput, &apos;removeEventListener&apos;);
      instance.destroy();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith(&apos;input&apos;, expect.any(Function));
    });

    it(&apos;removes pageshow listener from window&apos;, () =&gt; {
      mockOptions.json = mockSearchData;
      const instance = searchInstance.init(mockOptions);
      
      const removeEventListenerSpy = vi.spyOn(window, &apos;removeEventListener&apos;);
      instance.destroy();
      
      expect(removeEventListenerSpy).toHaveBeenCalledWith(&apos;pageshow&apos;, expect.any(Function));
    });

    it(&apos;clears debounce timer&apos;, async () =&gt; {
      mockOptions.json = mockSearchData;
      const instance = searchInstance.init(mockOptions);
      
      const input = mockOptions.searchInput;
      input.value = &apos;Test&apos;;
      input.dispatchEvent(new KeyboardEvent(&apos;input&apos;, { key: &apos;t&apos; }));
      
      instance.destroy();
      
      await new Promise(resolve =&gt; setTimeout(resolve, mockOptions.debounceTime! + 10));
      
      expect(mockOptions.resultsContainer.innerHTML).toBe(&apos;&apos;);
    });

    it(&apos;clears search state from storage&apos;, () =&gt; {
      mockOptions.json = mockSearchData;
      const instance = searchInstance.init(mockOptions);
      
      searchInstance.search(&apos;Test&apos;);
      expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
      
      instance.destroy();
      expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });
  });
});</file><file path="tests/Templater.test.ts">import { describe, it, beforeEach, expect } from &apos;vitest&apos;;
import * as templater from &apos;../src/Templater&apos;;

describe(&apos;Templater&apos;, () =&gt; {
  beforeEach(() =&gt; {
    templater.setOptions({
      template: &apos;{foo}&apos;,
      pattern: /\{(.*?)\}/g
    });
  });

  it(&apos;renders the template with the provided data&apos;, () =&gt; {
    expect(templater.compile({ foo: &apos;bar&apos; })).toBe(&apos;bar&apos;);

    templater.setOptions({
      template: &apos;&lt;a href=&quot;{url}&quot;&gt;url&lt;/a&gt;&apos;
    });

    expect(templater.compile({ url: &apos;http://google.com&apos; })).toBe(&apos;&lt;a href=&quot;http://google.com&quot;&gt;url&lt;/a&gt;&apos;);
  });

  it(&apos;renders the template with the provided data and query&apos;, () =&gt; {
    expect(templater.compile({ foo: &apos;bar&apos; })).toBe(&apos;bar&apos;);

    templater.setOptions({
      template: &apos;&lt;a href=&quot;{url}?query={query}&quot;&gt;url&lt;/a&gt;&apos;
    });

    expect(templater.compile({ url: &apos;http://google.com&apos;, query: &apos;bar&apos; })).toBe(&apos;&lt;a href=&quot;http://google.com?query=bar&quot;&gt;url&lt;/a&gt;&apos;);
  });

  it(&apos;replaces not found properties with the original pattern&apos;, () =&gt; {
    const template = &apos;{foo}&apos;;
    templater.setOptions({
      template
    });
    expect(templater.compile({ x: &apos;bar&apos; })).toBe(template);
  });

  it(&apos;allows custom patterns to be set&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{{foo}}&apos;,
      pattern: /\{\{(.*?)\}\}/g
    });
    expect(templater.compile({ foo: &apos;bar&apos; })).toBe(&apos;bar&apos;);
  });

  it(&apos;middleware gets parameter to return new replacement&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{foo} - {bar}&apos;,
      middleware(prop: string, value: string) {
        if (prop === &apos;bar&apos;) {
          return value.replace(/^\//, &apos;&apos;);
        }
      }
    });

    const compiled = templater.compile({ foo: &apos;foo&apos;, bar: &apos;/leading/slash&apos; });

    expect(compiled).toBe(&apos;foo - leading/slash&apos;);
  });

  it(&apos;compile accepts optional query parameter&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{foo}&apos;,
      middleware(_prop: string, value: string, _template: string, query?: string) {
        if (query) {
          return `${value} (query: ${query})`;
        }
        return value;
      }
    });

    const compiled = templater.compile({ foo: &apos;bar&apos; }, &apos;test&apos;);
    expect(compiled).toBe(&apos;bar (query: test)&apos;);
  });

  it(&apos;middleware receives matchInfo when available&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{desc}&apos;,
      middleware(_prop: string, value: string, _template: string, _query?: string, matchInfo?: any[]) {
        if (matchInfo &amp;&amp; matchInfo.length &gt; 0) {
          return `${value} [${matchInfo.length} matches]`;
        }
        return value;
      }
    });

    const data = {
      desc: &apos;hello world&apos;,
      _matchInfo: {
        desc: [
          { start: 0, end: 5, text: &apos;hello&apos;, type: &apos;exact&apos; }
        ]
      }
    };

    const compiled = templater.compile(data, &apos;hello&apos;);
    expect(compiled).toBe(&apos;hello world [1 matches]&apos;);
  });

  it(&apos;middleware maintains backward compatibility with 3 parameters&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{foo}&apos;,
      middleware(_prop: string, value: string) {
        return value.toUpperCase();
      }
    });

    const compiled = templater.compile({ foo: &apos;bar&apos; }, &apos;query&apos;);
    expect(compiled).toBe(&apos;BAR&apos;);
  });

  it(&apos;middleware receives query but not matchInfo when matchInfo is unavailable&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{foo}&apos;,
      middleware(_prop: string, value: string, _template: string, query?: string, matchInfo?: any[]) {
        if (query &amp;&amp; !matchInfo) {
          return `${value} (query: ${query}, no matches)`;
        }
        return value;
      }
    });

    const compiled = templater.compile({ foo: &apos;bar&apos; }, &apos;test&apos;);
    expect(compiled).toBe(&apos;bar (query: test, no matches)&apos;);
  });

  it(&apos;compile works without query parameter (backward compatible)&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;{foo}&apos;,
      middleware(_prop: string, value: string) {
        return value;
      }
    });

    const compiled = templater.compile({ foo: &apos;bar&apos; });
    expect(compiled).toBe(&apos;bar&apos;);
  });

  it(&apos;demonstrates README example: uppercase title middleware&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;&lt;li&gt;{title}&lt;/li&gt;&apos;,
      middleware(prop: string, value: string) {
        if (prop === &apos;title&apos;) {
          return value.toUpperCase();
        }
        return undefined
      }
    });

    const data = { title: &apos;my post&apos; };
    const compiled = templater.compile(data);
    expect(compiled).toBe(&apos;&lt;li&gt;MY POST&lt;/li&gt;&apos;);
  });

  it(&apos;demonstrates multiple property processing with different transformations&apos;, () =&gt; {
    templater.setOptions({
      template: &apos;&lt;li&gt;&lt;a href=&quot;{url}&quot;&gt;{title}&lt;/a&gt;&lt;p&gt;{desc}&lt;/p&gt;&lt;/li&gt;&apos;,
      middleware(prop: string, value: string) {
        if (prop === &apos;url&apos;) {
          return value.replace(/^\//, &apos;&apos;); // Remove leading slash
        }
        if (prop === &apos;title&apos;) {
          return value.toUpperCase();
        }
        return undefined;
      }
    });

    const data = { 
      url: &apos;/blog/post&apos;, 
      title: &apos;my post&apos;, 
      desc: &apos;description&apos; 
    };
    const compiled = templater.compile(data);
    expect(compiled).toBe(&apos;&lt;li&gt;&lt;a href=&quot;blog/post&quot;&gt;MY POST&lt;/a&gt;&lt;p&gt;description&lt;/p&gt;&lt;/li&gt;&apos;);
  });
});</file><file path="tests/utils.test.ts">import { describe, expect, it } from &apos;vitest&apos;;
import { clone, isJSON, isObject, merge, NoSort } from &apos;../src/utils&apos;;

describe(&apos;utils&apos;, () =&gt; {

  describe(&apos;merge&apos;, () =&gt; {
    it(&apos;merges objects&apos;, () =&gt; {
      const defaultOptions = { foo: &apos;&apos;, bar: &apos;&apos; };
      const options = { bar: &apos;overwritten&apos; };
      const mergedOptions = merge(defaultOptions, options);

      expect(mergedOptions.foo).toBe(defaultOptions.foo);
      expect(mergedOptions.bar).toBe(options.bar);
    });

    it(&apos;merges objects with overlapping keys&apos;, () =&gt; {
      const defaultOptions = { foo: &apos;default&apos;, bar: &apos;default&apos; };
      const options = { bar: &apos;custom&apos; };
      const mergedOptions = merge(defaultOptions, options);

      expect(mergedOptions).toEqual({ foo: &apos;default&apos;, bar: &apos;custom&apos; });
    });

    it(&apos;merges when the second object is empty&apos;, () =&gt; {
      const defaultOptions = { foo: &apos;default&apos;, bar: &apos;default&apos; };
      const options = {};
      const mergedOptions = merge(defaultOptions, options);

      expect(mergedOptions).toEqual(defaultOptions);
    });

    it(&apos;merges nested objects&apos;, () =&gt; {
      const defaultOptions = { foo: { nested: &apos;default&apos; }, bar: &apos;default&apos; };
      const options = { foo: { nested: &apos;custom&apos; } };
      const mergedOptions = merge(defaultOptions, options);

      expect(mergedOptions).toEqual({ foo: { nested: &apos;custom&apos; }, bar: &apos;default&apos; });
    });

    it(&apos;does not mutate the original objects&apos;, () =&gt; {
      const defaultOptions = { foo: &apos;default&apos;, bar: &apos;default&apos; };
      const options = { bar: &apos;custom&apos; };
      const defaultOptionsCopy = { ...defaultOptions };
      const optionsCopy = { ...options };

      merge(defaultOptions, options);

      expect(defaultOptions).toEqual(defaultOptionsCopy);
      expect(options).toEqual(optionsCopy);
    });
  });

  describe(&apos;isJSON&apos;, () =&gt; {
    it(&apos;returns true for plain objects&apos;, () =&gt; {
      expect(isJSON({ foo: &apos;bar&apos; })).toBe(true);
      expect(isJSON({})).toBe(true);
      expect(isJSON({ nested: { key: &apos;value&apos; } })).toBe(true);
    });

    it(&apos;returns true for arrays&apos;, () =&gt; {
      expect(isJSON([])).toBe(true);
      expect(isJSON([1, 2, 3])).toBe(true);
      expect(isJSON([{ foo: &apos;bar&apos; }])).toBe(true);
    });

    it(&apos;returns false for null&apos;, () =&gt; {
      expect(isJSON(null)).toBe(false);
    });

    it(&apos;returns false for undefined&apos;, () =&gt; {
      expect(isJSON(undefined)).toBe(false);
    });

    it(&apos;returns false for primitives&apos;, () =&gt; {
      expect(isJSON(42)).toBe(false);
      expect(isJSON(0)).toBe(false);
      expect(isJSON(&apos;string&apos;)).toBe(false);
      expect(isJSON(&apos;&apos;)).toBe(false);
      expect(isJSON(true)).toBe(false);
      expect(isJSON(false)).toBe(false);
    });

    it(&apos;returns true for Date objects&apos;, () =&gt; {
      expect(isJSON(new Date())).toBe(true);
    });

    it(&apos;returns true for RegExp objects&apos;, () =&gt; {
      expect(isJSON(/regex/)).toBe(true);
    });

    it(&apos;returns false for functions&apos;, () =&gt; {
      expect(isJSON(() =&gt; {})).toBe(false);
      expect(isJSON(function() {})).toBe(false);
    });
  });

  describe(&apos;NoSort&apos;, () =&gt; {
    it(&apos;always returns 0&apos;, () =&gt; {
      expect(NoSort()).toBe(0);
    });
  });

  describe(&apos;isObject&apos;, () =&gt; {
    it(&apos;returns true for plain objects&apos;, () =&gt; {
      expect(isObject({})).toBe(true);
      expect(isObject({ key: &apos;value&apos; })).toBe(true);
    });

    it(&apos;returns false for arrays&apos;, () =&gt; {
      expect(isObject([])).toBe(false);
      expect(isObject([1, 2, 3])).toBe(false);
    });

    it(&apos;returns false for null&apos;, () =&gt; {
      expect(isObject(null)).toBe(false);
    });

    it(&apos;returns false for primitive types&apos;, () =&gt; {
      expect(isObject(42)).toBe(false);
      expect(isObject(&apos;string&apos;)).toBe(false);
      expect(isObject(true)).toBe(false);
      expect(isObject(undefined)).toBe(false);
    });
  });

  describe(&apos;clone&apos;, () =&gt; {
    it(&apos;creates a deep clone of an object&apos;, () =&gt; {
      const obj = { foo: &apos;bar&apos;, nested: { key: &apos;value&apos; } };
      const clonedObj = clone(obj);

      expect(clonedObj).toEqual(obj);
      expect(clonedObj).not.toBe(obj);
      expect(clonedObj.nested).not.toBe(obj.nested);
    });

    it(&apos;creates a deep clone of an array&apos;, () =&gt; {
      const arr = [{ foo: &apos;bar&apos; }, { key: &apos;value&apos; }];
      const clonedArr = clone(arr);

      expect(clonedArr).toEqual(arr);
      expect(clonedArr).not.toBe(arr);
      expect(clonedArr[0]).not.toBe(arr[0]);
    });

    it(&apos;returns primitive values as is&apos;, () =&gt; {
      expect(clone(42)).toBe(42);
      expect(clone(&apos;string&apos;)).toBe(&apos;string&apos;);
      expect(clone(null)).toBe(null);
      expect(clone(undefined)).toBe(undefined);
    });

    it(&apos;handles empty objects and arrays&apos;, () =&gt; {
      expect(clone({})).toEqual({});
      expect(clone([])).toEqual([]);
    });

    it(&apos;does not modify the original object&apos;, () =&gt; {
      const obj = { foo: &apos;bar&apos;, nested: { key: &apos;value&apos; } };
      const clonedObj = clone(obj);

      clonedObj.nested.key = &apos;modified&apos;;
      expect(obj.nested.key).toBe(&apos;value&apos;);
    });
  });
});</file><file path=".gitignore">*.sublime-workspace
npm-debug.log

.sass-cache/
_site/
node_modules/
cypress/videos/
cypress/screenshots/
.DS_Store
.idea
package-lock.json
.jekyll-cache
coverage/**</file><file path="CONTRIBUTING.md"># Contributing to Simple-Jekyll-Search

This is fork from Christian Lei&apos;s [Simple-Jekyll-Search](https://github.com/christian-fei/Simple-Jekyll-Search) repository,
which was archived on March 2022.
I wanted to keep the project alive since I use it for my own theme [Type-on-strap](https://github.com/sylhare/Type-on-Strap)

Thank you for considering contributing to Simple-Jekyll-Search! 
We welcome contributions of all kinds, including bug fixes, feature requests, documentation improvements, and more.

## Developer Setup

Install the dependencies and build the project:

```bash
yarn
```

Lint, build and run the tests:

```bash
yarn build
```

#### Acceptance tests

This should start and kill the example jekyll blog and run the cypress tests.
Make sure to `build` before so you run the tests against the latest version.

```bash
npm run cypress:run 
```</file><file path="cypress.config.ts">import { defineConfig } from &apos;cypress&apos;;

export default defineConfig({
  e2e: {
    baseUrl: &apos;http://localhost:4000/Simple-Jekyll-Search/&apos;,
    supportFile: &apos;cypress/support/e2e.ts&apos;,
    specPattern: &apos;cypress/e2e/**/*.ts&apos;,
    video: false,
    screenshotOnRunFailure: false,
    setupNodeEvents(on, _config) {
      on(&apos;before:run&apos;, (details) =&gt; {
        console.log(&apos;🚀 Starting Cypress tests:&apos;, details.specs?.length || 0, &apos;spec(s) to run&apos;);
        console.log(`Running on: ${details.browser?.name} ${details.browser?.version}`);
        console.log(&apos;📝 Make sure Jekyll server is running at http://localhost:4000/Simple-Jekyll-Search/&apos;);
        console.log(&apos;💡 Run: cd docs &amp;&amp; bundle exec jekyll serve --baseurl /Simple-Jekyll-Search&apos;);
        return Promise.resolve();
      });

      on(&apos;after:run&apos;, (_results) =&gt; {
        console.log(&apos;✅ Cypress test run completed!&apos;);
        return Promise.resolve();
      });
    },
  },
});</file><file path="eslint.config.js">import typescript from &apos;@typescript-eslint/eslint-plugin&apos;;
import typescriptParser from &apos;@typescript-eslint/parser&apos;;

export default [
  {
    ignores: [&apos;dist/**&apos;, &apos;node_modules/**&apos;, &apos;coverage/**&apos;],
  },
  {
    files: [&apos;**/*.ts&apos;],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: &apos;module&apos;,
      },
    },
    plugins: {
      &apos;@typescript-eslint&apos;: typescript,
    },
    rules: {
      ...typescript.configs.recommended.rules,
      &apos;@typescript-eslint/no-unused-expressions&apos;: &apos;off&apos;,
      &apos;@typescript-eslint/explicit-function-return-type&apos;: &apos;off&apos;,
      &apos;@typescript-eslint/no-explicit-any&apos;: &apos;off&apos;,
      &apos;@typescript-eslint/no-unused-vars&apos;: [
        &apos;error&apos;,
        {
          args: &apos;all&apos;,
          argsIgnorePattern: &apos;^_&apos;,
          caughtErrors: &apos;all&apos;,
          caughtErrorsIgnorePattern: &apos;^_&apos;,
          destructuredArrayIgnorePattern: &apos;^_&apos;,
          varsIgnorePattern: &apos;^_&apos;,
          ignoreRestSiblings: true,
        },
      ],
    },
  },
];</file><file path="LICENSE.md">The MIT License (MIT)

Copyright (c) 2015 Christian Fei
Copyright (c) 2025 Sylhare

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the &quot;Software&quot;), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED &quot;AS IS&quot;, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.</file><file path="package.json">{
  &quot;name&quot;: &quot;simple-jekyll-search&quot;,
  &quot;version&quot;: &quot;2.1.1&quot;,
  &quot;description&quot;: &quot;A simple JavaScript library to add search functionality to any Jekyll blog - Fast, lightweight, client-side search. Fork of Simple Jekyll Search from https://github.com/christian-fei/Simple-Jekyll-Search&quot;,
  &quot;main&quot;: &quot;dest/simple-jekyll-search.js&quot;,
  &quot;type&quot;: &quot;module&quot;,
  &quot;scripts&quot;: {
    &quot;cypress&quot;: &quot;cypress run&quot;,
    &quot;cypress:browser&quot;: &quot;cypress run --browser&quot;,
    &quot;cypress:run&quot;: &quot;node scripts/start-jekyll.js &amp;&amp; sleep 8 &amp;&amp; cypress run; node scripts/kill-jekyll.js&quot;,
    &quot;lint&quot;: &quot;eslint . --ext .ts&quot;,
    &quot;lint:fix&quot;: &quot;eslint . --ext .ts --fix&quot;,
    &quot;pretest&quot;: &quot;yarn run lint&quot;,
    &quot;build&quot;: &quot;tsc &amp;&amp; vite build &amp;&amp; terser dest/simple-jekyll-search.js -o dest/simple-jekyll-search.min.js&quot;,
    &quot;prebuild&quot;: &quot;yarn run test&quot;,
    &quot;postbuild&quot;: &quot;node scripts/stamp.js &lt; dest/simple-jekyll-search.min.js &gt; dest/simple-jekyll-search.min.js.tmp &amp;&amp; mv dest/simple-jekyll-search.min.js.tmp dest/simple-jekyll-search.min.js &amp;&amp; yarn run copy-example-code&quot;,
    &quot;copy-example-code&quot;: &quot;cp dest/simple-jekyll-search.min.js docs/assets/js/&quot;,
    &quot;test&quot;: &quot;vitest run --coverage&quot;,
    &quot;test:unit&quot;: &quot;vitest run --exclude &apos;**/performance/**&apos; --coverage&quot;,
    &quot;test:benchmark&quot;: &quot;NODE_OPTIONS=&apos;--max-old-space-size=4096&apos; vitest run tests/performance/&quot;,
    &quot;test:watch&quot;: &quot;vitest&quot;,
    &quot;start&quot;: &quot;cd docs; jekyll serve&quot;,
    &quot;prestart:docs&quot;: &quot;yarn run build&quot;,
    &quot;start:docs&quot;: &quot;cd docs &amp;&amp; bundle exec jekyll serve&quot;
  },
  &quot;repository&quot;: {
    &quot;type&quot;: &quot;git&quot;,
    &quot;url&quot;: &quot;git+https://github.com/sylhare/Simple-Jekyll-Search.git&quot;
  },
  &quot;author&quot;: &quot;Sylhare&quot;,
  &quot;license&quot;: &quot;MIT&quot;,
  &quot;files&quot;: [
    &quot;dest&quot;,
    &quot;src&quot;
  ],
  &quot;bugs&quot;: {
    &quot;url&quot;: &quot;https://github.com/sylhare/Simple-Jekyll-Search/issues&quot;
  },
  &quot;homepage&quot;: &quot;https://github.com/sylhare/Simple-Jekyll-Search&quot;,
  &quot;engines&quot;: {
    &quot;node&quot;: &quot;&gt;=24&quot;
  },
  &quot;devDependencies&quot;: {
    &quot;@types/jsdom&quot;: &quot;^27.0.0&quot;,
    &quot;@types/node&quot;: &quot;^25.2.0&quot;,
    &quot;@typescript-eslint/eslint-plugin&quot;: &quot;^8.54.0&quot;,
    &quot;@typescript-eslint/parser&quot;: &quot;^8.54.0&quot;,
    &quot;@vitest/coverage-v8&quot;: &quot;^4.0.18&quot;,
    &quot;cypress&quot;: &quot;^15.9.0&quot;,
    &quot;eslint&quot;: &quot;^9.39.2&quot;,
    &quot;jsdom&quot;: &quot;^27.4.0&quot;,
    &quot;terser&quot;: &quot;^5.46.0&quot;,
    &quot;ts-node&quot;: &quot;^10.9.2&quot;,
    &quot;typescript&quot;: &quot;^5.9.3&quot;,
    &quot;vite&quot;: &quot;7.3.1&quot;,
    &quot;vitest&quot;: &quot;^4.0.18&quot;
  },
  &quot;ts-node&quot;: {
    &quot;esm&quot;: true,
    &quot;experimentalSpecifierResolution&quot;: &quot;node&quot;
  },
  &quot;resolutions&quot;: {
    &quot;js-yaml&quot;: &quot;^4.1.1&quot;
  }
}</file><file path="README.md"># Simple-Jekyll-Search

A JavaScript library to add search functionality to any Jekyll blog.
A replacement for the archived [Simple Jekyll Search](https://github.com/christian-fei/Simple-Jekyll-Search) from Christian Fei.

## Use case

You have a blog built with Jekyll and want a **lightweight search functionality** that is:
- Purely client-side
- No server configurations or databases to maintain
- Set up in just **5 minutes**

## Getting started

### Create `search.json`

Place the following code in a file called `search.json` in your Jekyll blog. 
(You can also get a copy [from here](/docs/assets/data/search.json))

This file will be used as a small data source to perform the searches on the client side:

```yaml
---
layout: none
---
[
  {% for post in site.posts %}
    {
      &quot;title&quot;    : &quot;{{ post.title | escape }}&quot;,
      &quot;category&quot; : &quot;{{ post.category }}&quot;,
      &quot;tags&quot;     : &quot;{{ post.tags | join: &apos;, &apos; }}&quot;,
      &quot;url&quot;      : &quot;{{ post.url | relative_url }}&quot;,
      &quot;date&quot;     : &quot;{{ post.date }}&quot;
    } {% unless forloop.last %},{% endunless %}
  {% endfor %}
]
```

### Preparing the plugin

#### Add DOM elements

SimpleJekyllSearch needs two `DOM` elements to work:

- a search input field
- a result container to display the results

For example with the default configuration, 
you need to place the following code within the layout where you want the search to appear.
(See the configuration section below to customize it)

```html
&lt;!-- HTML elements for search --&gt;
&lt;input type=&quot;text&quot; id=&quot;search-input&quot; placeholder=&quot;Search blog posts..&quot;&gt;
&lt;ul id=&quot;results-container&quot;&gt;&lt;/ul&gt;
```

### Usage

Customize `SimpleJekyllSearch` by passing in your configuration options:

```js
var sjs = SimpleJekyllSearch({
  searchInput: document.getElementById(&apos;search-input&apos;),
  resultsContainer: document.getElementById(&apos;results-container&apos;),
  json: &apos;{{ &quot;/assets/data/search.json&quot; | relative_url }}&apos;,
})
```

The script and library needs to be imported in the `head` of your layout, or at the end of the `body` tag.

#### returns { search }

A new instance of SimpleJekyllSearch returns an object, with the only property `search`.
The `search` is a function used to simulate a user input and display the matching results.


```js
var sjs = SimpleJekyllSearch({ ...options })
sjs.search(&apos;Hello&apos;)
```

💡 it can be used to filter posts by tags or categories!

## Options

Here is a table for the available options, usage questions, troubleshooting &amp; guides:

| Option                 | Type           | Required | Description                                                                                                                                                                        |
|------------------------|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `searchInput`          | Element        | Yes      | The input element on which the plugin should listen for keyboard events and trigger the searching and rendering for articles.                                                      |
| `resultsContainer`     | Element        | Yes      | The container element in which the search results should be rendered in. Typically, a `&lt;ul&gt;`.                                                                                      |
| `json`                 | String \| JSON | Yes      | You can either pass in an URL to the `search.json` file, or the results in form of JSON directly, to save one round trip to get the data.                                          |
| `noResultsText`        | String         | No       | The HTML that will be shown if the query didn&apos;t match anything.                                                                                                                    |
| `limit`                | Number         | No       | You can limit the number of posts rendered on the page.                                                                                                                            |
| `strategy`             | String         | No       | Selects the built-in search behavior: `&apos;literal&apos;` (default), `&apos;fuzzy&apos;`, `&apos;wildcard&apos;`, or `&apos;hybrid&apos;`.                                                                               |
| `exclude`              | Array          | No       | Pass in a list of terms you want to exclude (terms will be matched against a regex, so URLs, words are allowed).                                                                   |
| `success`              | Function       | No       | A function called once the data has been loaded.                                                                                                                                   |
| `debounceTime`         | Number         | No       | Limit how many times the search function can be executed over the given time window. If no `debounceTime` (milliseconds) is provided a search will be triggered on each keystroke. |
| `searchResultTemplate` | String         | No       | The template of a single rendered search result. (match liquid value eg: `&apos;&lt;li&gt;&lt;a href=&quot;{{ site.url }}{url}&quot;&gt;{title}&lt;/a&gt;&lt;/li&gt;&apos;`                                                    |

### Configurable strategies

The `strategy` option can also accept an object for advanced tuning:

```js
SimpleJekyllSearch({
  // ...
  strategy: {
    type: &apos;hybrid&apos;,
    options: {
      minFuzzyLength: 4,
      preferFuzzy: true,
      maxSpaces: 1   // Let `*` span up to 1 space (default: 0 = stop at spaces)
    }
  }
})
```

- `options` mirrors the hybrid strategy options (fuzzy length, priority, etc.) and also accepts `maxSpaces` for wildcard matching.
- `options.maxSpaces` lets wildcard searches capture up to _n_ spaces inside each `*` segment so patterns like `hel*rld` can match `&quot;hello brave world&quot;` when `maxSpaces &gt;= 1`. (You can still set `options.maxSpaces` when using the dedicated `&apos;wildcard&apos;` strategy.)

## Middleware

### templateMiddleware (Function) [optional]

A function that will be called whenever a match in the template is found.
It gets passed the current property name, property value, template, query, and match information.
If the function returns a non-undefined value, it gets replaced in the template.

**New Interface:**
```js
templateMiddleware(prop, value, template, query?, matchInfo?)
```

- `prop`: The property name being processed from the JSON data.
- `value`: The property value
- `template`: The template string
- `query`: The search query (optional)
- `matchInfo`: Array of match information objects with start/end positions and match types (optional)

This can be useful for manipulating URLs, highlighting search terms, or custom formatting.

**Basic Example:**
```js
SimpleJekyllSearch({
  // ...other config
  searchResultTemplate: &apos;&lt;li&gt;{title}&lt;/li&gt;&apos;,
  templateMiddleware: function(prop, value, template, query, matchInfo) {
    if (prop === &apos;title&apos;) {
      return value.toUpperCase()
    }
  },
})
```

**How it works:**
- Template: `&apos;&lt;li&gt;{title}&lt;/li&gt;&apos;`
- When processing `{title}`: `prop = &apos;title&apos;`, `value = &apos;my post&apos;` → returns `&apos;MY POST&apos;`
- Final result: `&apos;&lt;li&gt;MY POST&lt;/li&gt;&apos;`


### sortMiddleware (Function) [optional]

A function that will be used to sort the filtered results.

By setting custom values in the search.json file, you can group the results by section or any other property.

Example:

```js
SimpleJekyllSearch({
  // ...other config
  sortMiddleware: function(a, b) {
    var astr = String(a.section) + &quot;-&quot; + String(a.caption);
    var bstr = String(b.section) + &quot;-&quot; + String(b.caption);
    return astr.localeCompare(bstr)
  },
})
```

### Built-in Highlight Middleware (Function) [optional]

Simple-Jekyll-Search now includes built-in highlighting functionality that can be easily integrated:

```js
import { createHighlightTemplateMiddleware } from &apos;simple-jekyll-search/middleware&apos;;

SimpleJekyllSearch({
  // ...other config
  templateMiddleware: createHighlightTemplateMiddleware({
    className: &apos;search-highlight&apos;,  // CSS class for highlighted text
    maxLength: 200,                 // Maximum length of highlighted content
    contextLength: 30               // Characters of context around matches
  }),
})
```

**Highlight Options:**
- `className`: CSS class name for highlighted spans (default: &apos;search-highlight&apos;)
- `maxLength`: Maximum length of content to display (truncates with ellipsis)
- `contextLength`: Number of characters to show around matches when truncating

**CSS Styling:**
```css
.search-highlight {
  background-color: yellow;
  font-weight: bold;
}
```</file><file path="tsconfig.json">{
  &quot;compilerOptions&quot;: {
    &quot;target&quot;: &quot;es2020&quot;,
    &quot;module&quot;: &quot;es2020&quot;,
    &quot;lib&quot;: [&quot;dom&quot;, &quot;es2020&quot;],
    &quot;declaration&quot;: true,
    &quot;outDir&quot;: &quot;./dest&quot;,
    &quot;rootDir&quot;: &quot;./src&quot;,
    &quot;strict&quot;: true,
    &quot;esModuleInterop&quot;: true,
    &quot;skipLibCheck&quot;: true,
    &quot;forceConsistentCasingInFileNames&quot;: true,
    &quot;moduleResolution&quot;: &quot;bundler&quot;,
    &quot;resolveJsonModule&quot;: true,
    &quot;isolatedModules&quot;: true,
    &quot;noEmit&quot;: false,
    &quot;sourceMap&quot;: false,
    &quot;typeRoots&quot;: [&quot;./node_modules/@types&quot;, &quot;./src/types&quot;]
  },
  &quot;files&quot;: [&quot;src/index.ts&quot;],
  &quot;include&quot;: [&quot;src/**/*&quot;],
  &quot;exclude&quot;: [&quot;node_modules&quot;, &quot;dest&quot;, &quot;docs&quot;, &quot;tests&quot;]
}</file><file path="vite.config.ts">import { resolve } from &apos;path&apos;;
import { defineConfig } from &apos;vitest/config&apos;;

export default defineConfig({
  build: {
    outDir: &apos;dest&apos;,
    lib: {
      entry: resolve(__dirname, &apos;src/index.ts&apos;),
      name: &apos;SimpleJekyllSearch&apos;,
      fileName: (_format) =&gt; &apos;simple-jekyll-search.js&apos;,
      formats: [&apos;umd&apos;],
    },
    minify: false,
    sourcemap: false,
    rollupOptions: {
      output: {
        generatedCode: {
          preset: &apos;es2015&apos;,
          symbols: true
        },
        exports: &apos;named&apos;
      }
    }
  },
  test: {
    environment: &apos;jsdom&apos;,
    maxWorkers: 4,
    coverage: {
      provider: &apos;v8&apos;,
      reporter: [&apos;text&apos;, &apos;lcov&apos;],
      include: [&apos;src/**/*.ts&apos;],
      exclude: [
        &apos;**/*.d.ts&apos;,
        &apos;**/*.test.ts&apos;,
        &apos;**/*.spec.ts&apos;,
        &apos;**/types.ts&apos;,
        &apos;**/index.ts&apos;
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    }
  }
});</file></files>
~~~
````

So, your tasks, as the ASSISTANT, are all the necessary and sufficient ones to properly implement each and every feature/capability of the artifacts from the above given referenced `https://github.com/sylhare/Simple-Jekyll-Search` repository source-code within my jekyll static site github repository located at `https://github.com/ib-bsb-br/ib-bsb-br.github.io`, in order to coherently, seamsless, with holistical cohesiveness, and organically implement and enclose as many features and capabilities as possible while considering the idiosyncrasies of this jekyll static site of mine.
