#!/usr/bin/python3

import feedparser
import html

def get_title(entry):
    if 'letterboxd_filmtitle' in entry:
        return f"Review: {html.escape(entry['letterboxd_filmtitle'])}"
    return html.escape(entry['title'])

def get_description(entry):
    return html.escape(entry['title']) if '<p>' in entry['description'] else entry['description']

def stringify_entry(entry):
    return f"""
    <item>
        <title>{get_title(entry)}</title>
        <description>{get_description(entry)}</description>
        <link>{entry['link']}</link>
        <guid>{entry['link']}</guid>
        <pubDate>{entry['published']}</pubDate>
    </item>
    """

base = feedparser.parse('html/rss.xml')
lxd = feedparser.parse('https://letterboxd.com/purkka/rss', agent='purkkafi-rss-bot')

entries = []

entries.extend(base['entries'])
entries.extend(lxd['entries'])

entries.sort(key=lambda e: e['published_parsed'], reverse=True)
entries = entries[:20]

entries_string = ''.join(stringify_entry(e) for e in entries)

with open('html/rss.xml', 'w') as f:
    f.write(f"""<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{base['feed']['title']}</title>
        <link>{base['feed']['link']}</link>
        <description>{base['feed']['description']}</description>
        <atom:link href="https://purkka.fi/rss.xml" rel="self" type="application/rss+xml" />
        {entries_string}
    </channel>
</rss>
""")

def get_date(entry):
    date = entry['published_parsed']
    return f'{date.tm_mday}.{date.tm_mon}.{date.tm_year}'
    
def beagicify_entry(entry):
    return f"\external{{{get_title(entry)}}}{{{entry['link']}}}{{{get_date(entry)}}}{{{entry['published']}}}{{{get_description(entry)}}}"

new_content = '\n'.join(beagicify_entry(e) for e in entries)

with open('beagic/new_content.bgc', 'w') as f:
    f.write(new_content)
