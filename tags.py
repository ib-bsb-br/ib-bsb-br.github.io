import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union, Any
import json
import argparse
from typing import Set, Tuple
THRESHOLD = 1


def extract_frontmatter(file_content: str) -> str:
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ''
    content_lines = file_content.split('\n')
    if content_lines[0].strip() == '---':
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n'.join(content_lines[1:i])
                break
    return frontmatter


def generate_partial_tags(tag: str) -> List[str]:
    """Generates all partial tags for a given tag."""
    parts = tag.split('>')
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append('>'.join(parts[j:j + i]))
    return partial_tags


class JsonOutputHandler:
    

def write(self, data: dict, json_output_file: str):
        """Writes the tag data to a JSON file."""
        

def convert_data(obj):
            if isinstance(obj, (set, frozenset)):
                return sorted(list(obj))
            elif isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=convert_data, sort_keys=True)
        logging.info(f'Tag data has been written to {json_output_file}')


def generate_mermaid_graph(tag_data: Union[List[Dict[str, Any]], Dict[str, Any]], direction: str='TD') -> str:
    """Generates Mermaid ER diagram code for the tag structure."""
    graph = ['erDiagram']
    added_nodes = set()
    added_edges = set()
    

def sanitize_tag(tag: str) -> str:
        """Sanitize the tag name for use in Mermaid syntax."""
        return tag.replace('>', '_').replace(' ', '_').replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('à', 'a').replace('â', 'a').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('í', 'i').replace('ì', 'i').replace('î', 'i').replace('ó', 'o').replace('ò', 'o').replace('ô', 'o').replace('õ', 'o').replace('ú', 'u').replace('ù', 'u').replace('û', 'u').replace('ü', 'u')
    

def add_node(tag: str, data: Dict[str, Any]) -> str:
        """Adds a node (entity) to the graph if it hasn't been added yet."""
        safe_tag = sanitize_tag(tag)
        if safe_tag not in added_nodes:
            node_

def = f'    {safe_tag} {{'
            graph.append(node_def)
            for parent in data.get('parents', []):
                graph.append(f'        parent {sanitize_tag(parent)}')
            for child in data.get('children', []):
                graph.append(f'        child {sanitize_tag(child)}')
            for related, count in data.get('related', {}).items():
                graph.append(f'        related_{count} {sanitize_tag(related)}')
            graph.append('    }')
            added_nodes.add(safe_tag)
        return safe_tag
    for tag in sorted(tag_data.keys()):
        data = tag_data[tag]
        safe_tag = add_node(tag, data)
        for parent in data.get('parents', []):
            safe_parent = add_node(parent, tag_data[parent])
            edge = f'    {safe_parent} ||--|| {safe_tag} : SUBSET_OF'
            if edge not in added_edges:
                graph.append(edge)
                added_edges.add(edge)
        for child in data.get('children', []):
            safe_child = add_node(child, tag_data[child])
            edge = f'    {safe_tag} ||--|| {safe_child} : SUBSET_OF'
            if edge not in added_edges:
                graph.append(edge)
                added_edges.add(edge)
    return '\n'.join(graph)


