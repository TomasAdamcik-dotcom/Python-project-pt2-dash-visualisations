# dependencies
from typing import Literal
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from pandas.io.pytables import Selection
import plotly.express as px
import csv
from ast import literal_eval

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
                                    
                                    id='products-first-dropdown', 
                                    options=[
                                        {'label': 'Overall', 'value': 'overall'},
                                        {'label': 'By region', 'value': 'region'},
                                        {'label': 'By county', 'value': 'county'},
                                        {'label': 'By product category', 'value': 'category'}
                                    ],
                                    placeholder='Select view',
                                ),

                    ])),
                    dbc.Col(html.Div([
                            html.P('Select product purchases detail:'),        
                            dcc.Dropdown(
                                id='products-second-dropdown', 
                                options=[
                                    {'label': 'none', 'value': 'none'}
                                ],
                                placeholder='First, select view',
                                disabled=True
                            ),
                            
                    ])),
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
            dbc.Row(dbc.Col(html.Div(html.H2('Branches performance outlook')))),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id='branches-performance-dropdown',
                        # options=[
                        #     {'label': 'Overall', 'value': 'overall'},
                        #     {'label': 'Per region', 'value': 'per_region'},
                        #     {'label': 'Per county', 'value': 'per_county'}
                        # ],
                        options=[
                            {'label': 'Overall', 'value': 'branch'},
                            {'label': 'Per region', 'value': 'region'},
                            {'label': 'Per county', 'value': 'county'}
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
    Output(component_id='chart-products-top5', component_property='figure'),
    Output(component_id='chart-products-bottom5', component_property='figure'),
    Input(component_id='products-first-dropdown', component_property='value')
)

def update_products_drilldown(first_selection):
    if first_selection == 'overall':
        # get visual
        visuals_pt1_df_overall = visuals_pt1_df.groupby('product').sum().reset_index().sort_values(by='qty',ascending=False)
        topfigure_df = visuals_pt1_df_overall.head(5)
        topfigure_chart = px.bar(topfigure_df, x='product', y='qty', title='Top 5 products overall', labels={'product': '', 'qty': 'Quantity of purchased products'})
        bottomfigure_df = visuals_pt1_df_overall.tail(5)
        bottomfigure_chart = px.bar(bottomfigure_df, x='product', y='qty', title='Bottom 5 products overall', labels={'product': '', 'qty': 'Quantity of purchased products'})
        return topfigure_chart, bottomfigure_chart
    else:
        return {}, {}
    # 1st visual dropdown #############################
@app.callback(
    Output(component_id='products-second-dropdown', component_property='disabled'),
    Output(component_id='products-second-dropdown', component_property='options'),
    Output(component_id='products-second-dropdown', component_property='placeholder'),
    Input(component_id='products-first-dropdown', component_property='value'),
)

def update_second_drilldown(first_drilldown_selection):
    if first_drilldown_selection == 'region':
        with open('data/regions.txt') as f:
            options = literal_eval(f.read())        
        return False, options, f'Please select {first_drilldown_selection}'
    elif first_drilldown_selection == 'county':
        with open('data/counties.txt') as f:
            options = literal_eval(f.read())
        return False, options, f'Please select {first_drilldown_selection}'
    elif first_drilldown_selection == 'category':
        with open('data/product_categories.txt') as f:
            options = literal_eval(f.read())
        return False, options, f'Please select product {first_drilldown_selection}'
    else:
        return True, [], 'First, select view'



# 2nd visual ##########################################

@app.callback(
    Output(component_id='top10-sales-branch', component_property='figure'),
    Output(component_id='bottom10-sales-branch', component_property='figure'),
    Output(component_id='top10-qty-branch', component_property='figure'),
    Output(component_id='bottom10-qty-branch', component_property='figure'),
    Input(component_id='branches-performance-dropdown' ,component_property='value')
)

def update_branches_performance(dropdown_selection):
    if dropdown_selection is not None:
        sales_df = visuals_pt2_df.groupby(dropdown_selection).sum().reset_index().sort_values(by='amount_in_gbp', ascending=False)
        top10_sales_df = sales_df.head(10)
        top10_sales_chart = px.bar(top10_sales_df, x=dropdown_selection, y='amount_in_gbp', title='Top 10 regions by sales')
        bottom10_sales_df = sales_df.tail(10)
        bottom10_sales_chart = px.bar(bottom10_sales_df, x=dropdown_selection, y='amount_in_gbp', title='Bottom 10 regions by sales')
        
        qty_df = visuals_pt2_df.groupby(dropdown_selection).sum().reset_index().sort_values(by='qty', ascending=False)
        top10_qty_df = qty_df.head(10)
        top10_qty_chart = px.bar(top10_qty_df, x=dropdown_selection, y='qty', title='Top 10 regions by sold products')
        bottom10_qty_df = qty_df.tail(10)
        bottom10_qty_chart = px.bar(bottom10_qty_df, x=dropdown_selection, y='qty', title='Bottom 10 regions by sold products')
        
        return top10_sales_chart, bottom10_sales_chart, top10_qty_chart, bottom10_qty_chart
    else:
        return {}, {}, {}, {}

# run
app.run_server(debug=True)





