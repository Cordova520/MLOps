from flask import Flask, abort, request, jsonify
import torch
import onnxruntime as ort
import numpy as np
from transformers import RobertaTokenizer
from pathlib import Path


app = Flask(__name__)

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

# Locate ONNX model relative to this Python file
MODEL_PATH = Path(__file__).resolve().parent / "roberta-sequence-classification-9.onnx"

# Load ONNX model using CPU execution
session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

def to_numpy(tensor):
    """
    Convert a PyTorch tensor or NumPy array to a NumPy array.
    """
    if isinstance(tensor, np.ndarray):
        return tensor

    if hasattr(tensor, "detach"):
        return tensor.detach().cpu().numpy()

    return np.asarray(tensor)

@app.route('/')
def home():
    return "<h1> RoBERTA Sentiment Analysis </h1>"

@app.route("/predict", methods=["POST"])
def predict():

    # Get JSON request
    data = request.get_json(silent=True)

    # Validate input: expect a list containing a string
    if (
        not isinstance(data, list)
        or len(data) == 0
        or not isinstance(data[0], str)
    ):
        return jsonify({
            "error": "Expected JSON list containing a string"
        }), 400

    # Extract text from the list
    text = data[0]

    # Tokenize using PyTorch tensors
    input_ids = torch.tensor(
        tokenizer.encode(
            text,
            add_special_tokens=True
        )
    ).unsqueeze(0)

    # Prepare ONNX inputs
    inputs = {
        session.get_inputs()[0].name: to_numpy(input_ids)
    }

    # Run inference
    outputs = session.run(None, inputs)

    # Get predicted class
    results = np.argmax(outputs[0], axis=1)

    return jsonify({
        "positive": bool(results[0])
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")

#You can interact with the API using curl or Postman. For example, using curl: 
#curl -X POST --header "Content-Type: application/json" --data '["everything is awful"]' http://192.168.100.18:8000/predict
#Just replace the IP address with your own. You can also use Postman to send a POST request to the /predict endpoint with a JSON body containing a list with a single string.
#Also you can change the text in the list to test different inputs. The API will return a JSON response indicating whether the sentiment is positive or not.