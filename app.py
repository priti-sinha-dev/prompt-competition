import streamlit as st
import google.generativeai as genai
import json
import time

# Configure Gemini API
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

SCENARIOS = {
    1: "Create a REST API endpoint in Python that handles user authentication with JWT tokens and rate limiting.",
    2: "Build a responsive product card component in React that shows product image, price, rating, and add-to-cart button."
}

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

def evaluate(prompt, scenario):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        code = model.generate_content(f"{scenario}\n\n{prompt}").text
        judge = model.generate_content(f"Rate 0-100: {code[:500]}. Return JSON: {{'total': number, 'feedback': 'text'}}").text
        try:
            return json.loads(judge.strip().replace('```json', '').replace('```', '')), code
        except:
            return {"total": 50, "feedback": "Parse error"}, code
    except Exception as e:
        # Fallback debugging
        return {"total": 0, "feedback": f"Error: {str(e)}"}, "Error generating code"

st.title("🏆 Prompt Competition")

tab1, tab2 = st.tabs(["Submit", "Leaderboard"])

with tab1:
    scenario = st.radio("Scenario:", [1, 2])
    st.info(SCENARIOS[scenario])
    name = st.text_input("Name:")
    prompt = st.text_area("Your Prompt:", height=100)
    
    if st.button("🚀 Submit", type="primary"):
        if name and prompt:
            with st.spinner("Evaluating..."):
                start = time.time()
                score_data, code = evaluate(prompt, SCENARIOS[scenario])
                elapsed = time.time() - start
                
                st.success(f"Done in {elapsed:.1f}s!")
                st.metric("Score", f"{score_data['total']}/100")
                st.write(f"**Feedback:** {score_data.get('feedback', 'N/A')}")
                
                with st.expander("Generated Code"):
                    st.code(code)
                
                st.session_state.leaderboard.append({
                    'name': name, 'scenario': scenario, 
                    'score': score_data['total']
                })
        else:
            st.error("Fill all fields!")

with tab2:
    if st.session_state.leaderboard:
        sorted_lb = sorted(st.session_state.leaderboard, key=lambda x: x['score'], reverse=True)
        for i, e in enumerate(sorted_lb[:10]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            st.write(f"{medal} **{e['name']}** - {e['score']} pts (Scenario {e['scenario']})")
    else:
        st.info("No submissions yet!")

