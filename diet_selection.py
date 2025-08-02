# diet_selection.py

import difflib

valid_diets = [
    "balanced",
    "weight loss",
    "muscle gain",
    "keto",
    "vegan",
    "vegetarian",
    "diabetic-friendly",
    "mediterranean",
    "custom"
]

def get_user_diet_preference():
    print("👋 Welcome to the Smart Nutrition Assistant!")
    print("Please type your dietary goal or preference (e.g., 'keto', 'vegan', 'weight loss', or 'custom'):")

    user_input = input("📝 Your diet preference: ").strip().lower()
    closest_matches = difflib.get_close_matches(user_input, valid_diets, n=1, cutoff=0.6)

    if closest_matches:
        selected_diet = closest_matches[0]
        if selected_diet == "custom":
            return handle_custom_diet()
        else:
            print(f"\n✅ You selected: {selected_diet.capitalize()}")
            return {"type": selected_diet}
    else:
        print("❌ Unrecognized diet type.")
        print("Supported diets are:")
        for diet in valid_diets:
            print(f"- {diet}")
        return get_user_diet_preference()

def handle_custom_diet():
    print("\n📝 Please describe your custom dietary goals in plain English.")
    print("Examples:")
    print("- I want to eat more fiber and less sugar.")
    print("- I'm avoiding dairy and trying to build muscle.")
    print("- Keep my calories under 2000 and prioritize plant-based protein.")
    
    custom_diet_description = input("\nDescribe your custom diet: ").strip()

    print("\n✅ Custom diet recorded. Passing to AI for interpretation...")
    return {
        "type": "custom",
        "description": custom_diet_description
    }

# Test this file independently
if __name__ == "__main__":
    user_diet = get_user_diet_preference()
    print("\n🧾 Final Diet Selection:")
    print(user_diet)
