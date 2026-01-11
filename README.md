# SMS Checker / Backend

The backend of this project provides a simple REST service that can be used to detect spam messages.
We have extended the base project [rohan8594/SMS-Spam-Detection](https://github.com/rohan8594/SMS-Spam-Detection), which introduces several basic classification models, and wrap one of them in a microservice.

The following sections will explain you how to get started.
The project **requires a Python 3.12 environment** to run (tested with 3.12.9).
Use the `requirements.txt` file to restore the required dependencies in your environment.

---

## Training the Model

You have two options for training: manual (local/Docker) or automated (GitHub Actions).

### Option 1: Manual Training (Local Development)

To train the model manually, you can create a local environment...

    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

... or you train in a Docker container (recommended):

    $ docker run -it --rm -v ./:/root/sms/ python:3.12.9-slim bash
    ... (container startup)
    $ cd /root/sms/
    $ pip install -r requirements.txt

Once all dependencies have been installed, the data can be preprocessed and the model trained by creating the output folder and invoking three commands:

    $ mkdir output
    $ python src/read_data.py
    Total number of messages:5574
    ...
    $ python src/text_preprocessing.py
    [nltk_data] Downloading package stopwords to /root/nltk_data...
    [nltk_data]   Unzipping corpora/stopwords.zip.
    ...
    $ python src/text_classification.py

The resulting model files will be placed as `.joblib` files in the `output/` folder.

### Option 2: Automated Training (F9 - Production)

For production use, we provide automated model training via GitHub Actions that creates versioned releases.

#### Triggering Automated Training

1. Go to **Actions** tab → **"Train and Release Model"**
2. Click **"Run workflow"**
3. Select branch (usually `main`)
4. Enter version number (e.g., `1.0.0`)
5. Click **"Run workflow"**

The workflow will:
- Train the model on GitHub's servers
- Create a versioned GitHub Release
- Upload `model.joblib` and `preprocessor.joblib`
- Make files publicly downloadable

**Training duration**: 2-5 minutes

#### Versioning Strategy

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- `1.0.0` - Initial production release
- `1.1.0` - Improvements (better accuracy)
- `1.1.1` - Bug fixes, retraining
- `2.0.0` - Breaking changes (new architecture)
- `1.0.0-beta` - Pre-release for testing

#### Downloading Released Models

**Via Command Line:**
```bash
VERSION="1.0.0"
curl -L -O "https://github.com/doda25-team19/model-service/releases/download/v${VERSION}/model.joblib"
curl -L -O "https://github.com/doda25-team19/model-service/releases/download/v${VERSION}/preprocessor.joblib"
```

**Via Browser:**
Navigate to: `https://github.com/doda25-team19/model-service/releases`


## Serving Recommendations

To make the models accessible, you need to start the microservice by running the `src/serve_model.py` script from within the virtual environment that you created before, or in a fresh Docker container (recommended):

    $ docker run -it --rm -p 8081:8081 -v ./:/root/sms/ python:3.12.9-slim bash
    ... (container startup)
    $ cd /root/sms/
    $ pip install -r requirements.txt
    $ python src/serve_model.py

The server will start on port 8081.
Once its startup has finished, you can either access [localhost:8081/apidocs](http://localhost:8081/apidocs) in your browser to interact with the service, or you send `POST` requests to request predictions, for example with `curl`:

    $ curl -X POST "http://localhost:8081/predict" -H "Content-Type: application/json" -d '{"sms": "test ..."}'
    {
      "classifier": "decision tree",
      "result": "ham",
      "sms": "test ..."
    }

---

## Troubleshooting

### Automated Training Issues

| Problem | Solution |
|---------|----------|
| Training workflow fails | Check Actions logs, verify dependencies in `requirements.txt`, test locally first |
| Release already exists | Use a new version number or delete the existing release |
| Files not uploaded to release | Verify training step logs show files created in `output/` directory |
| Can't load preprocessor | Import preprocessing functions before loading: `from text_preprocessing import _text_process, _extract_message_len` |