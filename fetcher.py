import feedparser
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

SOURCES = [
    {'name': 'Financial Times', 'url': 'https://www.ft.com/?format=rss', 'type': 'news'},
    {'name': 'Wall Street Journal', 'url': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml', 'type': 'news'},
    {'name': 'New York Times', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'type': 'news'},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/world/rss', 'type': 'news'},
    {'name': 'Nikkei Asia', 'url': 'https://asia.nikkei.com/rss/feed/nar', 'type': 'news'},
    {'name': 'Handelsblatt', 'url': 'https://www.handelsblatt.com/contentexport/feed/top-themen', 'type': 'news'},
    {'name': 'Le Monde', 'url': 'https://www.lemonde.fr/rss/une.xml', 'type': 'news'},
    {'name': 'Washington Post', 'url': 'https://feeds.washingtonpost.com/rss/world', 'type': 'news'},
    {'name': 'SCMP', 'url': 'https://www.scmp.com/rss/91/feed', 'type': 'news'},
    {'name': 'Foreign Affairs', 'url': 'https://www.foreignaffairs.com/rss.xml', 'type': 'news'},
    {'name': 'INSS', 'url': 'https://www.inss.org.il/he/feed/', 'type': 'research'}
]

def fetch_and_build():
    news_items = []
    translator = GoogleTranslator(source='auto', target='iw')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    now = datetime.now().strftime("%d/%m/%Y בשעה %H:%M")
    
    for src in SOURCES:
        try:
            # שימוש ב-timeout ארוך יותר למניעת נפילות
            resp = requests.get(src['url'], headers=headers, timeout=20)
            # שימוש ב-parser ספציפי ליציבות ב-GitHub
            feed = feedparser.parse(resp.content)
            
            if feed.entries:
                entry = feed.entries[0]
                title = translator.translate(entry.title)
                desc = entry.get('summary', entry.get('description', ''))[:200]
                summary = translator.translate(desc) if desc else "לחץ לפרטים"
                
                news_items.append({
                    'source': src['name'], 'title': title, 'summary': summary,
                    'link': entry.link, 'domain': src['url'].split('/')[2]
                })
        except: continue

    cards_html = "".join([f"""
        <div class="card" onclick="window.open('{i['link']}', '_blank')">
            <div class="source-header">
                <img src="https://www.google.com/s2/favicons?sz=64&domain={i['domain']}" class="favicon">
                {i['source']}
            </div>
            <h3>{i['title']}</h3>
            <p>{i['summary']}...</p>
        </div>""" for i in news_items])

    full_html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>מבט עולמי - לוח מלא</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 20px; }}
            .container {{ max-width: 1200px; margin: auto; }}
            header {{ background: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            .update-bar {{ background: #fff3cd; padding: 10px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; text-align: center; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #007bff; transition: 0.3s; }}
            .card:hover {{ transform: translateY(-5px); }}
            .source-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-weight: bold; color: #666; }}
            .favicon {{ width: 18px; height: 18px; }}
            h3 {{ margin: 0 0 10px 0; font-size: 1.1em; color: #111; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>מבט עולמי 🌍</h1>
                <div class="update-bar">עודכן לאחרונה: {now}</div>
            </header>
            <div class="grid">{cards_html}</div>
        </div>
    </body>
    </html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)

if __name__ == "__main__":
    fetch_and_build()
