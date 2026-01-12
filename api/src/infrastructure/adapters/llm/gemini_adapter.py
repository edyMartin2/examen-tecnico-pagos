import requests
import json
import os 
import dotenv
dotenv.load_dotenv()

def GeminiAPI(text: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:streamGenerateContent?key={os.getenv('GEMINIAPIKEY')}"

    payload = json.dumps({
    "contents": [
        {
        "role": "user",
        "parts": [
            {
            "text": f"summarize this text: {text}"
            }
        ]
        }
    ],
    "generationConfig": {
        "thinkingConfig": {
        "thinkingBudget": 0
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    try:
        data = response.json()
        result_text = ""
        
        # Gemini sends a list of objects if it's a stream, or a single object if not.
        # But requests.json() might return a list if the response is actually a JSON list.
        # The prompt implies a list-like structure in the response example.
        
        if isinstance(data, list):
            for item in data:
                if 'candidates' in item:
                    for candidate in item['candidates']:
                        if 'content' in candidate and 'parts' in candidate['content']:
                            for part in candidate['content']['parts']:
                                if 'text' in part:
                                    result_text += part['text']
        elif isinstance(data, dict):
             if 'candidates' in data:
                for candidate in data['candidates']:
                    if 'content' in candidate and 'parts' in candidate['content']:
                        for part in candidate['content']['parts']:
                            if 'text' in part:
                                result_text += part['text']
                                
        return result_text.strip()
    except Exception as e:
        return f"Error parsing response: {str(e)} - Raw: {response.text}"
