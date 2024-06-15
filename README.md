Fikr - AI-Powered Islamic Chatbot

Welcome to Fikr, an AI-powered chatbot designed to assist with answering Islamic questions. This guide will help you set up and run the Fikr application.
Prerequisites

Before you begin, ensure you have the following installed:

    Python 3.8 or later
    pip (Python package installer)

Installation

    Clone the repository to your local machine:

    sh

git clone https://github.com/yourusername/fikr.git
cd fikr

Install the required Python packages:

sh

pip install -r requirements.txt

Create a .env file in the root directory of the project and add your API keys and Firebase credentials. Example:

makefile

    FIREBASE_API_KEY=your_firebase_api_key
    OPENAI_API_KEY=your_openai_api_key
    vecto_api_token=your_vecto_api_token
    vector_space_id=your_vector_space_id

    Also, ensure you have your Firebase credentials file (logintest-12b8b-e89e95a21c52.json) in the root directory.

Running the Application
Backend

    Start the backend server:

    sh

    python backend.py

    The backend server will run on http://127.0.0.1:5000.

Frontend

    Launch the Streamlit application:

    sh

    streamlit run main.py

    Open your web browser and go to http://localhost:8501 to access the Fikr application.

Usage

    About: Learn about the Fikr application and its features.
    Account: Sign in or create a new account to use the chatbot. You can also reset your password here.
    History: View your previous chat sessions.
    Chat: Interact with the Fikr chatbot to get answers to your Islamic questions.

Troubleshooting

    Ensure all environment variables are correctly set in the .env file.
    Make sure the backend server is running before starting the Streamlit app.
    Check the terminal/console for any error messages and address them accordingly.

Contributing

We welcome contributions! Please read our Contributing Guide for more details.
License

This project is licensed under the MIT License - see the LICENSE file for details.

Thank you for using Fikr! If you have any questions or feedback, feel free to reach out.