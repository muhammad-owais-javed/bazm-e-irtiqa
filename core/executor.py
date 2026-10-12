import docker
import base64

client = docker.from_env()

def execute_in_sandbox(code_string):
    """Injects and runs the code inside the visual-sandbox container."""
    try:
        # Find the visual sandbox container
        sandbox = client.containers.get('visual-sandbox')
        
        # 1. Base64 encode the code to safely pass it through the terminal
        encoded_code = base64.b64encode(code_string.encode('utf-8')).decode('utf-8')
        
        # 2. Command to decode, save, install dependencies, and run
        # It also opens Firefox on the virtual desktop to view the app!
        bash_command = f"""
        echo "{encoded_code}" | base64 -d > /tmp/app.py &&
        apt-get update && apt-get install -y python3-pip firefox &&
        pip3 install flask &&
        pkill -f python3 || true &&  # Kill any old servers
        python3 /tmp/app.py & 
        sleep 3 && 
        DISPLAY=:1 firefox http://127.0.0.1:5000 &
        """
        
        print("⏳ [Executor] Injecting code into Visual Sandbox..." )
        exit_code, output = sandbox.exec_run(
            cmd=["bash", "-c", bash_command],
            user="root"
        )
        
        if exit_code == 0:
            return True, "Success! Server started and Firefox opened."
        else:
            return False, output.decode('utf-8')
            
    except Exception as e:
        return False, str(e)
