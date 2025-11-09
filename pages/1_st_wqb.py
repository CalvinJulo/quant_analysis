# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pandas as pd
import streamlit as st
from pages.common_lib import run_wqb
import time


st.info('This is the basic intro of wqb\n\n-- connect to wqb\n\n-- simulate, filter, check')

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
st.write('Current time:',current_time)


sessionState_List = ['sess_username','sess_password','sess_alpha_id', 'sess_alpha_data', 'sess_multi_alpha_data',
                     'sess_dataset_id', 'sess_dataset_data', 'sess_multi_dataset_data','sess_field_id', 
                     'sess_field_data', 'sess_multi_field_data']

for i in sessionState_List:
    if i not in st.session_state:
        st.session_state[i] = ''


# Username and password to WQB
with st.sidebar:
    with st.expander("Log in"):
      st.session_state['sess_username'] = st.text_input('wqb username', 'xx')
      st.session_state['sess_password'] = st.text_input('wqb password', 'xx',type='password')


@st.cache_resource
def get_wqb(username, password):
  wqbs = run_wqb.log_wqbs(username, password)
  return wqbs

wqbs =get_wqb(st.session_state['sess_username'], st.session_state['sess_password'])



sidebar_selectbox = st.sidebar.multiselect(
    "Feature",
    ("Check Field", "Filter Alphas", "Simulate Alphas")
)

def filter_alpha():
  alpha_id = st.text_input('Alpha ID', '')
  alpha_id_data= run_wqb.get_alpha_data(wqbs, alpha_id)

  show_alpha_data = st.radio(
    "Alpha data",["alpha_data_json", "alpha_data_dataframe", "alpha_data_arrange"],horizontal=True)

  if show_alpha_data =="alpha_data_json":
    st.write(alpha_id_data)
  elif show_alpha_data =="alpha_data_dataframe":
    alpha_data_dataframe = pd.json_normalize(alpha_id_data)
    st.write(alpha_data_dataframe.T)


if "Check Field" in sidebar_selectbox:
  st.write("Check Field")
if "Filter Alphas" in sidebar_selectbox:
  filter_alpha()
if "Simulate Alphas" in sidebar_selectbox:
  st.write("Simulate Alphas")


