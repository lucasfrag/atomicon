from .base_verdict import BaseVerdict


class LLMVerdict(BaseVerdict):

    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"
    NEE = "NOT ENOUGH EVIDENCE"
    CONFLICT = "CONFLICTING EVIDENCE/CHERRYPICKING"

    def __init__(self, llm):
        self.llm = llm

    # -----------------------------
    # 🧠 PROMPT
    # -----------------------------
    def build_prompt(self, context):

        # 🔥 usar stance estruturado
        stance_block = "\n\n".join(
            f"[{s.get('label', 'UNKNOWN')}] {s.get('text', '')}"
            for s in getattr(context, "stances", [])[:8]
        )

        # 🔥 fallback: evidência bruta
        raw_evidence = "\n\n".join(
            e["text"] if isinstance(e, dict) else str(e)
            for e in getattr(context, "evidence", [])[:5]
        )

        return f"""
Task: Determine the final verdict of a claim based on evidence.

Claim:
{context.claim}

---

Evidence with stance labels:
{stance_block}

---

Additional raw evidence:
{raw_evidence}

---

Scores:
- SUPPORT score: {getattr(context, "support_score", 0):.2f}
- REFUTE score: {getattr(context, "refute_score", 0):.2f}

---

Instructions:

1. PRIORITIZE stance labels when they are consistent.

2. If multiple pieces of evidence are labeled REFUTED → REFUTED.

3. If multiple pieces are labeled SUPPORTED → SUPPORTED.

4. If evidence explicitly says something is false, fake, or did not happen → REFUTED.

5. If evidence clearly confirms the claim → SUPPORTED.

6. If evidence is weak, missing, or irrelevant → NOT ENOUGH EVIDENCE.

7. If both strong support and refutation exist → CONFLICTING EVIDENCE/CHERRYPICKING.

---

CRITICAL RULES:

- Absence of evidence for a claim asserting existence → REFUTED
- Explicit negation ("did not happen", "fake", "false") → REFUTED
- Do NOT ignore stance labels

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

        if "CONFLICTING EVIDENCE/CHERRYPICKING" in r:
            return self.CONFLICT

        if "NOT ENOUGH" in r or "INSUFFICIENT" in r:
            return self.NEE

        return self.NEE

    # -----------------------------
    # 🎯 RUN
    # -----------------------------
    def run(self, context):

        # 🔥 fallback crítico (sem stance → usa contagem simples)
        if not getattr(context, "stances", None):

            texts = " ".join(
                e["text"] if isinstance(e, dict) else str(e)
                for e in getattr(context, "evidence", [])
            ).lower()

            if any(w in texts for w in ["fake", "false", "did not", "never"]):
                context.verdict = self.REFUTED
                return context

        prompt = self.build_prompt(context)

        response = self.llm.generate(prompt)

        context.verdict = self.normalize(response)

        return context