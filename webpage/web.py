import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("InfoGuru: Business Intelligence Solutions", style={'text-align': 'center'}),
        html.P("Tailored RAG and Local LLM Model for Business-Specific Responses", style={'text-align': 'center'}),
    ], style={'padding': '50px', 'background-color': '#1E1E1E', 'color': 'white'}),

    # About Section
    html.Div([
        html.H2("About InfoGuru", style={'text-align': 'center'}),
        html.P(
            "InfoGuru is a cutting-edge solution combining Retrieval-Augmented Generation (RAG) and a local LLM model "
            "to generate accurate, business-specific responses while ensuring data privacy.",
            style={'text-align': 'center', 'max-width': '800px', 'margin': 'auto'}
        ),
    ], style={'padding': '50px'}),

    # Example Plotly Visualization
    html.Div([
        html.H2("Business Insights", style={'text-align': 'center'}),
        dcc.Graph(
            id='example-graph',
            figure=go.Figure(
                data=[go.Bar(x=['Service A', 'Service B', 'Service C'], y=[10, 20, 30])],
                layout=go.Layout(title='Service Performance', barmode='group')
            )
        )
    ], style={'padding': '50px'}),

    # Contact Section
    html.Div([
        html.H2("Contact Us", style={'text-align': 'center'}),
        html.P("Email: contact@infoguru.com", style={'text-align': 'center'}),
        html.P("Phone: +1 (123) 456-7890", style={'text-align': 'center'}),
    ], style={'padding': '50px', 'background-color': '#1E1E1E', 'color': 'white'}),

    # Footer
    html.Div([
        html.P("© 2024 InfoGuru. All rights reserved.", style={'text-align': 'center'})
    ], style={'padding': '20px', 'background-color': '#000', 'color': 'white'})
])

if __name__ == '__main__':
    app.run_server(debug=True)
