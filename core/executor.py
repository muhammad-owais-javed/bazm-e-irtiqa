import docker
import base64

client = docker.from_env()

def execute_in_sandbox(code_string):
    """Robust Python-based execution monitor."""
    try:
        sandbox = client.containers.get('visual-sandbox')
        encoded_code = base64.b64encode(code_string.encode('utf-8')).decode('utf-8')
        
        # We switch to 'midori' - a lightweight browser that doesn't use Snap!
        test_script = f"""
import base64, subprocess, time, urllib.request

code = base64.b64decode("{encoded_code}").decode('utf-8')
with open('/tmp/app.py', 'w') as f:
    f.write(code)

# Install Midori instead of Firefox
subprocess.run(['apt-get', 'update', '-qq'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(['apt-get', 'install', '-y', 'python3-pip', 'midori', 'psmisc', '-qq'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(['pip3', 'install', 'flask', 'requests', '-q'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run(['pkill', '-f', 'app.py'])

process = subprocess.Popen(['python3', '/tmp/app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(3)

if process.poll() is not None:
    out, _ = process.communicate()
    print("CRASH: " + out.decode('utf-8'))
    exit(1)

try:
    urllib.request.urlopen("http://127.0.0.1:5000", timeout=3 )
    print("SUCCESS")
except Exception as e:
    print(f"CRASH: Server running, but port 5000 failed: {{e}}")
    process.terminate()
    exit(1)
"""
        encoded_tester = base64.b64encode(test_script.encode('utf-8')).decode('utf-8')
        bash_cmd = f"echo '{encoded_tester}' | base64 -d > /tmp/tester.py && python3 /tmp/tester.py"
        
        exit_code, output = sandbox.exec_run(cmd=["bash", "-c", bash_cmd], user="root")
        
        if "SUCCESS" in output.decode('utf-8'):
            # Docker's native way to launch a detached GUI app cleanly!
            sandbox.exec_run(
                cmd=["midori", "http://127.0.0.1:5000"],
                environment={"DISPLAY": ":1"},
                user="root",
                detach=True
             )
            return True, "Server started perfectly."
        else:
            return False, output.decode('utf-8')
            
    except Exception as e:
        return False, str(e)
