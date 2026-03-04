import feedparser
import time
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

SOURCES = [
    {'name': 'Financial Times', 'url': 'https://www.ft.com/?format=rss', 'type': 'news'},
    {'name': 'Wall Street Journal', 'url': 'https://feeds.a.dj.com/rss/RSSWorldNews.xml', 'type': 'news'},
    {'name': 'New York Times', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'type': 'news'},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/world/rss', 'type': 'news'},
    {'name': 'Nikkei Asia', 'url': 'https://asia.nikkei.com/rss/feed/nar', 'type': 'news'},
    {'name': 'INSS', 'url': 'https://www.inss.org.il/he/feed/', 'type': 'research'}
]

def fetch_and_build():
    news_items = []
    translator = GoogleTranslator(source='auto', target='iw')
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # זמן העדכון הנוכחי
    now = datetime.now().strftime("%d/%m/%Y בשעה %H:%M")
    
    print(f"--- מעדכן את הלוח: {now} ---")
    
    for src in SOURCES:
        try:
            print(f"סורק: {src['name']}...")
            resp = requests.get(src['url'], headers=headers, timeout=12)
            feed = feedparser.parse(resp.content)
            if feed.entries:
                entry = feed.entries[0]
                title = translator.translate(entry.title)
                summary = translator.translate(entry.get('summary', '')[:180])
                
                news_items.append({
                    'source': src['name'],
                    'title': title,
                    'summary': summary,
                    'link': entry.link,
                    'domain': src['url'].split('/')[2]
                })
        except: continue

    cards_html = "".join([f"""
        <div class="card" onclick="window.open('{item['link']}', '_blank')">
            <div class="source-header">
                <img src="https://www.google.com/s2/favicons?domain={item['domain']}" class="favicon">
                {item['source']}
            </div>
            <h3>{item['title']}</h3>
            <p>{item['summary']}...</p>
        </div>""" for item in news_items])

    full_html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>מבט עולמי מעודכן</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: auto; }}
            header {{ background: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            .update-bar {{ background: #fff3cd; padding: 10px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; color: #856404; display: flex; justify-content: center; align-items: center; gap: 15px; }}
            .refresh-btn {{ background: #007bff; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-family: inherit; font-weight: bold; }}
            .refresh-btn:hover {{ background: #0056b3; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #007bff; }}
            .source-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-weight: bold; color: #666; }}
            .favicon {{ width: 16px; height: 16px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>מבט עולמי 🌍</h1>
                <div class="update-bar">
                    <span>עודכן לאחרונה: {now}</span>
                    <button class="refresh-btn" onclick="location.reload()">רענן דף</button>
                </div>
            </header>
            <div class="grid">{cards_html}</div>
        </div>
    </body>
    </html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("המערכת עודכנה!")

if __name__ == "__main__":
    fetch_and_build()