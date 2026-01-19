# gym-occupancy
A small scraper to scrape the occupancy of gyms.

**There is a deployed application to visualize the data: https://gym-occupancy.fly.dev/**

And see my blog post from January 2026 about this data (in German): [Von Neujahrsvorsätzen bis Abend-Peak: Was 10 Monate Fitnessdaten verraten](https://digital.ebp.ch/2026/01/19/von-neujahrsvorsaetzen-bis-abend-peak-was-10-monate-fitnessdaten-verraten/)

## Usage

Convert git history to one big CSV file:

```
uv run extract_git_history.py -i occupancy.csv -o occupancy_history.csv --start-at be9808b76526d4b8646232e1d63148f10930576b
```

To run the streamlit application:

```
uv run streamlit run app.py
```

There are two notebooks on how to analyze this data, see:

- [`plot_data.ipynb`](https://github.com/metaodi/gym-occupancy/blob/main/plot_data.ipynb)
- [`analyze_timeseries.ipynb`](https://github.com/metaodi/gym-occupancy/blob/main/analyze_timeseries.ipynb)
