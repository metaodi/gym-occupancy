#!/usr/bin/env python
# coding: utf-8

import streamlit as st

import os
import io
import zipfile
import logging

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
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


@st.cache_data(ttl=900)
def load_data():
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token:
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

    df = pd.read_csv("occupancy_history.csv", parse_dates=["timestamp_utc"])
    df["timestamp_utc"] = df.timestamp_utc.dt.tz_localize("UTC")
    df["timestamp_cet"] = df.timestamp_utc.dt.tz_convert("Europe/Zurich")
    df["gym"] = df.gym.str.replace("Fitnesspark ", "")
    return df


df = load_data()

gym_query = st.query_params.get_all('gyms') or []

gyms = sorted(df.gym.unique())
gym_options = st.multiselect(
    "Welches Gym möchtest du anschauen?",
    gyms,
    gym_query,
)
# select a gym
st.query_params.gyms = gym_options

df["timestamp_cet"] = df["timestamp_cet"].dt.round("5min")
df_pivot = df.pivot(index="timestamp_cet", columns="gym", values="occupancy")
df_pivot = df_pivot.ffill()
st.line_chart(df_pivot, y=gym_options)

st.dataframe(df_pivot)


# display content
for gym in gym_options:
    df_gym = df[df.gym == gym]
    st.header(f"Data table: {gym}")
    st.dataframe(df_gym)

st.divider()
st.markdown('&copy; 2025 Stefan Oderbolz | [Github Repository](https://github.com/metaodi/gym-occupancy)')

