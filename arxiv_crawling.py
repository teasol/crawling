import feedparser
import pandas as pd 
from datetime import datetime 

def search_arxiv(keywords, max_results=30):
    base_url = "http://export.arxiv.org/api/query?"
    query = " OR ".join(f"all:{kw}" for kw in keywords)
    search_query = f"search_query={query}&max_results={max_results}"
    feed = feedparser.parse(base_url + search_query)

    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "authors": entry.author,
            "summary": entry.summary,
            "published": datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ"),
            "link": entry.link
        })
    
    return papers 
