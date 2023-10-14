import random
import requests
from bs4 import BeautifulSoup
import json
import time
import utils
import csv
import pandas as pd
import streamlit as st
import time


global_state = {
    'initial_seconds': 0,
    'seconds': 0
}

def timerstate():
    return global_state


class RandomQuestionGenerator():

    def __init__(self):
        pass

    def returnMap(self, question_id, title, href, difficulty_level, premium):

        result = {
            "question_id": question_id ,
            "title": title,
            "href":href ,
            "difficulty_level": difficulty_level,
            "premium": premium
        }

        return result


    def LeetCodeRandomQuestionGenerator(self, category_list, listype, difficulty_level, is_premium):

        if difficulty_level == "Random":
            difficulty_level = 0
        elif difficulty_level == "Easy":
            difficulty_level = 1
        elif difficulty_level == "Medium":
            difficulty_level = 2
        elif difficulty_level == "Hard":
            difficulty_level = 3


        while True:
            with open('data/{}.json'.format(listype), 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            # Check if the "Category" key exists in the data
            if listype not in data:
                return "Invalid data format. Missing 'Category' key.", None

            # Filter the provided category list to include only existing categories
            existing_categories = [cat for cat in category_list if cat in data[listype]]

            if not existing_categories:
                return "No valid categories found.", None

            # Choose a random category from the filtered list
            random_category_name = random.choice(existing_categories)

            # Get the list of questions for the randomly selected category
            questions_list = data[listype][random_category_name]

            if not questions_list:
                return f"No questions found for category '{random_category_name}'", None

            # Choose a random question from the list
            random_question = random.choice(questions_list)
           # print(random_question)
            if random_question != None:

                question_id = random_question["question_id"]
                title = random_question["title"]
                href ="https://leetcode.com{}".format(random_question["href"])
                difficultyLevel = random_question["difficulty_level"]
                premium = random_question["premium"]


                if difficulty_level == 0 and is_premium == "Random":
                    return self.returnMap(question_id, title, href, difficultyLevel, premium)

                elif random_question["difficulty_level"] == difficulty_level and random_question["premium"] == is_premium:

                    return self.returnMap(question_id, title, href, difficultyLevel, premium)

                elif( difficulty_level == 0 and is_premium != "Random"):
                    if(random_question["premium"] == is_premium):
                        return self.returnMap(question_id, title, href, difficultyLevel, premium)

                elif (is_premium == "Random" and difficulty_level != 0):
                    if (random_question["difficulty_level"] == difficulty_level):
                        return self.returnMap(question_id, title, href, difficulty_level, premium)

            else:
                result = {
                    "question_id": None,
                    "title": None,
                    "href": None,
                    "difficulty_level": None,
                    "premium": None
                }

                return result


    def CodeForcesRandomQuestionGenerator(self, file_name, lowerlimit, upperlimit, target_tags):

        with open("data/{}.json".format(file_name), 'r') as file:
            all_problems = json.load(file)["result"]["problems"]


        # Filter problems by tags
        if  "ALL" in target_tags:
            # If "ALL" is specified, don't filter by tags
            filtered_problems = all_problems
        else:
            filtered_problems = [
                problem for problem in all_problems
                if set(target_tags).issubset(set(problem.get("tags", [])))
            ]

            # Filter problems by rating
        filtered_problems = [
            problem for problem in filtered_problems
            if problem.get("rating") and lowerlimit <= problem["rating"] <= upperlimit
        ]

        # Check if there are any filtered problems
        if filtered_problems:
            # Select a random problem from the filtered list
            random_problem = random.choice(filtered_problems)

            question_id = "{}{}".format(random_problem["contestId"], random_problem["index"])
            title = random_problem["name"]
            href = "https://codeforces.com/problemset/problem/{}/{}".format(random_problem["contestId"], random_problem["index"])
            difficulty_level = random_problem["rating"]
            premium = False


            return self.returnMap(question_id, title, href, difficulty_level, premium)

        else:
            result = {
                "question_id": None,
                "title": None,
                "href": None,
                "difficulty_level": None,
                "premium": None
            }

            return result



class DumpCSVData():

    def __init__(self):
        self.api_res = self.fetch_leetcode_question_data()


    def fetch_leetcode_question_data(self):

        api_url = 'https://leetcode.com/api/problems/all'

        return requests.get(api_url)
    
    
    def extract_columns(self, csvfile):

        # Open the CSV file for readin
            # Create a CSV reader
        csv_content = csvfile.read().decode('utf-8').splitlines()
        reader = csv.DictReader(csv_content)

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
    
        with open('data/{}.json'.format(existing_data_path), 'r') as file:
            existing_data = json.load(file)


        new_category_data = {
        category_name: self.extract_columns(csv_file_path)
        }

        existing_data[existing_data_path].update(new_category_data)


        with open('data/{}.json'.format(existing_data_path), 'w') as file:
            json.dump(existing_data, file, indent=2)
    

    def run(self, existing_data_path, category_name, csv_file_path):
        self.add_new_category(existing_data_path, category_name, csv_file_path)




class DumpLeetcodeAPIData():

    def __init__(self):
        pass
    

    def getLeetcodeData(self, api_url):
        
        response = requests.get(api_url)

        result_list = []
        if response.status_code == 200:
            data = response.json()

            for entry in data["stat_status_pairs"]:
                question_title = entry["stat"]["question__title"]

                question_id = entry["stat"]["question_id"]
                title_slug = entry["stat"]["question__title_slug"]
                difficulty_level = entry["difficulty"]["level"]
                premium = entry["paid_only"]
                
                result = {
                    "title": question_title,
                    "question_id": question_id,
                    "title_slug": title_slug,
                    "href": "/problems/{}".format(title_slug),
                    "difficulty_level": difficulty_level,
                    "premium": premium
                }

                result_list.append(result)

        return result_list 


    def add_new_category(self, existing_data_path, category_name, json_Data):
    
        with open('data/{}.json'.format(existing_data_path), 'r') as file:
            existing_data = json.load(file)


        new_category_data = {
        category_name: json_Data
        }

        existing_data[existing_data_path].update(new_category_data)


        with open('data/{}.json'.format(existing_data_path), 'w') as file:
            json.dump(existing_data, file, indent=2)
    

    def run(self, existing_data_path, category_name, api_url):

        json_data = self.getLeetcodeData(api_url)
        self.add_new_category(existing_data_path, category_name, json_data)



class CountDown:
    def __init__(self):
        pass

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(mins), int(secs))

    def countdown_timer(self):
        timer_placeholder = st.empty()
        progress_bar = st.progress(0)
        text_element = st.empty()

        while global_state['seconds']:
            timer_text = self.format_time(global_state['seconds'])
            timer_placeholder.text(timer_text)

            # Update progress bar
            progress_percentage = 1 - global_state['seconds'] / global_state['initial_seconds']
            progress_percentage = max(0, min(1, progress_percentage))  # Ensure it's within [0, 1]
            progress_bar.progress(progress_percentage)

            # Display time remaining and elapsed time
            time_remaining_str = self.format_time(global_state['seconds'])
            elapsed_str = self.format_time(global_state['initial_seconds'] - global_state['seconds'])
            text_element.text(f"Time Remaining: {time_remaining_str} | Elapsed Time: {elapsed_str}")

            time.sleep(1)
            global_state['seconds'] -= 1

        # Display final values
        progress_bar.progress(1.0)
        text_element.text(f"Time Remaining: 00:00:00 | Elapsed Time: {self.format_time(global_state['initial_seconds'])}")
        st.success("Time's up!")

    def run(self, user_input, is_start):

        if is_start:
            try:
                global_state['initial_seconds'] = int(user_input * 60 * 60)  # Convert hours to seconds
                global_state['seconds'] = global_state['initial_seconds']
                if global_state['initial_seconds'] > 0:
                    self.countdown_timer()
                else:
                    st.error("Please enter a valid time format.")
            except ValueError:
                st.error("Please enter a valid time format.")


def SubmitContest(questionsPair, timeTaken):
    pass