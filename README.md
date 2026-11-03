# NV Seismic Data Availability
Automated dashboard showing annual data availability for the **NV seismic network**, updated monthly via GitHub Actions.

**Live page:** https://aschlesin.github.io/NV_Seismic_Data_Availability/

## Overview

Queries the [EarthScope MUSTANG Measurements service](https://service.earthscope.org/mustang/measurements/1/) for `percent_availability` records on the NV network. The script filters the selected channels (`EHZ`, `HHZ`, `CHZ`, `CH3`, `HH3`, `HN3`, `HNZ`, `CNZ`, `CN3`, `BNZ`, `BN3`), averages their daily availability percentages by calendar year, and generates an interactive Plotly timeline with each annual percentage labeled on its segment.

Annual values average the daily records returned by MUSTANG; missing days are not treated as 0%. The current year is a partial-year value.

## Repository contents

| File | Description |
|------|-------------|
| `Run_DataAvailability.py` | Main script — queries MUSTANG, calculates annual availability, and writes `index.html` |
| `requirements.txt` | Python dependencies |
| `.github/workflows/update.yml` | GitHub Actions workflow — runs daily at 06:00 UTC and commits updated outputs |
| `index.html` | Generated interactive timeline (served via GitHub Pages) |


## Running locally

```bash
pip install -r requirements.txt kaleido
python Run_DataAvailability.py
```

Open `index.html` in a browser to view the interactive chart.

## Automation

The GitHub Actions workflow (`.github/workflows/update.yml`) runs on the first day of each month at 06:00 UTC. It:
1. Installs dependencies
2. Runs `Run_DataAvailability.py`
3. Commits and pushes the updated `index.html` back to the repository

GitHub Pages then serves the updated `index.html` automatically.

## Data source

[EarthScope MUSTANG Measurements Web Service](https://service.earthscope.org/mustang/measurements/1/)

