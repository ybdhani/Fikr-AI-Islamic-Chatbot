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
        # Step 0.5: Summarize chat into a general question, taking the more recent chats as reference
        summary_prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following conversation into a general question:\n{messages}"}
        ]
        
        summary_response = client.chat.completions.create(
            model=model,
            messages=summary_prompt_messages,
            max_tokens=50,
            temperature=0.5
        )
        summarized_question = summary_response.choices[0].message.content.strip()

        # Step 1: Initial answer from OpenAI's general knowledge
        initial_response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150,
            temperature=0.5
        )
        initial_answer = initial_response.choices[0].message.content.strip()

        # Step 2: Summarization of the question for the vector query
        prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following question in 10-15 words for a vector search query: {summarized_question}"}
        ]
        
        summary_response = client.chat.completions.create(
            model=model,
            messages=prompt_messages,
            max_tokens=30,
            temperature=0.5
        )
        summarized_query = summary_response.choices[0].message.content.strip()

        # Replace \u200f with spaces
        summarized_query_cleaned = summarized_query.replace('\u200f', ' ')

        # Step 3: Redirect the summarized query to the vector database
        query_result = lookup_vector_database(summarized_query_cleaned)
        
        # Format the query results for display
        vector_related_content = "\n\n".join([format_vector_result(i+1, result) for i, result in enumerate(query_result)])

        # Step 3.5: Generate an answer based only on the vector search results
        vector_based_prompt_messages = [
            {"role": "system", "content": "You are an Islamic scholar."},
            {"role": "user", "content": f"Based on the following related contents, answer the user's question: {user_question}\n\nHere are the related contents:\n{vector_related_content}"}
        ]
        
        vector_based_response = client.chat.completions.create(
            model=model,
            messages=vector_based_prompt_messages,
            max_tokens=200,
            temperature=0.5
        )
        vector_based_answer = vector_based_response.choices[0].message.content.strip()

        # Step 4: Combine the initial answer with the vector search based answer to form the refined answer
        final_prompt_messages = [
            {"role": "system", "content": "You are an Islamic scholar."},
            {"role": "user", "content": f"The user asked: {user_question}\n\nInitial Answer:\n{initial_answer}\n\nHere are the related contents:\n{vector_related_content}\n\nVector Search Based Answer:\n{vector_based_answer}\n\nCombine the initial answer with the vector search based answer to provide a comprehensive response strictly from an Islamic perspective."}
        ]

        final_response = client.chat.completions.create(
            model=model,
            messages=final_prompt_messages,
            max_tokens=200,
            temperature=0.5
        )
        final_assistant_message = final_response.choices[0].message.content.strip()

        # Format the response for the frontend
        response_content = (
            f"### Summarized Question:\n{summarized_question}\n\n"
            f"### Initial Answer:\n{initial_answer}\n\n"
            f"### Vector Search Based Answer:\n{vector_related_content}\n\n"
            f"### Answer Based on Vector Search Results:\n{vector_based_answer}\n\n"
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
