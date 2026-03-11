import json


def load_averitec_dataset(path):

    with open(path, "r") as f:

        data = json.load(f)

    claims = []

    for i, item in enumerate(data):

        claims.append({
            "id": i,
            "claim": item["claim"],
            "label": item.get("label")
        })

    return claims