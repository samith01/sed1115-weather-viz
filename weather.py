"""Create a four-panel weather summary from hourly Environment Canada climate data.

Usage:
    python weather.py [file.csv]

The script reads an hourly CSV, converts timestamps to local Alberta time,
and saves a summary graphic as weather_insights.png.
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt

# ---- load and clean ----
# Use the CSV path from the command line when provided.
# With no argument, fall back to the Whitecourt sample that ships with the repo.
if len(sys.argv) < 2:
    FILE = "en_climate_hourly_AB_3067371_04-2016_P1H.csv"
    print("no file given, using", FILE)
else:
    FILE = sys.argv[1]

# Read the raw climate file and keep only the columns needed for the charts.
df = pd.read_csv(FILE, parse_dates=["Date/Time (UTC)"], encoding="utf-8-sig")
df = df.rename(columns={"Date/Time (UTC)": "time", "Temp (°C)": "temp",
                        "Wind Spd (km/h)": "wind", "Stn Press (kPa)": "press"})

# Convert the timestamps to local time so the plots match the station's clock rather than UTC values recorded in the source file.
df["time"] = df["time"].dt.tz_localize("UTC").dt.tz_convert("America/Edmonton")
df = df.set_index("time")

# Keep the station name for the figure title.
station = df["Station Name"].iloc[0]

# Prepare the data
# A rolling 24-hour mean helps highlight overall temperature trends without losing the short-term variability visible in the raw hourly series.
temp24 = df["temp"].rolling(24, min_periods=12).mean()

# Build a day-by-hour matrix so the heatmap can compare each hour across the full record.
grid = df["temp"].groupby([df.index.date, df.index.hour]).mean().unstack()

# Split the day into four standard blocks for wind comparison: early morning, morning,afternoon, and evening/night.
blocks = pd.cut(df.index.hour, [-1, 5, 11, 17, 23], labels=["00-06", "06-12", "12-18", "18-24"])
wind_groups = [g.dropna().values for _, g in df["wind"].groupby(blocks, observed=False)]

# Plot
# Set a consistent base font for the panel layout.
plt.rcParams.update({"font.size": 12})
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
fig.suptitle(f"{station} - hourly weather (local time)", fontsize=15)

# Top-left panel: hourly temperatures with a smoothed 24-hour trend line.
ax[0, 0].plot(df["temp"], lw=0.7, color="lightsteelblue", label="Hourly")
ax[0, 0].plot(temp24, lw=2, color="tab:red", label="24 h average")
ax[0, 0].set(title="Temperature", ylabel="°C")
ax[0, 0].legend()

# Top-right panel: heatmap showing each hour of the day across all dates in the record.
im = ax[0, 1].imshow(grid.T, aspect="auto", origin="lower", cmap="coolwarm")
ax[0, 1].set(title="Temperature by day and hour", xlabel="Day of month", ylabel="Hour of day")
ax[0, 1].set_xticks(range(0, len(grid), 5))
ax[0, 1].set_xticklabels([d.day for d in grid.index[::5]])
fig.colorbar(im, ax=ax[0, 1], label="°C")

# Bottom-left panel: wind distribution by time-of-day using a boxplot.
ax[1, 0].boxplot(wind_groups, tick_labels=["00-06", "06-12", "12-18", "18-24"])
ax[1, 0].set(title="Wind speed by time of day", xlabel="Local hours", ylabel="km/h")

# Bottom-right panel: atmospheric pressure over time.
ax[1, 1].plot(df["press"], color="tab:green")
ax[1, 1].set(title="Station pressure", ylabel="kPa")

# Rotate the x-axis labels on the temperature and pressure plots to improve readability.
for a in (ax[0, 0], ax[1, 1]):
    a.tick_params(axis="x", rotation=45)

# Save the final figure and print a quick summary of how much data was used.
plt.tight_layout()
plt.savefig("weather_insights.png", dpi=150)
print("valid temp hours:", df["temp"].count(), "of", len(df))
