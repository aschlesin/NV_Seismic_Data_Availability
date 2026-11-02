import requests
import pandas as pd
import plotly.express as px

url = (
    'https://service.earthscope.org/mustang/measurements/1/query'
    '?metric=percent_availability&net=NV&sta=*&loc=*&cha=*&format=json&nodata=404'
)
response = requests.get(url, timeout=60)
response.raise_for_status()
response_data = response.json()

availability_records = response_data.get('measurements', {}).get('percent_availability', [])
df_availability = pd.DataFrame(availability_records)

selected_channels = ['EHZ', 'HHZ', 'CHZ', 'CH3', 'HH3', 'HN3', 'HNZ', 'CNZ', 'CN3', 'BNZ', 'BN3']
df_filtered = df_availability[df_availability['cha'].isin(selected_channels)]

plot_df = df_filtered.copy()
plot_df['start'] = pd.to_datetime(plot_df['start'])
plot_df['value'] = pd.to_numeric(plot_df['value'], errors='coerce')

group_columns = ['net', 'sta', 'loc', 'cha', 'qual', 'target']
annual_df = (
    plot_df.set_index('start')
    .groupby(group_columns)['value']
    .resample('YS')
    .mean()
    .rename('annual_availability_pct')
    .reset_index()
    .sort_values(['start', 'target'])
)
annual_df['period_end'] = annual_df['start'] + pd.DateOffset(years=1)
annual_df['bar_label'] = (
    annual_df['sta']
    + '.'
    + annual_df['loc'].fillna('')
    + '.'
    + annual_df['cha']
)

fig = px.timeline(
    annual_df,
    x_start='start',
    x_end='period_end',
    y='bar_label',
    color='cha',
    text='annual_availability_pct',
    hover_data=['net', 'sta', 'loc', 'cha', 'qual', 'annual_availability_pct'],
    title='Annual Data Availability — NV Network',
    labels={
        'bar_label': 'Station.Location.Channel',
        'start': 'Year',
        'cha': 'Channel',
        'annual_availability_pct': 'Availability (%)',
    },
    width=1400,
    height=max(800, min(5000, 40 * annual_df['bar_label'].nunique())),
)
fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='inside',
    insidetextanchor='middle',
    textfont_color='white',
)
fig.update_xaxes(tickformat='%Y')
fig.update_yaxes(autorange='reversed')
fig.write_html('index.html')
