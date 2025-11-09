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
from datetime import datetime


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

  st.write('## Alpha')
  alpha_id = st.text_input('Alpha id', '')
  alpha_id_data= run_wqb.get_alpha_data(wqbs, alpha_id)

  show_alpha_data = st.radio(
    "Alpha data",[ "alpha_data_dataframe", "alpha_data_json","search_alpha"],horizontal=True)
  if show_alpha_data =="alpha_data_json":
    st.write(alpha_id_data)
  elif show_alpha_data =="alpha_data_dataframe":
    alpha_data_dataframe = pd.json_normalize(alpha_id_data)
    st.write(alpha_data_dataframe.T)
    st.write(pd.DataFrame(alpha_id_data['is']['checks']))
  elif show_alpha_data =="search_alpha":
    filter_alpha_attr_orignal =[{'status':'UNSUBMITTED','region':'USA','universe':'TOP3000',
                                 'from_date':datetime(2025, 1, 28, 12, 30,0),'to_date':datetime(2030, 1, 1, 12, 30,0),
                                 'check':'off'}]
    filter_alpha_attr_df =st.data_editor(
      pd.DataFrame(filter_alpha_attr_orignal),
      key="filter_alpha_attr_editor",
      hide_index=True,
      use_container_width=True,
      num_rows="fixed",
      column_config={
        'status':st.column_config.SelectboxColumn("status",options=['UNSUBMITTED','ACTIVE','DECOMMISSIONED']),
        'region':st.column_config.SelectboxColumn("region",options=["USA"]),
        'check': st.column_config.SelectboxColumn("check", options=['off','on']),
        'universe': st.column_config.SelectboxColumn("universe", options=['TOP3000', 'TOP1000', 'TOP500', 'Top200', 'TOPSP500']),
        'from_date': st.column_config.DatetimeColumn("from_date",min_value=datetime(2023, 6, 1,0,0,0),max_value=datetime(2030, 1, 1,0,0,0)),
        'to_date': st.column_config.DatetimeColumn("to_date",min_value=datetime(2023, 6, 1,0,0,0),max_value=datetime(2030, 1, 1,0,0,0)),   
      }
        )
    filter_alpha_attr_dict=filter_alpha_attr_df.to_dict('records')[0]
    get_multi_alpha_data=run_wqb.filter_alphas(wqbs=wqbs,status=filter_alpha_attr_dict['status'],region=filter_alpha_attr_dict['region'],
                                               universe=filter_alpha_attr_dict['universe'],check=filter_alpha_attr_dict['check'],
                                               from_date=filter_alpha_attr_dict['from_date'],to_date=filter_alpha_attr_dict['to_date'])
    
    st.write('alpha count:',len(get_multi_alpha_data))
    st.write(pd.json_normalize(get_multi_alpha_data))





def check_field():
  # dataset
  st.write('## Dataset')
  dataset_id_list=['analyst4','model51','univ1','socialmedia8','fundamental2','fundamental6','model16','pv1','pv13','news12','news18','socialmedia12','option8','option9']
  
  dataset_id = st.text_input('Dataset id', '')
  dataset_id_data= run_wqb.get_dataset_data(wqbs, dataset_id)

  show_dataset_data = st.radio(
    "Dataset data",[ "dataset_data_dataframe","dataset_data_json", "dataset_data_arrange"],horizontal=True)
  if show_dataset_data =="dataset_data_json":
    st.write(dataset_id_data)
  elif show_dataset_data =="dataset_data_dataframe":
    dataset_data_dataframe = pd.json_normalize(dataset_id_data)
    st.write(dataset_data_dataframe.T)
    st.write(pd.DataFrame(dataset_id_data['data']))
    st.write(pd.DataFrame(dataset_id_data['researchPapers']))
    
  # field 
  st.write('## Field')
  field_id = st.text_input('field id', '')
  field_id_data= run_wqb.get_field_data(wqbs, field_id)
  show_field_data = st.radio("Field data",[ "field_data_dataframe","field_data_json", "search_field","field_info"],horizontal=True)
  if show_field_data =="field_data_json":
    st.write(field_id_data)
  elif show_field_data =="field_data_dataframe":
    field_data_dataframe = pd.json_normalize(field_id_data)
    st.write(field_data_dataframe.T)
    st.write(pd.DataFrame(field_id_data['data']))
  elif show_field_data =="search_field":
    filter_field_attr_orignal =[{'region':'USA','delay':1,'universe':'TOP3000','search':None,'dataset_id':None}]
    filter_field_attr_df =st.data_editor(
      pd.DataFrame(filter_field_attr_orignal),
      key="filter_field_attr_editor",
      hide_index=True,
      use_container_width=True,
      num_rows="fixed",
      column_config={
        'region':st.column_config.SelectboxColumn("region",options=["USA"]),
        'delay': st.column_config.SelectboxColumn("delay", options=[1,0]),
        'universe': st.column_config.SelectboxColumn("universe", options=['TOP3000', 'TOP1000', 'TOP500', 'Top200', 'TOPSP500'])}
        )
    filter_field_attr_dict=filter_field_attr_df.to_dict('records')[0]
    get_multi_field_data=run_wqb.get_multi_field_data(wqbs=wqbs,region=filter_field_attr_dict['region'],delay=filter_field_attr_dict['delay'],
                                                      universe=filter_field_attr_dict['universe'],search=filter_field_attr_dict['search'],
                                                      dataset_id=filter_field_attr_dict['dataset_id'])
    st.write('field count:', len(get_multi_field_data))
    st.write(pd.json_normalize(get_multi_field_data))



def simulate_alpha():
  st.write('Simulate Alpha')
  set_alpha_attr_orignal =[{'regular':'liabilities/assets','region':'USA','universe':'TOP3000',
                            'delay':1,'decay':4,'truncation':0.8,'neutralization':'SUBINDUSTRY'}]
  set_alpha_attr_df =st.data_editor(
    pd.DataFrame(set_alpha_attr_orignal),
    key="set_alpha_attr_editor",
    # hide_index=True,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        'region':st.column_config.SelectboxColumn("region",options=["USA"]),
        'delay': st.column_config.SelectboxColumn("delay", options=[1,0]),
        'universe': st.column_config.SelectboxColumn("universe", options=['TOP3000', 'TOP1000', 'TOP500', 'Top200', 'TOPSP500']),
        'neutralization': st.column_config.SelectboxColumn("universe", options=['SUBINDUSTRY','NONE', 'MARKET', 'SECTOR', 'INDUSTRY' ]),
        'decay': st.column_config.NumberColumn("decay", min_value=0),
        'truncation': st.column_config.NumberColumn("truncation", min_value=0,max_value=1,)
      }
  )
  set_alpha_attr_dict=set_alpha_attr_df.to_dict('records')
  # get_multi_field_data=run_wqb.get_multi_field_data(wqbs=wqbs,region=filter_field_attr_dict['region'],delay=filter_field_attr_dict['delay'],
    #                                                  universe=filter_field_attr_dict['universe'],search=filter_field_attr_dict['search'],
    #                                                  dataset_id=filter_field_attr_dict['dataset_id'])
  
  st.write('alpha setting count:', len(set_alpha_attr_dict))
  st.write(pd.json_normalize(set_alpha_attr_dict))
  if st.button('simulate'):
    st.write('ss')

  


if "Check Field" in sidebar_selectbox:
  check_field()
if "Filter Alphas" in sidebar_selectbox:
  filter_alpha()
if "Simulate Alphas" in sidebar_selectbox:
  simulate_alpha()


