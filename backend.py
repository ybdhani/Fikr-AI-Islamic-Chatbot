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

    # Construct the prompt for summarization
    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    prompt_messages.extend(messages)
    prompt_messages.append(
        {"role": "user", "content": "Summarize the key topics and concepts from the above conversation in 10-15 words for a vector search query, put emphasis on the latest request. If the prompts are significantly unrelated, choose the later topics"}
    )
    
    print(prompt_messages)
    try:
        # Call the OpenAI API to get the summary
        response = client.chat.completions.create(
            model=model,
            messages=prompt_messages,
            max_tokens=30,  # Set max_tokens to limit the response length
            temperature=0.5
        )
        # Extract the summarized content from the response
        assistant_message = response.choices[0].message.content.strip()
        
        print(messages)
        return jsonify({"content": assistant_message})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
