import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.resume_parser import load_resume_data
from utils.ai_bot import initialize_knowledge_base, get_ai_response, find_relevant_context

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load Resume Data on Startup
PDF_PATH = os.path.join(os.getcwd(), "ASISH RESUME - Google Docs.pdf")
print(f"Loading resume from: {PDF_PATH}")
resume_data = load_resume_data(PDF_PATH)
raw_resume_text = resume_data.get("raw_text", "")

# Initialize AI Knowledge Base
initialize_knowledge_base(raw_resume_text)

@app.route('/')
def index():
    return render_template('index.html', resume=resume_data)

@app.route('/chat', methods=['POST'])
def chat():
    print('Chat request received')
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "Please say something!"})

    # RAG: Retrieve context
    context = find_relevant_context(user_message)
    
    # Get AI Response
    bot_response = get_ai_response(user_message, context)
    
    return jsonify({"response": bot_response})

@app.route('/contact', methods=['POST'])
def contact():
    # Placeholder for contact form logic
    # In a real app, this would send an email
    data = request.json
    print(f"Contact form submitted: {data}")
    return jsonify({"success": True, "message": "Message received!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
