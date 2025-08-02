import requests
import os
import streamlit as st


# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = st.secrets["openrouter_ai_key"]


def get_llm_diet_feedback(nutrition_data, user_diet_description):
    lines = []
    for food in nutrition_data:
        if food['calories'] is not None:
            lines.append(
                f"- {food['item']}: {food['calories']} kcal, {food['protein']}g protein, {food['carbs']}g carbs, {food['fat']}g fat"
            )

    meal_text = "\n".join(lines)
    prompt = f"""
User diet goal/description:
\"\"\"{user_diet_description}\"\"\"

Meal nutritional info:
{meal_text}

Give a heading and then please analyze this meal according to the diet goal, mention any nutrients that are lacking or excessive, and suggest what could be added or removed to better fit the diet.
No follow up questions""".strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemma-3-4b-it:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        result = res.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("⚠️ Error:", e)
        print("Raw response:", res.text)
        return "⚠️ No response from model."

# Test block
if __name__ == "__main__":
    nutrition = [
        {'item': 'grilled chicken', 'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
        {'item': 'white rice', 'calories': 129, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
        {'item': 'broccoli', 'calories': 34, 'protein': 2.8, 'carbs': 6.6, 'fat': 0.4}
    ]
    user_desc = "I am following a ketogenic diet, low in carbs and high in fat."
    feedback = get_llm_diet_feedback(nutrition, user_desc)
    print("\n🧠 LLM Diet Feedback:\n", feedback)
