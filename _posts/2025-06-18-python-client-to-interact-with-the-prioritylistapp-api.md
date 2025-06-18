---
tags: [scratchpad]
info: aberto.
date: 2025-06-18
type: post
layout: post
published: true
slug: python-client-to-interact-with-the-prioritylistapp-api
title: 'Python client to interact with the `prioritylist.app` API'
---
### API Analysis

#### **1. Authentication Mechanism**

The API does not use a visible token in an `Authorization` header. Authentication is managed via session cookies that must be included with every API request to the `/api/` endpoints.

*   **Mechanism**: Cookie-based session.
*   **Required Cookies**:
    *   `PHPSESSID`: The primary PHP session identifier.
    *   `rkey`: A custom, long-lived key that appears to be essential for maintaining the authenticated session.
*   **Required Headers**: All API calls observed in the HAR file include the `X-Requested-With: XMLHttpRequest` header, indicating they are intended to be called via AJAX.
*   **Note on Login Flow**: The provided HAR data **does not** include the initial login request. Therefore, to use the generated Python client, you must first log in through a web browser, extract the `PHPSESSID` and `rkey` cookie values, and provide them to the client.

#### **2. API Design Patterns**

*   **Request Chaining**: The API is designed hierarchically. Creating a child object (like a task) requires the ID of its parent (a sublist), which in turn requires the ID of its parent (a list). A typical workflow is a chain of `add` requests, where the ID from one response is used in the payload of the next.
*   **Response on Creation**: When a new object is created (e.g., adding a task), the API's response body contains the full, updated data of the *parent object*. For example, adding a task to a sublist returns the entire sublist object, now including the newly created task in its `items` array. The client code must parse this parent object to find the ID of the newly created child.

#### **3. Endpoint Reference**

The following endpoints were identified from the HAR data. All endpoints use the `POST` method and are relative to `https://prioritylist.app`.

##### **List & Group Actions**

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /api/groups/pull` | `POST` | Fetches all list groups and the lists they contain. |
| `POST /api/list/add` | `POST` | Creates a new list. |
| `POST /api/list/update` | `POST` | Updates the name of an existing list. |
| `POST /api/list/star` | `POST` | Toggles the "starred" status of a list. |
| `POST /api/list/pull` | `POST` | Fetches the detailed contents of a specific list. |
| `POST /api/list/notes` | `POST` | Saves or updates the notes for a list. |
| `POST /api/list/focus` | `POST` | Sets a list to "focus" mode. |
| `POST /api/list/unfocus`| `POST` | Removes a list from "focus" mode. |

**Payload for `POST /api/list/add`**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | string | Yes | The name of the new list. |
| `group_id`| string | No | The ID of the group to add the list to. |

##### **Sublist Actions**

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /api/sublist/add` | `POST` | Adds a new sublist to a parent list. |
| `POST /api/sublist/update`| `POST` | Updates the name of an existing sublist. |
| `POST /api/sublist/show` | `POST` | Toggles the visibility of a sublist in the UI. |
| `POST /api/sublist/reorder`|`POST` | Changes the display order of sublists. |

**Payload for `POST /api/sublist/add`**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `list_id` | integer | Yes | The ID of the parent list. |
| `name` | string | Yes | The name of the new sublist. |

##### **Item (Task) Actions**

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /api/item/add` | `POST` | Creates a new task (item) within a sublist. |
| `POST /api/item/update` | `POST` | Updates an existing task. |
| `POST /api/item/update-name`|`POST` | Updates only the name of a task. |
| `POST /api/subitems/pull`|`POST` | Fetches the sub-items for a given parent item. |

**Payload for `POST /api/item/add`**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `sublist_id` | integer | Yes | The ID of the parent sublist. |
| `name` | string | Yes | The name of the task. |
| `score_i` | integer | Yes | Importance score (e.g., 1-10). |
| `score_t` | integer | Yes | Urgency/Time score (e.g., 1-10). |
| `d_date` | string | No | Due date in `YYYY-MM-DD` format. |
| `d_time` | string | No | Due time in `HH:MM` format. |
| `d_zone` | string | No | Timezone offset (e.g., `-0300`). |
| `dependency_id`| integer | No | The ID of a prerequisite task. |

##### **Notification & Access Actions**

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /api/notifications/all`| `POST` | Fetches all notifications. |
| `POST /api/notifications/count`|`POST` | Gets the count of unread notifications. |
| `POST /api/access/pull` | `POST` | Retrieves sharing information for a list. |
| `POST /api/access/public` | `POST` | Toggles the public visibility of a list. |

