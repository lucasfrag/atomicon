from serpapi import GoogleSearch
from utils.cache_utils import load_cache, save_cache
from config import Config


class SerpAPISearch:

    def __init__(self):
        self.api_key = Config.SERPAPI_KEY
        self.cache = load_cache()

    def search(self, query):

        if query in self.cache:
            return self.cache[query]

        params = {
            "q": query,
            "api_key": self.api_key
        }

        try:
            search = GoogleSearch(params)
            data = search.get_dict()
        except Exception:
            return []

        results = [r["link"] for r in data.get("organic_results", []) if "link" in r]

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