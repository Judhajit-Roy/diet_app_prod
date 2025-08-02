# main.py

from diet_selection import get_user_diet_preference
from image_analysis import get_food_items_from_image
# from image_analysis_openrouter import get_food_items_from_image
from nutrition_lookup import get_nutrition_for_all
from diet_evaluator import get_llm_diet_feedback
# from diet_evaluator_openrouter import get_llm_diet_feedback

def main():
    print("🍽️ Welcome to the AI Nutrition Assistant")
    print("========================================\n")

    # Step 1: Get user's diet preference or goal
    diet = get_user_diet_preference()
    user_description = diet["description"] if diet["type"] == "custom" else diet["type"]

    # Step 2: Image to food items
    image_path = input("\n📷 Enter the path to your food image: ").strip()
    food_items = get_food_items_from_image(image_path)

    if not food_items:
        print("❌ Could not identify any food items from the image.")
        return

    print("\n🍱 Detected food items:")
    for item in food_items:
        print(f" - {item}")

    # Step 3: Nutrition lookup
    print("\n🔍 Fetching nutrition data...")
    nutrition_data = get_nutrition_for_all(food_items)

    print("\n📊 Nutrition Summary:")
    for food in nutrition_data:
        print(f"{food['item'].title()}: {food['calories']} kcal, "
              f"{food['protein']}g protein, {food['carbs']}g carbs, {food['fat']}g fat")

    # Step 4: LLM-based evaluation
    print("\n🤖 Evaluating your meal based on your diet goal...\n")
    feedback = get_llm_diet_feedback(nutrition_data, user_description)

    print("🧠 AI Feedback:")
    print("----------------------------------------")
    print(feedback)
    print("----------------------------------------")

if __name__ == "__main__":
    main()
