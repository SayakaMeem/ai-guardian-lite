@echo off
echo Starting AI Guardian Lite...
cd /d D:\GitProjects\ai-guardian-lite
if not exist outputs mkdir outputs
python guardian.py
pause