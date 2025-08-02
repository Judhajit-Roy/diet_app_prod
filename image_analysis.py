import requests, base64, os, json

def get_food_items_from_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as img:
        b64_img = base64.b64encode(img.read()).decode("utf-8")

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3",
        "prompt": "List the foods shown in this image clearly, separated by commas. (only list of strings)",
        "images": [b64_img],
        "stream": False
    })

    try:
        result = res.json()
    except json.JSONDecodeError:
        lines = res.text.strip().split("\n")
        for line in reversed(lines):
            try:
                result = json.loads(line)
                break
            except:
                continue
        else:
            return []

    result_text = result.get("response", "")
    print("Response:", result_text)
    food_items = [item.strip().lower() for item in result_text.split(",") if item.strip()]
    return food_items

# Test block
if __name__ == "__main__":
    path = input("Enter path to test image: ").strip()
    foods = get_food_items_from_image(path)
    print("✅ Detected foods:", foods)
