import requests, json, os
from requests.auth import HTTPDigestAuth
from icalendar import Calendar
from pathlib import Path

url = os.environ.get("CALENDAR_URL")
username = os.environ.get("CALENDAR_USER")
password = os.environ.get("CALENDAR_PASS")

if not all([url, username, password]):
    print("Missing CALENDAR_URL/CALENDAR_USER/CALENDAR_PASS.")
    exit(1)

try:
    r = requests.get(url, auth=HTTPDigestAuth(username, password), timeout=30)
    r.raise_for_status()
    cal = Calendar.from_ical(r.text)
    events = []
    for comp in cal.walk():
        if comp.name == "VEVENT":
            start = comp.get('DTSTART'); end = comp.get('DTEND')
            if start and end:
                events.append({
                    "title": str(comp.get('SUMMARY', 'No Title')),
                    "start": start.dt.isoformat(),
                    "end":   end.dt.isoformat()
                })
    Path("assets/data").mkdir(parents=True, exist_ok=True)
    with open("assets/data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(events)} events.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)
