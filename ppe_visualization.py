import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from maps import create_map
from dash import Dash

import dash_bootstrap_components as dbc

FOOTER_IMAGE = "https://user-images.githubusercontent.com/58998109/113497688-5b429580-94d4-11eb-98fe-8ca084ff0eee.png"
BG_IMAGE = "https://user-images.githubusercontent.com/58998109/113497198-ac9c5600-94cf-11eb-85fe-6dc48eb286d9.png"


def _init_app() -> Dash:
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

    return app


def read_markdown(file_path):
    with open(file_path, "r") as f:
        return dcc.Markdown(f.read())


def build_navbar():
    return dbc.NavbarSimple(brand="PPE Supply Visualization",
                            color="primary",
                            dark=True,
                            style={"margin-bottom": "20px",
                                   "margin-left": "-20px",
                                   "margin-right": "-20px"})


def build_export_region_dropdown_block():
    return dcc.Dropdown(
        options=[
            {'label': 'China', 'value': 'China'},
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'US', 'value': 'US'},
            {'label': 'North America', 'value': 'NorthAmerica'},
            {'label': 'Europe', 'value': 'EU15'}
        ],
        value='China',
        id="region"
    )


def build_ppe_dropdown_block():
    return dcc.Dropdown(
        options=[
            {'label': '630790', 'value': '630790'},
            {'label': '392690', 'value': '392690'},
            {'label': '621010', 'value': '621010'},
            {'label': '392620', 'value': '392620'},
            {'label': '900490', 'value': '900490'},
            {'label': '401511', 'value': '401511'}
        ],
        value=['630790'],
        multi=True,
        id="ppe"
    )


def build_year_slider():
    return dcc.Slider(
        min=2017,
        max=2019,
        marks={i + 2017: str(i + 2017) for i in range(3)},
        value=2017,
        id="year",
        vertical=False,
        verticalHeight=100
    )


def build_footer():
    return dbc.Container(children=[html.Footer(className="border-top", children=[
        dbc.Row(children=[
            dbc.Col(children=read_markdown("markdowns/group.md"), sm=12, lg=6),
            dbc.Col(children=read_markdown("markdowns/credit.md"), sm=12, lg=6)
        ], style={"margin-top": "10px",
                  "background": "white",
                  "background-image": F"url({FOOTER_IMAGE})"})
    ])])


def build_layout(app: Dash) -> Dash:
    app.layout = html.Div(children=[
        # Navbar
        dbc.Container(children=[build_navbar()]),

        # Contents
        dbc.Container(children=[
            dbc.Container(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        # Introduction
                        read_markdown("markdowns/intro.md"),
                    ], sm=12, md=12, lg=6),

                    dbc.Col(children=[
                        # Control components
                        read_markdown("markdowns/control_components.md"),
                        html.Label('Export Region', style={"margin-top": "20px"}),
                        build_export_region_dropdown_block(),
                        html.Label('PPE', style={"margin-top": "20px"}),
                        build_ppe_dropdown_block(),
                        html.Label('Year', style={"margin-top": "20px"}),
                        build_year_slider()],
                        sm=12, md=12, lg=6
                    )],
                    style={"font-size": "20px"}
                )
            ]),

            # Visualization
            dbc.Container(children=[
                html.H2("Map", style={"margin-top": "20px"}),
                dcc.Graph(id="ppe_map"),
            ]),
        ], style={"background": "white",
                  "padding-top": "30px"}
        ),
        # Footer
        build_footer()
    ], style={
        "background-image": F"url({BG_IMAGE})"}
    )

    @app.callback(
        Output(component_id='ppe_map', component_property='figure'),
        [Input(component_id='region', component_property='value'),
         Input(component_id='ppe', component_property='value'),
         Input(component_id='year', component_property='value')]
    )
    def update_map(region, ppe, year):
        return create_map(region, ppe, str(year))

    return app


if __name__ == '__main__':
    _app = _init_app()
    _app = build_layout(_app)
    _app.run_server(debug=True)
