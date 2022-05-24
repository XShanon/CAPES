from bs4 import BeautifulSoup as bs4
import requests
import feedparser
import urllib.parse
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def findfeed(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw, features="lxml")
    feed_urls = html.findAll("link", rel="alternate")
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get("type",None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href",None)
                    if href:
                        possible_feeds.append(href)

    possible_feeds.append(site+"/feed")
    possible_feeds.append(site)
    parsed_url = urllib.parse.urlparse(site)
    base = parsed_url.scheme+"://"+parsed_url.hostname
    atags = html.findAll("a")
    for a in atags:
        href = a.get("href",None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                possible_feeds.append(href)
    for url in list(set(possible_feeds)):
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url.find('comments') == -1:
                result.append(url)
    if result:    
        return(result[0])
    else:
        return 
