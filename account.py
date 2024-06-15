import streamlit as st
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

backend_url = "http://127.0.0.1:5000"

def app():
    st.title('Sign in or create an account')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'userid' not in st.session_state:
        st.session_state.userid = ''
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    def sign_up_with_email_and_password(email, password, username=None):
        try:
            payload = {
                "email": email,
                "password": password,
                "username": username
            }
            r = requests.post(f'{backend_url}/signup', json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(response['error'])
            else:
                return response.get('email')
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email, password):
        try:
            payload = {
                "email": email,
                "password": password
            }
            r = requests.post(f'{backend_url}/signin', json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(response['error'])
            else:
                user_info = {
                    'email': response['email'],
                    'username': response.get('displayName'),  # Retrieve username if available
                    'userid': response['localId']
                }
                return user_info
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            payload = {"email": email}
            r = requests.post(f'{backend_url}/reset-password', json=payload)
            response = r.json()
            if 'error' in response:
                st.warning(response['error'])
            else:
                return True, "Reset email Sent"
        except Exception as e:
            return False, str(e)

    def load_chat_from_backend(user_id):
        try:
            r = requests.get(f'{backend_url}/chat_histories', params={"user_id": user_id})
            response = r.json()
            if 'error' in response:
                st.warning(response['error'])
                return []
            user_chats = [chat for chat in response if chat['user_id'] == user_id]
            return user_chats
        except Exception as e:
            print(f'Failed to load chat history: {e}')
            return []


    def f():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.userid = userinfo['userid']
            st.session_state.chat_history = load_chat_from_backend(userinfo['userid'])

            global Usernm
            Usernm = userinfo['username']
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
        except Exception as e: 
            st.warning(f'Login Failed: {e}')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''
        st.session_state.userid = ''
        st.session_state.chat_history = []

    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            print(email)
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 
        
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:  # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")
            
            if st.button('Create my account'):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            st.button('Login', on_click=f)
            forget()
            
    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)
        
def main():
    app()

if __name__ == "__main__":
    main()
