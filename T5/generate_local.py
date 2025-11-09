from T5.model import create_model
import argparse

def generate_title(model_path, abstract):
    model = create_model(model_path, use_cuda=False)
    abss = ["summarize: " + abstract]
    predicted_title = model.predict(abss)
    return predicted_title

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", "-m", help="path to model", type=str, default="outputs/best_model")
    parser.add_argument("--abstract", "-a", help="abstract to generate title", type=str)
    args = parser.parse_args()
    predicted_title = generate_title(args.model_path, args.abstract)
    print(predicted_title)
