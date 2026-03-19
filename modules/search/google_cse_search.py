import requests
from utils.cache_utils import load_cache, save_cache
from config import Config


class GoogleCSESearch:

    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY
        self.cx = Config.GOOGLE_CSE_ID
        self.cache = load_cache()

    def search(self, query):

        if query in self.cache:
            return self.cache[query]

        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": 5
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
        except Exception:
            return []

        results = [item["link"] for item in data.get("items", []) if "link" in item]

        self.cache[query] = results
        save_cache(self.cache)

        return results

    def run(self, context):
        queries = [context.claim] + getattr(context, "questions", [])
        urls = []

        for q in queries:
            urls.extend(self.search(q))

        context.search_results = list(set(urls))[:10]
        return context