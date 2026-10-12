import time
import requests
from prometheus_client import start_http_server, Gauge

# 1. Define the metrics we want to track
OLLAMA_UP = Gauge('ollama_status', '1 if Ollama is running, 0 if down' )
MODELS_LOADED = Gauge('ollama_models_loaded', 'Number of models currently in RAM')

def fetch_metrics():
    try:
        # 2. Ask Ollama what models are currently loaded in memory
        response = requests.get("http://ollama-server:11434/api/ps", timeout=5 )
        
        if response.status_code == 200:
            OLLAMA_UP.set(1) # It is alive
            models = response.json().get('models', [])
            MODELS_LOADED.set(len(models)) # Count how many models are loaded
        else:
            OLLAMA_UP.set(0)
    except Exception:
        # If the connection fails, mark it as down
        OLLAMA_UP.set(0)

if __name__ == '__main__':
    # 3. Start the server on port 8000 for Prometheus to read
    start_http_server(8000 )
    print("AI Metrics Exporter started on port 8000...")
    
    # 4. Check Ollama every 5 seconds
    while True:
        fetch_metrics()
        time.sleep(5)