def process_tags(posts_dir: str) -> tuple[Dict[str, Any], List[str]]:
   """
   Processes tags from markdown files, handling nested tags, highlighting exact matches,
   preventing duplicates using file paths, and generating a Mermaid graph.
   Ensures all outputs are deterministically ordered.
   """
   tag_frequency = defaultdict(int)
   all_posts = []
   seen_posts = set()
   logging.info(f"Processing markdown files in directory: {posts_dir}")
   for filename in os.listdir(posts_dir):
       if not filename.endswith(".md"):
          continue
       file_path = os.path.join(posts_dir, filename)
       if file_path in seen_posts:
          logging.warning(f"Skipping duplicate post: {filename}")
          continue
       seen_posts.add(file_path)
       with open(file_path, "r", encoding="utf-8") as f:
          file_content = f.read()
       frontmatter_str = extract_frontmatter(file_content) # Renamed to avoid conflict
       if not frontmatter_str:
          logging.warning(f"No frontmatter found in {filename}")
          continue
       try:
          post_data = yaml.safe_load(frontmatter_str)
       except yaml.YAMLError as e:
          logging.error(f"Error parsing frontmatter in {filename}: {e}")
          continue
       tags = post_data.get("tags", [])
       if isinstance(tags, str):
          tags = [tag.strip() for tag in tags.split(",")]
       elif not isinstance(tags, list):
          tags = [str(tags)]
       for tag in tags:
          for partial_tag in generate_partial_tags(tag):
              tag_frequency[partial_tag] += 1
       title = post_data.get("title", os.path.splitext(filename)[0])
       url = "/" + "-".join(filename.split("-")[3:]).replace(".md", "")
       try:
          post_date = datetime.strptime("-".join(filename.split("-")[:3]), "%Y-%m-%d")
       except ValueError:
          logging.warning(f"Unable to parse date from filename {filename}")
          post_date = datetime.min # Or handle as per your needs
       all_posts.append({"title": title, "url": url, "date": post_date, "tags": tags})
   tag_data_intermediate = defaultdict( # Renamed to avoid confusion
       lambda: {"parents": set(), "children": set(), "related": defaultdict(int), "posts": []}
   )
   combined_tags_set = set()
   for post in all_posts:
       for tag in post["tags"]:
          tag_parts = tag.split(">")
          # full_tag_path = tag # This variable was defined but not used in a way that affects the following logic directly
          if len(tag_parts) > 1:
              combined_tags_set.add(tag)
              # Original logic for parents/children based on full tag if it's combined
              # Example: if "A>B>C" is a tag, "A>B" is parent of "A>B>C", "A" is parent of "A>B>C"
              # This part of the original logic might need careful review if it was complex.
              # The provided diff focused on sorting existing sets.
              # For simplicity, let's assume the original parent/child logic for combined tags was:
              for i in range(len(tag_parts) -1): # Corrected loop range
                 parent_of_combined = ">".join(tag_parts[:i+1])
                 # This seems to be what the original script intended for combined tags.
                 # The user's original script had:
                 # tag_data[tag]["parents"].add(tag_parts[i])
                 # tag_data[tag_parts[i]]["children"].add(tag)
                 # This implies 'tag' (full_tag_path) gets parents like 'A', 'B' if tag is 'A>B>C'
                 # And 'A' gets 'A>B>C' as a child, 'B' gets 'A>B>C' as child.
                 # Let's stick to the user's original logic for populating these sets first.
                 if i < len(tag_parts) -1: # ensure we don't create self-parent
                     current_parent_segment = tag_parts[i]
                     tag_data_intermediate[tag]["parents"].add(current_parent_segment)
                     tag_data_intermediate[current_parent_segment]["children"].add(tag)
          for partial_tag in generate_partial_tags(tag):
              if tag_frequency[partial_tag] >= THRESHOLD:
                 post_entry = {
                     "title": post["title"], "url": post["url"],
                     "highlighted": partial_tag == tag, "date": post["date"],
                 }
                 tag_data_intermediate[partial_tag]["posts"].append(post_entry)
          # Original parent-child relationship logic from the script
          for i in range(1, len(tag_parts)):
              parent_tag = ">".join(tag_parts[:i])
              # The child_tag in the original script was ">".join(tag_parts[i:]), which is not what's usually meant by child in this context.
              # It should be the full tag if parent_tag is a prefix. Or, the current segment.
              # Let's assume 'child_tag' here refers to the 'tag' itself relative to its 'parent_tag' prefix.
              # The original logic was:
              # child_tag_original_logic = ">".join(tag_parts[i:]) # This seems problematic
              # For a tag "A>B>C":
              # i=1: parent="A", child_original_logic="B>C"
              # i=2: parent="A>B", child_original_logic="C"
              # This creates relationships like A -> B>C and A>B -> C.
              # And also A -> A>B and A>B -> A>B>C via the combined_tags logic.
              # This area might need semantic clarification in the original script's intent.
              # For now, replicating the provided script's structure:
              child_segment_for_parent = ">".join(tag_parts[i:]) # As per original script's structure
              if (
                 tag_frequency[parent_tag] >= THRESHOLD
                 and tag_frequency[child_segment_for_parent] >= THRESHOLD # This check might be on 'tag' itself
              ):
                 tag_data_intermediate[child_segment_for_parent]["parents"].add(parent_tag)
                 tag_data_intermediate[parent_tag]["children"].add(child_segment_for_parent)
          for other_tag in post["tags"]:
              if (
                 other_tag != tag
                 and tag_frequency[other_tag] >= THRESHOLD
                 and tag_frequency[tag] >= THRESHOLD # Check full_tag_path (which is 'tag')
                 and other_tag not in tag_data_intermediate[tag]["parents"]
                 and other_tag not in tag_data_intermediate[tag]["children"]
              ):
                 tag_data_intermediate[tag]["related"][other_tag] += 1
                 tag_data_intermediate[other_tag]["related"][tag] += 1
   # Remove tags with no posts
   tag_data_filtered = {
       tag_key: data for tag_key, data in tag_data_intermediate.items() if data["posts"]
   }
   # Sort posts within each tag by date (most recent first) - this was already in original
   # And clean up relationships, now with sorting
   final_tag_data = {}
   for tag_key in sorted(list(tag_data_filtered.keys())): # Iterate sorted keys for final dict
       data = tag_data_filtered[tag_key]
       # Sort posts
       data["posts"] = sorted(
          data["posts"], key=lambda x: x.get("date", datetime.min), reverse=True
       )
       # Clean and sort parents, children, related
       current_parents = {p for p in data["parents"] if p in tag_data_filtered}
       data["parents"] = sorted(list(current_parents))
       current_children = {c for c in data["children"] if c in tag_data_filtered}
       data["children"] = sorted(list(current_children))
       current_related = {
          r: count for r, count in data["related"].items() if r in tag_data_filtered
       }
       data["related"] = {k: current_related[k] for k in sorted(current_related.keys())}
       final_tag_data[tag_key] = data
   sorted_combined_tags = sorted(list(combined_tags_set))
   return final_tag_data, sorted_combined_tags


