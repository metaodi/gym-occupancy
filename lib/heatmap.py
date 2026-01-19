import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, date


opening_hours = {
       'Zürich Stadelhofen': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 20,
       },
       'Zug Eichstätte': {
           'start_hour': 6,
           'end_hour': 23,
           'start_hour_weekend': 8,
           'end_hour_weekend': 21,
       },
       'Greifensee Milandia': {
           'start_hour': 8,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 20,
       },
       'Regensdorf': {
           'start_hour': 8,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Winterthur': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Zürich Glattpark': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Zürich Puls 5': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 20,
       },
       'Zürich Sihlcity': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 20,
       },
       'Zürich Stockerhof': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Luzern National': {
           'start_hour': 7,
           'end_hour': 23,
           'start_hour_weekend': 8,
           'end_hour_weekend': 22,
       },
       'Luzern Allmend': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Baden Trafo': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 20,
       },
       'Basel Heuwaage': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 9,
           'end_hour_weekend': 19,
       },
       'Bern City': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
       'Oberhofen': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 18,
       },
       'Ostermundigen Time-Out': {
           'start_hour': 6,
           'end_hour': 22,
           'start_hour_weekend': 8,
           'end_hour_weekend': 20,
       },
}


def generate_heatmap(df, gym):
    df = remove_entries_outside_openinghours(df, gym)
    order = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    
    heat = df.groupby(['weekday', 'hour'])['occupancy'].mean().reset_index()
    pivot = heat.pivot(index='weekday', columns='hour', values='occupancy').reindex(order)

    fig, ax = plt.subplots(figsize=(7,3))
    sns.heatmap(pivot, cmap='viridis', annot=False, ax=ax)
    ax.set_xlabel("Stunde")
    ax.set_ylabel("Wochentag")

    return fig


def remove_entries_outside_openinghours(df, gym):
    # Einträge ausserhalb der Öffnungszeiten entfernen
    gym_opening_hours = opening_hours[gym]

    df['start_hour'] = np.nan
    df['end_hour'] = np.nan

    df.loc[((df['gym'] == gym) & (df.dow < 5)), "start_hour"] = gym_opening_hours['start_hour']
    df.loc[((df['gym'] == gym) & (df.dow < 5)), "end_hour"] = gym_opening_hours['end_hour']
    df.loc[((df['gym'] == gym) & (df.dow >= 5)), "start_hour"] = gym_opening_hours['start_hour_weekend']
    df.loc[((df['gym'] == gym) & (df.dow >= 5)), "end_hour"] = gym_opening_hours['end_hour_weekend']

    df = df[(df.hour >= df.start_hour) & (df.hour <= df.end_hour)]

    # remove today and the first day, since today data is most probably not complete
    df = df[(df.date < datetime.now().date()) & (df.date > date(2025, 3, 23))]

    return df