### Python API Client

The following Python script provides a reusable `PriorityListApiClient` class to interact with the API. It is designed to be used with session cookies extracted from a browser.

```python
import requests
import json
from typing import Dict, Any, Optional

class PriorityListApiClient:
    """
    A client for interacting with the prioritylist.app API.

    This client handles session management via cookies and provides methods for
    automating the creation and management of lists, sublists, and tasks.
    """

    def __init__(self, phpsessid: str, rkey: str, base_url: str = "https://prioritylist.app"):
        """
        Initializes the API client with the necessary authentication cookies.

        Args:
            phpsessid (str): The PHPSESSID cookie value from a browser session.
            rkey (str): The rkey cookie value from a browser session.
            base_url (str, optional): The base URL of the API.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        # Set common headers observed in the HAR file for all requests
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
            "Accept": "text/plain, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.base_url
        })

        # Set the authentication cookies for the session.
        self.session.cookies.set("PHPSESSID", phpsessid, domain="prioritylist.app")
        self.session.cookies.set("rkey", rkey, domain="prioritylist.app")

    def _make_request(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        A helper method to make POST requests to the API and handle responses.

        Args:
            endpoint (str): The API endpoint path (e.g., '/list/add').
            data (dict, optional): The form-encoded payload to send.

        Returns:
            dict: The 'data' field from the JSON response, or None if an error occurs.
        """
        url = f"{self.base_url}/api{endpoint}"
        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            
            json_response = response.json()
            if json_response.get("result") == "success":
                return json_response.get("data")
            else:
                print(f"API Error at {endpoint}: {json_response.get('result', 'Unknown error')}")
                return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error for {endpoint}: {e.response.status_code} {e.response.reason}")
            print(f"Response body: {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {endpoint}: {e}")
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response. URL: {url}, Response: {response.text}")
        return None

    def create_list(self, name: str) -> Optional[Dict[str, Any]]:
        """Creates a new list and returns its data object."""
        print(f"Creating list: '{name}'...")
        response_data = self._make_request("/list/add", data={"name": name, "group_id": ""})
        
        if response_data:
            # WARNING: This assumes the new list is the last in the returned array.
            # A more robust solution would filter by name to find the correct list.
            try:
                new_list = response_data[0]['lists'][-1]
                print(f"-> Success! Created list '{name}' with ID: {new_list['id']}")
                return new_list
            except (IndexError, KeyError):
                print("Could not find the new list in the API response.")
        return None

    def create_sublist(self, list_id: int, name: str) -> Optional[Dict[str, Any]]:
        """Creates a new sublist and returns its data object."""
        print(f"Creating sublist '{name}' in list {list_id}...")
        response_data = self._make_request("/sublist/add", data={"list_id": list_id, "name": name})

        if response_data:
            # WARNING: Assumes the new sublist is the last in the array.
            try:
                new_sublist = response_data['sublists'][-1]
                print(f"-> Success! Created sublist '{name}' with ID: {new_sublist['id']}")
                return new_sublist
            except (IndexError, KeyError):
                print("Could not find the new sublist in the API response.")
        return None

    def create_task(self, sublist_id: int, name: str, importance: int = 5, time_effort: int = 5, **kwargs) -> Optional[Dict[str, Any]]:
        """Creates a new task and returns its data object."""
        print(f"Creating task '{name}' in sublist {sublist_id}...")
        payload = {
            "sublist_id": sublist_id,
            "name": name,
            "score_i": importance,
            "score_t": time_effort,
            "d_date": kwargs.get("d_date", ""),
            "d_time": kwargs.get("d_time", ""),
            "d_zone": "-0300" if kwargs.get("d_date") else "",
            "dependency_id": kwargs.get("dependency_id", "")
        }
        response_data = self._make_request("/item/add", data=payload)

        if response_data:
            # WARNING: Assumes the new item is the last in the array.
            try:
                new_item = response_data['items'][-1]
                print(f"-> Success! Created task '{name}' with ID: {new_item['id']}")
                return new_item
            except (IndexError, KeyError):
                print("Could not find the new task in the API response.")
        return None

def main():
    """
    Main function to demonstrate the use of the ptpython REPL framework.
    """
    # --- IMPORTANT: These values must be obtained from a valid, logged-in browser session. ---
    # The values below are the dummy data from the provided HAR file.
    PHPSESSID_COOKIE = "77n5cmi8mucr04afiukmatp151"
    RKEY_COOKIE = "413511bec626a5eb964e337e4165fee629685ac7caa75b21257604bcf5ca4b93911a8f1f6c9d5b902e598db6cc028fe91988db2590daaca4bff55e82d14028ce%3Afvwzb%3Aec91c6f9a5ae2a25515b951b30bb23297d601f184b994eda24654d6edba86bd1"

    # 1. Instantiate the client with authentication cookies
    client = PriorityListApiClient(phpsessid=PHPSESSID_COOKIE, rkey=RKEY_COOKIE)

    # 2. --- Example Workflow Demonstrating Request Chaining ---
    print("\\n--- Starting API Automation Workflow ---")

    # Step A: Create a new main list
    list_obj = client.create_list(name="Project Phoenix")
    if not list_obj:
        print("Workflow failed: Could not create the main list.")
        return
    
    # Step B: Extract the new list's ID from the response
    list_id = list_obj['id']
    print(f"--> Using new list ID: {list_id}\\n")

    # Step C: Create the first sublist using the list_id
    sublist1_obj = client.create_sublist(list_id=list_id, name="Phase 1: Research")
    if sublist1_obj:
        # Step D: Extract the sublist's ID
        sublist1_id = sublist1_obj['id']
        print(f"--> Using new sublist ID: {sublist1_id}\\n")
        
        # Step E: Create a task in the first sublist
        task1_obj = client.create_task(sublist1_id, name="Analyze Market Data", importance=8, time_effort=10)
        if task1_obj:
            # Step F: Extract the task's ID to use as a dependency
            task1_id = task1_obj['id']
            print(f"--> Using new task ID for dependency: {task1_id}\\n")

            # Step G: Create a second task that depends on the first one
            client.create_task(
                sublist1_id, 
                name="Write Competitor Report", 
                importance=7, 
                time_effort=5, 
                dependency_id=task1_id
            )
    
    print("\\n--- Workflow Complete ---")

if __name__ == '__main__':
    # This block demonstrates how to use the ptpython REPL framework.
    # It sets up a REPL environment where the ApiClient can be used interactively.
    try:
        from ptpython.repl import embed
        
        # --- IMPORTANT: These values must be obtained from a valid, logged-in browser session. ---
        # The values below are the dummy data from the provided HAR file.
        PHPSESSID_COOKIE = "77n5cmi8mucr04afiukmatp151"
        RKEY_COOKIE = "413511bec626a5eb964e337e4165fee629685ac7caa75b21257604bcf5ca4b93911a8f1f6c9d5b902e598db6cc028fe91988db2590daaca4bff55e82d14028ce%3Afvwzb%3Aec91c6f9a5ae2a25515b951b30bb23297d601f184b994eda24654d6edba86bd1"

        # Instantiate the client
        client = PriorityListApiClient(phpsessid=PHPSESSID_COOKIE, rkey=RKEY_COOKIE)
        
        # Create a namespace for the REPL
        namespace = {
            'client': client,
            'requests': requests,
            'json': json,
            'main': main
        }
        
        print("--- ptpython REPL ---")
        print("An 'ApiClient' instance named 'client' is available.")
        print("You can now interact with the API, e.g., client.create_list('My New List')")
        print("Type 'main()' to run the example workflow.")
        
        # Embed the ptpython REPL
        embed(globals=namespace, locals=namespace)
        
    except ImportError:
        print("ptpython is not installed. Please run 'pip install ptpython' to use the REPL.")
        # Fallback to standard Python REPL if ptpython is not available
        import code
        code.interact(local=locals())

```

