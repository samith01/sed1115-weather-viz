"""Quick checks to run before submitting weather.py."""
import os
import subprocess

import pandas as pd

CSV = "en_climate_hourly_AB_3067371_04-2016_P1H.csv"


def test_csv_has_expected_columns():
    df = pd.read_csv(CSV, encoding="utf-8-sig")
    for col in ["Date/Time (UTC)", "Temp (°C)", "Wind Spd (km/h)",
                "Stn Press (kPa)", "Station Name"]:
        assert col in df.columns


def test_expected_row_counts():
    df = pd.read_csv(CSV, encoding="utf-8-sig")
    assert len(df) == 720  # 30 days x 24 hours
    assert df["Temp (°C)"].notna().sum() == 495


def test_script_runs_and_writes_png():
    result = subprocess.run(["python3", "weather.py"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "valid temp hours: 495 of 720" in result.stdout
    assert os.path.exists("weather_insights.png")
