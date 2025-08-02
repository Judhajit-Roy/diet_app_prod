# 🍽️ AI Nutrition Assistant

An AI-powered web app that helps users get nutritional feedback from meal images — personalized to their dietary goals.

Upload a photo of your meal, describe your diet (e.g., keto, vegan, muscle gain), and let the app:
- 🧠 Detect food items from the image using an AI model  
- 📊 Fetch nutrition facts for each item  
- 💡 Provide intelligent feedback based on your dietary goal  

Deployed via **Streamlit Cloud** and **Render**, powered by **OpenRouter AI models**.

---

## ✨ Features

- 📷 Upload food images directly from your device
- 🧠 AI identifies food items in the photo
- 🧾 Auto-fetches nutritional data (calories, protein, carbs, fat)
- 🎯 Personalized diet feedback using language models
- ✅ Supports common goals: `keto`, `vegan`, `weight loss`, `muscle gain`, or custom

---

## 🚀 Live Demo

- **Streamlit**: (https://foodintel.streamlit.app/)
- **Render**: (https://foodintel.onrender.com/)

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **AI Models**: [OpenRouter](https://openrouter.ai) (`gemma3`)
- **Nutrition Data**: [openfoodfacts](https://world.openfoodfacts.org/)
- **Deployment**: Streamlit Cloud / Render

---

## 🧪 Local Setup

```bash
git clone https://github.com/Judhajit-Roy/diet_app_prod.git
cd diet_app_prod
pip install -r requirements.txt
streamlit run streamlit_app.py
