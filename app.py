import streamlit as st


st.sidebar.title(":blue[CodeQuest Control Panel]")
st.title(":blue[Welcome To CodeQuest]")


control_panel_list = ["View Quest", "Dump Question"]

selected_control = st.sidebar.selectbox(label="Select Your Action: ", options=control_panel_list, index=0)