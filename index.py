# dependencies
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from pandas.io.pytables import Selection
import plotly.express as px

# initialisations
app = dash.Dash('',external_stylesheets=[dbc.themes.BOOTSTRAP])
visuals_pt1_df = pd.read_csv('data/2_visuals_pt1.csv', encoding='ISO-8859-1')
visuals_pt2_df = pd.read_csv('data/2_visuals_pt2.csv', encoding='ISO-8859-1')
visuals_pt3_df = pd.read_csv('data/2_visuals_pt3.csv', encoding='ISO-8859-1')
visuals_pt4_df = pd.read_csv('data/2_visuals_pt4.csv', encoding='ISO-8859-1')

# counties_df = pd.read_csv('data/counties.csv', encoding='ISO-8859-1')
# product_categories_df = pd.read_csv('data/product_categories.csv', encoding='ISO-8859-1')
# regions_df = pd.read_csv('data/regions.csv', encoding='ISO-8859-1')

# 3rd visual dataframes
top10_hourly_sale_df = visuals_pt3_df.sort_values(by='amount_in_gbp', ascending=False).head(10)
top10_hourly_sale_chart = px.bar(top10_hourly_sale_df, x='branch', y='amount_in_gbp', title='Top 10 performing branches by sales per hour')

# 4th visual dataframes
profitability_df = visuals_pt4_df.sort_values(by='profit', ascending=False)
top10_profitability_df = profitability_df.head(10)
top10_profitability_chart = px.bar(top10_profitability_df, x='branch', y='profit', title='Best 10 profitable branches')
bottom10_profitability_df = profitability_df.tail(10)
bottom10_profitability_chart = px.bar(bottom10_profitability_df, x='branch', y='profit', title='Least 10 profitable branches')

# layouts
app.layout = html.Div([
    dbc.Container([
    html.H1('Customer behaviour dashboard'),
        # 1st visual ############################################
    html.Div(
        [
            dbc.Row(dbc.Col(html.Div(html.H2('Products performance')))),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                                html.P('Select product purchases view:'),
                                dcc.Dropdown(
                                    id='product-purchases-by-selector', 
                                    options=[
                                        {'label': 'Overall', 'value': 'overall'},
                                        {'label': 'By region', 'value': 'by_region'},
                                        {'label': 'By county', 'value': 'by_county'},
                                        {'label': 'By product category', 'value': 'by_product_category'}
                                    ],
                                    placeholder='Select view',
                                    value='dont-show'
                                ),
                                html.P('Select product purchases detail:'),        
                                dcc.Dropdown(
                                    id='second_dropdown', 
                                    options=[
                                        {'label': 'Overall', 'value': 'overall'}
                                    ],
                                    placeholder='Select branch'
                                    )
                    ])),
                    dbc.Col(html.Div()),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div([       
                        dcc.Graph(
                        id='chart-products-top5',
                        figure={}
                        )])),
                    dbc.Col(html.Div([
                        dcc.Graph(
                        id='chart-products-bottom5',
                        figure={}
                        )
                    ])),
                ]

            )
        ]
    ),
        # 2nd visual ############################################
    html.Div([
            dbc.Row(dbc.Col(html.Div(html.H2('Branches performances')))),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='branches-performance-dropdown',
                        options=[
                            {'label': 'Overall', 'value': 'overall'},
                            {'label': 'Per region', 'value': 'per_region'},
                            {'label': 'Per county', 'value': 'per_county'}
                        ],
                        placeholder='Select your view'
                    )
                ),
                dbc.Col()
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='top10-sales-branch',
                        figure={}
                    )
                ),
                dbc.Col(
                    dcc.Graph(
                        id='bottom10-sales-branch',
                        figure={}
                    )                    
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='top10-qty-branch',
                        figure={}
                    )                    
                ),
                dbc.Col(
                    dcc.Graph(
                        id='bottom10-qty-branch',
                        figure={}
                    )                    
                ),
            ]),
            
    ]),
        # 3rd visual ############################################
    html.Div([
        dbc.Row(dbc.Col(html.Div(html.H2('Top performing branches by sales per hour')))),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                id='top10-branches-hourly-sale',
                figure=top10_hourly_sale_chart
                )
        )
        ),
    ]),
        # 4th visual ############################################   
    html.Div([
        dbc.Row(dbc.Col(html.H2('Profitability of branches'))),
        dbc.Row([
            dbc.Col(
                dcc.Graph(
                id='top10-branches-profitability',
                figure=top10_profitability_chart
                )
            ),
            dbc.Col(
                dcc.Graph(
                id='bottom10-branches-profitability',
                figure=bottom10_profitability_chart
                )
            )
            ]),
    ]),
])
])


# callbacks

