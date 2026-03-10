from rank_bm25 import BM25Okapi

class BM25Retriever:

    def run(self, context):

        if len(context.passages) == 0:

            print("No passages retrieved.")

            context.evidence = []

            return context

        tokenized = [p.split() for p in context.passages]

        bm25 = BM25Okapi(tokenized)
        query = context.claim + " " + " ".join(context.questions)

        scores = bm25.get_scores(query.split())

        ranked = sorted(
            zip(context.passages, scores),
            key=lambda x: x[1],
            reverse=True
        )

        context.evidence = [p for p, _ in ranked[:5]]

        return context