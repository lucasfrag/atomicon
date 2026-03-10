class JustificationGenerator:

    def __init__(self, llm):

        self.llm = llm

    def run(self, context):

        evidence_text = "\n\n".join(context.evidence[:5])

        prompt = f"""
You are a fact-checking assistant.

Claim:
{context.claim}

Evidence:
{evidence_text}

Verdict:
{context.verdict}

Write a short justification explaining why the evidence leads to this verdict.

The justification should be 2–3 sentences.
"""

        justification = self.llm.generate(prompt).strip()

        context.justification = justification

        return context