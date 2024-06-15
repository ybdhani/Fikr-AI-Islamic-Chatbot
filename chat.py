import streamlit as st
import requests
import uuid

def app():
    st.title("What are you thinking?")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "vector_answers" in message:
                with st.expander("See the Fikr process", expanded=False):
                    st.markdown(message["vector_answers"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = requests.post(
                "http://127.0.0.1:5000/chat",  # Replace with your Flask server URL
                json={
                    "session_id": st.session_state.session_id,
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

                if "vector_answers" in result:
                    st.session_state.messages[-1]["vector_answers"] = result["vector_answers"]
                    with st.expander("See the Fikr process", expanded=False):
                        st.markdown(result["vector_answers"])

            else:
                st.error("Error: " + response.json().get("error", "Unknown error"))

    # Floating button to move current chat to history and clear from page
    if st.button("New Chat", key="new_chat_button"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())


if __name__ == "__main__":
    app()
