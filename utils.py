import random
import requests
from bs4 import BeautifulSoup
import json
import time




def fetchCategories():
    json_file_path = 'data/Companies.json'

    # Read JSON data from file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Get all category names
    category_names = list(json_data['Companies'].keys())

    return category_names



def fetch_leetcode_question_data():

    api_url = 'https://leetcode.com/api/problems/all/?listId=rj89nhim'
    return requests.get(api_url)



def getLeetcodeData(questiontitle, api_response):
# Replace 'your_api_url_here' with the actual URL from which you are fetching the data

    if api_response.status_code == 200:
        data = api_response.json()

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
                    "title": question_title,
                    "href": "/problems/{}".format(title_slug),
                    "difficulty_level": difficulty_level,
                    "premium": premium
                }

                return result




def dumpData(html_code_raw, file_location):
    
    soup = BeautifulSoup(html_code_raw, 'html.parser')

    api_res = fetch_leetcode_question_data()
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

        leetcodedata = getLeetcodeData(title, api_res)

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