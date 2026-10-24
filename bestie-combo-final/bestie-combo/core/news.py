import requests
from core.config import Config

def get_latest_news():
    config = Config()
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={config.NEWS_API_KEY}"
    
    res = requests.get(url).json()
    articles = res.get("articles", [])[:3]

    return "\n".join([f"- {a['title']}" for a in articles])