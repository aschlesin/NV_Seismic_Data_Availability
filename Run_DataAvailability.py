import io
import requests
import plotly.express as px 
import pandas as pd


## Find the data availability in Earthscope
url = 'https://service.iris.edu/fdsnws/availability/1/extent?format=text&net=NV&cha=*&orderby=nslc_time_quality_samplerate&includerestricted=true&nodata=404'
r = requests.get(url)


lines = r.content.decode('utf-8').splitlines()
header = [l for l in lines if l.startswith('#')]
data_lines = [l for l in lines if l and not l.startswith('#')]

columns = header[-1].lstrip('#').split()
df_availability = pd.read_csv(
    io.StringIO('\n'.join(data_lines)),
    sep=r'\s+',
    names=columns,
    engine='python'
)


selected_channels = ['EHZ', 'HHZ', 'CHZ', 'CH3', 'HH3', 'HN3', 'HNZ','CNZ','CN3','BNZ','BN3']
df_filtered = df_availability[df_availability['Channel'].isin(selected_channels)]
df_filtered



plot_df = df_filtered.copy()
plot_df = plot_df.sort_values(by='Station')
plot_df['Earliest'] = pd.to_datetime(plot_df['Earliest'])
plot_df['Latest'] = pd.to_datetime(plot_df['Latest'])
plot_df['label'] = plot_df['Station'] + '.' +plot_df['Location']+'.'+ plot_df['Channel']

fig = px.timeline(
    plot_df,
    x_start='Earliest',
    x_end='Latest',
    y='label',
    color='Channel',
    title='Data Availability — NV Network',
    labels={'label': 'Station.Location.Channel'},
    width=1400,
    height=800,
)
fig.update_yaxes(autorange='reversed')
fig.write_html('index.html')
