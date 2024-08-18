import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Crea l'app Dash
app = dash.Dash(__name__)

# Carica i dati di SpaceX in un DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Ottieni il payload minimo e massimo dal DataFrame
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Layout dell'applicazione
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i} Kg' for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    html.Div(dcc.Graph(id='success-pie-chart')),
])

# Definisci il callback per aggiornare i grafici
@app.callback(
    [Output(component_id='success-payload-scatter-chart', component_property='figure'),
     Output(component_id='success-pie-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_charts(selected_site, selected_payload):
    # Filtra i dati per l'intervallo di payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
    
    if selected_site == 'ALL':
        # Grafico a dispersione per tutti i siti
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                                 color='Booster Version Category',
                                 title='Correlation between Payload and Success for all Sites')
        
        # Grafico a torta per tutti i siti
        pie_fig = px.pie(spacex_df, names='Launch Site', values='class', 
                         title='Total Success Launches by Site')
    else:
        # Filtra i dati per il sito selezionato
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                                 color='Booster Version Category',
                                 title=f'Correlation between Payload and Success for site {selected_site}')
        
        # Grafico a torta per il sito selezionato
        pie_fig = px.pie(filtered_df, names='class', 
                         title=f'Success vs. Failed Launches for site {selected_site}')
    
    return scatter_fig, pie_fig

# Esegui l'applicazione
if __name__ == '__main__':
    app.run_server(debug=True)