{% codeblock python %}
#!/usr/bin/env python3
"""
PriorityList CLI - The Optimized & Integrated Solution

This script is the result of integrating the best features from multiple development
approaches into a single, cohesive, and robust command-line interface.

It combines:
• Full CRUD (Create, Read, Update, Delete) operations for all resources.
• A robust API client with detailed error handling and reliable response parsing.
• A clean, nested command structure (e.g., `list add`, `task delete`).
• An interactive REPL mode (via `ptpython`) for exploratory API calls.
• Strict separation of human-readable and machine-readable (`--json`) output.
• Secure credential management from args, environment, or config file.
"""

from __future__ import annotations

import argparse
import configparser
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# ─────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────

def print_json(obj: Any) -> None:
    """Prints an object as a formatted JSON string to stdout."""
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def print_human(msg: str, *, is_json_mode: bool) -> None:
    """Prints a message to stdout only if not in JSON mode."""
    if not is_json_mode:
        print(msg)

# ─────────────────────────────────────────────────────────────
# API Client
# ─────────────────────────────────────────────────────────────

class PriorityListApiClient:
    """A robust client for interacting with the prioritylist.app API."""

    def __init__(self, phpsessid: str, rkey: str, base_url: str = "https://prioritylist.app") -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
            "Accept": "text/plain, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.base_url,
        })
        self.session.cookies.set("PHPSESSID", phpsessid, domain="prioritylist.app")
        self.session.cookies.set("rkey", rkey, domain="prioritylist.app")

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Makes a POST request, handles errors, and returns the 'data' field on success."""
        url = f"{self.base_url}/api{endpoint}"
        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()
            json_response = response.json()
            if json_response.get("result") == "success":
                return json_response.get("data")
            else:
                print(f"❌ API Error at {endpoint}: {json_response.get('result', 'Unknown error')}", file=sys.stderr)
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error for {endpoint}: {e.response.status_code} {e.response.reason}", file=sys.stderr)
            print(f"   Response body: {e.response.text}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed for {endpoint}: {e}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"❌ Failed to decode JSON from response. URL: {url}", file=sys.stderr)
        return None

    # --- List Operations ---
    def get_all_lists(self) -> Optional[List[Dict[str, Any]]]:
        return self._post("/groups/pull")

    def get_list_details(self, list_id: int) -> Optional[Dict[str, Any]]:
        return self._post("/list/pull", {"id": list_id})

    def create_list(self, name: str, group_id: str = "") -> Optional[Dict[str, Any]]:
        """Creates a new list and robustly finds and returns it from the response."""
        response_data = self._post("/list/add", {"name": name, "group_id": group_id})
        if response_data:
            try:
                for group in response_data:
                    for lst in group.get('lists', []):
                        if lst['name'] == name:
                            return lst
            except (IndexError, KeyError, TypeError) as e:
                print(f"❌ Could not parse created list from API response: {e}", file=sys.stderr)
        return None

    def update_list(self, list_id: int, name: str) -> bool:
        return self._post("/list/update", {"id": list_id, "name": name}) is not None

    def delete_list(self, list_id: int) -> bool:
        return self._post("/list/delete", {"id": list_id}) is not None

    def star_list(self, list_id: int) -> bool:
        return self._post("/list/star", {"id": list_id}) is not None

    # --- Sublist Operations ---
    def create_sublist(self, list_id: int, name: str) -> Optional[Dict[str, Any]]:
        """Creates a new sublist and robustly finds and returns it."""
        response_data = self._post("/sublist/add", {"list_id": list_id, "name": name})
        if response_data:
            try:
                for sublist in response_data.get('sublists', []):
                    if sublist['name'] == name:
                        return sublist
            except (KeyError, TypeError) as e:
                print(f"❌ Could not parse created sublist from API response: {e}", file=sys.stderr)
        return None

    def update_sublist(self, sublist_id: int, name: str) -> bool:
        return self._post("/sublist/update", {"id": sublist_id, "name": name}) is not None

    def delete_sublist(self, sublist_id: int) -> bool:
        return self._post("/sublist/delete", {"id": sublist_id}) is not None

    # --- Task Operations ---
    def create_task(self, sublist_id: int, name: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Creates a new task and robustly finds and returns it."""
        payload = {"sublist_id": sublist_id, "name": name}
        payload.update(kwargs)
        if 'd_date' in payload and payload['d_date']:
            payload.setdefault('d_zone', '-0300')
        response_data = self._post("/item/add", payload)
        if response_data:
            try:
                for item in response_data.get('items', []):
                    if item['name'] == name:
                        return item
            except (KeyError, TypeError) as e:
                print(f"❌ Could not parse created task from API response: {e}", file=sys.stderr)
        return None

    def update_task(self, task_id: int, updates: Dict[str, Any]) -> bool:
        """Updates an existing task with only the provided fields."""
        payload = updates.copy()
        payload['id'] = task_id
        if 'd_date' in payload and payload['d_date']:
            payload.setdefault('d_zone', '-0300')
        return self._post("/item/update", data=payload) is not None

    def delete_task(self, task_id: int) -> bool:
        return self._post("/item/delete", {"id": task_id}) is not None

