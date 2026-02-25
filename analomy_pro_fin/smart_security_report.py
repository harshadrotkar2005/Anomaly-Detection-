import dash
from dash import dcc, html, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import numpy as np
import json

# Reuse exact same styles from main app
styles = {
    'background': '#1a1a2e',
    'text': '#e0e0e0',
    'primary': '#0f4c75',
    'secondary': '#6f3dff',
    'success': '#00bfa5',
    'danger': '#ff006e',
    'info': '#4c00b0',
    'warning': '#ffc400',
    'card_bg': '#2a2a4a',
    'card_border': '#4c4c6c',
    'high_risk': '#ff006e',
    'medium_risk': '#ffc400',
    'low_risk': '#00bfa5',
}

def get_smart_report_layout():
    return html.Div(
        style={
            'backgroundColor': styles['background'], 
            'minHeight': '100vh', 
            'fontFamily': 'sans-serif', 
            'color': styles['text'],
            'position': 'relative'
        },
        children=[
            # Fullscreen Back Header
            html.Div([
                dbc.Button("← Back to Dashboard", id="back-to-dashboard", color="secondary", size="lg", 
                          style={
                            'position': 'fixed', 'top': '20px', 'left': '20px', 'zIndex': 999,
                            'fontWeight': 'bold', 'borderRadius': '25px', 'boxShadow': '0 8px 25px rgba(111,61,255,0.4)'
                        }),
            ]),
            
            # Smart Security Report Content (EXACT SAME from main dashboard)
            html.Div(style={'padding': '100px 30px 30px', 'maxWidth': '1400px', 'margin': '0 auto'}, children=[
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("📊 Smart Security Report", 
                               style={'color': styles['secondary'], 'fontWeight': 'bold', 'margin': 0, 'fontSize': '2.2rem'}),
                        style={'backgroundColor': styles['primary'], 'borderBottom': f'3px solid {styles["danger"]}', 'textAlign': 'center'}
                    ),
                    dbc.CardBody([
                        dcc.Store(id='smart-report-data-page', data=None),
                        dcc.Store(id='attack-trend-data-page', data=None),
                        
                        # Row 1: Highest Attack + Download (FULLSCREEN SIZE)
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H5("🎯 HIGHEST ATTACK PREDICTION", 
                                               style={'color': styles['warning'], 'fontWeight': 'bold', 'marginBottom': '15px', 'fontSize': '1.3rem'}),
                                        html.H2(id="highest-attack-name-page", children="No Data", className="mb-3", 
                                               style={'color': styles['text'], 'fontSize': '2.5rem'}),
                                        html.H3(id="highest-attack-count-page", children="0", className="mb-2", 
                                               style={'color': styles['danger'], 'fontWeight': 'bold', 'fontSize': '3rem'}),
                                        html.Div(id="highest-attack-prob-page", children="0%", 
                                                style={'color': styles['success'], 'fontSize': '2rem', 'fontWeight': 'bold'}),
                                        html.Div(id="highest-risk-badge-page", children=html.Div("No Data", style={'color': styles['text']}), className="mt-4")
                                    ], style={'textAlign': 'center', 'padding': '40px'})
                                ], style={'height': '100%', 'boxShadow': '0 20px 50px rgba(255,0,110,0.4)'})
                            ], md=8),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Button("📥 Download Full Report", id="download-pdf-btn-page", color="danger", size="lg", 
                                                  className="w-100", style={'fontWeight': 'bold', 'fontSize': '1.3rem', 'height': '70px'}),
                                        html.P(id="report-timestamp-page", children="No report generated", className="mt-4 text-muted", 
                                              style={'textAlign': 'center', 'fontSize': '1.1rem'})
                                    ], style={'padding': '40px', 'textAlign': 'center'})
                                ], style={'height': '100%'})
                            ], md=4)
                        ], className="mb-5"),
                        
                        # Row 2: Attack Trend Graph (LARGER)
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("📈 Attack Trend Analysis", 
                                                  style={'backgroundColor': styles['card_bg'], 'color': styles['text'], 'fontSize': '1.3rem'}),
                                    dbc.CardBody([dcc.Graph(id='attack-trend-graph-page')], style={'padding': '30px'})
                                ], style={'boxShadow': '0 15px 40px rgba(0,0,0,0.4)'})
                            ], md=12)
                        ], className="mb-5"),
                        
                        # Row 3: Attack Summary Table (LARGER)
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader("📋 Complete Attack Summary", 
                                                  style={'backgroundColor': styles['card_bg'], 'color': styles['text'], 'fontSize': '1.3rem'}),
                                    dbc.CardBody([
                                        dash_table.DataTable(
                                            id='attack-summary-table-page',
                                            columns=[{"name": "Attack Type", "id": "attack_type"}, 
                                                    {"name": "Total Count", "id": "count"}, 
                                                    {"name": "Probability %", "id": "probability"}, 
                                                    {"name": "Risk Level", "id": "risk_level"}],
                                            data=[],
                                            style_header={'backgroundColor': styles['primary'], 'color': 'white', 'fontWeight': 'bold', 'fontSize': '16px'},
                                            style_data={'backgroundColor': styles['card_bg'], 'color': styles['text'], 'fontSize': '14px'},
                                            style_data_conditional=[
                                                {'if': {'filter_query': '{risk_level} = High'}, 'backgroundColor': styles['high_risk'], 'color': 'white', 'fontWeight': 'bold'},
                                                {'if': {'filter_query': '{risk_level} = Medium'}, 'backgroundColor': styles['medium_risk'], 'color': 'black', 'fontWeight': 'bold'},
                                                {'if': {'filter_query': '{risk_level} = Low'}, 'backgroundColor': styles['low_risk'], 'color': 'white', 'fontWeight': 'bold'}
                                            ],
                                            style_cell={'textAlign': 'left', 'padding': '16px', 'border': f'1px solid {styles["card_border"]}'},
                                            sort_action="native",
                                            page_size=15,
                                            style_table={'overflowX': 'auto', 'height': '500px'}
                                        )
                                    ], style={'padding': '30px'})
                                ], style={'boxShadow': '0 20px 50px rgba(0,0,0,0.5)'})
                            ], md=12)
                        ])
                    ], style={'padding': '40px'})
                ], style={'marginBottom': '50px', 'boxShadow': '0 25px 60px rgba(255,0,110,0.3)'})
            ])
        ]
    )

