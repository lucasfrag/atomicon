from config import Config
from modules.search.brave_search import BraveSearch
from modules.search.google_cse_search import GoogleCSESearch
from modules.search.serpapi_search import SerpAPISearch

def get_searcher():

    if Config.SEARCH_ENGINE == "brave":
        return BraveSearch(api_key=Config.BRAVE_API_KEY)

    if Config.SEARCH_ENGINE == "serpapi":
        return SerpAPISearch()


    if Config.SEARCH_ENGINE == "google_cse":
        return GoogleCSESearch()


    return BraveSearch(api_key=Config.BRAVE_API_KEY)