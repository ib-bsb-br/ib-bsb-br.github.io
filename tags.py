import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Default threshold, can be overridden when calling process_tags
DEFAULT_THRESHOLD = 1

def extract_frontmatter(file_content: str) -> str:
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split("\n")
    if content_lines and content_lines[0].strip() == "---": # Check if content_lines is not empty
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == "---":
                frontmatter = "\n".join(content_lines[1:i])
                break
    return frontmatter

def generate_partial_tags(tag: str) -> List[str]:
    """Generates all partial tags for a given tag."""
    parts = tag.split(">")
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append(">".join(parts[j: j + i]))
    return partial_tags

def process_tags(posts_dir: str, threshold: int) -> Dict[str, Any]:
    """
    Processes tags from markdown files, handling nested tags, highlighting exact matches,
    preventing duplicates using file paths.
    """
    tag_frequency = defaultdict(int)
    all_posts = []
    seen_posts = set()

    logging.info(f"Processing markdown files in directory: {posts_dir} with threshold: {threshold}")

    if not os.path.isdir(posts_dir):
        logging.error(f"Posts directory not found: {posts_dir}")
        return {}

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(posts_dir, filename)
        if file_path in seen_posts:
            logging.warning(f"Skipping duplicate post: {filename}")
            continue
        seen_posts.add(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            continue

        frontmatter = extract_frontmatter(file_content)
        if not frontmatter:
            logging.warning(f"No frontmatter found in {filename}")
            continue

        try:
            post_data = yaml.safe_load(frontmatter)
            if not isinstance(post_data, dict): # Ensure frontmatter parses to a dictionary
                logging.warning(f"Frontmatter in {filename} did not parse to a dictionary. Skipping.")
                continue
        except yaml.YAMLError as e:
            logging.error(f"Error parsing frontmatter in {filename}: {e}")
            continue

        tags = post_data.get("tags", [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",")]
        elif not isinstance(tags, list):
            tags = [str(tags)] # Ensure tags are processed as a list

        # Count tag frequencies including partial tags
        for tag_item in tags:
            if isinstance(tag_item, str): # Process only string tags
                for partial_tag in generate_partial_tags(tag_item):
                    tag_frequency[partial_tag] += 1
            else:
                logging.warning(f"Non-string tag '{tag_item}' found in {filename}. Skipping this tag.")


        title = post_data.get("title", os.path.splitext(filename)[0])
        # Ensure URL generation is robust, handles cases with fewer than 3 hyphens
        filename_parts = filename.split("-")
        if len(filename_parts) > 3:
            url_slug = "-".join(filename_parts[3:]).replace(".md", "")
        else:
            url_slug = filename.replace(".md", "") # Fallback if filename format is unexpected
        url = "/" + url_slug


        try:
            # Attempt to parse date from filename (e.g., YYYY-MM-DD-rest-of-name.md)
            date_str = "-".join(filename_parts[:3])
            post_date = datetime.strptime(date_str, "%Y-%m-%d")
        except (ValueError, IndexError):
            logging.warning(f"Unable to parse date from filename {filename}. Using minimal date.")
            post_date = datetime.min # Or consider using file modification time as a fallback

        all_posts.append({"title": title, "url": url, "date": post_date, "tags": [t for t in tags if isinstance(t, str)]})

    # Second pass: Generate tag data based on frequency threshold
    tag_data_intermediate = defaultdict(
        lambda: {
            "parents": set(),
            "children": set(),
            "related": defaultdict(int),
            "posts": [],
        }
    )

    for post in all_posts:
        for tag in post["tags"]:
            tag_parts = tag.split(">")
            full_tag_path = tag

            # Detect combined tags and store parent/child relationships for the full tag path
            if len(tag_parts) > 1:
                parent_of_full_tag = ">".join(tag_parts[:-1])
                if tag_frequency[parent_of_full_tag] >= threshold and tag_frequency[full_tag_path] >= threshold :
                    tag_data_intermediate[full_tag_path]["parents"].add(parent_of_full_tag)
                    tag_data_intermediate[parent_of_full_tag]["children"].add(full_tag_path)


            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= threshold:
                    post_entry = {
                        "title": post["title"],
                        "url": post["url"],
                        "highlighted": partial_tag == full_tag_path, # Highlight if it's the exact full tag from post
                        "date": post["date"].isoformat() if isinstance(post["date"], datetime) else datetime.min.isoformat(),
                    }
                    tag_data_intermediate[partial_tag]["posts"].append(post_entry)

            # Establish hierarchical parent-child relationships between *all* relevant partial tags
            for i in range(len(tag_parts) - 1):
                current_parent_segment = ">".join(tag_parts[:i+1])
                current_child_segment = ">".join(tag_parts[:i+2]) # This will be tag_parts[0] > tag_parts[0]>tag_parts[1] etc.

                # Ensure child is a direct extension of parent
                if current_child_segment.startswith(current_parent_segment + ">") and \
                   tag_frequency[current_parent_segment] >= threshold and \
                   tag_frequency[current_child_segment] >= threshold:
                    tag_data_intermediate[current_child_segment]["parents"].add(current_parent_segment)
                    tag_data_intermediate[current_parent_segment]["children"].add(current_child_segment)


            # Track non-hierarchical (related) relationships between top-level tags in the same post
            for other_tag_in_post in post["tags"]:
                if (
                    other_tag_in_post != tag # Must be a different tag
                    and tag_frequency[other_tag_in_post] >= threshold # Other tag meets threshold
                    and tag_frequency[full_tag_path] >= threshold # Current tag meets threshold
                    # Check they are not hierarchically related to each other
                    and not (full_tag_path.startswith(other_tag_in_post + ">") or other_tag_in_post.startswith(full_tag_path + ">"))
                ):
                    tag_data_intermediate[full_tag_path]["related"][other_tag_in_post] += 1
                    # No need to add other_tag_in_post related to full_tag_path here, will be covered when other_tag_in_post is 'tag'

    # Remove tags with no posts after all processing
    final_tag_data = {
        tag: data for tag, data in tag_data_intermediate.items() if data["posts"] and tag_frequency[tag] >= threshold
    }

    # Clean up relationships to ensure they only point to tags present in final_tag_data
    for tag, data in final_tag_data.items():
        data["parents"] = {p for p in data["parents"] if p in final_tag_data}
        data["children"] = {c for c in data["children"] if c in final_tag_data}
        data["related"] = {
            r: count for r, count in data["related"].items() if r in final_tag_data
        }
        # Sort posts within each tag by date (most recent first)
        # Ensure date is a string (isoformat) for consistent sorting if mixed with datetime.min
        data["posts"] = sorted(
            data["posts"], key=lambda x: x.get("date", datetime.min.isoformat()), reverse=True
        )

    # Return sorted dictionary by tag name for deterministic output
    return dict(sorted(final_tag_data.items()))


class JsonOutputHandler:
    def write(self, data: dict, json_output_file: str):
        """Writes the tag data to a JSON file."""
        # Custom converter for sets (though data should already be listified by yaml_safe_dump_convert if used before)
        # and ensure datetimes are in isoformat.
        # The input `data` from `process_tags` already has dates as isoformat strings
        # and sets should have been handled by the sorting process if it converts them.
        # The main `process_tags` now returns a structure with lists and isoformat dates.
        def convert_data_for_json(obj: Any):
            if isinstance(obj, (set, frozenset)): # Should ideally not be present if data is from process_tags
                return sorted(list(obj))
            elif isinstance(obj, datetime): # Should ideally not be present
                return obj.isoformat()
            # Let json.dump handle other types or raise its own error
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable by custom handler")

        try:
            with open(json_output_file, 'w', encoding='utf-8') as f:
                # Pass data directly as it should be serializable.
                # If sets/datetimes are still in `data`, json.dump will fail without a default.
                # The `process_tags` and `yaml_safe_dump_convert` should pre-process these.
                # For safety, we can use a default handler but it implies data wasn't fully pre-processed.
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Tag data has been written to {json_output_file}")
        except TypeError as e:
            logging.error(f"JSON serialization error for {json_output_file}: {e}. Data might contain unhandled types.")
        except Exception as e:
            logging.error(f"Failed to write JSON to {json_output_file}: {e}")


def generate_mermaid_graph(
    tag_data: Dict[str, Any], direction: str = "TD"
) -> str:
    """Generates Mermaid ER diagram code for the tag structure."""
    graph = [f"erDiagram {direction}"] # Use direction parameter
    added_nodes = set()
    added_edges = set()

    def sanitize_tag(tag: str) -> str:
        """Sanitize the tag name for use in Mermaid syntax."""
        # Basic sanitization, consider a more robust slugify function if needed
        s_tag = tag.replace(">", "_gt_") # Make explicit to avoid confusion with actual underscores
        s_tag = s_tag.replace(" ", "_sp_")
        # Replace common problematic characters for Mermaid IDs
        s_tag = ''.join(c if c.isalnum() or c == '_' else '_' for c in s_tag)
        # Ensure it doesn't start with a number if that's an issue for Mermaid IDs (usually not for ERD names)
        return s_tag if s_tag else "empty_tag"


    # First, define all entities (tags)
    for tag, data in tag_data.items():
        safe_tag = sanitize_tag(tag)
        if safe_tag not in added_nodes:
            # Minimal entity definition for ERD, attributes can be added if necessary
            # For ERD, it's common to list attributes. Here, we just define the entity.
            # Example: graph.append(f"    {safe_tag} {{ string name \"{tag}\" }}")
            graph.append(f"    {safe_tag} [label=\"{tag}\"] {{}}") # Using custom label to show original tag name
            added_nodes.add(safe_tag)

    # Second, define all relationships
    for tag, data in tag_data.items():
        safe_tag = sanitize_tag(tag)

        for parent in data.get("parents", []):
            if parent in tag_data: # Ensure parent exists in the processed data
                safe_parent = sanitize_tag(parent)
                # Ensure nodes are defined before creating edges if not done in a separate pass
                if safe_parent not in added_nodes: # Should be added in the first pass
                    graph.append(f"    {safe_parent} [label=\"{parent}\"] {{}}")
                    added_nodes.add(safe_parent)

                edge = f"    {safe_parent} ||--o{{ {safe_tag} : \"parent_of/includes\"" # Example ERD relationship
                if edge not in added_edges:
                    graph.append(edge)
                    added_edges.add(edge)

        for child in data.get("children", []):
            if child in tag_data: # Ensure child exists
                safe_child = sanitize_tag(child)
                if safe_child not in added_nodes: # Should be added in the first pass
                     graph.append(f"    {safe_child} [label=\"{child}\"] {{}}")
                     added_nodes.add(safe_child)

                edge = f"    {safe_tag} o--|| {safe_child} : \"child_of/part_of\"" # Example ERD relationship
                # Avoid duplicate edges if parent-child is symmetric in definition
                reverse_edge_check = f"    {safe_child} ||--o{{ {safe_tag} : \"parent_of/includes\""
                if edge not in added_edges and reverse_edge_check not in added_edges:
                    graph.append(edge)
                    added_edges.add(edge)
        
        for related_tag_name, count in data.get("related", {}).items():
            if related_tag_name in tag_data:
                safe_related = sanitize_tag(related_tag_name)
                if safe_related not in added_nodes:
                     graph.append(f"    {safe_related} [label=\"{related_tag_name}\"] {{}}")
                     added_nodes.add(safe_related)
                # Use a different relationship type for "related"
                # Ensure order for edge to avoid duplicates (e.g., always A--B, not B--A)
                node_pair = tuple(sorted((safe_tag, safe_related)))
                edge = f"    {node_pair[0]} {{o--o}} {node_pair[1]} : \"related (count: {count})\""
                if node_pair[0] != node_pair[1] and edge not in added_edges: # Avoid self-loops unless intended
                    graph.append(edge)
                    added_edges.add(edge)


    return "\n".join(graph)

# Helper function for robust YAML serialization
def yaml_safe_dump_convert(data_to_convert: Any) -> Any:
    if isinstance(data_to_convert, dict):
        return {k: yaml_safe_dump_convert(v) for k, v in data_to_convert.items()}
    elif isinstance(data_to_convert, list):
        return [yaml_safe_dump_convert(i) for i in data_to_convert]
    elif isinstance(data_to_convert, (set, frozenset)):
        # Sort sets for consistent output, then convert elements
        return [yaml_safe_dump_convert(i) for i in sorted(list(data_to_convert))]
    elif isinstance(data_to_convert, datetime):
        return data_to_convert.isoformat()
    return data_to_convert


def save_output(output_data: Dict[str, Any], output_folders: List[str]):
    """Saves YAML, JSON, and Mermaid graph outputs to multiple directories."""
    if not output_data:
        logging.warning("No output data to save.")
        return

    prepared_yaml_data = yaml_safe_dump_convert(output_data)

    for output_folder in output_folders:
        try:
            os.makedirs(output_folder, exist_ok=True) # Ensure output folder exists
        except OSError as e:
            logging.error(f"Could not create directory {output_folder}: {e}")
            continue # Skip to next folder

        yaml_file = os.path.join(output_folder, 'processed_tags.yml')
        json_file = os.path.join(output_folder, 'processed_tags.json')
        mermaid_file = os.path.join(output_folder, 'tag_graph.html')

        # Save YAML
        try:
            with open(yaml_file, 'w', encoding='utf-8') as f:
                yaml.dump(prepared_yaml_data, f, allow_unicode=True, sort_keys=False) # sort_keys=False as data is already sorted dict
            logging.info(f"YAML data saved to {yaml_file}")
        except Exception as e:
            logging.error(f"Failed to save YAML to {yaml_file}: {e}")

        # Save JSON
        # Data for JSON should also be pre-processed similarly to YAML (sets to lists, datetimes to strings)
        # The `prepared_yaml_data` is suitable for JSON as well.
        json_handler = JsonOutputHandler()
        json_handler.write(prepared_yaml_data, json_file)


        # Generate and save Mermaid graph
        try:
            mermaid_graph_code = generate_mermaid_graph(output_data) # Pass original output_data
            mermaid_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tag Relationship Graph</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
        // Optional: Add custom styles or configurations for Mermaid if needed
        // mermaid.mermaidAPI.setConfig({{ theme: 'neutral' }});
    </script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .mermaid {{ text-align: center; }}
    </style>
</head>
<body>
    <h1>Tag Relationship Graph</h1>
    <div class="mermaid">
{mermaid_graph_code}
    </div>
    <script>
        // Log errors from mermaid rendering to console
        const mermaidDiv = document.querySelector('.mermaid');
        if (mermaidDiv && mermaidDiv.textContent.trim() !== "") {{
            try {{
                mermaid.run({{ nodes: [mermaidDiv] }});
            }} catch (e) {{
                console.error("Mermaid rendering error:", e);
                mermaidDiv.innerHTML = "<pre>Error rendering Mermaid graph. Check console.</pre>";
            }}
        }} else if (mermaidDiv) {{
             mermaidDiv.innerHTML = "<p>No graph data to display.</p>";
        }}
    </script>
</body>
</html>"""
            with open(mermaid_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_html_content)
            logging.info(f"Mermaid graph saved to {mermaid_file}")
        except Exception as e:
            logging.error(f"Failed to generate or save Mermaid graph to {mermaid_file}: {e}")


def main():
    """Main function to orchestrate tag processing and output saving."""
    # Example usage (make sure to update the directory paths accordingly):
    posts_directory = '_posts' # Ensure this directory exists and has .md files
    # Define output folders, e.g., for a Jekyll or static site generator structure
    output_folders = ['assets/data', '_data', '_includes/output_tags']

    # Create dummy _posts directory and a sample file for testing if it doesn't exist
    if not os.path.exists(posts_directory):
        logging.info(f"Creating dummy posts directory: {posts_directory}")
        os.makedirs(posts_directory)
        sample_post_content_1 = """---
title: Sample Post 1 - Python Basics
tags:
  - Tech>Python>Basics
  - Programming
  - Education
---
This is a sample post about basic Python programming.
"""
        with open(os.path.join(posts_directory, "2023-01-01-sample-post-1.md"), "w", encoding="utf-8") as f:
            f.write(sample_post_content_1)

        sample_post_content_2 = """---
title: Sample Post 2 - Advanced JavaScript
tags: Tech>JavaScript>Advanced, WebDev, Programming
---
This is a sample post about advanced JavaScript techniques and web development.
"""
        with open(os.path.join(posts_directory, "2023-01-02-sample-post-2.md"), "w", encoding="utf-8") as f:
            f.write(sample_post_content_2)
        
        sample_post_content_3 = """---
title: Sample Post 3 - Python for Data Science
tags:
  - Tech>Python>DataScience
  - Data Analysis
  - Programming
---
This is a sample post about using Python for Data Science.
"""
        with open(os.path.join(posts_directory, "2023-01-03-sample-post-3.md"), "w", encoding="utf-8") as f:
            f.write(sample_post_content_3)

    # Process the tags and generate the outputs
    # Pass the threshold value to process_tags
    processed_tag_data = process_tags(posts_directory, threshold=DEFAULT_THRESHOLD)
    if processed_tag_data:
        save_output(processed_tag_data, output_folders)
    else:
        logging.info("No tag data was processed. Skipping save output.")

if __name__ == '__main__':
    main()
