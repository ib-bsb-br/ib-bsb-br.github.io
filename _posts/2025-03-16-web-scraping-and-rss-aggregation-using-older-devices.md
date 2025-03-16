---
tags: [scratchpad]
info: aberto.
date: 2025-03-16
type: post
layout: post
published: true
slug: web-scraping-and-rss-aggregation-using-older-devices
title: 'Web scraping and RSS aggregation using older devices'
---
─────────────────────────────────────────────────────
1) CHOOSE AND INSTALL A LIGHTWEIGHT OPERATING SYSTEM
─────────────────────────────────────────────────────
• Netbooks: Install a lightweight distro such as Debian, Xubuntu, or MX Linux (32-bit if needed, otherwise 64-bit).  
• Raspberry Pi 3B: Use Raspberry Pi OS (Lite version for minimal resources, or the standard Raspberry Pi OS if you prefer a GUI).

─────────────────────────────────────────────────────
2) SYSTEM PREPARATION AND SECURITY
─────────────────────────────────────────────────────
• Update Package Repositories:
  sudo apt-get update && sudo apt-get upgrade -y
• (Optional) Harden SSH:
  - Disable password-based authentication:
    sudo nano /etc/ssh/sshd_config  
    PasswordAuthentication no  
  - Use keys or a well-managed password system if you prefer.  
• Install some helpful tools:
  sudo apt-get install git curl wget nano ufw -y

─────────────────────────────────────────────────────
3) SET UP BASIC PROJECT ENVIRONMENT
─────────────────────────────────────────────────────
a) Create a dedicated directory:
  mkdir -p ~/personal_info_retrieval  
  cd ~/personal_info_retrieval

b) Install Python 3 and pip (if not already):
  sudo apt-get install python3 python3-pip python3-venv -y

c) Create a Python virtual environment:
  python3 -m venv venv  
  source venv/bin/activate  

d) Install important libraries:
  pip install requests beautifulsoup4 feedparser lxml

─────────────────────────────────────────────────────
4) RSS AGGREGATION (SIMPLER, LOW-RESOURCE TASK)
─────────────────────────────────────────────────────
RSS (Really Simple Syndication) is an XML-based feed that many websites and blogs provide for publishing their updates.

a) Minimal Example Script (rss_aggregator.py):

#!/usr/bin/env python3
import feedparser
import datetime

RSS_FEEDS = [
    "https://example.com/feed",
    "https://anotherexample.com/rss",
]

def fetch_rss(feed_url):
    return feedparser.parse(feed_url)

if __name__ == "__main__":
    for feed_url in RSS_FEEDS:
        feed_data = fetch_rss(feed_url)
        print(f"=== {feed_url} ===")
        for entry in feed_data.entries[:5]:  # Limit to 5 items
            published_time = entry.get("published", "No date")
            title = entry.get("title", "No title")
            link  = entry.get("link", "")
            print(f"{published_time} | {title} | {link}")
        print()

• Save the file:
  nano rss_aggregator.py  
  (Paste in the script)  
  chmod +x rss_aggregator.py  

• Run manually:
  ./rss_aggregator.py  

b) Extended or More Advanced RSS Readers:
• Tiny Tiny RSS (TT-RSS), Miniflux, or FreshRSS can run on older hardware without heavy overhead.  
• If you want a GUI-based feed reader on a netbook, consider Newsboat (terminal-based) or Liferea (lightweight desktop application).

─────────────────────────────────────────────────────
5) BASIC WEB SCRAPING WORKFLOW
─────────────────────────────────────────────────────
Scraping retrieves HTML directly and extracts desired information—headlines, prices, etc.

a) Example: Basic Python Scraper (scraper.py)

#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import datetime

URLS = [
    "https://example.com/news",
    "https://anotherexample.org/blog",
]

def scrape_site(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        headlines = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
        
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "url": url,
            "headlines": headlines
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    for link in URLS:
        data = scrape_site(link)
        print(data)

• Save and run:
  nano scraper.py  
  chmod +x scraper.py  
  ./scraper.py  

b) Notes on Performance:
• Limit the depth of scraping. Stick to single pages or specifically targeted pages rather than crawling the entire domain.  
• Consider short timeouts (5–10 seconds) to prevent old devices from hanging if a site is unresponsive.

