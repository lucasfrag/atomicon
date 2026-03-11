from evaluation.evaluate_predictions import evaluate


PREDICTIONS = "predictions.json"

DATASET = "datasets/averitec/dev.json"


evaluate(PREDICTIONS, DATASET)