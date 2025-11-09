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
import asyncio
from datetime import datetime
# import logging



def log_wqbs(username, password):
  # logger = wqb.wqb_logger()
  # wqbs = WQBSession((username, password), logger=logger)
  wqbs = WQBSession((username, password))
  return wqbs

def get_alpha_data(wqbs,alpha_id):
  resp_alpha_data = wqbs.locate_alpha(alpha_id,log=None)
  return resp_alpha_data.json()



def filter_alphas(wqbs,status='UNSUBMITTED',region='USA',universe='TOP3000',
                  from_date=datetime(2025, 1, 28, 12, 30,0),to_date=datetime(2030, 1, 1, 12, 30,0),check='off'):
    if check=='on':
        sharpe=FilterRange.from_str('[1.58, inf)')
        fitness = FilterRange.from_str('[1, inf)')
        turnover = FilterRange.from_str('(-inf, 0.7]')
    else:
        sharpe=None
        fitness =None
        turnover=None

    lo = datetime.fromisoformat(from_date.strftime('%Y-%m-%dT%H:%M:%S%z-05:00'))
    hi = datetime.fromisoformat(to_date.strftime('%Y-%m-%dT%H:%M:%S%z-05:00'))
    resps_filter_alphas_data = wqbs.filter_alphas(
        status=status, # 'UNSUBMITTED','ACTIVE','DECOMMISSIONED'
        region=region,
        instrument_type=None,
        delay=1,
        universe=universe, # 'TOP3000, TOP1000, TOP500, Top200, TOPSP500'
        decay =None,
        neutralization=None,
        truncation=None,
        pasteurization=None,
        sharpe=sharpe,
        returns=None,
        fitness=fitness,
        turnover=turnover,
        drawdown=None,
        margin=None,
        self_correlation=None,
        date_created=FilterRange.from_str(f"[{lo.isoformat()}, {hi.isoformat()})"),
        order='dateCreated',
    )
    data_list=[]
    for resp in resps_filter_alphas_data:
        # alpha_ids.extend(item['id'] for item in resp.json()['results'])
        data_list.extend(resp.json()['results'])
    # print('filter alpha num')
    # print(len(data_list))
    return data_list


dataset_id_list=['analyst4','model51','univ1','socialmedia8','fundamental2','fundamental6','model16','pv1','pv13','news12','news18','socialmedia12','option8','option9']

def get_dataset_data(wqbs,dataset_id):
  resp_dataset_data= wqbs.locate_dataset(dataset_id)
  return resp_dataset_data.json()

def get_field_data(wqbs,field_id):
  resp_field_data= wqbs.locate_field(field_id)
  return resp_field_data.json()


def get_multi_field_data(wqbs,region='USA',delay=1,universe='TOP3000',search=None,dataset_id=None,category=None):
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


def simulate_one_alpha(wqbs,alpha):
    resp_alpha = asyncio.run(
        wqbs.simulate(
            alpha,  # `alpha` or `multi_alpha`
            on_nolocation=lambda vars: print('nolocation',vars['target'], vars['resp'], sep='\n'),
            on_start=lambda vars: print('start',alpha,vars['url']),
            on_finish=lambda vars: print('finish',vars['resp']),
            # on_success=lambda vars: print('success',vars['resp']),
            on_failure=lambda vars: print('failure',vars['resp']),
        )
    )
    status_code =resp_alpha.status_code
    # print(status_code)
    # print(resp_alpha.json())
    return resp_alpha.json()


def set_alpha(regular='liabilities/assets',universe='TOP3000',decay=4,
              neutralization='SUBINDUSTRY',truncation=0.08, delay=1):
    alpha_setting = {
        'type': 'REGULAR',
        'settings': {
            'instrumentType': 'EQUITY',
            'region': 'USA',
            'universe': universe, # 'TOP3000', 'TOP1000', 'TOP500', 'TOP200', 'TOPSP500'
            'delay': delay, # [0, 1]
            'decay': decay, # [0, 4, 10]
            'neutralization':neutralization , # 'NONE', 'MARKET', 'SECTOR', 'INDUSTRY', 'SUBINDUSTRY'
            'truncation': truncation, ## [0.01, 0.08]
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'OFF',
            'language': 'FASTEXPR',
            'visualization': False
        },
        'regular': regular,
    }
    return alpha_setting
