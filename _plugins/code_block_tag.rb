# _plugins/code_block_tag.rb
require 'cgi' # Required for HTML escaping

module Jekyll
  class CodeBlockTag < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      # Store the language specified in the tag (e.g., {% codeblock python %})
      @language = markup.strip
    end

    # Helper method to dedent code blocks
    def dedent(raw_code)
      # Split content into lines
      lines = raw_code.split("\n")

      # Find the minimum indentation of non-empty lines
      min_indent = lines.map do |line|
        match = line.match(/^\s+/)
        # Get indentation length if line is not empty and has indentation
        match ? match[0].length : 0 unless line.strip.empty?
      end.compact.min || 0 # Use compact to remove nils from empty lines, find min, default to 0

      # Remove the common minimum indentation from each line
      dedented_code = lines.map do |line|
        line.length >= min_indent ? line[min_indent..-1] : line
      end.join("\n")

      # Strip leading/trailing whitespace from the whole block after dedenting
      dedented_code.strip
    end

    def render(context)
      # Get the raw code content from within the block tags
      raw_code_content = super

      # --- Improvement: Dedent the code content ---
      code_content = dedent(raw_code_content)

      # Determine file extension based on the language
      extension = case @language
                  # (Keep all language cases as before)
                  when "python" then ".py"
                  when "html" then ".html"
                  when "javascript", "js" then ".js"
                  when "css" then ".css"
                  when "ruby", "rb" then ".rb"
                  when "bash", "shell", "sh" then ".sh"
                  when "json" then ".json"
                  when "xml" then ".xml"
                  when "yaml", "yml" then ".yaml"
                  when "markdown", "md" then ".md"
                  when "java" then ".java"
                  when "c" then ".c"
                  when "cpp", "c++" then ".cpp"
                  when "csharp", "cs" then ".cs"
                  when "go" then ".go"
                  when "php" then ".php"
                  when "swift" then ".swift"
                  when "typescript", "ts" then ".ts"
                  when "sql" then ".sql"
                  when "dockerfile" then ".dockerfile"
                  when "makefile", "mk" then ".mk"
                  when "toml" then ".toml"        
                  when "rust", "rs" then ".rs"
                  else ".txt"
                  end

      # Generate filename and download label
      filename = "#{@language}_code_block#{extension}"
      download_label = "Download #{@language.capitalize()}"

      # --- HTML Escaping (Still Crucial) ---
      # Escape for safe rendering inside <code> tag
      escaped_code_for_display = CGI.escapeHTML(code_content)
      # Escape for safe inclusion in the data-code attribute
      escaped_code_for_attribute = CGI.escapeHTML(code_content).gsub('"', '&quot;')

      # --- Generate the HTML Output (Corrected & Improved Structure) ---
      # Outer section: Container, accessibility role/label, data attributes.
      # Inner code tag: Contains escaped code, language class for syntax highlighters.
      # IMPORTANT: Requires CSS `white-space: pre;` or `pre-wrap;` on the container or code tag.
      <<~HTML
        <section class="code-block-container" role="group" aria-label="#{@language.capitalize} Code Block" data-filename="#{filename}" data-code="#{escaped_code_for_attribute}" data-download-link data-download-label="#{download_label}">
          <code class="language-#{@language}">#{escaped_code_for_display}</code>
        </section>
      HTML
      # Note: The closing </section> tag above correctly closes the outer section.
    end
  end
end

# Register the custom tag with Liquid
Liquid::Template.register_tag('codeblock', Jekyll::CodeBlockTag)
