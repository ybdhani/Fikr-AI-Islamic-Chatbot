import streamlit as st

def app():
    st.markdown("""
    <style>
    :root {
        --border-radius: 10px;
    }

    .main {
        padding: 0 20px 20px 20px; /* Removed top padding */
        border-radius: var (--border-radius);
        text-align: center;
    }
    .title {
        font-size: 36px;
        margin-bottom: 20px;
    }
    .content {
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 20px; /* Added margin-bottom for spacing */
    }
    .vector-image {
        text-align: center;
        margin-top: 20px;
    }
    .vector-image img {
        max-width: 60%;
        height: auto;
        border-radius: var(--border-radius);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main'>", unsafe_allow_html=True)
    
    st.markdown("<div class='title'>About Fikr</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='content'>
        Fikr is an advanced AI-powered chatbot designed to assist with answering Islamic questions. 
        While it provides accurate information sourced from trusted Hadith collections, it is not a substitute for a scholar or fatwa giver. 
        So far, the chatbot has been supplied with a hadith dataset containing all Hadiths from the six primary hadith collections. 
        The data is scraped from <a href='http://qaalarasulallah.com/' target='_blank'>qaalarasulallah.com</a>.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='title'>Vector Search</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='content'>
        Vector search is a sophisticated method of information retrieval that converts text into numerical vectors, capturing semantic meaning. 
        This allows Fikr to perform precise and contextually relevant searches across its database of Islamic texts.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    st.image('Vector_search.png', caption='Vector Space Illustration')

if __name__ == "__main__":
    app()
