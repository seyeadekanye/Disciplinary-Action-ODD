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
from ratios import profession_fine_license_ratio
from query import generate_professions_list, generate_dates_list, get_data


license_data, fine_data = get_data()
professions_options, num = generate_professions_list(license_data, fine_data)
dates = generate_dates_list(license_data, fine_data)

    
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
                   options= dates,
                   value= dates[-4]['value'],
               ),
            ], style={
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(250, 250, 250)',
                    'padding': '10px 5px'
            }), 

            html.Div([
                dcc.Graph(id='graph-1',
                          clickData = {'points': [{'x': professions_options[num]['value']}]}
                ),
              ]),

       ], style={'width': '48%', 'display': 'inline-block'}
       ),

   #right div

       html.Div([
            html.Div([
                dcc.Graph(id='graph-2'),
            ]),

       ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
       ),

   ]),

  html.Div([
      dcc.Graph(id='graph-3'),
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
    [Input(component_id='date-1', component_property='value'),
    Input(component_id='graph-1', component_property='clickData')]
)
def update_output_div_2(yr,clickData):
  click = clickData['points'][0]['x']
  x, y, count1, count2 = profession_fine_license_ratio(license_data=license_data, fine_data=fine_data,
    profession=click, profession_column_license='profession_id',
    profession_column_fine='profession_id', column_name1='licence_year',
    column_name2='disciplinary_year', year=yr)   

  data = [
      go.Pie(
        values = [x,y],
        labels = ['No Fines', 'Fines'],
        hole = 0.6)
  ]
  
  return {
      'data': data,
      'layout': go.Layout(
          annotations = [{'text': 'Licenses Issued: ' + str(count1) + "<br>" + 'Fines Issued: ' + str(count2), 'showarrow':False}],
          title=click + '<br>' + 'Licenses issued to Fines Recieved in '+ str(yr),
          hovermode='closest'
      )
  }
  
@app.callback(
   Output(component_id='graph-3', component_property='figure'),
    [Input(component_id='date-1', component_property='value'),
    Input(component_id='graph-1', component_property='clickData')]
)
def update_output_div_3(yr,clickData):
  click = clickData['points'][0]['x']
  year_list = [yr-4,yr-3,yr-2,yr-1,yr]
  year_list = [dt.strptime(str(yr),'%Y') for yr in year_list]
  count_list = []
  for year in year_list:
    _, _, _, count = profession_fine_license_ratio(license_data=license_data, fine_data=fine_data,
      profession=click, profession_column_license='profession_id',
      profession_column_fine='profession_id', column_name1='licence_year',
      column_name2='disciplinary_year', year=year.year)

    count_list.append(count)
  data = [
        go.Scatter(
          x=year_list,
          y=count_list,
          mode="markers+lines", 
          name='bird_name',
          line={'shape':'spline', 'smoothing':0.1, 'width':3},
          marker={'size': 6, 'opacity': .7})
  ]

  layout = go.Layout(
              title='5 Year Disciplinary Action Trend for ' + click + ' Linceses <br>' +
                    str(year_list[0].year) + ' to ' + str(year_list[-1].year), 
              xaxis={'title':'Year'}, 
              yaxis={'title':'Fine Count', 'range':[0,max(count_list) + 10]})


  return {
      'data': data,
      'layout': layout
  }

if __name__ == '__main__':
  app.run_server(debug=True)