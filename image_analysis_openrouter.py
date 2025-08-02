import requests, base64, os, json
import streamlit as st

# Replace with your actual OpenRouter API key
# OPENROUTER_API_KEY = st.secrets["openrouter_ai_key"]
OPENROUTER_API_KEY = os.getenv("openrouter_ai_key")

def get_food_items_from_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as img:
        b64_img = base64.b64encode(img.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-3-12b-it:free",  # Gemma-3B via OpenRouter
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts food items from an image."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "List the foods shown in this image clearly, separated by commas. (only list of strings)"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_img}"
                        }
                    }
                ]
            }
        ]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        result = res.json()
    except json.JSONDecodeError:
        print("Failed to parse response.")
        return []

    # Extract the response message
    try:
        response_text = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print("Unexpected response format:", result)
        return []

    print("Response:", response_text)
    food_items = [item.strip().lower() for item in response_text.split(",") if item.strip()]
    return food_items

# Test block
if __name__ == "__main__":
    path = input("Enter path to test image: ").strip()
    foods = get_food_items_from_image(path)
    print("✅ Detected foods:", foods)