# 1st visual ##########################################
@app.callback(
    Output(component_id='chart-products-top5',component_property='figure'), # output that goes to chart
    Output(component_id='chart-products-bottom5',component_property='figure'), # output that goes to chart
    Input(component_id='product-purchases-by-selector', component_property='value'), # input from 1st dropdown - taking value - used as first function parameter
    Input(component_id='second_dropdown', component_property='value') ## input from 2ns dropdown - taking value - used as second function parameter
)

def update_chart(first_dropdown_selection, second_dropdown_selection):
    if first_dropdown_selection == 'overall':
        visuals_pt1_df_overall = visuals_pt1_df.groupby('product').sum().reset_index().sort_values(by='qty',ascending=False)
        visuals_pt1_df_overall_top5 = visuals_pt1_df_overall.head(5)
        visuals_pt1_df_overall_bottom5 = visuals_pt1_df_overall.tail(5)
        topfigure = px.bar(visuals_pt1_df_overall_top5, x='product', y='qty', title='Top 5 products overall', labels={'product': '', 'qty': 'Quantity of purchased products'})
        bottomfigure = px.bar(visuals_pt1_df_overall_bottom5, x='product', y='qty', title='Bottom 5 products overall', labels={'product': '', 'qty': 'Quantity of purchased products'})
        return topfigure, bottomfigure
    elif first_dropdown_selection == 'by_region' and second_dropdown_selection is not None:
        # visuals_pt1_df_by_region = visuals_pt1_df.groupby(['region', 'product']).sum().reset_index().sort_values(by='qty',ascending=False)
        visuals_pt1_df_by_region = visuals_pt1_df[visuals_pt1_df['region'] == 'Wales'].groupby('product').sum().sort_values(by='qty', ascending=False)
        visuals_pt1_df_overall_top5 = visuals_pt1_df_by_region.head(5)
        visuals_pt1_df_overall_bottom5 = visuals_pt1_df_by_region.tail(5)
        topfigure = px.bar(visuals_pt1_df_overall_top5, x='product', y='qty')
        bottomfigure = px.bar(visuals_pt1_df_overall_bottom5, x='product', y='qty')

        return topfigure, bottomfigure
    return {}, {}


@app.callback(
    Output(component_id='second_dropdown',component_property='options'),
    Input(component_id='product-purchases-by-selector', component_property='value')
)

def update_second_dropdown(first_dorpdown_value):
    if first_dorpdown_value == 'by_region':
        return [{'label': 'East Midlands', 'value': 'East Midlands'},
                {'label': 'East of England', 'value': 'East of England'}]

    return []

# 2nd visual ##########################################















# East Midlands
# East of England
# London
# North East England
# North West England
# Northern Ireland
# Scotland
# South East England
# South West England
# Wales
# West Midlands
# Yorkshire and the Humber


"""
@app.callback(
    Output(component_id='second-product-drilldown-selector-div', component_property='style'),
    Output(component_id='chart-products-top5', component_property='figure'),
    # Output(component_id='chart-products-bottom5', component_property='figure'),
    Input(component_id='product-purchases-by-selector', component_property='value')
)


def get_summary(visual_1_type, top5):
    if visual_1_type is not None:
        if visual_1_type != 'overall':
            pass
            # show second dropdown
            #  return {'display': 'block'}

            if visual_1_type == 'by_region':
                # pass data to charts
                
                pass
            elif visual_1_type == 'by_county':
                # pass data to charts
                
                pass
            elif visual_1_type == 'by_product_category':
                # pass data to charts
                
                pass
        else:     
            # this is overall case - pass data to visuals - by parameters top5 and bottom5
            df = visuals_pt1_df.groupby('product').sum().sort_values(by='qty')
            top5_df = df.head(5)
            figure = px.bar(top5_df, x='product', y='qty')
            # bottom5_df = df.tail(5)
            return top5, figure
    else:
        pass

"""


"""
html.Div([
        # html.P('Select product purchases view:'),
        # dcc.Dropdown(
        #     id='product-purchases-by-selector', 
        #     options=[
        #         {'label': 'Overall', 'value': 'overall'},
        #         {'label': 'By region', 'value': 'by_region'},
        #         {'label': 'By county', 'value': 'by_county'},
        #         {'label': 'By product category', 'value': 'by_product_category'}
        #     ],
        #     placeholder='Select view',
        #     value='dont-show'
        # )
    ]),
    html.Div([
        # html.P('Select product purchases detail:'),        
        # dcc.Dropdown(
        #     id='second_dropdown', 
        #     options=[
        #         # options should be extract of list
        #         {'label': 'Overall', 'value': 'overall'}
        #     ],
        #     placeholder='Select branch'
        #     )
        ], 
        # id='second-product-drilldown-selector-div', 
        #     style={'display': 'block'}
        ),

    html.Span([ 
        # dcc.Graph(
        # id='chart-products-top5',
        # figure={}
        # ),
        # dcc.Graph(
        # id='chart-products-bottom5',
        # figure={}
        # )
    ]),
    ]),

"""

# run
app.run_server(debug=True)





