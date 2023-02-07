#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os.path
import re

def read_metadata(url):
    html = requests.get(url, headers={'User-Agent': 'purkkafibot'}).text
    print('parsing OG for', url)
    
    soup = BeautifulSoup(html, 'html.parser')

    title, by = soup.head.title.string.split(' by ')
    image = soup.head.find(property='og:image')
    description = soup.head.find(property='og:description')
    site = soup.head.find(property='og:site_name')
    
    return {
        'title': title,
        'by': by,
        'url': url,
        'site': site['content'] if site != None else '',
        'image': image['content'] if image != None else '',
        'description': description['content'] if description != None else ''
    }

urls = set()
for file in Path('pages').rglob('*.bgc'):
    with open(file) as f:
        urls.update(re.findall('\\\opengraph_preview\{(.+)\}', f.read()))
urls = list(urls)

CACHE_FILE = 'beagic/opengraph/.cache'
cache = str(sorted(urls))

if os.path.isfile(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        if cache == f.read():
            print('OG previews up to date')
            exit()

for url in urls:
    path = Path('beagic/opengraph', url)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('w') as f:
        meta = read_metadata(url)
        
        f.write(f"""
<a class="opengraphLink" href="{meta['url']}">
    <div class="opengraphPreview">
        <img class="opengraphThumb" src="{meta['image']}"/>
        <div class="opengraphContent">
            <p class="opengraphText">
                <span class="opengraphTitle">{meta['title']}</span>
                <br>
                by <span class="opengraphBy">{meta['by']}</span>
                <br>
                <span class="opengraphDescription">{meta['description']}</span>
            </p>
            <div class="opengraphSiteButton">
                View{(' on ' + meta['site']) if meta['site'] != '' else ''}
            </div>
        </div>
    </div>
</a>
        """)

with open(CACHE_FILE, 'w') as f:
    f.write(cache)
