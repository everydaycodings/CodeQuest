import json
import random

def fetchCategories():
    json_file_path = 'data/questions_data.json'

    # Read JSON data from file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Get all category names
    category_names = list(json_data['Category'].keys())

    return category_names



def get_random_question(category_list):

    with open('data/questions_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Check if the "Category" key exists in the data
    if "Category" not in data:
        return "Invalid data format. Missing 'Category' key.", None

    # Filter the provided category list to include only existing categories
    existing_categories = [cat for cat in category_list if cat in data["Category"]]

    if not existing_categories:
        return "No valid categories found.", None

    # Choose a random category from the filtered list
    random_category_name = random.choice(existing_categories)

    # Get the list of questions for the randomly selected category
    questions_list = data["Category"][random_category_name]

    if not questions_list:
        return f"No questions found for category '{random_category_name}'", None

    # Choose a random question from the list
    random_question = random.choice(questions_list)

    # Extract title and href from the random question
    random_title = random_question["title"]
    random_href = random_question["href"]

    result = {
        "Title": random_title,
        "Href": random_href
    }

    return result
