import os, re, time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
BASE = Path(__file__).parent
WATCH_DIR = Path(os.getenv("WATCH_PATH", BASE / "outputs"))
WATCH_DIR.mkdir(parents=True, exist_ok=True)
GEMINI_KEY = os.getenv("GOOGLE_API_KEY")
POLL_SEC = int(os.getenv("POLL_SEC", "2"))

print(f"--- AI Guardian Lite v4 + GEMINI 3.6 ---")
print(f"Watching: {WATCH_DIR}")
print(f"Gemini: {'ON' if GEMINI_KEY and 'your_gemini' not in GEMINI_KEY else 'OFF'}")

def ask_gemini(log_content):
    if not GEMINI_KEY or "your_gemini" in GEMINI_KEY:
        return None
    try:
        # NEW library Google wants in 2026
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)
        
        # Model name Google told you in error: gemini-3.6-flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # try 2.5-flash first, if fails use 3.6-flash
            contents=f"You are DevOps Guardian. Error:\n{log_content[:2000]}\n\nGive FIX: in English + Bangla: in 2 lines."
        )
        return response.text
    except Exception as e:
        print(f"Gemini failed: {e}, trying 3.6-flash...")
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=f"Fix this build error in 2 lines English + Bangla:\n{log_content[:2000]}"
            )
            return response.text
        except Exception as e2:
            print(f"Also failed: {e2}, using regex")
            return None

def regex_fix(content):
    if "stdio.h" in content: return "FIX: Use #include <cstdio> for C++\nBangla: C++ te <cstdio> use korun"
    if "stray" in content: return "FIX: Remove smart quotes\nBangla: Smart quote delete korun"
    return "FIX: Check line number for syntax error\nBangla: Line number dekhe thik korun"

while True:
    for log_file in WATCH_DIR.glob("*.log"):
        if "fixed_" in log_file.name: continue
        content = log_file.read_text(errors='ignore').strip()
        if not content: continue
        print(f"New log: {log_file.name}")
        ai_fix = ask_gemini(content)
        final_fix = ai_fix if ai_fix else regex_fix(content)
        out = WATCH_DIR / f"fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        out.write_text(f"ORIGINAL: {log_file.name}\n{content}\n\n--- AI FIX ---\n{final_fix}\nTime: {datetime.now()}\n", encoding='utf-8')
        print(f"[FIXED] -> {out.name}\n{final_fix[:150]}...")
        log_file.unlink(missing_ok=True)
    time.sleep(POLL_SEC)