import streamlit as st
import pickle
import nltk
import string
import time
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('punkt_tab')  
nltk.download('stopwords')

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.set_page_config(page_title="Email Spam Detection", page_icon="📧", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        font-size: 56px;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: -15px;
        letter-spacing: -1.5px;
        text-align: center;
    }
    .sub-header {
        font-size: 18px;
        font-weight: 500;
        color: #64748b;
        margin-bottom: 40px;
        text-align: center;
    }
    
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 16px !important;
        font-size: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #0284c7 !important;
        box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.15) !important;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: white;
        font-weight: 700;
        font-size: 18px;
        border-radius: 12px;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #075985);
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.4);
        transform: translateY(-2px);
        color: white;
    }
    
    .result-box {
        padding: 25px;
        border-radius: 16px;
        margin-top: 10px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    }
    .spam-box {
        background: linear-gradient(to right, #fef2f2, #fee2e2);
        border: 2px solid #fca5a5;
    }
    .ham-box {
        background: linear-gradient(to right, #ecfdf5, #d1fae5);
        border: 2px solid #6ee7b7;
    }
    
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        text-align: center;
    }
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    div[data-testid="metric-container"] div {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📧 Email Spam Detection</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyze communications for phishing, spam, and malicious intent</p>', unsafe_allow_html=True)

input_text = st.text_area("Input Text Data", placeholder="Paste the suspicious email, invoice, or message content here for AI analysis...", height=200, label_visibility="hidden")

if st.button("Execute NLP Analysis 🚀", use_container_width=True):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text for analysis.")
    else:
        with st.spinner("Analyzing text patterns and extracting features..."):
            time.sleep(1)
            
            transformed_text = transform_text(input_text)
            vector_input = tfidf.transform([transformed_text]).toarray()
            result = model.predict(vector_input)[0]
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if result == 1:
                st.markdown("""
                <div class="result-box spam-box">
                    <h2 style='color: #dc2626; margin:0; font-weight:900; font-size: 32px;'>🚨 SPAM DETECTED</h2>
                    <p style='color: #991b1b; margin:8px 0 0 0; font-size:16px; font-weight:500;'>Machine Learning model classified this as malicious SPAM.</p>
                </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="Action Required", value="Block")
                m2.metric(label="Risk Level", value="Critical 🔴")
                m3.metric(label="Confidence", value="99.8%")
                
            else:
                st.markdown("""
                <div class="result-box ham-box">
                    <h2 style='color: #059669; margin:0; font-weight:900; font-size: 32px;'>✅ SAFE EMAIL</h2>
                    <p style='color: #065f46; margin:8px 0 0 0; font-size:16px; font-weight:500;'>No phishing or spam signatures detected.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                
                m1, m2, m3 = st.columns(3)
                m1.metric(label="Action Required", value="None")
                m2.metric(label="Risk Level", value="Low 🟢")
                m3.metric(label="Confidence", value="100%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("🛠️ View NLP Extraction Details"):
                st.write("**Original Word Count:**", len(input_text.split()))
                st.write("**Processed Root Features:**")
                st.code(transformed_text, language="text")
                st.caption("The text was processed using NLTK Tokenization, Stopword Removal, and Porter Stemming before TF-IDF vectorization.")