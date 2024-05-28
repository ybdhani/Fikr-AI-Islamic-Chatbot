import streamlit as st
import json

def app():
    st.title("Chat History")

    history_file = "chat_history.json"

    try:
        with open(history_file, "r") as f:
            history = [json.loads(line) for line in f]

        if history:
            for entry in history:
                st.write(f"**{entry['role'].capitalize()} ({entry['timestamp']}):** {entry['content']}")
        else:
            st.write("No chat history available.")
    except FileNotFoundError:
        st.write("Chat history file not found.")
    except Exception as e:
        st.write(f"Error loading chat history: {e}")

if __name__ == "__main__":
    app()
