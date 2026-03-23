from .base_verdict import BaseVerdict


class LLMVerdict(BaseVerdict):

    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    NEE = "NOT ENOUGH EVIDENCE"
    CONFLICT = "CONFLICTING EVIDENCE/CHERRYPICKING"

    def __init__(self, llm):
        self.llm = llm

    # -----------------------------
    # 🧠 PROMPT (SEM STANCE!)
    # -----------------------------
    def build_prompt(self, context):

        # 🔹 evidências (top-k já rerankeadas)
        evidence_block = "\n\n".join(
            f"[{i+1}] {e['text']}"
            for i, e in enumerate(getattr(context, "evidence", [])[:8])
        )

        # 🔹 respostas derivadas (opcional, mas útil)
        qa_block = "\n\n".join(
            f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}"
            for qa in getattr(context, "qa_pairs", [])[:5]
        )

        return f"""
Task: Determine the final verdict of a claim based on evidence.

Claim:
{context.claim}

Claim date:
{context.claim_date}

Speaker:
{context.speaker}

---

Evidence:
{evidence_block}

---

Answers derived from evidence (may be incomplete or noisy):
{qa_block}

---

Instructions:

- You must determine whether the evidence SUPPORTS or REFUTES the claim.

- IMPORTANT:
  Evidence may refute a statement that is OPPOSITE to the claim.
  Always reason directly about the claim.

- Do NOT rely on keywords like "false", "fake", or "not true" alone.
  Interpret what is being negated.

- If evidence confirms the claim → SUPPORTED
- If evidence contradicts the claim → REFUTED
- If evidence is insufficient or unclear → NOT ENOUGH EVIDENCE
- If both strong support and refutation exist → CONFLICTING EVIDENCE/CHERRYPICKING

---

Output:
Return ONLY one label:

SUPPORTED
REFUTED
NOT ENOUGH EVIDENCE
CONFLICTING EVIDENCE/CHERRYPICKING
"""

    # -----------------------------
    # 🔤 NORMALIZAÇÃO
    # -----------------------------
    def normalize(self, response: str):

        if not response:
            return self.NEE

        r = response.strip().upper()

        if "REFUTE" in r or "FALSE" in r:
            return self.REFUTED

        if "SUPPORT" in r:
            return self.SUPPORTED

        if "CONFLICT" in r:
            return self.CONFLICT

        if "NOT ENOUGH" in r or "INSUFFICIENT" in r:
            return self.NEE

        return self.NEE

    # -----------------------------
    # 🎯 RUN
    # -----------------------------
    def run(self, context):

        # 🔹 fallback simples (caso extremo sem evidência)
        if not getattr(context, "evidence", None):
            context.verdict = self.NEE
            return context

        prompt = self.build_prompt(context)

        response = self.llm.generate(prompt)

        context.verdict = self.normalize(response)

        return context