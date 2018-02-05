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


# Generate profession list for app dropdown
A = license_data['profession_id'].unique()
B = fine_data['profession_id'].unique()
professions = list(set(A).intersection(set(B)))
professions_options = []
for profession in professions:
   professions_options.append({'label': profession, 'value': profession})

# Generate year list
date_options_list = np.arange(min(license_data['licence_year']), dt.now().year+3)
date_options = []
for date in date_options_list:
   date_options.append({'label': date, 'value': date})

# Generate random number to slice professions_option 
# to use for default profession
num = np.random.randint(0,len(professions_options))

    
app = dash.Dash()

app.layout = html.Div([
   html.Div([


       html.H1(['Delaware Licensing and Disciplinary Actions'],style={'textAlign':'center'}),

   #left div
       
       html.Div([
            html.Div([
                html.Label('Select A Year'),
                dcc.Dropdown(
                   id='date-1',
                   options= date_options,
                   value= date_options[-4]['value'],
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
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select A Year'),
                dcc.Dropdown(
                   id='date-2',
                   options= date_options,
                   value= date_options[-4]['value'],
               ),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}), 

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
    filtered_df = license_data[license_data['licence_year'] == yr]
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
    
    return {
        'data': data,
        'layout': go.Layout(
            xaxis=dict(
                    title='Profession',
                    showticklabels=False),
            yaxis=dict(
                    title='Count',
                    showticklabels=True),
            title='Number of Fines in A Year by Profession',
            hovermode='closest'
        )
    }


@app.callback(
   Output(component_id='graph-2', component_property='figure'),
   [Input(component_id='profession-2', component_property='value'),
    Input(component_id='date-2', component_property='value')]
)
def update_output_div_2(profession,yr):

  try:
    x, y = profession_fine_license_ratio(license_data=license_data, fine_data=fine_data, 
      profession=profession, profession_column_license='profession_id',
      profession_column_fine='profession_id', column_name1='licence_year',
      column_name2='disciplinary_year', year=yr)
  except TypeError:
    x,y = 100,0

  data = [
      go.Pie(
        values = [x,y],
        labels = ['No Fines', 'Fines'],
        hole = 0.4)
  ]
  
  return {
      'data': data,
      'layout': go.Layout(
          annotations = [{'text':profession[0:10], 'showarrow':False}],
          title='Licenses issued to Fines Recieved',
          hovermode='closest'
      )
  }

if __name__ == '__main__':
   app.run_server(debug=True)