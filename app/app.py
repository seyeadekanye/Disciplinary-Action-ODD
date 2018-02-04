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
               html.Label('Select A Profession Type'),
               dcc.Dropdown(
                   id='profession',
                   options= professions_options,
                   value=professions_options[num],
                   placeholder='Nursing...'
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select A Year'),
                dcc.Dropdown(
                   id='date-1',
                   options= date_options,
                   value= date_options[-4],
               ),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}), 

            html.Div(id='my-div-1', style={'width': '48%', 'display': 'inline-block'}),

       ], style={'width': '48%', 'display': 'inline-block'}
       ),

   #right div

       html.Div([
           html.Div([
               html.Label('Select A Profession Type'),
               dcc.Dropdown(
                   id='profession-2',
                   options= professions_options,
                   value=professions_options[num],
                   placeholder='Nursing...'
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select A Year'),
                dcc.Dropdown(
                   id='date-2',
                   options= date_options,
                   value= date_options[-4],
               ),
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}), 

            html.Div(id='my-div-2', style={'width': '48%', 'display': 'inline-block'}),

       ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
       ),

   ])
])

@app.callback(
   Output(component_id='my-div-1', component_property='children'),
   [Input(component_id='profession', component_property='value'),
    Input(component_id='date-1', component_property='value')]
)
def update_output_div_1(profession, yr):
   return 'year: "{}"'.format(str(yr['value']))

@app.callback(
   Output(component_id='my-div-2', component_property='children'),
   [Input(component_id='profession-2', component_property='value'),
    Input(component_id='date-2', component_property='value')]
)
def update_output_div_2(profession,yr):
   return 'You\'ve entered "{}"'.format(profession['value'])





if __name__ == '__main__':
   app.run_server(debug=True)