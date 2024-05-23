from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "gpt-3.5-turbo")

    try:
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False  # Stream is set to False to get the full response at once
        )
        # Extract the message content from the response
        assistant_message = response.choices[0].message.content
        
        return jsonify({"content": assistant_message})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
