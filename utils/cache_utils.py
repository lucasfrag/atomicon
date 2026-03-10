import json
import os

CACHE_FILE = "cache/search_cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    try:

        with open(CACHE_FILE, "r") as f:

            content = f.read().strip()

            if content == "":
                return {}

            return json.loads(content)

    except json.JSONDecodeError:

        print("Cache file corrupted. Resetting cache.")

        return {}


def save_cache(cache):

    os.makedirs("cache", exist_ok=True)

    with open(CACHE_FILE, "w") as f:

        json.dump(cache, f, indent=2)