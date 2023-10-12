import streamlit as st

import helpers
from utils import fetchCategories, fetchDataBasePath
from helpers import get_random_question, DumpLeetcodeAPIData, DumpCSVData, CountDown


import streamlit as st

st.set_page_config(
    page_title="CodeQuest",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'question_set' not in st.session_state:
            st.session_state.question_set = []


st.sidebar.title(":blue[CodeQuest Control Panel]")
st.title(":blue[Welcome To CodeQuest]")


category_list = fetchCategories(file_path="LeetCodeProblems")
control_panel_list = ["Random Quest", "Contest", "Dump Questions"]
dump_code_category = ["CSV Format", "LeetCode API"]

selected_control = st.sidebar.selectbox(label="Select Your Action: ", options=control_panel_list, index=0)


if control_panel_list[0] in selected_control:

    selected_categories = st.multiselect(label="Select Your Category/Company", options=category_list, default=category_list[0])

    col1, col2 = st.columns(2)
    with col1:
       difficulty_level_selector = st.selectbox(label="Select Your Difficulty Level", options=["Random", "Easy", "Medium", "Hard"])

    with col2:
        is_premium = st.selectbox(label="Do you want premium Questions", options=["Random", True, False])

    if(st.button("Fetch Random Question")):

        with st.spinner("Fetching Question.."):
            question_set = get_random_question(category_list=selected_categories, listype="LeetCodeProblems",
                                                   difficulty_level=difficulty_level_selector, is_premium=is_premium)

        col1, col2, col3, col4 = st.columns(4)

        question_title = "{}-{}".format(question_set["question_id"], question_set["title"])
        question_link = "https://leetcode.com{}".format(question_set["href"])
        difficulty_level = question_set["difficulty_level"]
        premium = str(question_set["premium"])

        with col1:
            st.subheader("Question")
            st.markdown("**{}**".format(question_title))
        
        with col2:
            st.subheader("Level")

            if difficulty_level == 1:
                st.caption(":green[Easy]")
            elif difficulty_level == 2:
                st.caption(":orange[Medium]")
            elif difficulty_level == 3:
                st.caption(":red[Hard]")
            else:
                st.caption(difficulty_level)
        
        with col3:
            st.subheader("Premium")
            if premium == "True":
                st.caption("Money :money_mouth_face:")
            elif premium == "False":
                st.caption("Free :thumbsup:")
        
        with col4:
            st.subheader("Link")
            st.markdown('<a href="{}" target="_blank">Question Link</a>'.format(question_link), unsafe_allow_html=True)



if control_panel_list[2] in selected_control:
    st.subheader("Control Pannel")

    format_selected = st.selectbox(label="Select your format", options=dump_code_category, index=0, key=33)

    st.divider()
    col1, col2 = st.columns(2)

    if dump_code_category[0] in  format_selected:
        with col1:
            st.markdown("##### Format Selected ")
            st.markdown("###### {}".format(format_selected))
            st.text(" ")
            st.text(" ")
            st.text(" ")
            st.text(" ")
            file_name = st.selectbox(label="Enter the Database Name(without .json extension)", options=fetchDataBasePath())
            
        
        with col2:
            uplodedfile = st.file_uploader(label="Upload Your csv file: ")
            st.text(" ")
            indexname = st.text_input(label="Enter the Category Name", placeholder="Google")
        
        if st.button("Dump"):
            
            dump = DumpCSVData()

            dump.run(file_name, indexname, uplodedfile)
            st.success("Added Questions to {}.json".format(file_name))



    if dump_code_category[1] in  format_selected:
        with col1:
            st.markdown("##### Format Selected ")
            st.markdown("###### {}".format(format_selected))
            st.text(" ")
            st.text(" ")
            file_name = st.selectbox(label="Enter the Database Name(without .json extension)", options=fetchDataBasePath())
            
        
        with col2:
            leetcodeApi = st.text_input(label="Enter Leetcode Api", placeholder="https://leetcode.com/api/problems/algorithms")
            st.text(" ")
            indexname = st.text_input(label="Enter the Category Name", placeholder="Google")
        
        if st.button("Dump"):
            
            dump = DumpLeetcodeAPIData()

            dump.run(file_name, indexname, leetcodeApi)
            st.success("Added Questions to {}.json".format(file_name))







if control_panel_list[1] in selected_control:

    selected_categories = st.multiselect(label="Select Your Category/Company", options=category_list,
                                         default=category_list[0])

    col1, col2 = st.columns(2)
    with col1:
        difficulty_level_selector = st.selectbox(label="Select Your Difficulty Level",
                                                 options=["Random", "Easy", "Medium", "Hard"])

        user_time_input = st.number_input("Enter time in hours (e.g., 1.5 for 1 hour 30 minutes):", min_value=0.00)

    with col2:
        is_premium = st.selectbox(label="Do you want premium Questions", options=["Random", True, False])
        number_of_questions = st.number_input(label="Enter Number Of Questions: ", min_value=1, step=1)

    if (st.button("Fetch Random Question")):
        st.session_state.question_set = []
        with st.spinner("Fetching Question.."):

            for i in range(0, number_of_questions):
                question_set_r = get_random_question(category_list=selected_categories, listype="LeetCodeProblems",
                                                   difficulty_level=difficulty_level_selector, is_premium=is_premium)

                st.session_state.question_set.append(question_set_r)


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Question")
        for question in st.session_state.question_set:
            title = question["title"]
            st.markdown("**{}**".format(title))
        st.text(" ")


    with col2:
        st.subheader("Level")
        for question in st.session_state.question_set:
            difficulty_level = question["difficulty_level"]
            if difficulty_level == 1:
                st.caption(":green[Easy]")
            elif difficulty_level == 2:
                st.caption(":orange[Medium]")
            elif difficulty_level == 3:
                st.caption(":red[Hard]")
            else:
                st.caption(difficulty_level)
        st.text(" ")

    with col3:
        st.subheader("Premium")
        for question in st.session_state.question_set:
            premium = question["premium"]
            if premium ==True:
                st.caption("Money :money_mouth_face:")
            elif premium == False:
                st.caption("Free :thumbsup:")
        st.text(" ")

    with col4:
        st.subheader("Link")
        for question in st.session_state.question_set:
            question_link = question["href"]
            st.markdown('<a href="{}" target="_blank">Question Link</a>'.format(question_link), unsafe_allow_html=True)

        st.text(" ")

    if st.button("Submit Contest"):
        st.code(helpers.global_state)

    if st.button("Start Contest"):
        CountDown().run(user_input=user_time_input, is_start=True)