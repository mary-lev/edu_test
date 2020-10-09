import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as opy

import pandas as pd
df = pd.read_json('core/messages.json')
df['long'] = df['text'].apply(lambda x: len(x) if x is not None else 0)

dn = df.groupby(['channel', 'date']).count()


fig = px.line(df, x="date", y="long", color='channel')
fig.update_xaxes(rangeslider_visible=True)


date_div = opy.plot(fig, auto_open=False, output_type='div')