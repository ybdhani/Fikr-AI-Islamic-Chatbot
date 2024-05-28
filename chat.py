import streamlit as st
import requests

def app():
    st.title("What are you thinking?")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = requests.post(
                "http://127.0.0.1:5000/chat",  # Replace with your Flask server URL
                json={
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    "model": st.session_state["openai_model"]
                }
            )

            if response.status_code == 200:
                result = response.json()
                st.markdown(result["content"])
                st.session_state.messages.append({"role": "assistant", "content": result["content"]})
            else:
                st.error("Error: " + response.json().get("error", "Unknown error"))

if __name__ == "__main__":
    app()
