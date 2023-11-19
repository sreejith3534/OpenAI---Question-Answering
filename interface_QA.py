import streamlit as st
import pandas as pd
from io import StringIO
import tkinter as tk
from tkinter import filedialog
from main_QA import final_mix_from_all_resumes


def get_directory_path(path_input):
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    print("status of click is==", path_input)
    if path_input:
        path_is = filedialog.askdirectory(master=root)
        print("selected path of the folder===", path_is)
        return path_is


def prepare_ui(project_name):
    st.title(project_name)
    st.write("Select input path")
    path_input = st.button("select file")
    specified_path = get_directory_path(path_input)
    print("state session==", st.session_state)
    if st.session_state:
        full_path = st.session_state["var"]
        print("full path is===", full_path)
        st.write("processing started")
        question_set = st.text_input('Enter your queries ')
        if question_set:
            question_lst = question_set.split(",")
            print("question lst is==", question_lst)
            res = final_mix_from_all_resumes(full_path, question_lst)
            print("result is==", res)
            column_names = question_lst.append("filename")
            df_queries = pd.DataFrame(res, columns=column_names)
            st.table(df_queries)
    st.session_state.var = specified_path


if __name__ == "__main__":
    try:
        st.set_page_config(layout="wide")
        prepare_ui("Resume Extractor")
    except Exception as e:
        st.write("issue identified as :", e)


#what is the name of candidate, what is email address, what are total organizations candidate has worked for,what is the total years of experience, what are the organizations the candidate has worked for