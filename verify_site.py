import requests
import time

def verify_site():
    print("Verifying site accessibility...")
    try:
        # 1. Homepage
        response = requests.get("http://localhost:5000")
        if response.status_code == 200:
            print("Homepage loaded successfully (Status 200).")
            if "Asish Kumar Behera" in response.text:
                print("Content check passed: 'Asish Kumar Behera' found.")
            else:
                print("Content check WARNING: 'Asish Kumar Behera' not found in homepage.")
        else:
            print(f"Homepage failed with status {response.status_code}")
            return

        # 2. Chat Endpoint
        print("Testing Chatbot API...")
        chat_payload = {"message": "Hello, who are you?"}
        chat_response = requests.post("http://localhost:5000/chat", json=chat_payload)
        
        if chat_response.status_code == 200:
            print("Chat API functional (Status 200).")
            data = chat_response.json()
            print(f"Chat Response: {data.get('response', 'No response field')}")
        else:
            print(f"Chat API failed with status {chat_response.status_code}")
            print(chat_response.text)

    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_site()
