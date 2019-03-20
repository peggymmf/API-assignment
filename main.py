# Edit by Peggy, 2019-03-19

# [START app]

import requests
from pandas import DataFrame
import datetime
from flask import Flask, Response

# Load json into a Python object
url = 'http://mysafeinfo.com/api/data?list=englishmonarchs&format=json'
r = requests.get(url)

# json to dataframe
df = DataFrame(r.json())

# change yrs to Year of Birth
df['Year of Birth'] = df.loc[:, 'yrs'].str.split('-').apply(lambda x: x[0])

# remove rows of 'House of Wessex'
df = df.drop(df[df['hse'] == 'House of Wessex'].index)

# reverse firstname using[::-1]
df['name_reverse'] = df.loc[:, 'nm'].str.split().apply(lambda x: x[0][::-1])

# sort names alphabetically
df = df.sort_values(by=['name_reverse'])

# change country to acronym
df['Country'] = df.loc[:, 'cty'].str.split().apply(lambda x: x[0][0]+x[1][0])

# add datestamp: Ingestion Time
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df.insert(0, 'Ingestion Time', now)

# creat new dataframe
df_new = df[['name_reverse', 'Country', 'hse', 'Year of Birth', 'Ingestion Time']]
# reset index
df_new = df_new.reset_index(drop=True)
# rename column
df_new = df_new.rename(index=str, columns={"name_reverse": "Name", "hse": "House"})

# save to csv file with headers
df_new.to_csv("answer.csv", header=True)

app = Flask(__name__)


# response to download csv file
@app.route("/")
def index():
    with open("answer.csv") as fp:
        csv = fp.read()
        return Response(
            csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename = answer.csv"})

    
if __name__ == "__main__":
    app.run()

# [END app]
