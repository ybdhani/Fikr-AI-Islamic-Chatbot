Introduction

Fikr is an experimental project aimed at leveraging cutting-edge AI technology to assist with answering Islamic questions. It's designed to serve as a step forward in integrating vector search and large language models (LLMs) for Islamic studies. Fikr currently supports a self-loaded vector database of Hadiths, containing texts from the six primary Hadith collections, which were scraped from qaalarasulallah.com and sourced from a Kaggle dataset (Hadith Dataset). While Fikr provides accurate information sourced from trusted Hadith collections, it is not a substitute for consulting a qualified scholar or fatwa giver.
Explanation of Main Files
1. about.py

The about.py file is responsible for displaying information about the Fikr project in the web application. It uses Streamlit to create a simple user interface with custom CSS for styling. Key components include:

    HTML/CSS for Styling: Custom styles are defined to enhance the visual appearance of the page.
    Markdown Sections: Information about Fikr and its vector search capabilities is presented using Markdown.
    Image Display: An illustrative image of vector search is included.

2. account.py

The account.py file manages user authentication, including sign-up, sign-in, and password reset functionalities. It interacts with a backend server for these operations. Key functions and components include:

    Session Management: Tracks user session states (e.g., username, useremail, userid, chat_history).
    Sign-Up and Sign-In Functions: Communicates with the backend to create and authenticate user accounts.
    Password Reset: Allows users to request a password reset link.
    Chat History Loading: Retrieves and displays chat history for logged-in users.

3. main.py

The main.py file serves as the entry point for the Streamlit web application. It integrates different modules and sets up the user interface. Key components include:

    Custom CSS: Sets global styles for the application.
    MultiApp Class: Manages the navigation between different app modules (about, account, history, chat).
    Sidebar Menu: Provides navigation options for the user to switch between different sections of the app.

4. backend.py

The backend.py file implements the backend server using Flask. It handles various API endpoints for user authentication, chat functionality, and chat history management. Key functionalities include:

    Firebase Integration: Uses Firebase for storing user data and chat histories.
    OpenAI Integration: Utilizes OpenAI's API to generate responses and summaries.
    Vector Search: Implements a vector search mechanism using Vecto for retrieving relevant Hadiths based on user queries.
    API Endpoints:
        /signup: Handles user registration.
        /signin: Manages user login.
        /reset-password: Sends password reset emails.
        /chat: Processes chat interactions and retrieves relevant Hadiths.
        /chat_histories: Retrieves summaries of user chat histories.
        /chat_history/<user_id>/<session_id>: Retrieves detailed chat history for a specific session.

5. history.py

The history.py file manages the display of user chat histories in the Streamlit app. It allows users to view and load past chat sessions. Key components include:

    Chat History Retrieval: Fetches chat summaries from the backend.
    Chat Detail Loading: Loads and displays detailed chat messages for a selected session.

6. chat.py

The chat.py file is responsible for the core chat functionality. It interacts with the backend to send user messages and receive AI-generated responses. It also handles displaying the conversation in the Streamlit app.
Methodology and How It Works

Fikr operates by integrating several advanced technologies and methodologies:

    User Interaction: Users interact with the Fikr app through a Streamlit-based web interface. They can sign up, log in, ask questions, and view their chat histories.

    Backend Processing:
        User Authentication: Managed using Firebase, allowing secure sign-up, sign-in, and password reset functionalities.
        Chat Handling: User messages are processed by the backend. The messages are summarized and used to query a vector database of Hadiths.
        Vector Search: The summarized query is transformed into numerical vectors and searched within the vector database using Vecto.
        AI Response Generation: OpenAI's API generates initial and refined responses based on the retrieved Hadiths and the user's question.

    Chat History Management: Chat histories are stored in Firebase and can be retrieved and displayed in the Streamlit app, allowing users to revisit past interactions.

By combining vector search with LLMs, Fikr aims to provide precise and contextually relevant answers to Islamic questions, showcasing the potential of AI in enhancing Islamic studies and research.
How to Launch the Streamlit App

To launch the Fikr Streamlit app, follow these steps:

    Clone the Repository:

    bash

git clone https://github.com/yourusername/fikr.git
cd fikr

Create a Virtual Environment:

bash

python -m venv venv

Activate the Virtual Environment:

    On Windows:

    bash

venv\Scripts\activate

On macOS/Linux:

bash

    source venv/bin/activate

Install Required Libraries:

bash

pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory with the following content:

env

FIREBASE_API_KEY=your_firebase_api_key
OPENAI_API_KEY=your_openai_api_key
vecto_api_token=your_vecto_api_token
vector_space_id=your_vector_space_id

Ensure Firebase Credentials File:
Ensure you have your Firebase credentials file (logintest-12b8b-e89e95a21c52.json) in the root directory.

Run the Backend Server:

bash

python backend.py

Run the Streamlit App:
In a new terminal window (with the virtual environment activated), run:

bash

    streamlit run main.py

The Streamlit app will launch locally and can be accessed in your browser at http://localhost:8501.
