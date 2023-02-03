from colorama import Style
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# df = pd.read_csv("HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")
# df_states = df[(~df["estado"].isna())&(df["codmun"].isna())]
# df_brasil = df[df["regiao"]=="Brasil"]
# df_brasil.to_csv("df_brasil.csv")
# df_states.to_csv("df_states.csv")


# =====================================================================
# Data Load
df_states = pd.read_csv("C:/Users/felip/OneDrive/Área de Trabalho/GIT/dashboard/Python/df_states.csv")

df_brasil = pd.read_csv("C:/Users/felip/OneDrive/Área de Trabalho/GIT/dashboard/Python/df_brasil.csv")

token = open("D:/Área de Trabalho/Dashboard COVID-19/.mapbox_token").read()
brazil_states = json.load(open("C:/Users/felip/OneDrive/Área de Trabalho/GIT/dashboard/Python/geojson/brazil_geo.json", "r"))

df_states_ = df_states[df_states["data"] == "2020-05-13"]

# Colunas que podem ser selecionadas para visualizar no gráfico de barras
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}

# =======================================
# Inicialização do dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

fig = px.choropleth_mapbox(df_states_, locations="estado",labels={'obitosAcumulados':'TEST'}, geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},zoom=4, color="obitosAcumulado", color_continuous_scale="Plotly3", opacity=0.3,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )

fig.update_layout(
                mapbox_accesstoken=token,
                paper_bgcolor="#242424",
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=True,
                font=dict(
                    family="Courier New, monospace",
                    color="white"
                )
                )
fig.layout.coloraxis.colorbar.title = 'Óbitos'
        
                
df_data = df_states[df_states["estado"] == "CE"]


fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#212225",
    plot_bgcolor="#212225",
    height=250,
    margin=dict(l=10, r=10, b=10, t=10),
    )



# =======================================
# Construção layout

app.layout = dbc.Container(
    children=[
        
        dbc.Row([
            dbc.Col([
                html.H2("PYTHON / COVID-19",id = "title",style={"text-align":"center","margin-top":"1px", "padding": "10px","background-color":"#242424","text-shadow": "2px 2px #000000","border-radius": "25px","box-shadow":"0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)","color":"white"}),
                html.Div([
                    dbc.Button("BRASIL",color="light ", id = "location-button", size="lg block", style={"width":"100%","color":"black", "font-weight":"bold", "background-color":"white"})
                ], style={"width":"100%"}),
                html.Div(id="div-test",children=[
                    html.P("Selecione uma data: ", style={"margin-top":"10px"}),
                    dcc.DatePickerSingle(
                        id="datePicker",
                        min_date_allowed=df_brasil["data"].min(),
                        max_date_allowed=df_brasil["data"].max(),
                        initial_visible_month = df_brasil["data"].min(),
                        date = df_brasil["data"].max(),
                        display_format = "DD/MM/YYYY",
                        style = {"border":"0px solid black","margin-left":"10px","margin-top":"10px"}
                    ),
                    dbc.Button("GERAL",color="light ", n_clicks=0, id = "Geral-Button", size="lg block", style={"width":"100%","color":"black", "font-weight":"bold", "background-color":"white","margin-left":"10px","margin-top":"10px"})
                ], style={"display":"flex","align":"center"}),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Curados"),
                                html.H4(style={"color":"#00fe00"}, id = "casos-curados-text"),
                                html.Span("Em Acompanhamento:"),
                                html.H5(style={"color":"#ffffff"}, id = "casos-acompanhamento-text"),
                            ])
                        ], color="dark", outline=True, style={ "margin-top":"5px","margin-bottom":"5px","box-shadow":"0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)", "color":"#ffffff"}),
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Contaminados"),
                                html.H4(style={"color":"#04c0f8"}, id = "casos-confirmados-text"),
                                html.Span("Novos casos  na data"),
                                html.H5(style={"color":"#ffffff"}, id = "novos-casos-text"),
                            ])
                        ], color="dark", outline=True, style={ "margin-top":"5px","margin-bottom":"5px","box-shadow":"0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)", "color":"#ffffff"}),
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Span("Óbitos Confirmados"),
                                html.H4(style={"color":"#fe0000"}, id = "obitos-text"),
                                html.Span("Óbitos na data"),
                                html.H5(style={"color":"#ffffff"}, id = "obitos-data-text"),
                            ])
                        ], color="dark", outline=True, style={ "margin-top":"5px","margin-bottom":"5px","box-shadow":"0 4px 4px 0 rgba(0,0,0,0.15), 0 4px 20px 0 rgba(0,0,0,0.19)", "color":"#ffffff"}),
                    ], md=4),
                ]),

                html.Div([
                    html.P("Seleciona o tipo de dado que deseja visualizar: ", style={"margin-top":"10px"}),
                    dcc.Dropdown(id="location-dropdown",
                        options=[{"label": j, "value":i} for i,j in select_columns.items()],
                        value="casosNovos",
                        style={"margin-top":"10px"}
                    ),
                    dcc.Graph(id="barGraph", figure=fig2)  
                ]),
            ],md=5, style={"padding":"10px","background-color":"#242424"}),

            dbc.Col([
                dcc.Loading(id="loading",type="default",children=[
                    dcc.Graph(id="choropleth_map", figure=fig,config= dict( displayModeBar = False),
                    style={"height":"100vh","margin-right":"10px"})
                ])
            ],md=7) ,
            html.P(id='placeholder')
        ], class_name="g-0")
    ], fluid=True)

# =======================================
# Interatividade
@app.callback(
    [
        # Output
        Output("casos-curados-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("obitos-text", "children"),
        Output("casos-acompanhamento-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-data-text", "children")
    ],  
    [
        # Imput
        Input("datePicker","date"),
        Input("location-button","children"),
    ]
)

def display_status(date, location):
    # print(location, date) 
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )



@app.callback(
        Output("barGraph", "figure"),
        [Input("location-dropdown", "value"),Input("location-button", "children")]
)
def plot_barGraph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]
    fig2 = go.Figure(layout={"template":"plotly_dark"})


    bar_plots = ["casosNovos", "obitosNovos"]

    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#212225",
        plot_bgcolor="#212225",
        height=250,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    
    return fig2


@app.callback(Output("choropleth_map","figure"),[Input("datePicker","date")])

def update_map(date):
    fig = px.choropleth_mapbox(df_states_, locations="estado",labels={'obitosAcumulados':'TEST'}, geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},zoom=4, color="obitosAcumulado", color_continuous_scale="Plotly3", opacity=0.3,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}
    )

    fig.update_layout(
                    mapbox_accesstoken=token,
                    paper_bgcolor="#242424",
                    mapbox_style="carto-darkmatter",
                    autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                    showlegend=True,
                    font=dict(
                        family="Courier New, monospace",
                        color="white"
                    )
                    )
    fig.layout.coloraxis.colorbar.title = 'Óbitos'

    return fig

@app.callback([
    Output("location-button","children"),
    Output("Geral-Button", 'n_clicks'),
    ],
    [
    Input("choropleth_map","clickData"),
    Input("location-button","n_clicks"),
    Input("Geral-Button", 'n_clicks') 
    ])
def update_location(click_data,n_clicks_location,n_clicks_Geral):
    if n_clicks_Geral:
        n_clicks_Geral = 0
        return ("BRASIL",0)
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-buttton.n_clicks_location":
        state = click_data["points"][0]["location"]
        return ("{}".format(state),0)
    else:
        return ("BRASIL",0)
        




# =======================================
# Inicializando serve

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
