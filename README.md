# 🏆 Prompt Engineering Competition

A simple, free, and instant-scoring prompt competition platform using Streamlit + Google Gemini.

## Features
- ✅ **100% FREE** - Uses Groq's free tier (30 req/min = 1,800/hour)
- ⚡ **Ultra-fast scoring** - Under 1 second response time!
- 🏆 **Live leaderboard** - Real-time rankings
- 📊 **Handles 50+ users** easily

## Quick Setup

### Get Free Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. This repo is already set up for deployment
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add `GROQ_API_KEY` in Secrets
5. Deploy! ✨

## Customize Scenarios

Edit `SCENARIOS` dict in `app.py`:
```python
SCENARIOS = {
    1: "Your first coding challenge description",
    2: "Your second coding challenge description"
}
```

