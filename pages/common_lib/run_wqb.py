# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：python 3.9
# Description：
"""
# CMD Run Command ： streamlit run /Users/xx.py --server.port 8501

from re import search

import wqb
from wqb import WQBSession, FilterRange
# import asyncio
# from datetime import datetime
# import logging



def log_wqbs(username, password):
  # logger = wqb.wqb_logger()
  # wqbs = WQBSession((username, password), logger=logger)
  wqbs = WQBSession((username, password))
  return wqbs

def get_alpha_data(wqbs,alpha_id):
  resp_alpha_data = wqbs.locate_alpha(alpha_id,log=None)
  return resp_alpha_data.json()


# dataset_id_list':'analyst4','model51','univ1','socialmedia8','fundamental2','fundamental6','model16','pv1','pv13','news12','news18','socialmedia12','option8','option9'

def get_dataset_data(wqbs,dataset_id):
  resp_dataset_data= wqbs.locate_dataset(dataset_id)
  return resp_dataset_data.json()



def get_field_data(wqbs,field_id):
  resp_field_data= wqbs.locate_field(field_id)
  return resp_field_data.json()



