import random
import requests
from bs4 import BeautifulSoup
import json
import time

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


def parse_html_question_markdown(html_content):
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract relevant information
    question_text = soup.find('div', class_='xFUwe').find_all('p')[:3]
    question_text = ' '.join([text.text.strip() for text in question_text])

    # Extract example inputs and outputs
    examples = soup.find('div', class_='xFUwe').find_all('pre')
    example_data = []
    for i, example in enumerate(examples, 1):
        example_input = example.find('strong', text='Input:').find_next('code').get_text(strip=True)
        example_output = example.find('strong', text='Output:').find_next('code').get_text(strip=True)
        example_data.append(f"Example {i} - Input: `{example_input}`, Output: `{example_output}`\n\n")

    # Extract constraints
    constraints = soup.find('div', class_='xFUwe').find('strong', text='Constraints:').find_next('ul')
    constraints_text = ' '.join([f"- {constraint.get_text(strip=True)}\n\n" for constraint in constraints.find_all('li')])

    # Combine everything into a Markdown text
    markdown_output = (
        f"{question_text}\n" + f"\nConstraints:\n{constraints_text}"
    )

    return markdown_output


def getLeetcodeData(questiontitle):
# Replace 'your_api_url_here' with the actual URL from which you are fetching the data
    api_url = 'https://leetcode.com/api/problems/all/?listId=rj89nhim'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        for entry in data["stat_status_pairs"]:
            question_title = entry["stat"]["question__title"]
            
            if question_title == questiontitle:

                question_id = entry["stat"]["question_id"]
                title_slug = entry["stat"]["question__title_slug"]
                difficulty_level = entry["difficulty"]["level"]
                premium = entry["paid_only"]
                
                result = {
                    "question_id": question_id,
                    "title_slug": title_slug,
                    "difficulty_level": difficulty_level,
                    "premium": premium
                }

                return result 
            


def dumpData(html_code_raw, file_location):
    soup = BeautifulSoup(html_code_raw, 'html.parser')

    # Find the list-group div
    #list_group_div = soup.find('div', class_='list-group')

    # Find all question items within the list-group div
    question_items = soup.find_all('li', class_='list-group-item question')

    # Extract data into a dictionary
    category_data = {
        "Category": {
            "StriverA-Z":[],
        }
    }

    for item in question_items:
        title_element = item.find('div', class_='question-title')
        title_parts = title_element.text.split('.', 1)
        question_number = title_parts[0].strip()
        title = title_parts[1].strip()
        link = title_element.find('a')['href']

        leetcodedata = getLeetcodeData(title)

        question_data = {
            "title": title,
            "href": link,
            "question_id": leetcodedata["question_id"],
            "title_slug": leetcodedata["title_slug"],
            "difficulty_level": leetcodedata["difficulty_level"],
            "premium": leetcodedata["premium"]
        }
        category_data["Category"]["StriverA-Z"].append(question_data)
        time.sleep(2)


    # Save the data to a JSON file
    json_file_path = file_location
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(category_data, json_file, ensure_ascii=False, indent=2)

    return 1