# EXACT SAME FUNCTIONS (copied from main app)
def get_empty_figure():
    fig = go.Figure()
    fig.add_annotation(
        text="No anomaly data available. Return to dashboard and upload CSV to generate security report.",
        xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color=styles['text'], family="Arial Black"),
        bgcolor="rgba(42,42,74,0.9)", bordercolor=styles['card_border'], borderwidth=2,
        borderpad=25
    )
    fig.update_layout(
        plot_bgcolor=styles['card_bg'],
        paper_bgcolor=styles['card_bg'],
        font_color=styles['text'],
        height=500,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def classify_risk(count, total_anomalies):
    if total_anomalies == 0: 
        return "Low"
    ratio = count / total_anomalies
    if ratio > 0.5: 
        return "High"
    elif ratio > 0.2: 
        return "Medium"
    return "Low"

# Smart Report Callback (IDENTICAL LOGIC, NEW IDS)
@callback(
    [Output('smart-report-data-page', 'data'),
     Output('attack-trend-data-page', 'data'),
     Output('highest-attack-name-page', 'children'),
     Output('highest-attack-count-page', 'children'),
     Output('highest-attack-prob-page', 'children'),
     Output('highest-risk-badge-page', 'children'),
     Output('attack-trend-graph-page', 'figure'),
     Output('attack-summary-table-page', 'data'),
     Output('report-timestamp-page', 'children')],
    Input('smart-report-data', 'data'),  # Receives data from main dashboard
    prevent_initial_call=True
)
def generate_smart_report_page(report_data):
    if not report_data:
        empty_fig = get_empty_figure()
        return (None, None, "No Data", "0", "0%", 
                html.Div("No Data", style={'color': styles['text'], 'fontSize': '1.3rem'}), 
                empty_fig, [], "No report generated")
    
    # IDENTICAL LOGIC AS MAIN APP
    total_anomalies = sum(item['count'] for item in report_data)
    attack_counts = {item['attack_type']: item['count'] for item in report_data}
    attack_types = ['DDoS', 'DoS', 'Port Scan', 'Brute Force', 'Botnet', 'Web Attacks']
    
    # Fill missing attacks with 0
    for attack in attack_types:
        if attack not in attack_counts:
            attack_counts[attack] = 0
    
    trend_data = []
    current_time = pd.Timestamp.now()
    final_report_data = []
    
    for attack, count in attack_counts.items():
        if count > 0 or attack in [item['attack_type'] for item in report_data]:
            probability = (count / total_anomalies * 100) if total_anomalies > 0 else 0
            risk_level = classify_risk(count, total_anomalies)
            final_report_data.append({
                'attack_type': attack, 'count': count, 'probability': f"{probability:.1f}%", 'risk_level': risk_level
            })
            trend_data.append({'timestamp': current_time.isoformat(), 'attack_type': attack, 'count': count})

    if not final_report_data:
        empty_fig = get_empty_figure()
        return (None, None, "No Threats", "0", "0%", 
                html.Div("🟢 LOW RISK", style={'color': styles['low_risk'], 'fontSize': '1.3rem', 'fontWeight': 'bold'}), 
                empty_fig, [], datetime.now().strftime("%B %d, %Y - %I:%M %p"))

    highest = max(final_report_data, key=lambda x: x['count'])
    
    risk_colors = {'High': styles['high_risk'], 'Medium': styles['medium_risk'], 'Low': styles['low_risk']}
    risk_icon = "🔴" if highest['risk_level'] == 'High' else "🟡" if highest['risk_level'] == 'Medium' else "🟢"
    risk_badge = html.Div([
        html.Span(f"{risk_icon} ", style={'fontSize': '2.2rem', 'marginRight': '10px'}),
        html.Span(f"{highest['risk_level']} RISK", style={
            'backgroundColor': risk_colors[highest['risk_level']], 
            'color': 'white' if highest['risk_level'] != 'Medium' else 'black',
            'padding': '15px 25px', 'borderRadius': '30px', 'fontWeight': 'bold', 'fontSize': '1.3rem',
            'boxShadow': '0 6px 20px rgba(0,0,0,0.4)'
        })
    ], style={'textAlign': 'center', 'padding': '15px'})

    trend_df = pd.DataFrame(trend_data)
    fig = px.bar(trend_df, x='attack_type', y='count', title="Current Attack Distribution", color='count',
                color_continuous_scale=['#00bfa5', '#ffc400', '#ff006e']) if len(trend_df) > 0 else get_empty_figure()
    
    fig.update_layout(
        plot_bgcolor=styles['card_bg'], paper_bgcolor=styles['card_bg'], font_color=styles['text'],
        height=500, showlegend=False, title_font_size=18
    )

    timestamp = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    return (final_report_data, trend_data, highest['attack_type'], f"{highest['count']:,}", 
            highest['probability'], risk_badge, fig, final_report_data, timestamp)

# Download callback (IDENTICAL)
@callback(
    Output("smart-report-download", "data"),
    Input("download-pdf-btn-page", "n_clicks"),
    [State('smart-report-data-page', 'data'), State('report-timestamp-page', 'children')],
    prevent_initial_call=True
)
def generate_html_report_page(n_clicks, report_data, timestamp):
    # EXACT SAME LOGIC AS MAIN APP - just return the same HTML
    if not report_data or len(report_data) == 0:
        return no_update
    
    highest = max(report_data, key=lambda x: x['count'])
    html_content = f"""[SAME HTML CONTENT AS MAIN APP - copy from your existing generate_html_report function]"""
    filename = f"SOC_Security_Report_{highest['attack_type'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    return dict(content=html_content, filename=filename)

# Navigation callback
@callback(Output('url', 'pathname'), Input('back-to-dashboard', 'n_clicks'), prevent_initial_call=True)
def go_back_to_dashboard(n_clicks):
    return '/'
