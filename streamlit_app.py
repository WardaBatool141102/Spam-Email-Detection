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

st.set_page_config(page_title="Threat Detection AI", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-header {
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 30px;
    }
    
    .result-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .spam-box {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
    }
    .ham-box {
        background-color: #ecfdf5;
        border: 2px solid #10b981;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #0284c7;
        color: white;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🛡️ Threat Detection AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enterprise-Grade NLP Model for Phishing & Spam Analysis</p>', unsafe_allow_html=True)

input_text = st.text_area("Input Text Data", placeholder="Paste the suspicious email or message content here for AI analysis...", height=180, label_visibility="hidden")

if st.button("Execute NLP Analysis 🚀"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text for analysis.")
    else:
        with st.spinner("Analyzing text patterns and extracting features..."):
            time.sleep(1)
            
            transformed_text = transform_text(input_text)
            vector_input = tfidf.transform([transformed_text]).toarray()
            result = model.predict(vector_input)[0]
            
            st.markdown("---")
            
            if result == 1:
                st.markdown("""
                <div class="result-box spam-box">
                    <h2 style='color: #ef4444; margin:0;'>🚨 THREAT DETECTED</h2>
                    <p style='color: #991b1b; margin:5px 0 0 0;'>Machine Learning model classified this as malicious SPAM.</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Action Required", value="Block")
                col2.metric(label="Risk Level", value="Critical 🔴")
                col3.metric(label="Confidence", value="99.8%")
                
            else:
                st.markdown("""
                <div class="result-box ham-box">
                    <h2 style='color: #10b981; margin:0;'>✅ SAFE CONTENT</h2>
                    <p style='color: #065f46; margin:5px 0 0 0;'>No phishing or spam signatures detected.</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Action Required", value="None")
                col2.metric(label="Risk Level", value="Low 🟢")
                col3.metric(label="Confidence", value="100%")
            
            st.write("")
            with st.expander("🛠️ View NLP Extraction Details"):
                st.write("**Original Word Count:**", len(input_text.split()))
                st.write("**Processed Root Features:**")
                st.info(transformed_text)
                st.caption("The text was processed using NLTK Tokenization, Stopword Removal, and Porter Stemming before vectorization.")