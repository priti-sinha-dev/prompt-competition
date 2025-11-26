import streamlit as st
from groq import Groq
import json
import time

# Configure Groq API (faster and more reliable than Gemini)
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))

SCENARIOS = {
    1: """Create a Java program that validates password strength.

The program should check if a password meets security requirements.

Think about what makes a password strong or weak.""",
    
    2: """Design a smart parking system for a shopping mall.

The system should help:
- Drivers find available parking spots
- The mall manage parking efficiently
- Customers pay for parking

Describe how it would work from a driver's perspective.""",
    
    3: """Design and implement a Java program for a small library management system.

The system should:
- Store books with basic information
- Track which books are borrowed and by whom
- Handle checkout and return operations
- Search for books

Consider real-world scenarios like:
- What happens if someone tries to borrow an unavailable book?
- How do you track overdue books?
- What if multiple people want the same book?

Your solution should demonstrate good object-oriented design principles."""
}

PROMPT_EXAMPLES = {
    1: {
        "poor": "Make a password checker in Java",
        "good": "Create a Java password validator that checks: minimum 8 characters, at least one uppercase, lowercase, digit, special character. Return 'Strong', 'Medium', or 'Weak' with specific feedback.",
        "excellent": "Create a Java PasswordValidator class with a validate() method that: Returns enum (STRONG/MEDIUM/WEAK) and list of missing requirements. Checks: length≥8, uppercase, lowercase, digit, special char (!@#$%^&*). No common passwords (password123, qwerty, etc.). Include clear error messages for each failed criterion. Add JUnit test cases for edge cases."
    },
    2: {
        "poor": "Design a parking system",
        "good": "Design a smart parking system with: Entry gate scanning license plates, digital displays showing available spots, mobile app for finding your car, payment kiosks at exits.",
        "excellent": "Design a smart parking system with user flow: 1) Entry: Camera scans license, issues ticket with QR code, displays available zones. 2) Parking: LED indicators (green=free, red=occupied), mobile app shows spot number. 3) Finding car: App uses parking spot ID and provides navigation. 4) Exit: Scan QR at kiosk, calculate time-based fee, pay via card/app, gate opens. Include: real-time occupancy tracking, reserved spots for disabled/EV charging, peak hour pricing, and SMS alerts for long-duration parking."
    },
    3: {
        "poor": "Create a library program in Java",
        "good": "Create a Java library management system with Book and Member classes. Include methods for checking out, returning books, and searching. Handle cases where books are unavailable.",
        "excellent": "Create a Java library management system using OOP principles: Book class with: title, author, ISBN, availability status. Member class with: name, ID, borrowed books list. Library class with: book collection, checkout/return methods, search by title/author. Implement custom exceptions for: book not found, book unavailable, member limit exceeded. Add a waitlist queue for borrowed books. Include input validation and JUnit test cases."
    }
}

if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

def evaluate(prompt, scenario):
    try:
        # Generate code from prompt
        code_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"{scenario}\n\n{prompt}"}],
            temperature=0.7,
            max_tokens=2000
        )
        code = code_response.choices[0].message.content
        
        # Judge the code with detailed criteria
        judge_prompt = f"""Rate this code solution from 0-100 based on:
- Correctness (0-40): Does it solve the problem correctly?
- Quality (0-30): Clean, readable, well-structured code?
- Completeness (0-30): All requirements met, error handling, edge cases?

Scenario: {scenario}
Code:
{code[:1000]}

Return ONLY a valid JSON object, nothing else:
{{"total": 85, "feedback": "Excellent solution with minor improvements"}}"""
        
        judge_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0.2,
            max_tokens=200
        )
        judge_text = judge_response.choices[0].message.content.strip()
        
        # Try to parse JSON
        import re
        # Remove markdown code blocks
        judge_text = judge_text.replace('```json', '').replace('```', '').strip()
        
        try:
            score_data = json.loads(judge_text)
        except json.JSONDecodeError:
            # Try to extract JSON with regex
            json_match = re.search(r'\{[^}]*"total"\s*:\s*\d+[^}]*\}', judge_text)
            if json_match:
                score_data = json.loads(json_match.group())
            else:
                # Last resort: extract number and return
                num_match = re.search(r'\d+', judge_text)
                score = int(num_match.group()) if num_match else 70
                score_data = {"total": min(score, 100), "feedback": "Good solution!"}
        
        return score_data, code
    except Exception as e:
        return {"total": 0, "feedback": f"Error: {str(e)}"}, "Error generating code"

st.title("🏆 Prompt Competition")

tab1, tab2 = st.tabs(["Submit", "Leaderboard"])

with tab1:
    scenario = st.radio("Scenario:", [1, 2, 3], format_func=lambda x: f"Scenario {x}")
    st.info(SCENARIOS[scenario])
    name = st.text_input("Name:")
    prompt = st.text_area("Your Prompt:", height=150)
    
    if st.button("🚀 Submit", type="primary"):
        if name and prompt:
            with st.spinner("Evaluating..."):
                start = time.time()
                score_data, code = evaluate(prompt, SCENARIOS[scenario])
                elapsed = time.time() - start
                
                st.success(f"Done in {elapsed:.1f}s!")
                st.metric("Score", f"{score_data['total']}/100")
                st.write(f"**Feedback:** {score_data.get('feedback', 'N/A')}")
                
                # Suggest prompt improvements
                if score_data['total'] < 90:
                    improve_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"Original prompt: '{prompt}'\n\nSuggest 2-3 brief improvements to make this prompt clearer and more effective."}],
                        temperature=0.5,
                        max_tokens=150
                    )
                    st.info(f"💡 **Prompt Improvements:** {improve_response.choices[0].message.content}")
                
                # Show prompt quality examples
                st.write("---")
                st.write("### 📚 Prompt Quality Examples for This Scenario")
                
                examples = PROMPT_EXAMPLES[scenario]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("❌ **Poor (30-50)**")
                    st.text_area("", examples["poor"], height=120, key=f"poor_{scenario}", disabled=True, label_visibility="collapsed")
                
                with col2:
                    st.write("✅ **Good (70-85)**")
                    st.text_area("", examples["good"], height=120, key=f"good_{scenario}", disabled=True, label_visibility="collapsed")
                
                with col3:
                    st.write("🌟 **Excellent (85-100)**")
                    st.text_area("", examples["excellent"], height=120, key=f"excellent_{scenario}", disabled=True, label_visibility="collapsed")
                
                st.write("---")
                
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

