"""
Flask API of the SMS Spam detection model model.
"""
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
import os
import urllib.request

from text_preprocessing import prepare, _extract_message_len, _text_process

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether an SMS is Spam.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                sms:
                    type: string
                    example: This is an example of an SMS.
    responses:
      200:
        description: "The result of the classification: 'spam' or 'ham'."
    """
    input_data = request.get_json()
    sms = input_data.get('sms')
    processed_sms = prepare(sms)

    model_path = os.environ.get('MODEL_FILE', 'output/model.joblib')
    model = joblib.load(model_path)

    prediction = model.predict(processed_sms)[0]

    res = {
        "result": prediction,
        "classifier": "decision tree",
        "sms": sms
    }
    print(res)
    return jsonify(res)

if __name__ == '__main__':
    model_path = 'output/model.joblib'
    preprocessor_path = 'output/preprocessor.joblib'
    model_url = os.environ.get('MODEL_URL', '')
    preprocessor_url = os.environ.get('PREPROCESSOR_URL', '')
    
    os.makedirs('output', exist_ok=True)
    
    # Download model if missing
    if not os.path.isfile(model_path):
        if model_url:
            print(f"Model file not found at {model_path}, downloading from {model_url}...")
            urllib.request.urlretrieve(model_url, model_path)
            print(f"Model downloaded to {model_path}")
        else:
            print(f"ERROR: Model file not found at {model_path} and no MODEL_URL provided!")
            exit(1)
    else:
        print(f"Model file found at {model_path}")
    
    # Download preprocessor if missing
    print("checking for preprocessor.joblib")
    if not os.path.isfile(preprocessor_path):
        print("no preprocessor file.")
        if preprocessor_url:
            print(f"Preprocessor file not found at {preprocessor_path}, downloading from {preprocessor_url}...")
            urllib.request.urlretrieve(preprocessor_url, preprocessor_path)
            print(f"Preprocessor downloaded to {preprocessor_path}")
        else:
            print(f"ERROR: Preprocessor file not found at {preprocessor_path} and no PREPROCESSOR_URL provided!")
            exit(1)
    else:
        print(f"Preprocessor file found at {preprocessor_path}")
    
    port = int(os.getenv("MODEL_PORT", 8081))
    app.run(host="0.0.0.0", port=port, debug=True)