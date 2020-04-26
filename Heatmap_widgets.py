#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json, datetime as dt
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Image, Layout
import os


# In[6]:


imgs = {}
case_imgs = {}
for imgfile in os.listdir('imgs/'):
    if imgfile != '.ipynb_checkpoints':
        file = open("imgs/"+imgfile, "rb")
        image = file.read()
        imgs[imgfile.split('.')[0]] = image
for imgfile in os.listdir('case_imgs/'):
    if imgfile != '.ipynb_checkpoints':
        file = open("case_imgs/"+imgfile, "rb")
        image = file.read()
        case_imgs[imgfile.split('.')[0]] = image
misinfo_widget = Image(
    value=imgs['CA'],
    layout=Layout(height='252px', width='400px')
    )
covid_widget = Image(
    value=case_imgs['CA'],
    layout=Layout(height='252px', width='400px'))


# In[11]:



def hover_fn(trace, points, state):
    inds = points.point_inds
    if inds:
        ind = inds[0]
        trace_index = points.trace_index
        state = trace['locations'][ind]
        if state in imgs:
            misinfo_widget.value = imgs[state]
            covid_widget.value = case_imgs[state]
    


# In[12]:


with open('covidstatesdaily.json') as f:
    #data = json.load(f)
    pandaData = pd.read_json(f)

fig = go.FigureWidget(data=[go.Choropleth(
    locations=pandaData[:50]['state'], # Spatial coordinates
    z = pandaData[:50]['positive'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Confirmed Cases",
    
)])
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
    #print(dataFramArr)
    
for frame in dataFramArr:
    trace = go.Choropleth(
    locations=frame['state'], # Spatial coordinates
    z = frame['positive'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Confirmed Cases",   
    )
    #trace.on_hover(hover_fn)
    fig.add_trace(trace)  
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
for trace in fig.data:
    trace.on_hover(hover_fn)
VBox([fig, HBox([misinfo_widget, covid_widget])])


# In[ ]:




