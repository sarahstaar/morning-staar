#!/usr/bin/env python3
"""Build the podcast feed (feed.xml) and a simple web page (index.html) for The Morning Staar.

Reads episodes.json (newest first). Each episode:
  {"date": "2026-10-22", "title": "...", "summary": "...", "audio_url": "...",
   "bytes": 5080916, "seconds": 318, "voice": "Daniel"}
Usage: python3 build_feed.py <site_base_url>
"""
import json, sys, html
from datetime import datetime, timezone
from email.utils import format_datetime

base = sys.argv[1].rstrip("/")
eps = json.load(open("episodes.json"))
esc = html.escape

def rfc822(d):
    # Episodes go out by 6:00 am Paris time; 04:00 UTC is always before that
    dt = datetime.strptime(d, "%Y-%m-%d").replace(hour=4, tzinfo=timezone.utc)
    return format_datetime(dt)

def hms(s):
    return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"

items = []
for e in eps:
    items.append(f"""    <item>
      <title>{esc(e['title'])}</title>
      <description>{esc(e['summary'])}</description>
      <itunes:summary>{esc(e['summary'])}</itunes:summary>
      <pubDate>{rfc822(e['date'])}</pubDate>
      <guid isPermaLink="false">morning-staar-{e['date']}</guid>
      <enclosure url="{esc(e['audio_url'])}" length="{e['bytes']}" type="audio/mpeg"/>
      <itunes:duration>{hms(e['seconds'])}</itunes:duration>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Morning Staar</title>
    <link>{base}/</link>
    <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>
    <language>en-gb</language>
    <description>Your daily briefing: AI, space, Tesla, technology and world news, plus the latest from Moonshots and Tesla Time News, the local weather and a thought for the day.</description>
    <itunes:author>The Morning Staar</itunes:author>
    <itunes:summary>Your daily five-minute briefing: AI, space, Tesla, technology and world news, the local weather and a thought for the day.</itunes:summary>
    <itunes:image href="{base}/cover.jpg"/>
    <image><url>{base}/cover.jpg</url><title>The Morning Staar</title><link>{base}/</link></image>
    <itunes:category text="News"><itunes:category text="Daily News"/></itunes:category>
    <itunes:explicit>false</itunes:explicit>
    <itunes:block>yes</itunes:block>
{chr(10).join(items)}
  </channel>
</rss>
"""
open("feed.xml", "w").write(feed)

rows = "\n".join(
    f'<li><div class="t">{esc(e["title"])}</div><div class="s">{esc(e["summary"])}</div>'
    f'<audio controls preload="none" src="{esc(e["audio_url"])}"></audio></li>' for e in eps)
page = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>The Morning Staar</title>
<style>
:root{{--bg:#14111f;--card:#1f1a30;--text:#f4ecff;--muted:#c9bcd9;--accent:#ffc35a}}
body{{margin:0;background:var(--bg);color:var(--text);font:17px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:680px;margin:0 auto;padding:24px 16px 48px}}
header{{display:flex;gap:16px;align-items:center;margin-bottom:24px}}
header img{{width:96px;height:96px;border-radius:12px}}
h1{{margin:0;font-size:1.6rem}} .sub{{color:var(--muted)}}
.feed{{background:var(--card);padding:14px 16px;border-radius:12px;margin-bottom:24px;word-break:break-all}}
.feed b{{color:var(--accent)}}
ul{{list-style:none;padding:0;margin:0;display:grid;gap:14px}}
li{{background:var(--card);border-radius:12px;padding:14px 16px}}
.t{{font-weight:600}} .s{{color:var(--muted);font-size:.95rem;margin:4px 0 10px}}
audio{{width:100%}}
</style></head><body><main>
<header><img src="cover.jpg" alt=""><div><h1>The Morning Staar</h1><div class="sub">Your daily briefing</div></div></header>
<div class="feed">Podcast feed: <b>{base}/feed.xml</b></div>
<ul>
{rows}
</ul></main></body></html>
"""
open("index.html", "w").write(page)
print(f"Built feed with {len(eps)} episode(s)")
