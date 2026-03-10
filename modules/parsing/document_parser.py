import requests
import trafilatura


class DocumentParser:

    def run(self, context):

        documents = []

        for url in context.search_results:

            try:

                downloaded = trafilatura.fetch_url(url)

                text = trafilatura.extract(downloaded)

                if text:

                    documents.append(text)

            except:

                continue

        context.documents = documents

        return context