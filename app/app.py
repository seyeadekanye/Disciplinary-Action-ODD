#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:56:27 2018

@author: Adekanye
"""

import dash
import pandas as pd
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

# professions_options = professions_options[0:6]
    
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
                value='',
                placeholder='Nursing...'
        )],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.DatePickerSingle(
                id='my-date-1',
                display_format='YYYY',
                placeholder='YYYY',
            ),
            html.Label('Enter a Year'),
        ]), 
            
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
                value='',
                placeholder='Massage Bodywork...'
        )],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.DatePickerSingle(
                id='my-date-2',
                display_format='YYYY',
                placeholder='YYYY',
            ),
            html.Label('Enter a Year'),
        ]), 
            
            html.Div(id='my-div-2', style={'width': '48%', 'display': 'inline-block'}),

    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),


    # html.Label('Multi-Select Dropdown'),
    # dcc.Dropdown(
    #     options=[
    #         {'label': 'New York City', 'value': 'NYC'},
    #         {'label': u'Montréal', 'value': 'MTL'},
    #         {'label': 'San Francisco', 'value': 'SF'}
    #     ],
    #     value=['MTL', 'SF'],
    #     multi=True
    # ),
    ])
])

@app.callback(
    Output(component_id='my-div-1', component_property='children'),
    [Input(component_id='profession', component_property='value')]
)
def update_output_div_1(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

@app.callback(
    Output(component_id='my-div-2', component_property='children'),
    [Input(component_id='profession-2', component_property='value')]
)
def update_output_div_2(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
