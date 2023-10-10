import streamlit as st
from utils import fetchCategories
from helpers import get_random_question, DumpLeetcodeAPIData, DumpCSVData


import streamlit as st

st.set_page_config(
    page_title="CodeQuest",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.sidebar.title(":blue[CodeQuest Control Panel]")
st.title(":blue[Welcome To CodeQuest]")

category_list_category = fetchCategories(file_path="Categories")
category_list_company = fetchCategories("Companies")
category_list = ["All"] + category_list_category + category_list_company
control_panel_list = ["Random Quest", "Dump Questions"]
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

        if "All" in selected_categories:
            question_set = get_random_question(["All"], listype="All", difficulty_level=difficulty_level_selector, is_premium=is_premium)
        elif selected_categories in category_list_company:
            question_set = get_random_question(selected_categories, listype="Companies", difficulty_level=difficulty_level_selector, is_premium=is_premium)
        else:
            question_set = get_random_question(selected_categories, listype="Categories",
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



if control_panel_list[1] in selected_control:
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
            file_name = st.text_input(label="Enter the Database Name(without .json extension)", placeholder="mydatabasename")
            
        
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
            file_name = st.text_input(label="Enter the Database Name(without .json extension)", placeholder="mydatabasename")
            
        
        with col2:
            leetcodeApi = st.text_input(label="Enter Leetcode Api", placeholder="https://leetcode.com/api/problems/algorithms")
            st.text(" ")
            indexname = st.text_input(label="Enter the Category Name", placeholder="Google")
        
        if st.button("Dump"):
            
            dump = DumpLeetcodeAPIData()

            dump.run(file_name, indexname, leetcodeApi)
            st.success("Added Questions to {}.json".format(file_name))

