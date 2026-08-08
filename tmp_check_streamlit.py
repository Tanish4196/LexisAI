import os
import sys
import subprocess
import time
from pathlib import Path

os.chdir(r'C:\Users\sharm\OneDrive\Desktop\Leagal-RAG')
print('cwd:', os.getcwd())
print('app exists:', Path('app.py').exists())
print('.env exists:', Path('.env').exists())
print('.env.example exists:', Path('.env.example').exists())
print('OPENROUTER_API_KEY env present:', bool(os.getenv('OPENROUTER_API_KEY')))
try:
    from src.config import get_openrouter_api_key
    print('config.get_openrouter_api_key():', bool(get_openrouter_api_key()))
except Exception as e:
    print('config import failed:', e)

cmd = [sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.headless', 'true', '--server.port', '8501']
print('cmd:', cmd)
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    time.sleep(10)
    out = proc.stdout.read(16384)
    print('output len:', len(out))
    print(out)
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    print('returncode:', proc.returncode)
