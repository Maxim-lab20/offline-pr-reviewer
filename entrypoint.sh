#!/bin/bash

# Wait for Ollama service to be ready
until curl -s http://ollama:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama service..."
  sleep 5
done

echo "Ollama service is up. Checking and pulling gemma:2b model..."

python -c "
import ollama
import time

model_name = 'gemma:2b'

def pull_model():
    print(f'Attempting to pull {model_name}...')
    try:
        ollama.pull(model_name)
        print(f'{model_name} pulled successfully.')
        return True
    except ollama.ResponseError as e:
        print(f'Error pulling {model_name}: {e}')
        return False

# Check if the model is already available
try:
    models = ollama.list()
    if any(model['name'] == model_name for model in models['models']):
        print(f'{model_name} is already available.')
    else:
        # Model not found, attempt to pull it
        if not pull_model():
            print('Failed to pull model after retries. Exiting.')
            exit(1)
except ollama.ResponseError as e:
    print(f'Error listing models: {e}')
    # If listing fails, try to pull anyway
    if not pull_model():
        print('Failed to pull model after retries. Exiting.')
        exit(1)

"

echo "gemma:2b model configured. Starting application..."
exec python app.py
