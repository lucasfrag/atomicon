import os
import json

class ResultWriter:

    def __init__(self):
        self.results = []

    def add(self, item, result):
        steps = []

        num_steps = len(result.qa_pairs)

        for i in range(num_steps):

            qa = result.qa_pairs[i]

            # pega evidence do step
            if isinstance(result.evidence, list) and i < len(result.evidence):
                evidence_list = result.evidence[i]
            else:
                evidence_list = result.evidence

            # garante que é lista
            if not isinstance(evidence_list, list):
                evidence_list = [evidence_list]

            # pega stance do step
            if isinstance(result.stances, list) and i < len(result.stances):
                stance = result.stances[i]
            else:
                stance = None

            processed_evidence = []

            for ev in evidence_list:

                if isinstance(ev, dict):
                    processed_evidence.append({
                        "text": ev.get("text"),
                        "bm25_score": ev.get("bm25_score"),
                        "rerank_score": ev.get("rerank_score"),
                        "label": stance.get("label") if isinstance(stance, dict) else stance
                    })
                else:
                    processed_evidence.append({
                        "text": str(ev),
                        "label": stance
                    })

            step = {
                "question": qa.get("question"),
                "answer": qa.get("answer"),
                "evidence": processed_evidence
            }

            steps.append(step)

        self.results.append({
            "claim": item.get("claim"),
            "prediction": result.verdict,
            "gold_label": item.get("label"),
            "speaker": item.get("speaker"),
            "pipeline": {
                "steps": steps,
                "final_verdict": result.verdict
            }
        })

    def save(self, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)