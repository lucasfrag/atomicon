import json


def normalize(label):

    label = label.lower().strip()

    mapping = {
        "supported": "supported",
        "refuted": "refuted",
        "not enough evidence": "not enough evidence",
        "conflicting": "conflicting",
        "conflicting evidence/cherrypicking": "conflicting"
    }

    return mapping.get(label, label)


def evaluate(predictions_path, dataset_path):

    with open(predictions_path) as f:
        predictions = json.load(f)

    with open(dataset_path) as f:
        dataset = json.load(f)


    gold_labels = {
        i: normalize(item["label"])
        for i, item in enumerate(dataset)
    }


    correct = 0
    total = 0


    for pred in predictions:

        claim_id = pred["id"]

        predicted = normalize(pred["predicted_label"])

        gold = gold_labels.get(claim_id)


        if gold is None:
            continue


        total += 1

        if predicted == gold:
            correct += 1


    accuracy = correct / total if total else 0


    print("\n===== Evaluation =====\n")

    print("Total claims:", total)
    print("Correct:", correct)
    print("Accuracy:", round(accuracy, 3))