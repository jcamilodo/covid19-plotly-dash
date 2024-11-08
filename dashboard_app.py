import json
import os
from urllib.request import urlopen
import urllib3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import plotly.express as px
import pandas as pd

from utils import agrupar_departamentos, ciudad_indice, muertes_mes_anio, frecuencia_muertes
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

path = os.path.dirname(__file__)

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Covid19 Colombia - Data Analysis Dashboard')

#cargar informacion de datos georeferenciados
departamentos = None
with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/colombia.geo.json') as response:
#with open(f'{path}/colombia.geo.json') as response:
    departamentos = json.load(response)

#leer achivo desde google drive
"""
El archivo previamente fue preparado en los siguiente campos
FECHA DEFUNCIÓN 
FECHA REGISTRO 
EDAD FALLECIDO 
RANGO EDAD (nuevo campo)
"""

file_id = "1VnQzJi-C-b4-LfHFDg3Yq2yBw5IghDBJ"
dwn_url='https://drive.google.com/uc?id=' + file_id
df = pd.read_csv(dwn_url)

# Convert 'FECHA DEFUNCIÓN' to datetime objects, handling errors
df['FECHA DEFUNCIÓN'] = pd.to_datetime(df['FECHA DEFUNCIÓN'], errors='coerce')

# Filter los datos por los años para tenerlos listos para su proceso
df_2020 = df[df['FECHA DEFUNCIÓN'].dt.year == 2020]
df_2021 = df[df['FECHA DEFUNCIÓN'].dt.year == 2021]


#informacion de datos para el mapa
#Mapa: número total de muertes por covid-19 confirmadas por departamento para el año 2021.
# Filter by COVID-19 = CONFIRMADOS
grouped_dpto_2021 = agrupar_departamentos(df_2021)
locs = grouped_dpto_2021['DEPARTAMENTO']
for loc in departamentos['features']:
    loc['id'] = loc['properties']['NOMBRE_DPT']

fig_mapa = go.Figure(go.Choroplethmapbox(
                    geojson=departamentos,
                    locations=locs,
                    z=grouped_dpto_2021['CANTIDAD'],
                    colorscale='Picnic',
                    colorbar_title="Número"))
fig_mapa.update_layout(mapbox_style="carto-positron",
                        mapbox_zoom=4.0,
                        height=600,
                        mapbox_center = {"lat": 4.570868, "lon": -74.2973328})

# Gráfico de barras horizontal: las 5 ciudades con el mayor índice de muertes por casos de covid-19 confirmados para el año 2021.
municipio_counts = ciudad_indice(df_2021, 5)
fig_mpios = px.bar(municipio_counts, y='MUNICIPIO', x='INDICE_PER', orientation='h', text='INDICE_PER')
fig_mpios.update_xaxes(title_text='Indice de Muertes')
#fig_mpios.update_layout(xaxis_title='Indice por Municipio')

covid_counts = df_2021.groupby('COVID-19').size().reset_index(name='CANTIDAD')
confirmados = covid_counts[covid_counts['COVID-19']=="CONFIRMADO"]['CANTIDAD'].values[0]
sospechosos = covid_counts[covid_counts['COVID-19']=="SOSPECHOSO"]['CANTIDAD'].values[0]
descartados = covid_counts[covid_counts['COVID-19']=="DESCARTADO"]['CANTIDAD'].values[0]
fig_dptos = px.pie(covid_counts, values='CANTIDAD', names='COVID-19', color_discrete_sequence=px.colors.qualitative.Pastel2)


#Gráfico de línea: total de muertes covid-19 confirmados por mes para el año 2020 y 2021.
grouped_by_month = muertes_mes_anio(df)
fig_mes_anio = px.line(grouped_by_month, x='Year-Month', y='CANTIDAD', 
              markers=True, text="CANTIDAD")
#fig.update_traces(textposition="bottom right")
fig_mes_anio.update_xaxes(title_text='Año-Mes')


