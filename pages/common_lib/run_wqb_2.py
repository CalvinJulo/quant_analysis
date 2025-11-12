# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xx.py
# Time       ：2021/9/11 19:02
# Author     ：
# version    ：
# Description：https://github.com/rocky-d/wqb, https://github.com/YHYYDS666/WorldQuant-Brain-Alpha
"""

import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from time import sleep

print('Current time:', datetime.now())

def con_session(username, password):
    session = requests.Session()
    session.auth = HTTPBasicAuth(username, password)
    sess_resp = session.post('https://api.worldquantbrain.com/authentication')
    status_code=sess_resp.status_code
    print(status_code,'success' if status_code==201 else 'fail')
    print(sess_resp.json())
    return session
# session = con_session(username,password)


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



def simulate_alpha(session,alpha):
    sim_post_resp = session.post('https://api.worldquantbrain.com/simulations',json=alpha)
    if sim_post_resp.status_code != 201:
        print(f"fail post: {sim_post_resp.status_code})")
    print('post_resp:',sim_post_resp.headers)
    sim_process_url=sim_post_resp.headers['Location']
    start_time = datetime.now()
    while True:
        sim_get_resp=session.get(sim_process_url)
        print('get_resp:', sim_post_resp.headers)
        retry_after = float(sim_get_resp.headers.get('Retry-After',0))
        if retry_after==0:
            sleep(3)
            alpha_id = sim_get_resp.json()["alpha"]  # the final simulation result
            alpha_data = get_one_alpha_data(alpha_id)
            break
        sleep(retry_after)
    cost_time = datetime.now()-start_time
    print(cost_time)
    print(alpha_id)
    return alpha_data

def get_one_alpha_data(session,alpha_id):
    # https://api.worldquantbrain.com/alphas/ZY5ajp7n'
    alpha_url = f'https://api.worldquantbrain.com/alphas/{alpha_id}'
    get_alpha_resp = session.get(alpha_url)
    alpha_data = get_alpha_resp.json()
    return alpha_data

def get_datasets_categories(session):
    dataset_url ='https://api.worldquantbrain.com/data-categories'
    get_dataset_resp = session.get(dataset_url)
    dataset_data = get_dataset_resp.json()
    return dataset_data


def get_operators(session):
    operator_url ='https://api.worldquantbrain.com/operators'
    get_operator_resp = session.get(operator_url)
    operator_data = get_operator_resp.json()
    return operator_data

def get_field(session,delay=1,region='USA',universe='TOP3000',dataset_id=None):
    field_url = (f'https://api.worldquantbrain.com/data-fields?delay={delay}&instrumentType=EQUITY'
                 f'&region={region}&universe={universe}'+'&limit=50&offset={offset}')
    if dataset_id is not None:
        field_url=field_url+f'&dataset.id={dataset_id}'
    total_count = session.get(field_url.format(offset=0)).json()['count']
    all_field_data = []
    for offset in range(0, total_count, 50):
        resp = session.get(field_url.format(offset=offset))
        all_field_data.extend(resp.json()['results'])
    return all_field_data


def filter_alpha(session):
    get_all_alpha_url = 'https://api.worldquantbrain.com/users/self/alphas?limit=20&offset={offset}'
    total_count = session.get(get_all_alpha_url.format(offset=0)).json()['count']
    all_alpha_data = []
    for offset in range(0, total_count, 50):
        resp = session.get(get_all_alpha_url.format(offset=offset))
        all_alpha_data.extend(resp.json()['results'])
    return all_alpha_data

def submit_alpha(session,alpha_id):
    submit_alpha_url = f'https://api.worldquantbrain.com/alphas/{alpha_id}/submit'
    submit_post_resp = session.post(submit_alpha_url)
    if submit_post_resp.status_code != 201:
        print(f"fail post: {submit_post_resp.status_code})")
    while True:
        submit_get_resp=session.get(submit_alpha_url)
        print('get_resp:', submit_post_resp.headers)
        retry_after = float(submit_get_resp.headers.get('Retry-After',0))
        if retry_after==0:
            if submit_get_resp.status_code == 200:
                return 'sucess'
        sleep(retry_after)





HTTP_API_WORLDQUANTBRAIN_COM = 'http://api.worldquantbrain.com'
HTTPS_API_WORLDQUANTBRAIN_COM = 'https://api.worldquantbrain.com'
WQB_API_URL = HTTPS_API_WORLDQUANTBRAIN_COM
URL_ALPHAS = WQB_API_URL + '/alphas'
URL_ALPHAS_ALPHAID = URL_ALPHAS + '/{}'
URL_ALPHAS_ALPHAID_CHECK = URL_ALPHAS_ALPHAID + '/check'
# URL_ALPHAS_ALPHAID_SUBMIT = URL_ALPHAS_ALPHAID + '/submit'
URL_ALPHAS_ALPHAID_SUBMIT = 'http://api.worldquantbrain.com:443/alphas/{}/submit'
URL_AUTHENTICATION = WQB_API_URL + '/authentication'
URL_DATACATEGORIES = WQB_API_URL + '/data-categories'
URL_DATAFIELDS = WQB_API_URL + '/data-fields'
URL_DATAFIELDS_FIELDID = URL_DATAFIELDS + '/{}'
URL_DATASETS = WQB_API_URL + '/data-sets'
URL_DATASETS_DATASETID = URL_DATASETS + '/{}'
URL_OPERATORS = WQB_API_URL + '/operators'
URL_SIMULATIONS = WQB_API_URL + '/simulations'
URL_USERS = WQB_API_URL + '/users'
URL_USERS_SELF = URL_USERS + '/self'
URL_USERS_SELF_ALPHAS = URL_USERS_SELF + '/alphas'

a1 ='https://api.worldquantbrain.com/data-fields?delay=1&instrumentType=EQUITY&region=USA&universe=TOP3000&limit=50&offset=0'
a7 ='https://api.worldquantbrain.com/users/self/alphas?limit=20&offset=10'
b4='https://api.worldquantbrain.com/data-fields?dataset.id=analyst4&delay=1&instrumentType=EQUITY&region=USA&universe=TOP3000&limit=50&offset=0'


