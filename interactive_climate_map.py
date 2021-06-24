# import libraries
import pandas as pd
import numpy as np
import plotly as py

# Plotly Components

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# read the data
data = pd.read_csv("data/GlobalLandTemperaturesByCountry.csv")
# data.head()

# check null values in each column
print("Null values in each column:", data.isnull().sum())


# Data Cleaning>>>>>>>>>>>

# drop AverageTemperatureUncertainty
data = data.drop(columns="AverageTemperatureUncertainty")

# rename the columns
data = data.rename(columns={
    'dt': 'Date',
    'AverageTemperature': 'AvgTemp'
})

# drop rows with null values
data = data.dropna()


# Data Preprocessing>>>>>>>>>>

# grouping by country name and date columns
data_countries = data.groupby(['Country', 'Date']).sum(
).reset_index().sort_values('Date', ascending=False)

# masking by the data range
start_date = '2000-01-01'
end_date = '2002-01-01'

mask = (data_countries['Date'] > start_date) & (
    data_countries['Date'] <= end_date)

data_countries = data_countries.loc[mask]

# Data Visualization>>>>>>>>>>

# creating the visualization
fig = go.Figure(data=go.Choropleth(
    locations=data_countries['Country'], locationmode='country names',
    z=data_countries['AvgTemp'], colorscale='Reds',
    marker_line_color='black', marker_line_width=0.5
))

fig.update_layout(
    title_text='Climate Change', title_x=0.5,
    geo=dict(showframe=False, showcoastlines=False,
             projection_type='equirectangular')
)

fig.show()

# manipulating the original dataframe
data_countrydate = data_countries.groupby(
    ['Date', 'Country']).sum().reset_index()

# creating the visualization
fig = px.choropleth(
    data_countrydate, locations="Country", locationmode="country names",
    color="AvgTemp", hover_name="Country", animation_frame="Date"
)

fig.update_layout(
    title_text='Average Temperature Change', title_x=0.5,
    geo=dict(showframe=False, showcoastlines=False)
)

fig.show()
