# frozen_string_literal: true

module Jekyll
  class RenderMermaid < Liquid::Block
    def render(context)
      text = super.strip
      mermaid_script = generate_mermaid_script

      <<~HTML
        <div class='mermaid' style='white-space: pre-wrap;'>#{text}</div>
        <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
        <script type='module'>
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
          #{mermaid_script}
        </script>
      HTML
    end

    private

    def generate_mermaid_script
      <<~SCRIPT
        const mermaidConfig = {
          startOnLoad: true,
          theme: 'default',
          flowchart: { useMaxWidth: false, htmlLabels: true, curve: 'cardinal' }
        };

        mermaid.initialize(mermaidConfig);

        document.addEventListener('DOMContentLoaded', () => {
          const svgElement = document.querySelector("div.mermaid>svg"); 
          if (svgElement) {
            svgPanZoom(svgElement, {
              minZoom: 0.5,
              maxZoom: 10,
              fit: true,
              contain: false,
              controlIconsEnabled: true,
              center: true,
              refreshRate: "auto",
            });
          } else {
            // Fallback if the SVG is not found immediately (e.g., async loading)
            const observer = new MutationObserver(() => {
              const svg = document.querySelector("div.mermaid>svg");
              if (svg) {
                svgPanZoom(svg, {
              minZoom: 0.5,
              maxZoom: 10,
              fit: true,
              contain: false,
              controlIconsEnabled: true,
              center: true,
              refreshRate: "auto",
            });
                observer.disconnect(); // Stop observing once the SVG is found 
              }
            });
    
            observer.observe(document.querySelector("div.mermaid"), { childList: true, subtree: true });
          }
        });
      SCRIPT
    end
  end
end

Liquid::Template.register_tag('mermaid', Jekyll::RenderMermaid)