#Gráfico de histograma de frecuencias de muertes covid-19 confirmados por edades quinquenales (ejemplo: 0-4, 5-9,.....,85-89, 90 o más) para el año 2020.
rango_edad_counts = frecuencia_muertes(df_2020)
# Create the histogram
fig_histo = px.histogram(rango_edad_counts, x='RANGO EDAD', y='CANTIDAD')
fig_histo.update_xaxes(title_text='Rango de Edad')
fig_histo.update_yaxes(title_text='Número de Muertes')


def generate_stats_card (title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '50px','alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px','fontSize': '22px','fontWeight': 'bold'}),
                html.H4(title, className="card-title", style={'margin': '0px','fontSize': '18px','fontWeight': 'bold'})
            ], style={'textAlign': 'center', 'heigh': '150px'}),
        ], style={'paddingBlock':'10px',"backgroundColor":'#33afff','border':'none','borderRadius':'10px'})
    )



# Define the layout of the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src="./assets/reporte-icon.png",width=150), width=2),
            dbc.Col(
                html.Div(
                    html.H2(
                    "Reporte de mortalidad en Colombia de los casos de covid-19 para el año 2020 y 2021"
                    ),
                )
            ,width=9),
        ]),        
        
        dbc.Row([
            dbc.Col(generate_stats_card("Confirmadosss",confirmados,"./assets/confirmado.png"), width=3),
            dbc.Col(generate_stats_card("Sospechoso", sospechosos,"./assets/sospechoso.png"), width=3),
            dbc.Col(generate_stats_card("Descartado",descartados,"./assets/descartado.png"), width=3),
        ],style={'marginBlock': '10px'}),
        dbc.Row([
            html.Div([
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                html.Div(
                                    html.H4("Número total de muertes por covid-19 confirmadas por departamento para el año 2021"),
                                )
                            ),
                            dbc.Row(
                                html.Div([
                                    dcc.Graph(id='mapa', figure=fig_mapa),
                                ], style={'width': '100%', 'display': 'inline-block'}),
                            ),
                        ]),
                    ]),        
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                html.Div(
                                    html.H5("5 ciudades con el mayor índice de muertes por casos de covid-19 confirmados para el año 2021 "),
                                )
                            ),
                            dbc.Row(
                                html.Div([
                                    dcc.Graph(id='mpios', figure=fig_mpios),
                                ], style={'width': '100%', 'display': 'inline-block'}),
                            ),
                        ]),
                        dbc.Col([
                            dbc.Row(
                                html.Div(
                                    html.H5("Total de los casos de covid-19 reportados como confirmados, sospechosos y descartados para el año 2021."),
                                )
                            ),
                            dbc.Row(
                                html.Div([
                                    dcc.Graph(id='dptos', figure=fig_dptos),
                                ], style={'width': '100%', 'display': 'inline-block'}),
                            ),
                        ]),
                    ]),        
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                html.Div(
                                    html.H5("Total de muertes por COVID-19 confirmadas por mes (2020-2021)"),
                                )
                            ),
                            dbc.Row(
                                html.Div([
                                    dcc.Graph(id='mes_anio', figure=fig_mes_anio),
                                ], style={'width': '100%', 'display': 'inline-block'}),
                            ),
                        ]), 
                    ]),        
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(
                                html.Div(
                                    html.H5("Histograma de Frecuencias de Muertes por COVID-19 Confirmadas por Edades Quinquenales (2020)"),
                                )
                            ),
                            dbc.Row(
                                html.Div([
                                    dcc.Graph(id='histo', figure=fig_histo),
                                ], style={'width': '100%', 'display': 'inline-block'}),
                            ),
                        ]),                                                
                    ]),        

                ])
            ])    
        ])
    ], style={'padding': '0px', 'width': '100%'})
], style={'backgroundColor': 'white', 'width': '100%', 'minHeight': '100vh'})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)