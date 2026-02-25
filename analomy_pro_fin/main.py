# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from scipy.stats import zscore
# import dash
# from dash import dcc, html, dash_table
# from dash.dependencies import Input, Output, State
# import base64
# import io
# import dash_bootstrap_components as dbc
# import numpy as np
# app = dash.Dash(__name__, title="Anomaly Detector", external_stylesheets=[dbc.themes.CYBORG])

# styles = {
#     'background': '#1a1a2e',
#     'text': '#e0e0e0',
#     'primary': '#0f4c75',
#     'secondary': '#6f3dff',
#     'success': '#00bfa5',
#     'danger': '#ff006e',
#     'info': '#4c00b0',
#     'warning': '#ffc400',
#     'card_bg': '#2a2a4a',
#     'card_border': '#4c4c6c',
#     'sidebar_bg': '#121226',
#     'sidebar_text': '#ffffff',
# }
# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <style>
#             @keyframes fadeIn {
#                 0% { opacity: 0; }
#                 100% { opacity: 1; }
#             }
#             .fade-in {
#                 animation: fadeIn 1s ease-in-out;
#             }
#             @keyframes pulse {
#                 0% { transform: scale(1); }
#                 50% { transform: scale(1.05); }
#                 100% { transform: scale(1); }
#             }
#             .pulse {
#                 animation: pulse 2s infinite;
#             }
#             .card {
#                 transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
#                 border: 1px solid ''' + styles['card_border'] + ''';
#                 border-radius: 10px;
#                 background-color: ''' + styles['card_bg'] + ''';
#             }
#             .card:hover {
#                 transform: translateY(-5px);
#                 box-shadow: 0 10px 20px rgba(0,0,0,0.2);
#             }
#             /* Custom styling for the dropdown */
#             .Select-control, .Select-menu-outer, .Select-input {
#                 background-color: ''' + styles['card_bg'] + ''' !important;
#                 color: ''' + styles['text'] + ''' !important;
#                 border: 1px solid ''' + styles['card_border'] + ''' !important;
#             }
#             .Select-placeholder {
#                 color: ''' + styles['text'] + ''' !important;
#                 opacity: 0.6;
#             }
#             .Select-value-label {
#                 color: ''' + styles['text'] + ''' !important;
#             }
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''

# app.layout = html.Div(
#     style={'backgroundColor': styles['background'], 'minHeight': '100vh', 'fontFamily': 'sans-serif', 'display': 'flex', 'color': styles['text']},
#     children=[
       
#         dbc.Container(
#             style={'backgroundColor': styles['sidebar_bg'], 'width': '250px', 'padding': '20px', 'minHeight': '100vh', 'position': 'fixed', 'top': 0, 'left': 0},
#             children=[
#                 html.H2(
#                     "Anomaly Detector",
#                     style={'color': styles['secondary'], 'fontSize': '1.8rem', 'fontWeight': 'bold', 'marginBottom': '30px', 'textAlign': 'center', 'textShadow': '2px 2px 4px rgba(0,0,0,0.5)'}
#                 ),
#                 html.Div([
#                     dbc.NavLink("Dashboard", href="/", active="exact", className="nav-link", style={'color': styles['sidebar_text'], 'fontWeight': 'bold', 'fontSize': '1.1rem'}),
#                     html.A("Reports", id="download-report-link", href="#", className="nav-link", style={'color': styles['sidebar_text'], 'opacity': 0.7, 'fontSize': '1.1rem', 'textDecoration': 'none'}),
#                 ]),
#                 html.Hr(style={'borderColor': styles['sidebar_text'], 'marginTop': '20px', 'marginBottom': '20px'}),
#                 html.H5("Analysis Controls", style={'color': styles['sidebar_text'], 'fontSize': '1.2rem'}),
#                 html.P("Select Feature:", style={'color': styles['sidebar_text'], 'marginTop': '15px'}),
#                 dcc.Dropdown(
#                     id='feature-dropdown',
#                     placeholder="Select a numerical feature...",
#                     style={'color': styles['text'], 'backgroundColor': styles['card_bg'], 'border': 'none'},
#                     className="mb-3"
#                 ),
#                 html.P("Z-Score Threshold:", style={'color': styles['sidebar_text'], 'marginTop': '20px'}),
#                 dcc.Slider(
#                     id='z-score-threshold-slider',
#                     min=1, max=5, step=0.1, value=3,
#                     marks={i: {'label': str(i), 'style': {'color': styles['sidebar_text']}} for i in range(1, 6)},
#                     tooltip={"placement": "bottom", "always_visible": True},
#                     className="mt-2"
#                 ),
#                 html.Hr(style={'borderColor': styles['sidebar_text'], 'marginTop': '20px', 'marginBottom': '20px'}),
#                 html.P(
#                     "Drag and Drop or Click to Upload CSV",
#                     style={'textAlign': 'center', 'color': styles['sidebar_text'], 'fontSize': '1rem'}
#                 ),
#                 dcc.Upload(
#                     id='upload-data',
#                     children=html.Div([
#                         dbc.Button(
#                             'Upload File',
#                             color="info",
#                             className="btn-block",
#                             style={'width': '100%'}
#                         )
#                     ]),
#                     style={'marginTop': '10px'},
#                     multiple=False
#                 ),
               
