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
  logger = wqb.wqb_logger()
  wqbs = WQBSession((username, password), logger=logger)


def get_alpha_data(alpha_id):
    resp_alpha_data_one_id = wqbs.locate_alpha(alpha_id,log=None)
    return resp_alpha_data_one_id.json()



