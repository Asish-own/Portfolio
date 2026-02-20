import os
import groq
from dotenv import load_dotenv

load_dotenv()

try:
    print("Testing Groq client...")
    client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    print("Groq client initialized.")
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="llama3-8b-8192"
    )
    print("Groq completion success:", completion.choices[0].message.content)
except Exception as e:
    print(f"Groq Error: {e}")
