module Jekyll
  class CodeBlockTag < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
      @language = markup.strip
    end

    def render(context)
      code_content = super.strip.gsub(/^\s+/, "")

      # Determine file extension and MIME type based on language
      extension, mime_type = case @language
                              when "python" then [".py", "text/x-python"]
                              when "html" then [".html", "text/html"]
                              when "javascript" then [".js", "text/javascript"]
                              when "css" then [".css", "text/css"]
                              when "ruby" then [".rb", "text/x-ruby"]
                              when "bash", "shell" then [".sh", "text/x-sh"]
                              when "json" then [".json", "application/json"]
                              when "xml" then [".xml", "application/xml"]
                              when "yaml" then [".yaml", "text/yaml"]
                              when "markdown" then [".md", "text/markdown"]
                              when "java" then [".java", "text/x-java"]
                              when "c" then [".c", "text/x-c"]
                              when "cpp" then [".cpp", "text/x-c++"]
                              when "csharp" then [".cs", "text/x-csharp"]
                              when "go" then [".go", "text/x-go"]
                              when "php" then [".php", "text/x-php"]
                              when "swift" then [".swift", "text/x-swift"]
                              when "typescript" then [".ts", "text/typescript"]
                              when "sql" then [".sql", "text/x-sql"]
                              when "dockerfile" then [".dockerfile", "text/x-dockerfile"]
                              when "makefile" then [".mk", "text/x-makefile"]
                              else [".txt", "text/plain"] # Default
                              end

      filename = "#{@language}_code-block#{extension}"
      download_label = "Download #{@language.capitalize()}"

      # Escape code content for safe use in HTML attributes
      escaped_code_content = code_content.gsub('"', '&quot;')
      
      # Construct HTML output with data attributes 
      "<section data-filename=\"#{filename}\" data-code=\"#{escaped_code_content}\" data-download-link data-download-link-label=\"#{download_label}\" class=\"language-#{@language} line-numbers\" style=\"white-space:pre-wrap;\"><code class=\"language-#{@language}\">#{code_content}</code></section>"
    end
  end
end

Liquid::Template.register_tag('codeblock', Jekyll::CodeBlockTag)
