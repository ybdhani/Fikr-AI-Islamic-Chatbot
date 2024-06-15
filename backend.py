from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from vecto import Vecto
import json, csv, datetime
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Vecto
token = os.getenv("vecto_api_token")
vector_space_id = os.getenv("vector_space_id")
vs = Vecto(token, vector_space_id)

# Load chat history from file
CHAT_HISTORY_FILE = "chat_history.json"
chat_history = []

def load_chat_history():
    global chat_history
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            chat_history = json.load(f)
    except FileNotFoundError:
        chat_history = []
    except Exception as e:
        print(f"Error loading chat history: {e}")

load_chat_history()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get("session_id", str(uuid.uuid4()))  # Create a new session_id if not provided
    messages = data.get("messages", [])
    model = data.get("model", "gpt-3.5-turbo")

    user_question = messages[-1]['content']

    try:
        # Step 2: Summarize chat into a general question for vector query
        summary_prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following conversation into a general question, taking into account the most recent question as emphasis if they are unrelated:\n{messages}"}
        ]
        
        summary_response = client.chat.completions.create(
            model=model,
            messages=summary_prompt_messages,
            max_tokens=50,
            temperature=0.5
        )
        summarized_question = summary_response.choices[0].message.content.strip()

        # Step 3: Generate initial answer
        initial_response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=150,
            temperature=0.5
        )
        initial_answer = initial_response.choices[0].message.content.strip()

        # Step 4: Summarize question for vector search
        query_prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following question in 10-15 words for a vector search query: {summarized_question}"}
        ]
        
        query_response = client.chat.completions.create(
            model=model,
            messages=query_prompt_messages,
            max_tokens=30,
            temperature=0.5
        )
        summarized_query = query_response.choices[0].message.content.strip().replace('\u200f', ' ')

        # Step 5: Vector database lookup
        vector_results = lookup_vector_database(summarized_query)
        formatted_vector_results = "\n\n".join([format_vector_result(i+1, result) for i, result in enumerate(vector_results[:5])])

        # Step 6: Generate source-based answer
        vector_based_prompt_messages = [
            {"role": "system", "content": "You are an Islamic scholar."},
            {"role": "user", "content": f"Based on the following related contents, answer the user's question: {user_question}\n\nHere are the related contents:\n{formatted_vector_results}"}
        ]
        
        vector_based_response = client.chat.completions.create(
            model=model,
            messages=vector_based_prompt_messages,
            max_tokens=200,
            temperature=0.5
        )
        vector_based_answer = vector_based_response.choices[0].message.content.strip()

        # Step 7: Refine final answer
        final_prompt_messages = [
            {"role": "system", "content": "You are an Islamic scholar."},
            {"role": "user", "content": f"The user asked: {user_question}\n\nInitial Answer:\n{initial_answer}\n\nHere are the related contents:\n{formatted_vector_results}\n\nVector Search Based Answer:\n{vector_based_answer}\n\nCombine the initial answer with the vector search based answer to provide a comprehensive response strictly from an Islamic perspective."}
        ]

        final_response = client.chat.completions.create(
            model=model,
            messages=final_prompt_messages,
            max_tokens=400,
            temperature=0.5
        )
        final_assistant_message = final_response.choices[0].message.content.strip()

        # Save chat history
        save_chat_history(session_id, messages + [{"role": "assistant", "content": final_assistant_message}], summarized_question)

        # Step 8: Format the response
        vector_answers = (
            f"### Summarized Question:\n{summarized_question}\n\n"
            f"#### Vector Query: \n{summarized_query}\n\n"
            f"### Initial Answer:\n{initial_answer}\n\n"
            f"### Vector Search Based Answer:\n{vector_based_answer}\n\n"
            f"### Sources:\n{formatted_vector_results}"
        )

        return jsonify({"content": final_assistant_message, "vector_answers": vector_answers, "session_id": session_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat_histories', methods=['GET'])
def chat_histories():
    summaries = [{"summary": entry["summary"], "timestamp": entry["timestamp"]} for entry in chat_history if entry.get("summary")]
    return jsonify(summaries)

@app.route('/chat_history/<timestamp>', methods=['GET'])
def chat_history_by_timestamp(timestamp):
    for entry in chat_history:
        if entry["timestamp"] == timestamp:
            return jsonify(entry["messages"])
    return jsonify({"error": "Chat history not found."}), 404

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

def save_chat_history(session_id, messages, summary, filename="chat_history.json"):
    global chat_history
    timestamp = datetime.datetime.now().strftime("%I:%M %p %d/%m/%Y")
    existing_session = next((entry for entry in chat_history if entry["session_id"] == session_id), None)
    if existing_session:
        existing_session["messages"] = messages
        existing_session["summary"] = summary
        existing_session["timestamp"] = timestamp
    else:
        chat_entry = {
            "session_id": session_id,
            "timestamp": timestamp,
            "summary": summary,
            "messages": messages
        }
        chat_history.append(chat_entry)
    
    with open(filename, "w") as f:
        json.dump(chat_history, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
