import requests
from requests.auth import HTTPDigestAuth
import json
from icalendar import Calendar
import os
from pathlib import Path

# --- CONFIGURATION ---
CENTRAL_API_URL = "https://arcreformas.com.br/api/published"
OUTPUT_FILE = Path("assets/data/published_content.json")

# iCal credentials from GitHub Actions secrets
ICAL_URL = os.getenv("ICAL_URL")
ICAL_USER = os.getenv("ICAL_USER")
ICAL_PASS = os.getenv("ICAL_PASS")

def fetch_ical_events():
    """Fetches and parses events from the iCal feed."""
    if not all([ICAL_URL, ICAL_USER, ICAL_PASS]):
        print("iCal credentials not found in environment variables. Skipping.")
        return []

    print("Fetching iCal events...")
    try:
        response = requests.get(ICAL_URL, auth=HTTPDigestAuth(ICAL_USER, ICAL_PASS), timeout=15)
        response.raise_for_status()

        calendar = Calendar.from_ical(response.text)
        events = []
        for component in calendar.walk():
            if component.name == "VEVENT":
                try:
                    event = {
                        "title": str(component.get('SUMMARY')),
                        "start": component.get('DTSTART').dt.isoformat(),
                        "end": component.get('DTEND').dt.isoformat(),
                    }
                    events.append(event)
                except Exception as e:
                    print(f"Skipping a malformed VEVENT: {e}")
        print(f"Successfully fetched {len(events)} iCal events.")
        return events
    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, 'status_code', 'Connection Error')
        print(f"Failed to access iCal feed. Status code: {status_code}")
        print(f"Error: {e}")
        return []

def fetch_published_notes():
    """Fetches published notes from the central API."""
    print("Fetching published notes from Central API...")
    try:
        response = requests.get(CENTRAL_API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        notes = data.get("tasks", [])
        print(f"Successfully fetched {len(notes)} published notes.")
        return notes
    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, 'status_code', 'Connection Error')
        print(f"Failed to access Central API. Status code: {status_code}")
        print(f"Error: {e}")
        return []
    except json.JSONDecodeError:
        print("Failed to decode JSON response from Central API.")
        return []

def main():
    """Main function to fetch all data and write to file."""

    # Create the data directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Fetch data from all sources
    ical_events = fetch_ical_events()
    published_notes = fetch_published_notes()

    # Combine into a single data structure
    combined_data = {
        "events": ical_events,
        "notes": published_notes
    }

    # Write to the output file
    print(f"Writing combined data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print("Script finished successfully.")

if __name__ == "__main__":
    main()