#                 dcc.Download(id="download-report-trigger"),
#             ]
#         ),
       
#         html.Div(
#             style={'flexGrow': 1, 'padding': '30px', 'marginLeft': '250px'},
#             className="fade-in",
#             children=[
             
#                 dbc.Row([
#                     dbc.Col(
#                         children=[
#                             html.H1("Anomaly Detection Dashboard", style={'color': styles['text'], 'fontSize': '2.5rem', 'fontWeight': 'bold'}),
#                             html.P("Dynamic analysis of CSV data with real-time visualizations.", style={'color': styles['text'], 'opacity': 0.8}),
#                         ],
#                         width=12,
#                     ),
#                 ], className="mb-4"),

              
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody([
#                                     html.H5("Total Rows", className="card-title text-muted"),
#                                     html.H3("0", id="total-rows-kpi", className="card-text text-light font-weight-bold pulse")
#                                 ]),
#                             ),
#                             md=4,
#                         ),
#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody([
#                                     html.H5("Numerical Features", className="card-title text-muted"),
#                                     html.H3("0", id="numeric-features-kpi", className="card-text text-info font-weight-bold pulse")
#                                 ]),
#                             ),
#                             md=4,
#                         ),
#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody([
#                                     html.H5("Total Anomalies", className="card-title text-muted"),
#                                     html.H3("0", id="total-anomalies-kpi", className="card-text text-danger font-weight-bold pulse")
#                                 ]),
#                             ),
#                             md=4,
#                         ),
#                     ],
#                     className="mb-4",
#                 ),
                
             
#                 dcc.Loading(
#                     id="loading-spinner",
#                     type="circle",
#                     color=styles['secondary'],
#                     children=html.Div(id='output-data-upload'),
#                     className="p-4"
#                 ),
                
            
#                 dcc.Store(id='stored-data', data=None),
#                 dcc.Store(id='numeric-cols', data=None),
#                 dcc.Store(id='anomalous-data-store', data=None),

              
#                 html.Div(
#                     id='plots-container',
#                     children=[
                    
#                         dbc.Row([
#                             dbc.Col(
#                                 dbc.Card(
#                                     dbc.CardBody([
#                                         html.H5("Normal vs. Abnormal", className="card-title"),
#                                         dcc.Graph(id='anomaly-scatter-plot', figure=go.Figure())
#                                     ]),
#                                 ),
#                                 id='scatter-plot-col',
#                                 md=12,
#                             )
#                         ], className="mb-4"),
                        
                       
#                         dbc.Row(id='histogram-plots-row', className="mb-4"),

#                         dbc.Row([
#                             dbc.Col(
#                                 dbc.Card(
#                                     dbc.CardBody([
#                                         html.H5("Anomalous Data Points", className="card-title"),
#                                         dash_table.DataTable(
#                                             id='anomaly-table',
#                                             columns=[],
#                                             data=[],
#                                             style_header={
#                                                 'backgroundColor': styles['card_bg'],
#                                                 'color': styles['text'],
#                                                 'fontWeight': 'bold'
#                                             },
#                                             style_data={
#                                                 'backgroundColor': styles['card_bg'],
#                                                 'color': styles['text']
#                                             },
#                                             style_cell={
#                                                 'textAlign': 'left',
#                                                 'padding': '10px',
#                                                 'border-bottom': '1px solid ' + styles['card_border']
#                                             },
#                                             style_table={'overflowX': 'auto'}
#                                         )
#                                     ]),
#                                 ),
#                                 md=12
#                             )
#                         ])
#                     ],
#                     style={'display': 'none'}
#                 )
#             ]
#         )
#     ]
# )

# @app.callback(
#     [Output('output-data-upload', 'children'),
#      Output('plots-container', 'style'),
#      Output('feature-dropdown', 'options'),
#      Output('stored-data', 'data'),
#      Output('numeric-cols', 'data'),
#      Output('total-rows-kpi', 'children'),
#      Output('numeric-features-kpi', 'children')],
#     [Input('upload-data', 'contents')],
#     [State('upload-data', 'filename')]
# )
# def handle_file_upload(contents, filename):
#     if contents is None:
#         return (
#             html.Div(
#                 "Please upload a CSV file to get started.",
#                 style={'textAlign': 'center', 'color': styles['secondary'], 'padding': '20px'}
#             ),
#             {'display': 'none'},
#             [],
#             None,
#             None,
#             "0",
#             "0"
#         )

#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
    
#     try:
#         if 'csv' in filename:
#             df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
#         else:
#             return (
#                 html.Div('Please upload a CSV file.', style={'color': styles['danger'], 'textAlign': 'center'}),
#                 {'display': 'none'},
#                 [],
#                 None,
#                 None,
#                 "0",
#                 "0"
#             )
#     except Exception as e:
#         return (
#             html.Div(f'There was an error processing this file: {e}', style={'color': styles['danger'], 'textAlign': 'center'}),
#             {'display': 'none'},
#             [],
#             None,
#             None,
#             "0",
#             "0"
#         )

#     numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    
#     return (
#         None,
#         {'display': 'block'},
#         [{'label': col.replace('_', ' ').title(), 'value': col} for col in numeric_columns],
#         df.to_dict('records'),
#         numeric_columns,
#         str(len(df)),
#         str(len(numeric_columns))
#     )

# @app.callback(
#     [Output('anomaly-scatter-plot', 'figure'),
#      Output('histogram-plots-row', 'children'),
#      Output('anomaly-table', 'data'),
#      Output('anomaly-table', 'columns'),
#      Output('total-anomalies-kpi', 'children'),
#      Output('anomalous-data-store', 'data')],
#     [Input('stored-data', 'data'),
#      Input('numeric-cols', 'data'),
#      Input('feature-dropdown', 'value'),
#      Input('z-score-threshold-slider', 'value')]
# )
# def update_analysis(data, numeric_cols, selected_feature, z_score_threshold):
#     if data is None or selected_feature is None or numeric_cols is None:
#         return go.Figure(), [], [], [], "0", None

#     df = pd.DataFrame(data)

#     if selected_feature not in df.columns or df[selected_feature].dtype not in ['int64', 'float64']:
#         return go.Figure(), [], [], [], "0", None

#     df['z_score'] = zscore(df[selected_feature].dropna())
#     df['anomaly_label'] = df['z_score'].apply(
#         lambda x: 'Abnormal' if abs(x) > z_score_threshold else 'Normal'
#     )
    
#     anomalous_points = df[df['anomaly_label'] == 'Abnormal'].copy()
    
#     scatter_x = selected_feature
#     other_features = [col for col in numeric_cols if col != selected_feature]
#     scatter_y = other_features[0] if other_features else selected_feature
    
#     if scatter_x == scatter_y:
#         df['index'] = df.index
#         scatter_y = 'index'

#     anomaly_scatter = px.scatter(
#         df,
#         x=scatter_x,
#         y=scatter_y,
#         color='anomaly_label',
#         title=f'Anomaly Detection: {scatter_x.replace("", " ").title()} vs. {scatter_y.replace("", " ").title()}',
   
#         color_discrete_map={'Normal': '#90ee90', 'Abnormal': styles['danger']},
#         hover_data=[scatter_x, scatter_y, 'z_score']
#     )
#     anomaly_scatter.update_layout(plot_bgcolor=styles['card_bg'], paper_bgcolor=styles['card_bg'], font=dict(color=styles['text']))

#     histogram_plots = []
#     for col in numeric_cols:
#         hist_fig = px.histogram(
#             df,
#             x=col,
#             color='anomaly_label',
#             title=f'Distribution of {col.replace("_", " ").title()}',
          
#             color_discrete_map={'Normal': '#90ee90', 'Abnormal': styles['danger']}
#         )
#         hist_fig.update_layout(plot_bgcolor=styles['card_bg'], paper_bgcolor=styles['card_bg'], font=dict(color=styles['text']))
        
#         histogram_plots.append(
#             dbc.Col(
#                 dbc.Card(
#                     dbc.CardBody([
#                         html.H5(f'{col.replace("_", " ").title()} Distribution', className="card-title"),
#                         dcc.Graph(figure=hist_fig)
#                     ]),
#                 ),
#                 md=6,
#             )
#         )

#     anomalous_points = df[df['anomaly_label'] == 'Abnormal'].copy()
#     anomalous_points['index'] = anomalous_points.index
#     anomalous_points['z_score'] = anomalous_points['z_score'].round(2)
#     anomalous_table_data = anomalous_points.to_dict('records')
    
#     table_cols = [{'name': i.replace('_', ' ').title(), 'id': i} for i in ['index'] + numeric_cols + ['z_score']]
#     total_anomalies_count = len(anomalous_points)
#     anomalous_data_json = anomalous_points.to_json(date_format='iso', orient='split')
#     return (
#         anomaly_scatter,
#         histogram_plots,
#         anomalous_table_data,
#         table_cols,
#         str(total_anomalies_count),
#         anomalous_data_json
#     )

# @app.callback(
#     Output("download-report-trigger", "data"),
#     [Input("download-report-link", "n_clicks")],
#     [State('anomalous-data-store', 'data')],
#     prevent_initial_call=True,
# )
# def generate_report(n_clicks, anomalous_data_json):
#     if n_clicks and anomalous_data_json:
#         df = pd.read_json(anomalous_data_json, orient='split')
#         return dcc.send_data_frame(df.to_csv, "anomaly_report.csv")
#     return None

# if __name__ == '__main__':
#     app.run(debug=True)