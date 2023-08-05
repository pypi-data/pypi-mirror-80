import argparse

import kenlm
from flask import Flask, request, jsonify, render_template

model = None

app = Flask(__name__)


class KenlmModel(kenlm.Model):
    def score(self, raw_text):
        text = " ".join(raw_text)

        result = super().score(text, bos=True, eos=True)

        return result

@app.route("/")
def index_page():
    return render_template('language_model_index.html')


@app.route("/parse", methods=["GET"])
def single_parse_service():
    global model

    text = request.args.get("q")

    if not text:
        raise ValueError("missing q")

    result = model.perplexity(text)

    return jsonify(result)


@app.route("/parse", methods=["POST"])
def batch_parse_service():
    text_list = request.get_json()

    if not text_list:
        raise ValueError("text list is missing")

    result = [model.perplexity(text) for text in text_list]

    return jsonify(result)


def load_model(model_file: str):
    return KenlmModel(model_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_file", help="KenLM model file")

    config = vars(parser.parse_args())

    model = load_model(config["model_file"])

    app.run(host="0.0.0.0")
