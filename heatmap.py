import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, datetime as dt
import numpy as np

with open('covidstatesdaily.json') as f:
    #data = json.load(f)
    pandaData = pd.read_json(f)

fig = go.Figure()

dataFramArr = []
mydata = pd.DataFrame(columns=['date','state','positive'])
currDate = ""
for index, row in pandaData.iterrows():
    if(currDate == ""):
        currDate = row['date']
    if(row['date'] != currDate):
        currDate = row['date']
        dataFramArr.append(mydata)
        mydata = pd.DataFrame(columns=['date','state','positive'])
    mydata.loc[index] = [row['date'],row['state'],row['positive']]
    
for frame in dataFramArr:
    fig.add_trace(go.Choropleth(
    locations=frame['state'], # Spatial coordinates
    z = np.log10(frame['positive']), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    text = frame['positive'],
    zmin = 1,
    zmax = 6,
    colorbar=dict(title='Confirmed Cases',
        tickvals = [1,2,3,4,5,5.5],
        ticktext = ['10','100','1000','10000','100000','300000'],
    )
    ))
steps = []
for i in range(len(dataFramArr)-1,-1,-1):
    date = dt.date(2020,4,25) + dt.timedelta(-i-1)
    step = dict(method='restyle',
                args=['visible', [False] * int((len(dataFramArr)))],
                label='{}/{}'.format(date.month, date.day))
    step['args'][1][i] = True
    steps.append(step)
#print(steps)
sliders = [dict(active=0,
                pad={"t": 1},
                steps=steps)]    
layout = dict(geo=dict(scope='usa',
                       projection={'type': 'albers usa'}),
              sliders=sliders)

fig.update_layout(layout)

fig.show()
