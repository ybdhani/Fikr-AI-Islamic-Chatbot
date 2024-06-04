import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.app_logo import add_logo
import os
from dotenv import load_dotenv
load_dotenv()

# Import your different app modules
import about, history, account, chat

# Set the page config
st.set_page_config(
    page_title="Fikr",
)

# Define a custom CSS style with your font
custom_css = """
    <style>
        /* Set the font-family to your imported font */
        body {
            font-family: 'Encode Sans Condensed', sans-serif;
        }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            # Display the logo image
            st.image("blackfikrlogo.png", use_column_width=True)

            app = option_menu(
                menu_title='',
                options=['About', 'Account', 'History', 'Chat'],
                icons=['info-circle-fill', 'person-circle', 'clock-history', 'chat-left-dots'],
                menu_icon='',
                default_index=1,
                styles={
                    "container": {"padding": "5!important"},
                    "icon": {"font-size": "23px"},
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "3px", "--hover-color": "#d2d2d2"},
                    "nav-link-selected": {"background-color": "#f76d4f"},
                }
            )

        if app == 'About':
            about.app()
        elif app == "Account":
            account.app()
        elif app == "History":
            history.app()
        elif app == 'Chat':
            chat.app()

# Initialize and run the app
app = MultiApp()
app.run()
