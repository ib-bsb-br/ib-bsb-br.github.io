import os
import re
import yaml

POSTS_DIR = '_posts'  # Adjust if your posts are located elsewhere

for root, dirs, files in os.walk(POSTS_DIR):
    for filename in files:
        if filename.endswith('.md') or filename.endswith('.markdown'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split front matter and body
            parts = content.split('---')
            if len(parts) < 3:
                continue  # Skip files without proper front matter
            front_matter_raw = parts[1]
            body = '---'.join(parts[2:])

            front_matter = yaml.safe_load(front_matter_raw)
            body_lines = body.strip().split('\n')

            bibref_value = None
            new_body_lines = []
            for line in body_lines:
                # Use regex to match lines starting with 'bibref', optional colon, capturing the value
                match = re.match(r'^\s*[Bb]ibref\s*:?\s*(.*)', line)
                if match and bibref_value is None:
                    bibref_value = match.group(1).strip()
                else:
                    new_body_lines.append(line)

            if bibref_value:
                # Update the 'comment' field in the front matter
                front_matter['comment'] = bibref_value

                # Reconstruct the content
                new_front_matter_raw = yaml.dump(front_matter, allow_unicode=True, sort_keys=False).strip()
                new_content = f'---\n{new_front_matter_raw}\n---\n\n' + '\n'.join(new_body_lines)

                # Write the updated content back to the file
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(new_content)