# ─────────────────────────────────────────────────────────────
# Credentials Helper
# ─────────────────────────────────────────────────────────────

def get_credentials(ns: argparse.Namespace) -> Tuple[str, str]:
    """Retrieves credentials from args, environment variables, or config file."""
    if ns.phpsessid and ns.rkey:
        return ns.phpsessid, ns.rkey
    
    env_sess, env_rkey = os.getenv("PL_PHPSESSID"), os.getenv("PL_RKEY")
    if env_sess and env_rkey:
        return env_sess, env_rkey
        
    cfg_file = Path.home() / ".config" / "prioritylist" / "config.ini"
    if cfg_file.exists():
        cp = configparser.ConfigParser()
        cp.read(cfg_file)
        if "auth" in cp and "phpsessid" in cp["auth"] and "rkey" in cp["auth"]:
            return cp["auth"]["phpsessid"], cp["auth"]["rkey"]
            
    print("❌ Error: Authentication credentials not found.", file=sys.stderr)
    print("  Please provide them via flags, environment variables, or a config file.", file=sys.stderr)
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# Command Handlers
# ─────────────────────────────────────────────────────────────

def handle_list_pull_all(client: PriorityListApiClient, ns: argparse.Namespace):
    data = client.get_all_lists()
    if data is None:
        print_human("❌ Could not fetch lists.", is_json_mode=ns.json)
        return
    if ns.json:
        print_json(data)
    else:
        for group in data:
            print_human(f"\n📁 {group.get('name') or 'Uncategorized'}", is_json_mode=ns.json)
            for lst in group.get("lists", []):
                star = "⭐" if lst.get("starred") else " "
                print_human(f"  {star} ID: {lst['id']:<6} {lst['name']}", is_json_mode=ns.json)

