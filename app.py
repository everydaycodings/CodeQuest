import streamlit as st
from utils import fetchCategories
from helpers import get_random_question


import streamlit as st

st.set_page_config(
    page_title="CodeQuest",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.sidebar.title(":blue[CodeQuest Control Panel]")
st.title(":blue[Welcome To CodeQuest]")


category_list = fetchCategories()
control_panel_list = ["View Quest", "Dump Question"]

selected_control = st.sidebar.selectbox(label="Select Your Action: ", options=control_panel_list, index=0)

selected_categories = st.multiselect(label="Select Your Categorie", options=category_list, default=category_list[0])




if(st.button("Fetch Random Question")):

    question_set = get_random_question(selected_categories)

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
