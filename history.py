import streamlit as st
import requests

def app():
    st.title("Chat History")

    if 'userid' not in st.session_state or not st.session_state.userid:
        st.warning("You need to be signed in to see the chat history.")
        return

    history_endpoint = "http://localhost:5000/chat_histories"
    chat_history_endpoint = "http://localhost:5000/chat_history"

    if "loaded_chat" not in st.session_state:
        st.session_state.loaded_chat = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    try:
        response = requests.get(history_endpoint, params={"user_id": st.session_state.userid})
        if response.status_code == 200:
            history = response.json()
            if history:
                selected_summary = st.selectbox(
                    "Select a chat history summary to load:",
                    options=[f"{entry['timestamp']} - {entry['summary']} ({entry['session_id']})" for entry in history]
                )
                if selected_summary:
                    selected_uuid = selected_summary.split(' (')[-1][:-1]
                    if st.button("Load Selected Chat History"):
                        chat_response = requests.get(f"{chat_history_endpoint}/{selected_uuid}")
                        if chat_response.status_code == 200:
                            chat_messages = chat_response.json()
                            st.session_state.messages = chat_messages
                            st.session_state.loaded_chat = True
                            st.success("Chat loaded successfully")
                            st.experimental_rerun()
                        else:
                            st.error("Error loading chat history.")
            else:
                st.write("No chat history available.")
        else:
            st.error("Error fetching chat summaries.")
    except Exception as e:
        st.error(f"Error loading chat history: {e}")

    if st.session_state.loaded_chat and st.session_state.messages:
        st.write("### Chat Messages")
        for message in st.session_state.messages:
            st.write(f"{message['role']}: {message['content']}")

if __name__ == "__main__":
    app()