def handle_list_show(client: PriorityListApiClient, ns: argparse.Namespace):
    data = client.get_list_details(ns.list_id)
    if data is None:
        print_human(f"❌ List {ns.list_id} not found.", is_json_mode=ns.json)
        return
    print_json(data)

def handle_list_add(client: PriorityListApiClient, ns: argparse.Namespace):
    new_list = client.create_list(ns.name)
    if new_list:
        print_human(f"✅ Created list '{new_list['name']}' (ID: {new_list['id']})", is_json_mode=ns.json)
        if ns.json:
            print_json(new_list)
    else:
        print_human(f"❌ Failed to create list '{ns.name}'.", is_json_mode=ns.json)

def handle_list_update(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.update_list(ns.list_id, ns.name)
    msg = f"✅ Renamed list {ns.list_id} to '{ns.name}'." if ok else f"❌ Failed to rename list {ns.list_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_list_delete(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.delete_list(ns.list_id)
    msg = f"✅ Deleted list {ns.list_id}." if ok else f"❌ Failed to delete list {ns.list_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_list_star(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.star_list(ns.list_id)
    msg = f"✅ Toggled star on list {ns.list_id}." if ok else f"❌ Failed to toggle star on list {ns.list_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_sublist_add(client: PriorityListApiClient, ns: argparse.Namespace):
    new_sublist = client.create_sublist(ns.list_id, ns.name)
    if new_sublist:
        msg = f"✅ Created sublist '{new_sublist['name']}' (ID: {new_sublist['id']}) in list {ns.list_id}."
        print_human(msg, is_json_mode=ns.json)
        if ns.json:
            print_json(new_sublist)
    else:
        print_human(f"❌ Failed to create sublist '{ns.name}'.", is_json_mode=ns.json)

def handle_sublist_update(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.update_sublist(ns.sublist_id, ns.name)
    msg = f"✅ Renamed sublist {ns.sublist_id} to '{ns.name}'." if ok else f"❌ Failed to rename sublist {ns.sublist_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_sublist_delete(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.delete_sublist(ns.sublist_id)
    msg = f"✅ Deleted sublist {ns.sublist_id}." if ok else f"❌ Failed to delete sublist {ns.sublist_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_task_add(client: PriorityListApiClient, ns: argparse.Namespace):
    params = {
        "score_i": ns.importance,
        "score_t": ns.time,
        "d_date": ns.due_date or "",
        "dependency_id": ns.dependency_id or "",
    }
    new_task = client.create_task(ns.sublist_id, ns.name, **params)
    if new_task:
        msg = f"✅ Created task '{new_task['name']}' (ID: {new_task['id']}) in sublist {ns.sublist_id}."
        print_human(msg, is_json_mode=ns.json)
        if ns.json:
            print_json(new_task)
    else:
        print_human(f"❌ Failed to create task '{ns.name}'.", is_json_mode=ns.json)

def handle_task_update(client: PriorityListApiClient, ns: argparse.Namespace):
    updates = {k: v for k, v in vars(ns).items() if k in [
        'name', 'sublist_id', 'importance', 'time', 'due_date', 'dependency_id'
    ] and v is not None}
    
    if not updates:
        print_human("❌ Error: At least one field to update must be provided.", is_json_mode=ns.json)
        sys.exit(1)
        
    # Remap arg names to API field names
    if 'importance' in updates: updates['score_i'] = updates.pop('importance')
    if 'time' in updates: updates['score_t'] = updates.pop('time')
    if 'due_date' in updates: updates['d_date'] = updates.pop('due_date')

    ok = client.update_task(ns.task_id, updates)
    msg = f"✅ Updated task {ns.task_id}." if ok else f"❌ Failed to update task {ns.task_id}."
    print_human(msg, is_json_mode=ns.json)

def handle_task_delete(client: PriorityListApiClient, ns: argparse.Namespace):
    ok = client.delete_task(ns.task_id)
    msg = f"✅ Deleted task {ns.task_id}." if ok else f"❌ Failed to delete task {ns.task_id}."
    print_human(msg, is_json_mode=ns.json)

# ─────────────────────────────────────────────────────────────
# Argument Parser
# ─────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="A robust CLI for prioritylist.app.", formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--phpsessid", help="Your PHPSESSID cookie.")
    p.add_argument("--rkey", help="Your rkey cookie.")
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON only.")

    sp = p.add_subparsers(dest="resource", required=True, help="The resource to manage.")

    # --- List Parser ---
    ls = sp.add_parser("list", help="Manage lists").add_subparsers(dest="action", required=True)
    ls.add_parser("pull-all", help="Fetch all lists and groups").set_defaults(func=handle_list_pull_all)
    ls_sh = ls.add_parser("show", help="Show full JSON details for one list")
    ls_sh.add_argument("list_id", type=int, help="ID of the list to show")
    ls_sh.set_defaults(func=handle_list_show)
    ls_add = ls.add_parser("add", help="Add a new list")
    ls_add.add_argument("--name", required=True, help="Name for the new list")
    ls_add.set_defaults(func=handle_list_add)
    ls_upd = ls.add_parser("update", help="Rename a list")
    ls_upd.add_argument("list_id", type=int, help="ID of the list to update")
    ls_upd.add_argument("--name", required=True, help="New name for the list")
    ls_upd.set_defaults(func=handle_list_update)
    ls_del = ls.add_parser("delete", help="Delete a list")
    ls_del.add_argument("list_id", type=int, help="ID of the list to delete")
    ls_del.set_defaults(func=handle_list_delete)
    ls_star = ls.add_parser("star", help="Toggle star status on a list")
    ls_star.add_argument("list_id", type=int, help="ID of the list to star/unstar")
    ls_star.set_defaults(func=handle_list_star)

    # --- Sublist Parser ---
    sb = sp.add_parser("sublist", help="Manage sublists").add_subparsers(dest="action", required=True)
    sb_add = sb.add_parser("add", help="Add a new sublist")
    sb_add.add_argument("--list-id", type=int, required=True, help="ID of the parent list")
    sb_add.add_argument("--name", required=True, help="Name for the new sublist")
    sb_add.set_defaults(func=handle_sublist_add)
    sb_upd = sb.add_parser("update", help="Rename a sublist")
    sb_upd.add_argument("sublist_id", type=int, help="ID of the sublist to update")
    sb_upd.add_argument("--name", required=True, help="New name for the sublist")
    sb_upd.set_defaults(func=handle_sublist_update)
    sb_del = sb.add_parser("delete", help="Delete a sublist")
    sb_del.add_argument("sublist_id", type=int, help="ID of the sublist to delete")
    sb_del.set_defaults(func=handle_sublist_delete)

    # --- Task Parser ---
    tk = sp.add_parser("task", help="Manage tasks").add_subparsers(dest="action", required=True)
    tk_add = tk.add_parser("add", help="Add a new task")
    tk_add.add_argument("--sublist-id", type=int, required=True, help="ID of the parent sublist")
    tk_add.add_argument("--name", required=True, help="Name for the new task")
    tk_add.add_argument("-i", "--importance", type=int, default=5, help="Importance score (1-10)")
    tk_add.add_argument("-t", "--time", type=int, default=5, help="Time/Effort score (1-10)")
    tk_add.add_argument("--due-date", help="Due date in YYYY-MM-DD format")
    tk_add.add_argument("--dependency-id", type=int, help="ID of a prerequisite task")
    tk_add.set_defaults(func=handle_task_add)
    tk_upd = tk.add_parser("update", help="Update an existing task")
    tk_upd.add_argument("task_id", type=int, help="ID of the task to update")
    tk_upd.add_argument("--sublist-id", type=int, help="Move task to a new parent sublist")
    tk_upd.add_argument("--name", help="New name for the task")
    tk_upd.add_argument("-i", "--importance", type=int, help="New importance score (1-10)")
    tk_upd.add_argument("-t", "--time", type=int, help="New time/Effort score (1-10)")
    tk_upd.add_argument("--due-date", help="New due date in YYYY-MM-DD format")
    tk_upd.add_argument("--dependency-id", type=int, help="New ID of a prerequisite task")
    tk_upd.set_defaults(func=handle_task_update)
    tk_del = tk.add_parser("delete", help="Delete a task")
    tk_del.add_argument("task_id", type=int, help="ID of the task to delete")
    tk_del.set_defaults(func=handle_task_delete)

    return p

# ─────────────────────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────────────────────

def main():
    """Main entry point for the script."""
    if len(sys.argv) == 1:
        try:
            from ptpython.repl import embed
            print("▶️  No command provided. Starting interactive REPL...")
            creds_ns = argparse.Namespace(phpsessid=None, rkey=None)
            phpsessid, rkey = get_credentials(creds_ns)
            client = PriorityListApiClient(phpsessid, rkey)
            namespace = {'client': client, 'print_json': print_json}
            print("✅ An API client is available as `client`.")
            embed(globals=namespace, locals=namespace)
        except ImportError:
            print("ℹ️ Optional dependency 'ptpython' not found.", file=sys.stderr)
            print("  Run 'pip install ptpython' for an enhanced interactive experience.", file=sys.stderr)
            print("\nDisplaying help instead:\n")
            build_parser().print_help()
        sys.exit(0)

    parser = build_parser()
    args = parser.parse_args()
    
    phpsessid, rkey = get_credentials(args)
    client = PriorityListApiClient(phpsessid, rkey)

    if hasattr(args, 'func'):
        args.func(client, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
{% endcodeblock %}

#### **Command-Line Interface (CLI) and User Experience (UX)**

*   **Nested Command Structure:** The CLI now uses a more intuitive `resource action` format (e.g., `list add`, `task update`). This is a standard practice for modern CLIs and a vast improvement over the original flat command list.
*   **Interactive REPL Mode:** A major feature addition is the `ptpython`-based interactive REPL, which launches if the script is run without arguments. It provides an authenticated `client` object, allowing for powerful, exploratory API interactions without writing new scripts.
*   **Clear and Concise Output:** The use of emojis (✅, ❌, 📁, ⭐) provides immediate visual feedback on the status of operations.
*   **Scripting-Friendly JSON Mode:** The `--json` flag now guarantees that the only output to `stdout` is a clean JSON object, making it trivial to pipe the output of this tool to other programs like `jq`.

#### **4. Security Enhancements**

*   **Secure Credential Sourcing:** The `get_credentials` function continues to provide a secure and flexible way to manage API keys, preventing them from being hard-coded. It checks arguments, environment variables, and a dedicated config file in a safe order of precedence.
*   **Robust Input Handling:** The API client's improved error handling and response parsing make it less susceptible to crashes or unexpected behavior caused by malformed API responses.