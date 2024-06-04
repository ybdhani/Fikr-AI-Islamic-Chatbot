import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

firebase_api_key = os.getenv("FIREBASE_API_KEY")

cred = credentials.Certificate("logintest-12b8b-e89e95a21c52.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            print('payload sigin',payload)
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName'),  # Retrieve username if available
                    'userid': data['localId']
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": firebase_api_key}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    def save_chat_to_firestore(user_id, message):
        try:
            doc_ref = db.collection("chats").document(user_id)
            doc_ref.update({
                "messages": firestore.ArrayUnion([message])
            })
        except:
            doc_ref.set({
                "messages": [message]
            })

    def load_chat_from_firestore(user_id):
        try:
            doc_ref = db.collection("chats").document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict().get("messages", [])
            else:
                return []
        except Exception as e:
            st.warning(f'Failed to load chat history: {e}')
            return []

    def f():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.userid = userinfo['userid']
            st.session_state.chat_history = load_chat_from_firestore(userinfo['userid'])

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
        
    if "signedout"  not in st.session_state:
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
        
        st.write("Chat History:")
        for message in st.session_state.chat_history:
            st.write(message)

        new_message = st.text_input("Type your message:")
        if st.button("Send"):
            if new_message:
                save_chat_to_firestore(st.session_state.userid, new_message)
                st.session_state.chat_history.append(new_message)

def main():
    app()

if __name__ == "__main__":
    main()
