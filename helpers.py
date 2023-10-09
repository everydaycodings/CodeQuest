import random
import requests
from bs4 import BeautifulSoup
import json
import time
import utils
import csv


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



class DumpData():

    def __init__(self):
        self.api_res = self.fetch_leetcode_question_data()


    def fetch_leetcode_question_data(self):

        api_url = 'https://leetcode.com/api/problems/all/?listId=rj89nhim'

        return requests.get(api_url)
    
    
    def extract_columns(self, csv_file_path):

        # Open the CSV file for reading
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Create a CSV reader
            reader = csv.DictReader(csvfile)

            # Extracted columns
            extracted_columns = []

            # Iterate over each row in the CSV file
            for row in reader:
                # Extract the desired columns
                problem_title = row["problem_name"]

                leetcodedata = utils.getLeetcodeData(problem_title, self.api_res)
                
                extracted_columns.append(leetcodedata)

        
        return extracted_columns


    def add_new_category(self, existing_data_path, category_name, csv_file_path):
    
        with open('{}.json'.format(existing_data_path), 'r') as file:
            existing_data = json.load(file)


        new_category_data = {
        category_name: self.extract_columns(csv_file_path)
        }

        existing_data["Category"].update(new_category_data)


        with open('{}.json'.format(existing_data_path), 'w') as file:
            json.dump(existing_data, file, indent=2)
    

    def run(self, existing_data_path, category_name, csv_file_path):
        self.add_new_category(existing_data_path, category_name, csv_file_path)

    