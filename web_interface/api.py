import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

api_key = ""  # <-- replace with your actual API key

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": api_key
}

data = {
    "contents": [
        {
            "parts": [
                {"text": "Explain how AI works in a few words"}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# Print raw response JSON
print(response.json())

# If you want just the model's text output:
try:
    text_output = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    print("Model response:", text_output)
except Exception as e:
    print("Could not parse response:", e)
