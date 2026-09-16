# Bazm-e-Irtiqa

Bazm-e-Irtiqa is a containerized, open-source multi-agent orchestration engine. Designed for local execution, it isolates specialized AI agents and open-weight Large Language Models (LLMs) to preserve host system integrity while providing a predictable development environment.

## Quick Start Guide

The core stack is containerized with Docker to ensure environment parity and reproducible execution.

### 1. Configure Your Environment

Create a `.env` file in the project root to define your target backend model. For resource-constrained hosts, lightweight models like `phi3` or `qwen2.5:0.5b` are recommended.

```env
# .env
LLM_MODEL=phi3
```

### 2. Launch the AI Engine

Start the infrastructure using Docker Compose. This will boot up the LLM server and automatically trigger a temporary container to pull the configured specified model.

```Bash
docker-compose up -d
```


### 3. Monitor the Model Download

Since AI models are large, the download may take few minutes. You can watch the progress of the automated puller by checking its logs:

```Bash
docker logs -f model-puller
```
_(Press `Ctrl+C` to exit the logs once the download is complete)._


### 4. Health Check & API Verification

Once the model is downloaded, verify that the AI engine is responsive by sending a test curl request to the local API:

```Bash
curl http://localhost:11434/api/generate -d '{
  "model": "phi3",
  "prompt": "In one short sentence, what is a multiagent system?",
  "stream": false
}'
```

### Expected Output:

A successful request returns an HTTP 200 with a JSON payload confirming execution.

```JSON
{
  "model": "phi3",
  "response": "A multiagent system is a computerized system composed of multiple interacting intelligent agents...",
  "done": true
}
```