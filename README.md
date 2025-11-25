# 🏆 Prompt Engineering Competition

A simple, free, and instant-scoring prompt competition platform using Streamlit + Google Gemini.

## Features
- ✅ **100% FREE** - Uses Gemini's free tier (1,500 requests/day)
- ⚡ **Instant scoring** - 2-4 second response time
- 🏆 **Live leaderboard** - Real-time rankings
- 📊 **Handles 50+ users** easily

## Quick Setup

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. This repo is already set up for deployment
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add `GEMINI_API_KEY` in Secrets
5. Deploy! ✨

## Customize Scenarios

Edit `SCENARIOS` dict in `app.py`:
```python
SCENARIOS = {
    1: "Your first coding challenge description",
    2: "Your second coding challenge description"
}
```

