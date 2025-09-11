#!/bin/bash

# Wait for Ollama service to be ready
until curl -s http://ollama:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama service..."
  sleep 5
done

echo "Ollama service is up. Pulling gemma:2b model..."
ollama pull gemma:2b

echo "gemma:2b model pulled. Starting application..."
exec python app.py
