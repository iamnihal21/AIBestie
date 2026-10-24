import webbrowser
import urllib.parse

class Browser:

    def open_url(self, url: str):
        webbrowser.open(url)

    def search_google(self, query: str):
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)