from rank_bm25 import BM25Okapi
from config import Config


class BM25Retriever:

    def __init__(self, top_k=None):
        self.top_k = top_k or Config.BM25_TOP_K

    def run(self, context):
        if not context.documents:
            return context

        # 🔹 escolher query
        if Config.USE_QUESTION_FOR_RETRIEVAL and context.questions:
            query = context.questions[-1]
        else:
            query = context.claim

        docs = context.documents

        # 🔥 tokenização robusta (suporta dict ou str)
        tokenized_docs = [
            (doc["text"] if isinstance(doc, dict) else doc).split()
            for doc in docs
        ]

        tokenized_query = query.split()

        bm25 = BM25Okapi(tokenized_docs)
        scores = bm25.get_scores(tokenized_query)

        # 🔥 ranking mantendo estrutura original
        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        top_docs = []

        for doc, score in ranked[:self.top_k]:

            if isinstance(doc, dict):
                new_doc = {
                    **doc,
                    "bm25_score": float(score)  # 🔥 adiciona score sem perder url
                }
            else:
                new_doc = {
                    "text": doc,
                    "url": None,
                    "bm25_score": float(score)
                }

            top_docs.append(new_doc)

        # 🔹 histórico (sem duplicar por URL se existir)
        if not hasattr(context, "retrieved_documents"):
            context.retrieved_documents = []

        seen = set(
            d.get("url", d.get("text"))
            for d in context.retrieved_documents
            if isinstance(d, dict)
        )

        for doc in top_docs:
            key = doc.get("url") or doc.get("text")
            if key not in seen:
                context.retrieved_documents.append(doc)
                seen.add(key)

        # 🔥 importante: manter formato consistente
        context.documents = top_docs

        return context