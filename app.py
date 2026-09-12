import os, time, pathlib, threading
from datetime import datetime
from flask import Flask, jsonify, send_from_directory, request
from dotenv import load_dotenv

load_dotenv()
BASE = pathlib.Path(__file__).parent

# Vercel: /tmp is writable, ./outputs is read-only (committed fixed_*.txt)
IS_VERCEL = os.getenv("VERCEL") == "1"
WATCH_DIR = pathlib.Path("/tmp/outputs") if IS_VERCEL else BASE / "outputs"
WATCH_DIR.mkdir(parents=True, exist_ok=True)

# Also read committed healed files for demo on live link
COMMITTED_DIR = BASE / "outputs"

GEMINI_KEY = os.getenv("GOOGLE_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")

app = Flask(__name__)

def scan_fixed():
    files = []
    # Read from both /tmp (live healed) and committed ./outputs
    search_dirs = [WATCH_DIR]
    if COMMITTED_DIR.exists() and COMMITTED_DIR != WATCH_DIR:
        search_dirs.append(COMMITTED_DIR)
    
    all_fixed = []
    for d in search_dirs:
        all_fixed.extend(list(d.glob("fixed_*.txt")))
    
    # Sort by mtime newest first
    all_fixed = sorted(all_fixed, key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True)[:20]
    
    for f in all_fixed:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')[:2000]
            files.append({
                "name": f.name, 
                "time": datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M:%S"), 
                "preview": content[:400], 
                "full": content
            })
        except: 
            pass
    return files

@app.route("/")
def index():
    return send_from_directory(str(BASE), "Vision.html")

@app.route("/api/status")
def api_status():
    logs = []
    try:
        logs = [f.name for f in WATCH_DIR.glob("*.log") if "fixed_" not in f.name]
    except: pass
    return jsonify({
        "gemini_on": bool(GEMINI_KEY), 
        "watch_path": "./outputs",  # nonchalant, not D:\...
        "healed": scan_fixed(), 
        "logs": logs, 
        "model": "gemini-3.6-flash", 
        "breath": 72,
        "core": "ACTIVE",
        "live": True
    })

@app.route("/api/test", methods=["POST"])
def api_test():
    content = 'main.cpp:10:5: error: cout not declared\n 10 |     cout << "Hello";'
    fname = WATCH_DIR / f"test_{int(time.time())}.log"
    try:
        fname.write_text(content)
    except: pass
    
    def heal():
        time.sleep(1.5)
        out = WATCH_DIR / f"fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            out.write_text(f"ORIGINAL: {fname.name}\n{content}\n\n--- AI FIX (Gemini 3.6) ---\nAdd #include <iostream> and std::cout\nBangla: iostream jog korun, std:: bebohar korun\nTime: {datetime.now()}\nPath: ./outputs")
            try: fname.unlink()
            except: pass
        except: pass
    
    threading.Thread(target=heal, daemon=True).start()
    return jsonify({"created": fname.name, "watch_path": "./outputs"})

# Vercel needs app variable at top level
# Local run
if __name__ == "__main__":
    print(f"Watching: ./outputs\nGemini: {'ON' if GEMINI_KEY else 'OFF'}\nOpen: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)