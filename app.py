import streamlit as st
from utils import fetchCategories
from helpers import get_random_question

st.sidebar.title(":blue[CodeQuest Control Panel]")
st.title(":blue[Welcome To CodeQuest]")


category_list = fetchCategories()
control_panel_list = ["View Quest", "Dump Question"]

selected_control = st.sidebar.selectbox(label="Select Your Action: ", options=control_panel_list, index=0)

selected_categories = st.multiselect(label="Select Your Categorie", options=category_list, default=category_list[0])




if(st.button("Fetch Random Question")):

    question_set = get_random_question(selected_categories)
    question_title = question_set["Title"]
    question_link = "https://leetcode.com{}".format(question_set["Href"])

    st.text(question_title)
    st.markdown('<a href="{}" target="_blank">Question Link</a>'.format(question_link), unsafe_allow_html=True)
