# streamlit_app.py

import streamlit as st
from diet_selection import get_user_diet_preference, valid_diets
# from image_analysis import get_food_items_from_image
from image_analysis_openrouter import get_food_items_from_image
from nutrition_lookup import get_nutrition_for_all
# from diet_evaluator import get_llm_diet_feedback
from diet_evaluator_openrouter import get_llm_diet_feedback
import os
import tempfile

st.set_page_config(page_title="AI Nutrition Assistant", layout="centered")

st.title("🍽️ AI Nutrition Assistant")
st.markdown("Upload a food image, describe your diet goal, and get AI-powered feedback on your meal.")

# Step 1: Get diet goal
st.subheader("1️⃣ Enter Your Diet Preference")

diet_input = st.text_input("Type your dietary goal (e.g., 'keto', 'vegan', 'muscle gain', or 'custom')", "")
diet_result = None

if diet_input:
    from difflib import get_close_matches
    match = get_close_matches(diet_input.lower(), valid_diets, n=1, cutoff=0.6)
    if match and match[0] == "custom":
        custom_diet_desc = st.text_area("Describe your custom diet goal:")
        if custom_diet_desc.strip():
            diet_result = {"type": "custom", "description": custom_diet_desc.strip()}
    elif match:
        st.success(f"✅ Diet matched: {match[0].capitalize()}")
        diet_result = {"type": match[0]}
    else:
        st.error("❌ Could not match your input to a known diet.")

# Step 2: Image upload
st.subheader("2️⃣ Upload a Meal Image")

uploaded_image = st.file_uploader("Choose a food image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Run when both diet and image are ready
if diet_result and uploaded_image:

    # show a preview of the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

    # Save the uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_image.read())
        tmp_path = tmp_file.name

    st.info("🔍 Detecting food items in the image...")
    try:
        food_items = get_food_items_from_image(tmp_path)
        if not food_items:
            st.error("❌ Could not detect any food items.")
        else:
            st.success("🍱 Detected food items:")
            st.write(", ".join(food_items))

            # Step 3: Nutrition info
            st.info("📊 Fetching nutritional data...")
            nutrition = get_nutrition_for_all(food_items)

            st.subheader("🍽️ Nutrition Breakdown")
            for food in nutrition:
                st.write(f"**{food['item'].title()}**: {food['calories']} kcal, {food['protein']}g protein, {food['carbs']}g carbs, {food['fat']}g fat")

            # Step 4: Evaluation
            st.info("🤖 Analyzing meal with your diet goal...")
            user_goal = diet_result["description"] if diet_result["type"] == "custom" else diet_result["type"]
            feedback = get_llm_diet_feedback(nutrition, user_goal)

            st.subheader("🧠 AI Feedback")
            st.write(feedback)
    finally:
        os.remove(tmp_path)
