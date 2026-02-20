# AI-Powered Portfolio Website

A modern portfolio website featuring an AI chatbot powered by Groq and RAG (Retrieval Augmented Generation) to answer questions about the portfolio owner's resume.

## Features
- **Modern UI/UX**: Glassmorphism design, smooth animations, and responsive layout.
- **AI Chatbot**: Context-aware chatbot trained on resume data.
- **Dynamic Content**: Clean project structure with Flask backend.
- **RAG Implementation**: Uses Sentence Transformers for embeddings and semantic search.

## Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd PORTFOLIO
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables**
    Create a `.env` file in the root directory and add your Groq API key:
    ```
    GROQ_API_KEY=your_api_key_here
    ```

4.  **Add Resume**
    Place your resume PDF file in the root directory named `ASISH RESUME - Google Docs.pdf`.

5.  **Run the Application**
    ```bash
    python app.py
    ```
    Access the website at `http://localhost:5000`.

## key Components
- `app.py`: Main Flask application.
- `utils/ai_bot.py`: Chatbot logic with RAG.
- `utils/resume_parser.py`: PDF text extraction.
- `static/js/script.js`: Frontend logic.
- `static/css/style.css`: Styling.

## technologies Used
- Python (Flask)
- HTML5, CSS3, JavaScript
- Groq API (LLM)
- Sentence Transformers (Embeddings)
- PyPDF (PDF Parsing)