─────────────────────────────────────────────────────
6) STORING AND MANAGING SCRAPED DATA
─────────────────────────────────────────────────────
Double-check you don’t fill your HDD with logs or data.

a) SQLite Database (light footprint):
• Install:
  sudo apt-get install sqlite3  
• Python usage:
  pip install sqlite3 (some distributions already have the sqlite3 module built in)
• In your Python script:
  
  import sqlite3
  
  conn = sqlite3.connect("mydata.db")
  c = conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS headlines (
               date TEXT,
               source_url TEXT,
               headline TEXT
             )""")
  # Insert data
  c.execute("INSERT INTO headlines VALUES (?, ?, ?)", (timestamp, url, headline))
  conn.commit()
  conn.close()

b) Simple Files or CSV:
• If your data volume is low, store results in JSON or CSV.  
• Example (appending JSON lines):
  
  import json
  
  with open("scraped_data.json", "a") as f:
      json.dump(data_dict, f)
      f.write("\n")

─────────────────────────────────────────────────────
7) AUTOMATION WITH CRON
─────────────────────────────────────────────────────
Use cron to schedule tasks so your netbook or Pi does not require manual intervention.

1. Edit crontab:
   crontab -e  
2. Add lines like:
   # Run RSS aggregator every 6 hours
   0 */6 * * * /home/pi/personal_info_retrieval/venv/bin/python /home/pi/personal_info_retrieval/rss_aggregator.py >> /home/pi/rss_aggregator.log 2>&1

   # Run web scraper every day at 01:00
   0 1 * * * /home/pi/personal_info_retrieval/venv/bin/python /home/pi/personal_info_retrieval/scraper.py >> /home/pi/scraper.log 2>&1

Adjust paths and times as needed. This ensures automatic updates without using extra memory.

─────────────────────────────────────────────────────
8) LIGHTWEIGHT DASHBOARD OR OUTPUT VIEW
─────────────────────────────────────────────────────
You can visualize your data in a minimal form:

• Console Tools:
  - Use simple CLI-based viewers (less, cat, sqlite3 interactive shell).
• Simple Web Interface (Flask):
  1. pip install flask  
  2. Example snippet:
     
     from flask import Flask, jsonify
     import json

     app = Flask(__name__)

     @app.route("/")
     def home():
         with open("scraped_data.json", "r") as f:
             lines = f.read().strip().split("\n")
             results = [json.loads(line) for line in lines]
         return jsonify(results)

     if __name__ == "__main__":
         app.run(host="0.0.0.0", port=5000)

• Access from LAN:
  http://<DEVICE_IP>:5000

─────────────────────────────────────────────────────
9) HARDWARE AND PERFORMANCE TIPS
─────────────────────────────────────────────────────
• Use minimal or no GUI on older netbooks and the Pi 3B.  
• Avoid persistent high CPU tasks. Space out scrape intervals to prevent HDD thrashing.  
• Maintain a single “control node” (e.g., Pi 3B) with data stored locally, and you can run remote scraping scripts on netbooks that send results back via scp/rsync if desired.  
• Keep the entire environment updated to avoid library vulnerabilities.

─────────────────────────────────────────────────────
10) TROUBLESHOOTING
─────────────────────────────────────────────────────
• If scraping fails or times out, check connectivity, site structure changes, or blocklists. Adjust user-agent or add small random sleep intervals in the script to avoid being flagged as a bot.  
• If the device slows down or runs hot, lower the scraping frequency.  
• If storage becomes scarce on the HDD, rotate or prune old data.

─────────────────────────────────────────────────────
CONCLUSION
─────────────────────────────────────────────────────
Following this guide, your 2010-era netbooks and Raspberry Pi 3B can continuously gather and organize online content with minimal overhead. RSS aggregation provides a quick, low-resource approach for sites offering feeds, while web scraping covers any sources lacking an accessible feed. By tying everything together with lightweight databases or file logging and a simple cron schedule, you can maintain efficient, automated personalized information retrieval despite modest hardware resources.