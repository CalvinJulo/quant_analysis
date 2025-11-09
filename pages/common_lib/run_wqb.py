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


def get_multi_field_data(wqbs=wqbs,region='USA',delay=1,universe='TOP3000',search=None,dataset_id=None,category=None):
    resp_multi_field_data = wqbs.search_fields(
      region=region, #'USA'
      delay=delay, # 0,1
      dataset_id=dataset_id,
      universe=universe, # 'TOP3000, TOP1000, TOP500, Top200, TOPSP500'
      search=search,  # 'price'
      category=category,  # 'pv', 'model', 'analyst'
        # theme=False,  # True, False
        # coverage=FilterRange.from_str('[0.8, inf)'),
        # type='<type>',  # 'MATRIX', 'VECTOR', 'GROUP', 'UNIVERSE'
        # alpha_count=FilterRange.from_str('[100, 200)'),
        # user_count=FilterRange.from_str('[1, 99]'),
        # order='<order>',  # 'coverage', '-coverage', 'alphaCount', '-alphaCount'
        # limit=50,
        # offset=0,
        # others=[],  # ['other_param_0=xxx', 'other_param_1=yyy']
    )
    data_list =[]
    for idx, resp in enumerate(resp_multi_field_data, start=1):
        for j in resp.json()['results']:
            data_list.append(j)
        # print('count:',resp.json()['count'])
        # print(resp.json()['results'])
    return data_list