def save_output(output_data: Dict[str, Any], output_dir: str, combined_tags_sorted: List[str]):
   """Saves YAML, JSON, and Mermaid graph outputs to a single, canonical directory."""
   # output_dir is now a single string argument
   os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists
   yaml_file = os.path.join(output_dir, 'processed_tags.yml')
   json_file = os.path.join(output_dir, 'processed_tags.json')
   mermaid_file = os.path.join(output_dir, 'tag_graph.mmd') # Changed extension
   # Save YAML
   logging.info(f"Saving YAML data to {yaml_file}")
   with open(yaml_file, 'w', encoding='utf-8') as f: # Added encoding
       yaml.dump(
          output_data, 
          f, 
          allow_unicode=True, 
          sort_keys=True,        # Added
          default_flow_style=False # Added for readability
       )
   logging.info(f"YAML data saved to {yaml_file}")
   # Save JSON
   logging.info(f"Saving JSON data to {json_file}")
   json_handler = JsonOutputHandler() 
   json_handler.write(output_data, json_file)
   # Generate and save Mermaid graph
   logging.info(f"Generating Mermaid graph for {mermaid_file}")
   mermaid_graph = generate_mermaid_graph(output_data) 
   with open(mermaid_file, 'w', encoding='utf-8') as f: # Added encoding
       f.write(mermaid_graph)
   logging.info(f"Mermaid graph saved to {mermaid_file}")
   # Optional: Save sorted combined_tags if needed
   # combined_tags_list_file = os.path.join(output_dir, 'combined_tags_sorted.txt')
   # logging.info(f"Saving sorted combined tags to {combined_tags_list_file}")
   # with open(combined_tags_list_file, 'w', encoding='utf-8') as f:
   #     for tag in combined_tags_sorted:
   #        f.write(tag + '\n')
   # logging.info(f"Sorted combined tags saved to {combined_tags_list_file}")


def main():
   parser = argparse.ArgumentParser(
       description="Processes tags from markdown files and generates YAML, JSON, and Mermaid graph outputs."
   )
   parser.add_argument(
       "--posts_dir",
       default="_posts",
       help="Directory containing markdown posts (default: %(default)s)",
   )
   parser.add_argument(
       "--output_dir",
       default="assets/data",
       help="Directory to save processed tag files (default: %(default)s)",
   )
   parser.add_argument(
       "--threshold",
       type=int,
       default=1, # Default from original script
       help="Minimum frequency for a tag to be processed (default: %(default)s)",
   )
   args = parser.parse_args()
   # Make THRESHOLD accessible to process_tags, either by passing or setting global
   # For this refactor, we'll update the global THRESHOLD.
   # Ensure THRESHOLD is defined globally in the script if it's not already.
   global THRESHOLD
   THRESHOLD = args.threshold
   logging.info(f"Using tag frequency threshold: {THRESHOLD}")
   tag_data_processed, combined_tags_list = process_tags(args.posts_dir)
   save_output(tag_data_processed, args.output_dir, combined_tags_list)
if __name__ == "__main__":
   main()
