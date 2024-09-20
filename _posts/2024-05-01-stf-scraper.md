---
title: STF Scraper [script]
date: 2024-05-01 00:00:00 -03:00
categories:
- Code
tags:
- scripts
- estudos
comment: https://github.com/mvdiogo/stf-web-scraper
info: aberto.
type: post
layout: post
mermaid: true
---

```
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def generate_url(assunto):
    """
    Generates a URL for the 'acordaos' base with the given subject.
    This function constructs a URL string that includes query parameters specifically designed to search within the 'acordaos' section of the STF website.
    """
    return f"https://jurisprudencia.stf.jus.br/pages/search?base=acordaos&sinonimo=true&plural=true&page=1&pageSize=250&queryString={assunto}&sort=_score&sortBy=desc"

def parse_item(html_page):
    """
    Parses the HTML content to extract relevant data from 'acordaos'.
    This function navigates through the HTML structure of the webpage, identifying and extracting necessary details such as the title, ementa, judicial body, and more.
    """
    results = []
    soup = BeautifulSoup(html_page, "html.parser")
    data = soup.find_all("div", class_="result-container")
    for item in data:
        title_element = item.find("h4", class_="ng-star-inserted")
        ementa_element = item.find("span", class_="jud-text ng-star-inserted")
        if title_element and ementa_element:
            title = title_element.text.strip()
            ementa = ementa_element.text.strip()
            dates = item.find_all("span", style="font-weight: normal;")
            turma = dates[0].text.strip() if dates else ""
            ministro = dates[1].text.strip() if len(dates) > 1 else ""
            indexacao_partes = [part.text.strip() for part in item.find_all("p", class_="jud-text m-0")]
            indexacao = indexacao_partes[0] if indexacao_partes else ""
            partes = indexacao_partes[1] if len(indexacao_partes) > 1 else ""
            product = {
                "Title": title,
                "Ementa": ementa,
                "Orgao colegiado": turma,
                "Ministro": ministro,
                "Indexação": indexacao,
                "Partes": partes,
            }
            results.append(product)
    return results

def main(assunto):
    """
    Main function to launch the browser, scrape 'acordaos' data, and save it.
    This function uses the Playwright library to open a browser, navigate to the generated URL, and call the parsing function to extract and save the data.
    """
    url = generate_url(assunto)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False) 
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        parsed = parse_item(page.content())
        print(json.dumps(parsed, indent=3, ensure_ascii=False))
        with open(f"acordaos - {assunto}.json", "w", encoding="utf-8") as file:
            json.dump(parsed, file, indent=3, ensure_ascii=False)
        browser.close()

if __name__ == "__main__":
    assunto = input("Enter the subject for 'acordaos': ")
    main(assunto)
```
