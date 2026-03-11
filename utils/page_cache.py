import os
import hashlib


CACHE_DIR = "cache/pages"


def get_cache_path(url):

    filename = hashlib.md5(url.encode()).hexdigest()

    return os.path.join(CACHE_DIR, filename + ".txt")


def load_page(url):

    path = get_cache_path(url)

    if os.path.exists(path):

        with open(path, "r") as f:

            return f.read()

    return None


def save_page(url, text):

    os.makedirs(CACHE_DIR, exist_ok=True)

    path = get_cache_path(url)

    with open(path, "w") as f:

        f.write(text)