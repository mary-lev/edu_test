import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

import pandas as pd
df = pd.read_json('data/messages.json')
df['long'] = df['text'].apply(lambda x: len(x) if x is not None else 0)
df['day'] = df['date'].dt.date

dn = df.groupby(['channel', 'day']).count()


fig = px.line(df, x='day', y='long', color='channel')
fig.update_xaxes(rangeslider_visible=True)


date_div = opy.plot(fig, auto_open=False, output_type='div')