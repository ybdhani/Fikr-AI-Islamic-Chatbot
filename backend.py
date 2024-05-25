from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from vecto import Vecto
import io

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Vecto
token = os.getenv("vecto_api_token")
vector_space_id = os.getenv("vector_space_id")
vs = Vecto(token, vector_space_id)

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
        {"role": "user", "content": "Generate a coherent and relevant query summarizing the key topics from the above conversation, with emphasis on the latest request. The summary should be in 10-15 words, focusing on main concepts for a vector search query."}
    )
    
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

        # Redirect the summarized query to the vector database
        query_result = lookup_vector_database(assistant_message)
        
        # Format the query results for display
        vector_related_content = "\n".join([f"Result {i+1}: {result}" for i, result in enumerate(query_result)])

        # Construct the prompt for generating the final response
        final_prompt_messages = [
            {"role": "system", "content": "You are an inventory AI that has a list of available items and expiry dates."},
            {"role": "user", "content": f"The user asked: {messages[-1]['content']}\n\nHere are the related contents:\n{vector_related_content}\n\nBased on the related content, provide a comprehensive response. If the related content does not help in answering the question, please apologize and state that the information is not sufficient to form a proper answer."}
        ]

        # Call the OpenAI API to generate the final response
        final_response = client.chat.completions.create(
            model=model,
            messages=final_prompt_messages,
            max_tokens=150,  # Adjust as needed
            temperature=0.5
        )
        # Extract the final response content
        final_assistant_message = final_response.choices[0].message.content.strip()

        return jsonify({"content": f"Vector Query Results:\n{vector_related_content}\n\nAssistant Response:\n{final_assistant_message}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def lookup_vector_database(query):
    top_k = 6
    response = vs.lookup_text_from_str(query, top_k)
    return response

if __name__ == '__main__':
    app.run(debug=True)
