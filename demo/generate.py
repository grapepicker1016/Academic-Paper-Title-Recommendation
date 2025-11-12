import os

MODEL_PATH = os.environ.get("MODEL_PATH", "outputs/best_model")

def recommend(model, abstract: str):
    abss = ["summarize: " + abstract]
    predicted_title = model.predict(abss)
    return predicted_title
