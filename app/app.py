#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:56:27 2018

@author: Adekanye
"""

import dash
import pandas as pd
import numpy as np
from datetime import datetime as dt
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from ratio import fine_license_ratio, profession_fine_license_ratio

# Read in pickled data

license_data = pd.read_pickle('licenses')
fine_data = pd.read_pickle('fines')


# Generate sorted profession list for app dropdown
A = license_data['profession_id'].unique()
B = fine_data['profession_id'].unique()
professions = sorted(list(set(A).intersection(set(B))))
professions_options = []
for profession in professions:
   professions_options.append({'label': profession, 'value': profession})

# Generate sorted year list for licenses
license_date_options_list = sorted([year for year in license_data['licence_year'].unique() if not np.isnan(year)])
date_options_licenses = []
for date in license_date_options_list:
   date_options_licenses.append({'label': date, 'value': date})

# Generate sorted year list for fines
fines_date_options_list = sorted([year for year in fine_data['disciplinary_year'].unique() if not np.isnan(year)])
date_options_fines = []
for date in fines_date_options_list:
   date_options_fines.append({'label': date, 'value': date})

# For Pie chart of Licenses to Fines ratio, we should use and intersection of the dates
# This Prevents errors when querying the data
C = license_date_options_list
D = fines_date_options_list
dates_intersect = sorted(list(set(C).intersection(set(D))))
dates_intersect_list = []
for date in dates_intersect:
   dates_intersect_list.append({'label': date, 'value': date})

# Generate random number to slice professions_option 
# to use for default profession
num = np.random.randint(0,len(professions_options))

    
app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
   html.Div([


       html.H1(['Delaware Licensing and Disciplinary Actions'],style={'textAlign':'center'}),

   #left div
       
       html.Div([
            html.Div([
                html.Label('Select A Year'),
                dcc.Dropdown(
                   id='date-1',
                   options= date_options_fines,
                   value= date_options_fines[-4]['value'],
               ),
            ]), 

            html.Div([
                dcc.Graph(id='graph-1')

              ]),

       ], style={'width': '48%', 'display': 'inline-block'}
       ),

   #right div

       html.Div([
           html.Div([
               html.Label('Select A Profession Type'),
               dcc.Dropdown(
                   id='profession-2',
                   options= professions_options,
                   value=professions_options[num]['value'],
                   placeholder='Nursing...'
                )
            ],),

            html.Div([
                dcc.Graph(id='graph-2')
            ]),

       ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
       ),

   ])
])


@app.callback(
   Output(component_id='graph-1', component_property='figure'),
   [Input(component_id='date-1', component_property='value')]
)
def update_output_div_1(yr):
    filtered_df = fine_data[fine_data['disciplinary_year'] == yr]
    grouped = filtered_df.groupby('profession_id')
    profession_dict = {}
    for profession in filtered_df['profession_id'].unique():
        profession_dict[profession] = len(grouped.get_group(profession))
    
    Profession_df = pd.DataFrame.from_dict(profession_dict, orient='index').reset_index()
    Profession_df.columns = ['Profession', 'Count']
    Profession_df.sort_values(['Count'], ascending=False, inplace=True)

    x=Profession_df['Count']
    y=Profession_df['Profession']

    data = [
        go.Bar(
          x = y,
          y = x)
    ]
    print (len(x),len(y))
    return {
        'data': data,
        'layout': go.Layout(
            xaxis=dict(
                    title='Profession',
                    showticklabels=False),
            yaxis=dict(
                    title='Count',
                    showticklabels=True),
            title='Number of Fines in ' + str(yr) + ' by Profession',
            hovermode='closest'
        )
    }


@app.callback(
   Output(component_id='graph-2', component_property='figure'),
   [Input(component_id='profession-2', component_property='value'),
    Input(component_id='date-1', component_property='value')]
)
def update_output_div_2(profession,yr):
  x, y, count1, count2 = profession_fine_license_ratio(license_data=license_data, fine_data=fine_data, 
    profession=profession, profession_column_license='profession_id',
    profession_column_fine='profession_id', column_name1='licence_year',
    column_name2='disciplinary_year', year=yr)

  data = [
      go.Pie(
        values = [x,y],
        labels = ['No Fines', 'Fines'],
        hole = 0.8)
  ]
  
  return {
      'data': data,
      'layout': go.Layout(
          # annotations = [{'text':profession, 'showarrow':False}],
          annotations = [{'text': 'Licenses Issued: ' + str(count1) + "<br>" + 'Fines Issued: ' + str(count2), 'showarrow':False}],
          title='Licenses issued to Fines Recieved in '+ str(yr),
          hovermode='closest'
      )
  }

if __name__ == '__main__':
   app.run_server(debug=True)