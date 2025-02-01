---

tags: [scripts>python]
info: aberto.
date: 2024-12-30
type: post
layout: post
published: true
slug: sort-json-data-based-on-datetime
title: 'Sort JSON data based on datetime'
---
{% codeblock python %}
import json
from datetime import datetime

def sort_json_by_datetime(json_data):
    """
    Sorts a list of JSON objects based on their datetime information.

    Args:
        json_data: A list of JSON objects, each containing a "content" field
                   with datetime information and potentially a "children" field
                   for nested objects.

    Returns:
        A new list of JSON objects sorted by datetime.
    """

    def extract_datetime(item):
        """
        Extracts the datetime string from the "content" field of a JSON object,
        parses it into a datetime object, and handles potential errors.
        """
        content = item["content"]
        parts = content.split("```\n")  # Split by "```\n"
        if len(parts) > 1:
            datetime_str = parts[1].strip() # Get the part after the delimiter
            try:
                datetime_obj = datetime.strptime(datetime_str, "%d/%m/%y, %H:%M")
                return datetime_obj
            except ValueError:
                return datetime.min
        else:
            return datetime.min # Handle cases where delimiter is not found.

    def sort_recursive(data):
        """
        Recursively sorts the list and its children based on datetime,
        handling errors gracefully.
        """
        # Sort the current level using the extracted datetime or datetime.min for errors
        sorted_data = sorted(data, key=lambda item: extract_datetime(item))

        # Recursively sort children
        for item in sorted_data:
            if "children" in item and item["children"]:
                item["children"] = sort_recursive(item["children"])

        return sorted_data

    return sort_recursive(json_data)

# Example Usage (assuming json_data is already loaded)
# sorted_data = sort_json_by_datetime(json_data)
# print(json.dumps(sorted_data, indent=2))
{% endcodeblock %}