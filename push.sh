#!/bin/bash
cd /c/Users/vranjan/prompt-competition
git add app.py
git commit -m "Update to gemini-pro model"
git push origin main
echo "Push completed!"
git log --oneline -1

