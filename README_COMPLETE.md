# AI DevOps Guardian Lite - Complete Guide
Location: D:\GitProjects\ai-guardian-lite
Goal: 0% C: drive usage, 100% on D:

## PROJECT NAME
ai-guardian-lite

## DEPENDENCY GUIDE
1. Node.js LTS (v18 or v20) - https://nodejs.org/
   Check: node -v , npm -v
2. n8n - installed via npx, no global install needed
3. Google Gemini API (free) - https://aistudio.google.com/app/apikey

## INSTALLATION - FROM ZERO

Step 0 - Check Node:
Open PowerShell:
  node -v
  npm -v
If not found, install Node.js LTS and restart PowerShell.

Step 1 - Create folders (ALL IN D):
  mkdir D:\GitProjects
  mkdir D:\GitProjects\ai-guardian-lite
  mkdir D:\GitProjects\ai-guardian-lite\outputs
  mkdir D:\GitProjects\ai-guardian-lite\n8n-data

Step 2 - Go to project:
  cd D:\GitProjects\ai-guardian-lite

Step 3 - Copy these files into D:\GitProjects\ai-guardian-lite:
  - package.json
  - workflow.json
  - .env.example -> rename to .env and put your Gemini key
  - START.bat

Step 4 - Install n8n (first time only, ~1 min):
  npm install
  OR just use: npx n8n --version

Step 5 - Start (D drive only mode):
  Double-click START.bat
  OR run in PowerShell:
  $env:N8N_USER_FOLDER="D:\GitProjects\ai-guardian-lite\n8n-data"
  $env:N8N_DIAGNOSTICS_ENABLED="false"
  npx n8n start

Step 6 - Open browser:
  http://localhost:5678
  Create owner account (admin@d.local / Admin1234)

Step 7 - Import workflow:
  n8n -> Import from File -> workflow.json
  Open node "Gemini Fix It" -> Create Credential -> paste Gemini API key
  Toggle workflow to ACTIVE

Step 8 - Test:
  Create file D:\GitProjects\ai-guardian-lite\outputs\error.txt
  Content: error: expected ';' before '}' token
  n8n will create fixed_*.txt with fix in same folder.

## FOLDER STRUCTURE
D:\GitProjects\ai-guardian-lite\
  ├─ n8n-data\         <- DB, workflows, creds (NEVER on C:)
  ├─ outputs\           <- compiler logs IN, fixes OUT
  ├─ workflow.json
  ├─ package.json
  ├─ .env
  └─ START.bat

## DAILY USE
Just double-click START.bat. Keep cmd window minimized. Open localhost:5678.

To stop: Press Ctrl+C in cmd window.

## IMPORTANT
- Never install n8n globally (npm i -g n8n) -> that goes to C:
- Always use npx n8n start with N8N_USER_FOLDER set to D:
- Everything you need is in D:\GitProjects
