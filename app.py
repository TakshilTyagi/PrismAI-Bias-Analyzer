import streamlit as st
import google.generativeai as genai
genai.configure(api_key="AIzaSyDHZuOf0vn_tYSrWWoC1PXDV8yDM3Zxo4A")
model = genai.GenerativeModel("models/gemini-2.5-flash")
st.set_page_config(page_title="PrismAI", page_icon="", layout="centered")
st.markdown("""
<style>`
header {visibility: hidden;}
footer {visibility: hidden;}
.stApp {
    background-color: #0e1117;
    color: white;
}
.big-title {
    font-size: 3.5rem;
    font-weight: 750;
    text-align: center;
}
.sub-title {
    font-size: 1.1rem;
    text-align: center;
    color: #b0b3b8;
}
/* Center text */
.center {
    text-align: center;
}
label {
    color: #ffffff !important;
    font-weight: 500;
    font-size: 15px;
}
textarea, input {
    background-color: #1c1f26 !important;
    color: white !important;
    border-radius: 8px;
}
.stButton>button {
    background-color: #262730;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #3a3b45;
}
.stProgress > div > div {
    background-color: #4cafef;
}
label {
    color: #ffffff !important;
    font-weight: 500;
    font-size: 15px;
}
textarea, input {
    background-color: #1c1f26 !important;
    color: white !important;
    caret-color: white !important;
    border: 1px solid #2c2f3a !important;
    border-radius: 8px;
}
.stDownloadButton>button {
    background-color: #4cafef !important;
    color: white !important;
    border-radius: 8px;
    height: 3em;
    font-size: 15px;
    border: none !important;
}
.stDownloadButton>button:hover {
    background-color: #3a9bdc !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="big-title"> Prism AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered BIAS detection for fair communication</div>', unsafe_allow_html=True)
username = st.text_input("Enter your name")
if username:
    st.markdown(f"<div class='center'>Welcome, <b>{username}</b> 👋</div>", unsafe_allow_html=True)
st.divider()
text = st.text_area("Enter text to analyze", height=100)
audio = st.audio_input("Dictate Your Text")
if audio is not None:
    st.audio(audio)
    st.info("This feature does not exist for now.")
col1, col2, col3 = st.columns([1,2,1])
with col2:
    analyze_clicked = st.button("Analyze Text for BIAS", use_container_width=True)
if analyze_clicked:
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"""
Analyze the following text for bias:
{text}
Return in this exact format:
Bias Level: <Low / Medium / High>
Bias Type: <type>
Confidence Score: <0-100%>
Explanation: <4 lines>
Neutral Version: <rewrite>
"""

            response = model.generate_content(prompt)

        st.divider()
        st.subheader(" Analysis Result")

        output = response.text.strip()
        lines = output.split("\n")
        data = {
            "Bias Level": "",
            "Bias Type": "",
            "Confidence Score": "",
            "Explanation": "",
            "Neutral Version": ""
        }
        current = None
        for line in lines:
            for key in data:
                if line.startswith(key):
                    data[key] = line.split(":",1)[1].strip()
                    current = key
                    break
            else:
                if current:
                    data[current] += " " + line.strip()
        bias_map = {
            "Low": 30,
            "Medium": 60,
            "High": 90
        }
        level = data["Bias Level"].capitalize()
        score = bias_map.get(level, 50)
        st.write("###Bias Score")
        st.progress(score)
        st.write(f"Bias Level: **{level} ({score}%)**")
        confidence = data["Confidence Score"] if data["Confidence Score"] else "N/A"
        st.metric(" Confidence Score", confidence)
        st.info(f"🔵 Bias Type: {data['Bias Type']}")
        st.write("📖 **Explanation**")
        st.write(data["Explanation"])
        st.success("✅ Neutral Version")
        st.write(data["Neutral Version"])
        report = f"""
User: {username}
Original Text:
{text}
Bias Level: {level}
Bias Type: {data['Bias Type']}
Confidence Score: {confidence}
Explanation:
{data['Explanation']}
Neutral Version:
{data['Neutral Version']}
"""
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name="bias_report.txt"
        )
st.divider()
st.markdown("<div class='center'>BUILT BY TAKSHIL BHARDWAJ </div>", unsafe_allow_html=True)
# redeploy trigger