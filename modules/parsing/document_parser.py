import trafilatura

from utils.page_cache import load_page, save_page


class DocumentParser:

    def run(self, context):

        documents = []

        for url in context.search_results:
            cached = load_page(url)

            if cached:
                documents.append({
                    "url": url,
                    "text": cached
                })
                continue

            try:
                downloaded = trafilatura.fetch_url(url)
                text = trafilatura.extract(downloaded)

                if text:
                    save_page(url, text)

                    documents.append({
                        "url": url,      # 🔥 mantém origem
                        "text": text
                    })

            except:
                continue

        context.documents = documents

        return context