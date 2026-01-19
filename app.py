#!/usr/bin/env python
# coding: utf-8

import streamlit as st

import os
import io
import zipfile
import logging

import requests
import pandas as pd
from datetime import datetime, timedelta, date
from ghapi.all import GhApi
from dotenv import load_dotenv, find_dotenv
from lib import heatmap

load_dotenv(find_dotenv())

log = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.captureWarnings(True)
log.setLevel(logging.DEBUG)


st.set_page_config(
    page_title="Gym Occupancy",
    page_icon="🤸‍♀️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

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
    df["timestamp"] = df["timestamp_utc"]
    df["timestamp_utc"] = df.timestamp.dt.tz_localize("UTC")
    df["timestamp_cet"] = df.timestamp_utc.dt.tz_convert("Europe/Zurich")
    df['hour'] = df['timestamp_cet'].dt.hour
    df['dow'] = df['timestamp_cet'].dt.dayofweek  # 0=Mo
    df['weekday'] = df['timestamp_cet'].dt.day_name("de_CH")
    df['date'] = df['timestamp_cet'].dt.date
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

# select date range
df["Datum"] = df["timestamp_cet"].dt.round("5min")
df["Uhrzeit"] = df["Datum"].dt.strftime("%H:%M")

min_date, max_date = df["timestamp"].min().date(), df["timestamp"].max().date() + timedelta(days=1)

start_date_str = st.query_params.get('start_date') or (df["timestamp"].max().date() - timedelta(weeks=8)).strftime("%Y-%m-%d")
end_date_str = st.query_params.get('end_date') or (df["timestamp"].max().date() + timedelta(days=1)).strftime("%Y-%m-%d")

start_date = date.fromisoformat(start_date_str)
end_date = date.fromisoformat(end_date_str)

values = st.slider("Welche Daten möchtest du anschauen?", min_value=min_date, max_value=max_date, value=[start_date, end_date], step=timedelta(days=1), format="DD.MM.YYYY")
start_date_str = (values[0]).strftime("%Y-%m-%d")
end_date_str = (values[1]).strftime("%Y-%m-%d")

st.query_params.start_date = start_date_str
st.query_params.end_date = end_date_str

df_subset = df[(df["Datum"] >= start_date_str) & (df["Datum"] <= end_date_str)]
df_pivot = df_subset.pivot(index="Datum", columns="gym", values="occupancy")
df_pivot = df_pivot.ffill()

st.line_chart(df_pivot, y=gym_options)


# display content
for gym in gym_options:
    df_gym = df[(df.gym == gym) & (df.Datum >= start_date_str) & (df.Datum <= end_date_str)]

    col1, col2 = st.columns(2)

    # Heatmap
    col1.header(f"Heatmap der Belegung: {gym}")
    fig = heatmap.generate_heatmap(df_gym, gym)
    col1.write(fig)

    # data table
    col2.header(f"Data table: {gym}")
    col2.dataframe(df_gym[["Datum", "Uhrzeit", "occupancy"]], hide_index=True)

st.divider()
st.markdown('&copy; 2026 Stefan Oderbolz | [Github Repository](https://github.com/metaodi/gym-occupancy)')

