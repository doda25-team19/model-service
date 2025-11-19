FROM python:3.12.9-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code and data
COPY smsspamcollection smsspamcollection
COPY src src

# service port
ENV MODEL_PORT=8081

EXPOSE 8081

# start the FastAPI service
CMD ["python", "src/serve_model.py"]
