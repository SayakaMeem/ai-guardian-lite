import os, time, pathlib, threading
from datetime import datetime
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
BASE = pathlib.Path(__file__).parent
WATCH_DIR = BASE / "outputs"
WATCH_DIR.mkdir(parents=True, exist_ok=True)
GEMINI_KEY = os.getenv("GOOGLE_API_KEY", "")

app = Flask(__name__)
CORS(app)

def scan_fixed():
    files = []
    for f in sorted(WATCH_DIR.glob("fixed_*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')[:2000]
            files.append({"name": f.name, "time": datetime.fromtimestamp(f.stat().st_mtime).strftime("%H:%M:%S"), "preview": content[:400], "full": content})
        except: pass
    return files

@app.route("/")
def index():
    return send_from_directory(str(BASE), "Vision.html")

@app.route("/api/status")
def api_status():
    logs = [f.name for f in WATCH_DIR.glob("*.log") if "fixed_" not in f.name]
    return jsonify({"gemini_on": bool(GEMINI_KEY), "watch_path": str(WATCH_DIR), "healed": scan_fixed(), "logs": logs, "model": "gemini-3.6-flash", "breath": 72})

@app.route("/api/test", methods=["POST"])
def api_test():
    content = 'main.cpp:10:5: error: cout not declared\n 10 |     cout << "Hello";'
    fname = WATCH_DIR / f"test_{int(time.time())}.log"
    fname.write_text(content)
    def heal():
        time.sleep(1.5)
        out = WATCH_DIR / f"fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        out.write_text(f"ORIGINAL: {fname.name}\n{content}\n\n--- AI FIX (Gemini 3.6) ---\nAdd #include <iostream> and std::cout\nBangla: iostream jog korun\nTime: {datetime.now()}")
        try: fname.unlink()
        except: pass
    threading.Thread(target=heal, daemon=True).start()
    return jsonify({"created": fname.name})

if __name__ == "__main__":
    print(f"Watching: {WATCH_DIR}\nGemini: {'ON' if GEMINI_KEY else 'OFF'}\nOpen: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)