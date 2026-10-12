# Bazm-e-Irtiqa

Bazm-e-Irtiqa is a containerized, open-source multi-agent orchestration engine. Designed for local execution, it isolates specialized AI agents and open-weight Large Language Models (LLMs) to preserve host system integrity while providing a predictable development environment.

## Core Features

- **Asynchronous Orchestration:** Utilizes Python's asyncio to execute non-dependent tasks concurrently (e.g., Frontend and Database agents working simultaneously) to optimize processing time.
- **Chain of Thought (CoT) Streaming:** Agents expose their internal reasoning (<thinking> tags) token-by-token before generating code, providing complete transparency into the AI's decision-making process.
- **Automated QA Feedback Loop:** A dedicated Quality Assurance agent reviews generated server code for syntax and logic errors. If issues are detected, it autonomously prompts the Backend agent for revisions before returning the final output.
- **Ephemeral Session Memory:** Agents maintain context throughout an active session, allowing users to issue iterative follow-up instructions (e.g., "Update the previous HTML to use a dark theme") without restarting the pipeline.

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

Once the model is downloaded, verify that the AI engine is responsive by sending a test curl request to the local API.

### Option A: Dynamic Test (Recommended)
This command automatically reads the LLM_MODEL variable from the .env file, removing the need to manually update the model name:

To test against currently downloaded and active model in Ollama, auto-detection can be performed using:
```bash
MODEL=$(grep '^LLM_MODEL=' .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
```

```bash
curl http://localhost:11434/api/generate -d "{
  \"model\": \"$MODEL\",
  \"prompt\": \"In one short sentence, what is a multiagent system?\",
  \"stream\": false
}"
```

### Option B: Quick Static Test

Alternatively, <your-model> can be replaced manually with the model name specified in the .env file (for example, phi3):

``` bash
curl http://localhost:11434/api/generate -d '{
  "model": "<your-model>",
  "prompt": "In one short sentence, what is a multiagent system?",
  "stream": false
}'
```
For example:

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

### 5. Start the Multi-Agent Factory
Bazm-e-Irtiqa utilizes a unified wrapper script (bzm) to abstract the underlying Docker execution commands.

First, ensure the script is executable:

```Bash
chmod +x bzm
```
The orchestration engine can be interacted with using three primary interfaces:

#### A. Web User Interface (Recommended)
Launches a rich, browser-based interface powered by Streamlit. It features real-time text streaming, visual separation of agent tasks, and collapsible code blocks.

```Bash
./bzm ui
```
Once running, navigate to http://localhost:8501 in your web browser.

#### B. Interactive Terminal (CLI )

A lightweight, terminal-based chat interface. It streams agent thought processes and generated code directly to standard output (stdout).

```Bash
./bzm chat
```

#### C. Automated Ping Test

Executes a static, pre-configured "Hello World" workflow to verify the end-to-end agent pipeline (Frontend -> Database -> Backend) without requiring manual input.

```Bash
./bzm ping
```


## Architecture Overview

The system strictly adheres to the principle of separation of concerns, ensuring that agent logic, core infrastructure, and presentation layers remain decoupled.

```text
bazm-e-irtiqa/
├── core/                  # LLM connection clients, async logic, and base configurations
├── agents/                # Specialized role definitions and prompts (Frontend, Backend, DB, QA)
├── interface/             # User interaction layers (CLI, Streamlit Web UI, Health checks)
├── bzm                    # Bash wrapper for simplified Docker container interaction
├── docker-compose.yml     # Multi-container infrastructure orchestration
└── Dockerfile             # Python environment containerization configuration
```

