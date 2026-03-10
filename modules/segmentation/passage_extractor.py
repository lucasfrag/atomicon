import re


class PassageExtractor:

    def run(self, context):

        passages = []

        for doc in context.documents:

            sentences = re.split(r"[.!?]\s+", doc)

            for s in sentences:

                if len(s) > 50:

                    passages.append(s.strip())

        context.passages = passages

        return context