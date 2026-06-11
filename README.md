# NV Seismic Data Availability

Automated dashboard showing data availability for the **NV seismic network**, updated daily via GitHub Actions.

**Live page:** https://aschlesin.github.io/NV_Seismic_Data_Availability/

## Overview

Queries the [EarthScope FDSN availability service](https://service.iris.edu/fdsnws/availability/1/) for all broadband and short-period vertical channels (`EHZ`, `HHZ`, `CHZ`, `CH3`, `HH3`, `HN3`, `HNZ`, `CNZ`, `CN3`) on the NV network, then generates an interactive Plotly timeline showing the earliest and latest data available for each station/channel.

## Repository contents

| File | Description |
|------|-------------|
| `Run_DataAvailability.py` | Main script — queries EarthScope, builds the timeline, writes `index.html` and `test.png` |
| `requirements.txt` | Python dependencies |
| `.github/workflows/update.yml` | GitHub Actions workflow — runs daily at 06:00 UTC and commits updated outputs |
| `index.html` | Generated interactive timeline (served via GitHub Pages) |
| `test.png` | Static snapshot of the latest timeline |

## Running locally

```bash
pip install -r requirements.txt kaleido
python Run_DataAvailability.py
```

Opens `index.html` in a browser to view the interactive chart.

## Automation

The GitHub Actions workflow (`.github/workflows/update.yml`) runs every day at 06:00 UTC. It:
1. Installs dependencies
2. Runs `Run_DataAvailability.py`
3. Commits and pushes updated `index.html` and `test.png` back to the repository

GitHub Pages then serves the updated `index.html` automatically.

## Data source

[EarthScope / IRIS FDSN Availability Web Service](https://service.iris.edu/fdsnws/availability/1/)

