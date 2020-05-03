import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table as dt
import numpy as np
import plotly
from plotly import graph_objs as go
import pandas as pd
import seaborn as sns

external_stylesheets = [
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = sns.load_dataset('iris')
index_values = df['species'].astype('category').cat.codes

def df_scatter(df):
    trace = go.Scatter(
        x=df['sepal_width'],
        y=df['sepal_length'],
        mode='markers',
        marker=dict(
            # marker to make size and color in the markers
            color=index_values,
            size=df['petal_width'] * 10),
        text=df['species'])
    data = [trace]
    return data


layout = go.Layout(xaxis=dict(title='Sepal Width'),
                   yaxis=dict(title='Sepal Length'),
                   height=300,
                   margin=dict(l=10, r=10, t=10, b=10),
                   hovermode='closest',
                   template='plotly')


def df_columns_his(df, columns):
    return html.Div([
        html.Div([
            dcc.Graph(id=column + '--row-ids',
                      figure={
                          'data': [
                              go.Histogram(y=df[column], name=i)
                              for i in df['species'].unique()
                          ],
                          'layout':
                          go.Layout(barmode='stack',
                                    height=250,
                                    margin=dict(t=50, b=50, l=50, r=50),
                                    title=column)
                      })
        ],
                 className='six columns') for column in columns
    ],
                    className='row')


app.layout = html.Div([
    html.Div([
        html.H1('Iris Sepal and Petal Scatter Chart',
                style={
                    'fond-family': 'Helvetica',
                    'margin-top': '20',
                    'margin-bottom': '0'
                },
                className='eight columns'),
        html.
        P('Show the width and lenth of the sepal and petal of different iris species',
          style={
              'margin-top': '20',
              'margin-bottom': '0'
          },
          className='eight columns')
    ],
             className='row'),
    html.Div([
        html.H5('Choose Species:'),
        dcc.Checklist(id='species_checklist',
                      options=[{
                          'label': i.upper(),
                          'value': i
                      } for i in df['species'].unique()],
                      value=df['species'].unique(),
                      labelStyle={'display': 'inline-block'})
    ],
             className='row'),
    html.Div(
        [
            html.Div([
                dcc.Graph(id='scatterplot',
                          figure={
                              'data': df_scatter(df),
                              'layout': layout
                          })
            ],
                     style={
                         'height': '300',
                         'margin-top': '0',
                         'margin-bottom': '0'
                     },
                     className='six columns'),
            html.Div(
                [
                    dt.DataTable(
                        id='datatable-row-ids',
                        columns=[
                            {
                                'name': i,
                                'id': i,
                                'deletable': True
                            } for i in df.columns
                            # omit the id column
                            if i != 'id'
                        ],
                        data=df.to_dict('records'),
                        editable=False,
                        filter_action="native",
                        sort_action="native",
                        sort_mode='multi',
                        row_selectable='multi',
                        row_deletable=False,
                        selected_rows=[],
                        page_action='native',
                        page_current=0,
                        page_size=6,
                    )
                ],
                style={
                    'height': '300',
                    'margin-top': '20',
                    'margin-bottom': '20',
                    'margin-right': '20'
                },
                className='six columns')
        ],
        className='row'),
    html.Div(id='datatable-row-ids-container',
             children=[
                 df_columns_his(df, columns=['sepal_width', 'sepal_length']),
                 df_columns_his(df, columns=['petal_width', 'petal_length'])
             ])
])


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('species_checklist', 'value')])
def update_figure(selected_species):
    dff=df[df['species'].isin(selected_species)]
    return {
        'data': df_scatter(dff),
        'layout': layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)
