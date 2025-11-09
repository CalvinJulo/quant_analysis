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

# Username and password from MongoDB Altas
with st.sidebar:
    username = st.text_input('username', 'xx')
    password = st.text_input('password', 'xx')


@st.cache_resource
def get_wqb(username, password):
  wqbs = run_wqb.log_wqbs(username, password)
  return wqbs


wqbs =get_wqb(username, password)

alpha_id = st.text_input('Alpha ID', '')
alpha_id_data= run_wqb.get_alpha_data(alpha_id, alpha_id)
st.write(alpha_id_data)




