#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import os.path
import re

NON_ALPHANUMERIC = re.compile('[^a-zA-Z0-9\\s]')
WHITESPACES = re.compile('\\s')

def get_id(title):
    title = NON_ALPHANUMERIC.sub('', title)
    title = WHITESPACES.sub('-', title)
    title = title.lower()
    return title

def read_metadata(url):
    req = requests.get(url, headers={'User-Agent': 'purkkafibot'})
    req.encoding = 'utf-8'
    html = req.text
    print('parsing OG for', url)
    
    soup = BeautifulSoup(html, 'html.parser')

    title, by = soup.head.title.string.split(' by ')
    description = soup.head.find(property='og:description')
    site = soup.head.find(property='og:site_name')
    link_id = get_id(title)
    
    itch_image_url = soup.head.find(property='og:image')['content']
    image_path = f'/assets/opengraph/{ link_id }.{ itch_image_url.split(".")[-1] }'
    
    with open(f'html/{image_path}', 'wb') as f:
        f.write(requests.get(itch_image_url).content)
    
    return {
        'title': title,
        'id': link_id,
        'by': by,
        'url': url,
        'site': site['content'] if site != None else '',
        'image': image_path,
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
        in_cache = f.read()
        if cache == in_cache:
            print('OG previews up to date')
            exit()

for url in urls:
    if url in in_cache:
        continue
    
    path = Path('beagic/opengraph', url)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with path.open('w') as f:
        meta = read_metadata(url)
        
        f.write(f"""
<a id="{meta['id']}" class="opengraphLink" href="{meta['url']}">
    <div class="opengraphPreview" style="--og-img: url('{meta['image']}')">
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

<div class="opengraphShare"><a href="#{meta['id']}">🔗</a></div>
""")

with open(CACHE_FILE, 'w') as f:
    f.write(cache)
