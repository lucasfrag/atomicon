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

        Explain briefly how the evidence relates to the claim.

        Do not judge people or accuse anyone of wrongdoing.
        Simply summarize the relationship between the evidence and the claim.

        Write 2–3 neutral sentences.
        """

        justification = self.llm.generate(prompt).strip()

        context.justification = justification

        return context