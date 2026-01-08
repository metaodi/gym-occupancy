# gym-occupancy
A small scraper to scrape the occupancy of gyms


## Usage

Convert git history to one big CSV file:

```
uv run extract_git_history.py -i occupancy.csv -o occupancy_history.csv --start-at be9808b76526d4b8646232e1d63148f10930576b
```

To run the streamlit application:

```
uv run streamlit run app.py