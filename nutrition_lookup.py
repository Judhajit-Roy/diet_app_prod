import requests
import time

def get_nutrition_info(food_item):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_item,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        product = data.get("products", [])[0] if data.get("products") else None

        if not product or 'nutriments' not in product:
            return {"item": food_item, "calories": None, "protein": None, "carbs": None, "fat": None}

        n = product['nutriments']
        return {
            "item": food_item,
            "calories": n.get("energy-kcal_100g"),
            "protein": n.get("proteins_100g"),
            "carbs": n.get("carbohydrates_100g"),
            "fat": n.get("fat_100g")
        }

    except:
        return {"item": food_item, "calories": None, "protein": None, "carbs": None, "fat": None}

def get_nutrition_for_all(food_items):
    data = []
    for item in food_items:
        print(f"🔍 Fetching nutrition for: {item}")
        info = get_nutrition_info(item)
        data.append(info)
        time.sleep(0.5)
    return data

# Test block
if __name__ == "__main__":
    test_items = ["broccoli", "grilled chicken", "white rice"]
    results = get_nutrition_for_all(test_items)
    for r in results:
        print(f"{r['item'].title()}: {r}")
