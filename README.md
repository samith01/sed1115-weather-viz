# SED1115 weather visualizer

Python script that reads an hourly Environment Canada climate CSV and draws four graphs.

## Setup

```
pip install -r requirements.txt
```

## Run

```
python weather.py en_climate_hourly_AB_3067371_04-2016_P1H.csv
```

No argument works too — it defaults to the sample CSV in this repo. Writes `weather_insights.png` and prints how many temperature hours were valid.

## The four panels

- **Temperature** — hourly readings (light blue) with a 24-hour moving average (red).
- **Temperature by day and hour** — each column is one day of April, each row an hour; shows daily temperature cycles.
- **Wind speed by time of day** — boxplot in four 6-hour blocks to compare morning, afternoon, and night.
- **Station pressure** — kPa over time.

Timestamps are converted from UTC to America/Edmonton (the station's local time).

## Data

Sample file: [Environment Canada Historic Climate](https://climate.weather.gc.ca), station **WHITECOURT** (Climate ID 3067371), April 2016, hourly. Available under the Open Government Licence – Canada; the file is included so the repo runs without downloading.

225 of the 720 hourly readings are missing for temperature (and wind/pressure), which is why the script prints `valid temp hours: 495 of 720` — the missing values are just not plotted.

## Tests

```
pytest
```

Three checks: the CSV has the expected columns, the row/valid-hour counts match, and the script runs and writes the PNG.

```
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
collected 3 items
test_weather.py ...                                                      [100%]
============================== 3 passed in 4.73s ===============================
```

## Originality

All code in this repo is my own. The plotting is standard `matplotlib`/`pandas` usage; the only external data is the Environment Canada CSV above.
