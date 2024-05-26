from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from vecto import Vecto

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

    user_question = messages[-1]['content']

    try:
        # Use ChatGPT to answer the user's question based on current knowledge
        initial_response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150,  # Adjust as needed
            temperature=0.5
        )
        initial_answer = initial_response.choices[0].message.content.strip()

        # Construct the prompt for summarization
        prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following question in 10-15 words for a vector search query: {user_question}"}
        ]
        
        # Call the OpenAI API to get the summary
        summary_response = client.chat.completions.create(
            model=model,
            messages=prompt_messages,
            max_tokens=30,  # Set max_tokens to limit the response length
            temperature=0.5
        )
        # Extract the summarized content from the response
        summarized_query = summary_response.choices[0].message.content.strip()

        # Replace \u200f with spaces
        summarized_query_cleaned = summarized_query.replace('\u200f', ' ')

        # Redirect the summarized query to the vector database
        query_result = lookup_vector_database(summarized_query_cleaned)
        
        # Format the query results for display
        vector_related_content = "\n\n".join([format_vector_result(i+1, result) for i, result in enumerate(query_result)])

        # Combine the initial ChatGPT answer with the relevant Hadiths
        combined_response = f"{initial_answer}\n\nHere are some related Hadiths:\n{vector_related_content}"

        # Construct the prompt for generating the final response
        final_prompt_messages = [
            {"role": "system", "content": "You are an Islamic scholar."},
            {"role": "user", "content": f"The user asked: {user_question}\n\nInitial Answer:\n{initial_answer}\n\nHere are the related contents:\n{vector_related_content}\n\nCombine the initial answer with the related Hadiths to provide a comprehensive response strictly from an Islamic perspective."}
        ]

        # Call the OpenAI API to generate the final response
        final_response = client.chat.completions.create(
            model=model,
            messages=final_prompt_messages,
            max_tokens=200,  # Adjust as needed
            temperature=0.5
        )
        # Extract the final response content
        final_assistant_message = final_response.choices[0].message.content.strip()

        # Format the response for the frontend
        response_content = (
            f"### Initial Answer:\n{initial_answer}\n\n"
            f"### Vector Search Based Answer:\n{combined_response}\n\n"
            f"### Refined Answer:\n{final_assistant_message}"
        )

        return jsonify({"content": response_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def lookup_vector_database(query):
    top_k = 10
    response = vs.lookup_text_from_str(query, top_k)
    return response

def format_vector_result(index, result):
    attributes = result.attributes
    return (f"Result {index}:\n"
            f"- Hadith Number: {attributes.get('hadith_no', 'N/A')}\n"
            f"- Chapter: {attributes.get('chapter', 'N/A')}\n"
            f"- Chapter Number: {attributes.get('chapter_no', 'N/A')}\n"
            f"- English Text: {attributes.get('text_en', 'N/A')}\n"
            f"- Source: {attributes.get('source', 'N/A')}\n\n"
            f"Arabic Text:\n{attributes.get('text_ar', 'N/A')}\n")

if __name__ == '__main__':
    app.run(debug=True)
