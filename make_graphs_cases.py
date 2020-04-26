import matplotlib.pyplot as plt
import json, pandas as pd, numpy as np
import datetime as dt

STATE_NAMES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
STATE_ABBR = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
abbrs_dict = dict(zip(STATE_ABBR, STATE_NAMES))
names_to_abbrs = dict(zip(STATE_NAMES, STATE_ABBR))
startDate = dt.date(2020,1,22)
endDate = dt.date(2020,4,25)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)

with open('covidstatesdaily.json') as f:
    pandaData = pd.read_json(f)

headers = ['date'] + STATE_ABBR
initial_data = np.zeros(((endDate-startDate).days,50),dtype=int)
dates = np.array(["{}/{}".format(date.month, date.day) for date in daterange(startDate, endDate)])
intarray = ['int32'] * 50
forced = dict(zip(STATE_ABBR, intarray))
initial_data = np.hstack((dates[:,None],initial_data))
state_data = pd.DataFrame(data=initial_data,columns = headers)
state_data = state_data.astype(forced)
print(state_data.shape)
for index, row in pandaData.iterrows():
    rawdate = str(row['date'])
    date = "{}/{}".format(rawdate[-3:-2],rawdate[-2:])
    state = row['state']
    if state in STATE_ABBR:
        entry = row['positive']
        state_data.loc[state_data['date']==date,state] = entry

for column in state_data.loc[:,'AL':'WY']:
    plt.cla()
    plt.plot(dates, state_data[column])
    plt.xlabel('Date')
    plt.ylabel('Positive test results of COVID-19')
    plt.title(abbrs_dict[column])
    plt.xticks(dates[::7])
    plt.savefig('case_imgs/'+column+'.png')

