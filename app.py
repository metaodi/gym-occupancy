#!/usr/bin/env python
# coding: utf-8

import streamlit as st

import os
import io
import zipfile
import logging

import requests
import pandas as pd
from ghapi.all import GhApi
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

log = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.captureWarnings(True)
log.setLevel(logging.DEBUG)


st.set_page_config(page_title="Gym Occupancy", menu_items=None)
st.title('Gym Occupancy')


# select a gym
gyms = [
    'Fitnesspark Zürich Stadelhofen',
    'Fitnesspark Zürich Puls 5',
    'Fitnesspark Zürich Stockerhof',
    'Fitnesspark Zürich Sihlcity',
]
selected_gym = st.sidebar.selectbox(
    'Select a gym',
    gyms,
    index=0,
)
st.query_params.gym = selected_gym

@st.cache_data
def load_data():
    github_token = os.environ['GITHUB_TOKEN']
    owner = os.getenv('GITHUB_REPO_OWNER', 'metaodi')
    repo = os.getenv('GITHUB_REPO', 'gym-occupancy')

    api = GhApi(owner=owner, repo=repo, token=github_token)
    artifacts = api.actions.list_artifacts_for_repo()['artifacts']
    latest_artificat = next(filter(lambda x: x['name'] == 'data-artifact', artifacts), {})

    # download using a seperate requests instance
    log.debug(f"Get latest artifact {latest_artificat['url']}")
    headers = {'Authorization': 'token ' + github_token}
    http = requests.Session()
    http.headers = headers
    r = http.get(latest_artificat["archive_download_url"], allow_redirects=False)
    log.debug(f"Download data from {r.headers['Location']}")
    dl_req = requests.get(r.headers["Location"])

    with zipfile.ZipFile(io.BytesIO(dl_req.content)) as zip_ref:
        log.debug(f"ZIP contains {zip_ref.namelist()}")
        zip_ref.extractall('.')

    df = pd.read_csv(f"occupancy_history.csv")
    return df


filtered_df = load_data()
filtered_df = filtered_df[filtered_df.gym == selected_gym]


# display content
st.header(f"Data table")
st.dataframe(filtered_df)
    

st.sidebar.markdown('&copy; 2025 Stefan Oderbolz | [Github Repository](https://github.com/metaodi/gym-occupancy)')

