import json
import os

from datasets.averitec_loader import load_averitec_dataset
from pipeline.context import ClaimContext

from run_pipeline import pipeline


DATASET_PATH = "datasets/averitec/dev.json"
OUTPUT_PATH = "predictions.json"
MAX_CLAIMS = 50

claims = load_averitec_dataset(DATASET_PATH)

claims = claims[:MAX_CLAIMS]


# carregar previsões existentes

if os.path.exists(OUTPUT_PATH):

    with open(OUTPUT_PATH, "r") as f:

        predictions = json.load(f)

else:

    predictions = []


processed_ids = {p["id"] for p in predictions}


for item in claims:

    if item["id"] in processed_ids:

        print("SKIPPING CLAIM:", item["id"])

        continue


    print("\n===================================")
    print("CLAIM:", item["claim"])
    print("===================================\n")


    context = ClaimContext(
        claim_id=item["id"],
        claim_text=item["claim"]
    )


    result = pipeline.run(context)


    prediction = {
        "id": item["id"],
        "claim": item["claim"],
        "predicted_label": result.verdict,
        "justification": result.justification,
        "evidence": result.evidence[:3]
    }


    predictions.append(prediction)


    # salvar incrementalmente

    with open(OUTPUT_PATH, "w") as f:

        json.dump(predictions, f, indent=2)


print("\nSaved predictions to:", OUTPUT_PATH)