import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import zscore
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import base64
import io
import dash_bootstrap_components as dbc
import numpy as np
from dashboard import get_dashboard_layout, _empty_fig, GRAPH_HEIGHT
from login import get_login_layout, get_register_layout, register_login_callbacks
from settings import get_settings_layout
from insights import get_insights_layout

# ──────────────────────────────────────────────
# Initialize Dash App
# ──────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title="Anomaly Detector",
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
)
server = app.server

styles = {
    'background':   '#1a1a2e',
    'text':         '#e0e0e0',
    'primary':      '#0f4c75',
    'secondary':    '#6f3dff',
    'success':      '#00bfa5',
    'danger':       '#ff006e',
    'info':         '#4c00b0',
    'warning':      '#ffc400',
    'card_bg':      '#2a2a4a',
    'card_border':  '#4c4c6c',
    'sidebar_bg':   '#121226',
    'sidebar_text': '#ffffff',
}

# ──────────────────────────────────────────────
# index_string
# ALL global CSS and the sidebar-toggle JS must
# live here. html.Style and html.Script are NOT
# valid Dash components and will raise AttributeError.
# ──────────────────────────────────────────────
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {%favicon%}
        {%css%}
        <style>

            /* ═══════════════════════════════════════════
               ANIMATIONS
            ═══════════════════════════════════════════ */
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            @keyframes pulse  { 0%,100% { transform: scale(1); } 50% { transform: scale(1.05); } }
            .fade-in { animation: fadeIn 0.8s ease-in-out; }
            .pulse   { animation: pulse 2s infinite; }

            /* ═══════════════════════════════════════════
               GLOBAL RESETS
            ═══════════════════════════════════════════ */
            *, *::before, *::after { box-sizing: border-box; }
            body, html {
                margin: 0;
                padding: 0;
                overflow-x: hidden;
                background-color: #1a1a2e !important;
                color: #e0e0e0 !important;
            }

            /* ═══════════════════════════════════════════
               DASHBOARD WRAPPER  — flex column on mobile,
               flex row (side-by-side) on desktop
            ═══════════════════════════════════════════ */
            #dashboard-wrapper {
                display: flex;
                flex-direction: row;       /* desktop: side by side */
                min-height: 100vh;
                background-color: #1a1a2e;
            }

            /* ═══════════════════════════════════════════
               SIDEBAR  — fixed left column on desktop
            ═══════════════════════════════════════════ */
            #sidebar {
                width: 260px;
                min-width: 260px;          /* never shrinks */
                min-height: 100vh;
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                z-index: 200;
                overflow-y: auto;
                background-color: #121226;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }

            /* ═══════════════════════════════════════════
               MAIN CONTENT  — takes remaining width
            ═══════════════════════════════════════════ */
            #main-content {
                margin-left: 260px;        /* same as sidebar width */
                flex: 1;
                min-width: 0;
                padding: 24px;
                background-color: #1a1a2e;
            }

            /* ═══════════════════════════════════════════
               HAMBURGER  — hidden on desktop
            ═══════════════════════════════════════════ */
            #sidebar-toggle { display: none; }

            /* ═══════════════════════════════════════════
               OVERRIDE CYBORG THEME — card colors
            ═══════════════════════════════════════════ */
            .card {
                background-color: #2a2a4a !important;
                border: 1px solid #4c4c6c !important;
                color: #e0e0e0 !important;
                border-radius: 10px;
                transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
            }
            .card:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(0,0,0,0.3); }
            .card-body   { background-color: #2a2a4a !important; color: #e0e0e0 !important; }
            .card-header {
                background-color: #0f4c75 !important;
                color: #e0e0e0 !important;
                border-bottom: 1px solid #4c4c6c !important;
            }
            .card-title { color: #a0a0b0 !important; }
            .card-text  { color: #e0e0e0 !important; }

            /* Dash dropdown dark-theme */
            .Select-control, .Select-menu-outer, .Select-input {
                background-color: #2a2a4a !important;
                color: #e0e0e0 !important;
                border: 1px solid #4c4c6c !important;
            }
            .Select-placeholder { color: #e0e0e0 !important; opacity: 0.6; }
            .Select-value-label { color: #e0e0e0 !important; }

            /* Nav links */
            .nav-link        { color: #ffffff !important; }
            .nav-link:hover  { color: #6f3dff !important; background: transparent !important; }
            .nav-link.active { color: #6f3dff !important; background: transparent !important; }

            /* HR */
            hr { border-color: #4c4c6c !important; opacity: 0.5; }

            /* Bootstrap row gutter reset */
            .row { margin-left: 0 !important; margin-right: 0 !important; }

            /* Tables scroll internally — no full-page horizontal scroll */
            .dash-table-container { overflow-x: auto; }

            /* Fixed graph height helper */
            .fixed-graph { height: 380px; }

            /* ═══════════════════════════════════════════
               TABLET  768 – 991 px
               Sidebar narrows, content adjusts
            ═══════════════════════════════════════════ */
            @media (min-width: 768px) and (max-width: 991px) {
                #sidebar      { width: 200px; min-width: 200px; }
                #main-content { margin-left: 200px; }
                .attack-col   { flex: 0 0 33.33%; max-width: 33.33%; }
            }

            /* ═══════════════════════════════════════════
               MOBILE  ≤ 767 px
               KEY CHANGE: sidebar moves to TOP, full width.
               No hamburger, no overlay, no hidden content.
               Main content flows naturally below the sidebar.
            ═══════════════════════════════════════════ */
            @media (max-width: 767px) {

                /* Wrapper stacks vertically */
                #dashboard-wrapper {
                    flex-direction: column;
                }

                /* Sidebar becomes a full-width top strip */
                #sidebar {
                    position: relative !important; /* leave normal flow */
                    width: 100% !important;
                    min-width: 0 !important;
                    min-height: unset !important;
                    height: auto !important;
                    top: auto; left: auto; bottom: auto;
                    padding: 16px;
                    overflow-y: visible;
                    overflow-x: hidden;
                    border-bottom: 2px solid #6f3dff;
                    /* Horizontal scroll for controls when needed */
                }

                /* Sidebar inner layout: wrap controls in a row */
                #sidebar-inner-controls {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 12px;
                    align-items: flex-start;
                }
                #sidebar-brand    { width: 100%; text-align: center; margin-bottom: 8px; }
                #sidebar-navlinks { width: 100%; display: flex; gap: 16px; }
                #sidebar-feature  { flex: 1 1 160px; min-width: 140px; }
                #sidebar-slider   { flex: 1 1 160px; min-width: 140px; }
                #sidebar-upload   { flex: 1 1 140px; min-width: 120px; }

                /* Main content: no left margin, full width */
                #main-content {
                    margin-left: 0 !important;
                    padding: 12px !important;
                    width: 100%;
                }

                /* KPI cards: one per row on very small, 2-up on wider phones */
                .kpi-col   { flex: 0 0 100%; max-width: 100%; margin-bottom: 10px; }

                /* Attack cards: 2 per row */
                .attack-col { flex: 0 0 50%; max-width: 50%; margin-bottom: 10px; }

                /* Header buttons wrap */
                #header-buttons { flex-wrap: wrap; gap: 6px; }
                #header-buttons .btn { font-size: 0.8rem; padding: 6px 10px; }

                /* Graphs take full width, maintain fixed height */
                .fixed-graph { height: 300px; }

                /* Prevent any child from causing horizontal scroll */
                #main-content * { max-width: 100%; }
            }

            /* ═══════════════════════════════════════════
               EXTRA SMALL  ≤ 480 px
            ═══════════════════════════════════════════ */
            @media (max-width: 480px) {
                .attack-col  { flex: 0 0 50%; max-width: 50%; }
                .kpi-col     { flex: 0 0 100%; max-width: 100%; }
                .card-body   { padding: 10px !important; }
                #main-content { padding: 8px !important; }
            }

        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

# ──────────────────────────────────────────────
# Root layout
# dcc.Store components live here so every page's
# callbacks can always find them.
# ──────────────────────────────────────────────
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

    dcc.Store(id='login-state',            data={'logged_in': False}),
    dcc.Store(id='stored-data'),
    dcc.Store(id='numeric-cols'),
    dcc.Store(id='anomalous-data-store'),
    dcc.Store(id='download-report-trigger'),
])


# ──────────────────────────────────────────────
# Settings
# ──────────────────────────────────────────────
@app.callback(
    Output("settings-store", "data"),
    Input("save-settings", "n_clicks"),
    State("theme-selector", "value"),
    State("refresh-interval", "value"),
    State("threshold-slider", "value"),
    State("alert-options", "value"),
    State("report-options", "value"),
    prevent_initial_call=True,
)
def save_settings(n, theme, refresh, threshold, alerts, reports):
    if n:
        return {
            "theme":            theme,
            "refresh_interval": refresh,
            "threshold":        threshold,
            "alerts":           alerts,
            "reports":          reports,
        }
    return dash.no_update


# ──────────────────────────────────────────────
# Page routing
# ──────────────────────────────────────────────
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    Input('login-state', 'data'),
)
def display_page(pathname, login_state):

    # 👉 Logout route
    if pathname == "/logout":
        return get_login_layout()

    if pathname == "/register":
        return get_register_layout()

    if not login_state or not login_state.get('logged_in'):
        return get_login_layout()

    if pathname == "/insights":
        return get_insights_layout()

    if pathname == "/settings":
        return get_settings_layout()

    return get_dashboard_layout()


# ──────────────────────────────────────────────
# File upload
# ──────────────────────────────────────────────
@app.callback(
    [
        Output('output-data-upload',   'children'),
        Output('feature-dropdown',     'options'),
        Output('stored-data',          'data'),
        Output('numeric-cols',         'data'),
        Output('total-rows-kpi',       'children'),
        Output('numeric-features-kpi', 'children'),
    ],
    Input('upload-data',  'contents'),
    State('upload-data',  'filename'),
)
def handle_file_upload(contents, filename):
    placeholder_msg = html.Span(
        "Please upload a CSV file to get started.",
        style={'textAlign': 'center', 'color': styles['secondary']},
    )

    if contents is None:
        return placeholder_msg, [], None, None, "0", "0"

    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename.lower():
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return (
                html.Span("Please upload a CSV file.", style={'color': styles['danger']}),
                [], None, None, "0", "0",
            )
    except Exception as e:
        return (
            html.Span(f"Error processing file: {e}", style={'color': styles['danger']}),
            [], None, None, "0", "0",
        )

    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    return (
        html.Span(
            f"✅ '{filename}' loaded — {len(df):,} rows, {len(numeric_columns)} numeric features.",
            style={'color': styles['success']},
        ),
        [{'label': col.replace('_', ' ').title(), 'value': col} for col in numeric_columns],
        df.to_dict('records'),
        numeric_columns,
        f"{len(df):,}",
        str(len(numeric_columns)),
    )


# ──────────────────────────────────────────────
# Anomaly detection
# ──────────────────────────────────────────────
@app.callback(
    [
        Output('anomaly-scatter-plot',   'figure'),
        Output('histogram-plots-row',    'children'),
        Output('anomaly-table',          'data'),
        Output('anomaly-table',          'columns'),
        Output('total-anomalies-kpi',    'children'),
        Output('anomalous-data-store',   'data'),
    ],
    [
        Input('stored-data',              'data'),
        Input('numeric-cols',             'data'),
        Input('feature-dropdown',         'value'),
        Input('z-score-threshold-slider', 'value'),
    ],
)
def update_analysis(data, numeric_cols, selected_feature, z_score_threshold):
    placeholder = _empty_fig()

    if data is None or selected_feature is None or numeric_cols is None:
        return placeholder, [], [], [], "0", None

    df = pd.DataFrame(data)

    if selected_feature not in df.columns or df[selected_feature].dtype not in ['int64', 'float64']:
        return placeholder, [], [], [], "0", None

    df['z_score'] = zscore(df[selected_feature].dropna())
    df['anomaly_label'] = df['z_score'].apply(
        lambda x: 'Abnormal' if abs(x) > z_score_threshold else 'Normal'
    )

    scatter_x = selected_feature
    other_features = [col for col in numeric_cols if col != selected_feature]
    scatter_y = other_features[0] if other_features else selected_feature
    if scatter_x == scatter_y:
        df['index'] = df.index
        scatter_y = 'index'

    scatter_fig = px.scatter(
        df,
        x=scatter_x,
        y=scatter_y,
        color='anomaly_label',
        title=(
            f'Anomaly Detection: {scatter_x.replace("_", " ").title()}'
            f' vs {scatter_y.replace("_", " ").title()}'
        ),
        color_discrete_map={'Normal': '#90ee90', 'Abnormal': styles['danger']},
        hover_data=[scatter_x, scatter_y, 'z_score'],
    )
    scatter_fig.update_layout(
        plot_bgcolor=styles['card_bg'],
        paper_bgcolor=styles['card_bg'],
        font={'color': styles['text']},
        height=GRAPH_HEIGHT,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    histogram_plots = []
    for col in numeric_cols:
        hist_fig = px.histogram(
            df,
            x=col,
            color='anomaly_label',
            title=f'Distribution of {col.replace("_", " ").title()}',
            color_discrete_map={'Normal': '#90ee90', 'Abnormal': styles['danger']},
        )
        hist_fig.update_layout(
            plot_bgcolor=styles['card_bg'],
            paper_bgcolor=styles['card_bg'],
            font={'color': styles['text']},
            height=GRAPH_HEIGHT,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        histogram_plots.append(
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5(
                        f'{col.replace("_", " ").title()} Distribution',
                        className="card-title",
                    ),
                    dcc.Graph(
                        figure=hist_fig,
                        config={'displayModeBar': False},
                        style={'height': f'{GRAPH_HEIGHT}px'},
                    ),
                ])),
                xs=12, md=6,
                className="mb-3",
            )
        )

    anomalous_points = df[df['anomaly_label'] == 'Abnormal'].copy()
    anomalous_points['index'] = anomalous_points.index
    anomalous_points['z_score'] = anomalous_points['z_score'].round(2)

    table_cols = [
        {'name': i.replace('_', ' ').title(), 'id': i}
        for i in ['index'] + numeric_cols + ['z_score']
    ]
    anomalous_data_json = anomalous_points.to_json(date_format='iso', orient='split')

    return (
        scatter_fig,
        histogram_plots,
        anomalous_points.to_dict('records'),
        table_cols,
        str(len(anomalous_points)),
        anomalous_data_json,
    )


# ──────────────────────────────────────────────
# Legacy CSV download  (sidebar "Reports" link)
# ──────────────────────────────────────────────
@app.callback(
    Output("download-report-trigger", "data"),
    Input("download-report-link", "n_clicks"),
    State('anomalous-data-store', 'data'),
    prevent_initial_call=True,
)
def generate_report(n_clicks, anomalous_data_json):
    if n_clicks and anomalous_data_json:
        df = pd.read_json(anomalous_data_json, orient='split')
        return dcc.send_data_frame(df.to_csv, "anomaly_report.csv")
    return None


# ──────────────────────────────────────────────
# Login / registration callbacks
# ──────────────────────────────────────────────
register_login_callbacks(app)

# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
