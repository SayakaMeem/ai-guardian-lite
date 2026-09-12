# AI Guardian Lite — DevOps Watcher

> **Pipeline: WOUND → WATCH → HEAL**
> A silent guardian that watches logs, thinks with Gemini 3.6, and heals itself.

Live DevOps watcher with meaning-driven UI. No raw paths. Just flow: log → eye → brain → fix.

**Repo:** https://github.com/SayakaMeem/ai-guardian-lite

---

### Meaning Pipeline

```
INCOMING — WOUNDS          THE GUARDIAN          HEALED
outputs/*.log       →    Eye sees, Brain thinks    →  fixed_*.txt
```

- **WOUND:** Error log drops into outputs/
- **WATCH:** Flask polls /api/status every 2s
- **HEAL:** Gemini 3.6 writes sutured fix EN+BN

### Quick Start
```bash
git clone https://github.com/SayakaMeem/ai-guardian-lite.git
cd ai-guardian-lite
copy .env.example .env
# Add key from https://aistudio.google.com/app/apikey
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000 - CORE ACTIVE
```

### Structure
```
Vision.html  # Pipeline UI
app.py       # Flask :5000
 guardian.py  # Watcher + Gemini
.env.example # Template
outputs/fixed_*.txt
```

Built nonchalant. Flow: log → eye → brain → fix.
