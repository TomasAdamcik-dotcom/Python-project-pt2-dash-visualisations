# dependencies
from typing import Literal
import dash
from dash.html.Center import Center
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from pandas.io.pytables import Selection
import plotly.express as px
import csv
from ast import literal_eval

# initialisations
app = dash.Dash("", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
visuals_pt1_df = pd.read_csv("data/2_visuals_pt1.csv", encoding="ISO-8859-1")
visuals_pt2_df = pd.read_csv("data/2_visuals_pt2.csv", encoding="ISO-8859-1")
visuals_pt3_df = pd.read_csv("data/2_visuals_pt3.csv", encoding="ISO-8859-1")
visuals_pt4_df = pd.read_csv("data/2_visuals_pt4.csv", encoding="ISO-8859-1")

# 3rd visual dataframes
top10_hourly_sale_df = visuals_pt3_df.sort_values(
    by="amount_in_gbp", ascending=False
).head(10)
top10_hourly_sale_chart = px.bar(
    top10_hourly_sale_df,
    x="branch",
    y="amount_in_gbp",
    title="Top 10 performing branches by sales per hour",
    labels={"branch": "", "amount_in_gbp": "Sales in GBP"},
).update_layout(title_x=0.5, title_y=0.85)

# 4th visual dataframes
graphs_labels = {"branch": "", "profit": "Profit in GBP"}
profitability_df = visuals_pt4_df.sort_values(by="profit", ascending=False)
top10_profitability_df = profitability_df.head(10)
top10_profitability_chart = px.bar(
    top10_profitability_df,
    x="branch",
    y="profit",
    title="Best 10 profitable branches",
    labels=graphs_labels,
).update_layout(title_x=0.5, title_y=0.85)

bottom10_profitability_df = profitability_df.tail(10)
bottom10_profitability_chart = px.bar(
    bottom10_profitability_df,
    x="branch",
    y="profit",
    title="Least 10 profitable branches",
    labels=graphs_labels,
).update_layout(title_x=0.5, title_y=0.85)

# layouts
app.layout = html.Div(
    [
        html.Header(
            [
                html.H1("Customer behaviour dashboard"),
            ]
        ),
        dbc.Container(
            [
                # 1st visual ############################################
                html.Div(
                    [
                        dbc.Row(dbc.Col(html.Div(html.H2("Products performance")))),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id="products-first-dropdown",
                                                options=[
                                                    {
                                                        "label": "Overall",
                                                        "value": "overall",
                                                    },
                                                    {
                                                        "label": "By region",
                                                        "value": "region",
                                                    },
                                                    {
                                                        "label": "By county",
                                                        "value": "county",
                                                    },
                                                    {
                                                        "label": "By product category",
                                                        "value": "category",
                                                    },
                                                ],
                                                placeholder="Select view",
                                                className='dropdown',
                                            ),
                                        ]
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id="products-second-dropdown",
                                                options=[],
                                                placeholder="First, select view",
                                                disabled=True,
                                                className='dropdown',
                                            ),
                                        ]
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [dcc.Graph(id="chart-products-top5", figure={})]
                                    )
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dcc.Graph(
                                                id="chart-products-bottom5", figure={}
                                            )
                                        ]
                                    )
                                ),
                            ]
                        ),
                    ], className='section-div',
                ),
                # 2nd visual ############################################
                html.Div(
                    [
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H2(
                                        "Branches performance outlook"
                                    )
                                )
                            )
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="branches-first-dropdown",
                                        options=[
                                            {"label": "Overall", "value": "branch"},
                                            {"label": "Per region", "value": "region"},
                                            {"label": "Per county", "value": "county"},
                                        ],
                                        placeholder="Select view",
                                        className='dropdown',
                                    )
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="branches-second-dropdown",
                                        options=[],
                                        placeholder="First, select view",
                                        className='dropdown',
                                        disabled=True,
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id="top10-sales-branch", figure={})),
                                dbc.Col(
                                    dcc.Graph(id="bottom10-sales-branch", figure={})
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dcc.Graph(id="top10-qty-branch", figure={})),
                                dbc.Col(dcc.Graph(id="bottom10-qty-branch", figure={})),
                            ]
                        ),
                    ], className='section-div',
                ),
                # 3rd visual ############################################
                html.Div(
                    [
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H2("Top performing branches by sales per hour")
                                )
                            )
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    id="top10-branches-hourly-sale",
                                    figure=top10_hourly_sale_chart,
                                )
                            )
                        ),
                    ], className='section-div',
                ),
                # 4th visual ############################################
                html.Div(
                    [
                        dbc.Row(dbc.Col(html.H2("Profitability of branches"))),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id="top10-branches-profitability",
                                        figure=top10_profitability_chart,
                                    )
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id="bottom10-branches-profitability",
                                        figure=bottom10_profitability_chart,
                                    )
                                ),
                            ]
                        ),
                    ], className='section-div-2',
                ),
            ]
        ),
        html.Footer(
            [
                html.Div(html.P("Tomas Adamcik @ 2021"), className='alignment'),
            ]
        ),        
    ],
)


# callbacks

# 1st visual ##########################################
@app.callback(
    Output(component_id="chart-products-top5", component_property="figure"),
    Output(component_id="chart-products-bottom5", component_property="figure"),
    Input(component_id="products-first-dropdown", component_property="value"),
    Input(component_id="products-second-dropdown", component_property="value"),
)
def update_products_drilldown(first_selection, second_selection):
    if first_selection == "overall":
        # get visual
        visuals_pt1_df_overall = (
            visuals_pt1_df.groupby("product")
            .sum()
            .reset_index()
            .sort_values(by="qty", ascending=False)
        )
        topfigure_df = visuals_pt1_df_overall.head(5)
        topfigure_chart = px.bar(
            topfigure_df,
            x="product",
            y="qty",
            title="Top 5 products overall",
            labels={"product": "", "qty": "Quantity of purchased products"}, 
        ).update_layout(title_x=0.5, title_y=0.85)

        bottomfigure_df = visuals_pt1_df_overall.tail(5)
        bottomfigure_chart = px.bar(
            bottomfigure_df,
            x="product",
            y="qty",
            title="Bottom 5 products overall",
            labels={"product": "", "qty": "Quantity of purchased products"},
        ).update_layout(title_x=0.5, title_y=0.85)
        return topfigure_chart, bottomfigure_chart
    elif first_selection != "overall" and second_selection is not None:
        visuals_pt1_df_region = (
            visuals_pt1_df[visuals_pt1_df[first_selection] == second_selection]
            .groupby("product")
            .sum()
            .reset_index()
            .sort_values(by="qty", ascending=False)
        )
        topfigure_df = visuals_pt1_df_region.head(5)
        topfigure_chart = px.bar(
            topfigure_df,
            x="product",
            y="qty",
            title=f"Top 5 products: {second_selection}",
            labels={"product": "", "qty": "Quantity of purchased products"},
        ).update_layout(title_x=0.5, title_y=0.85)

        bottomfigure_df = visuals_pt1_df_region.tail(5)
        bottomfigure_chart = px.bar(
            bottomfigure_df,
            x="product",
            y="qty",
            title=f"Bottom 5 products: {second_selection}",
            labels={"product": "", "qty": "Quantity of purchased products"},
        ).update_layout(title_x=0.5, title_y=0.85)
        return topfigure_chart, bottomfigure_chart
    else:
        return {}, {}

    # 1st visual dropdown #############################

#       1st visual dropdown list logic ################
@app.callback(
    Output(component_id="products-second-dropdown", component_property="disabled"),
    Output(component_id="products-second-dropdown", component_property="options"),
    Output(component_id="products-second-dropdown", component_property="placeholder"),
    Input(component_id="products-first-dropdown", component_property="value"),
)
def update_second_drilldown(first_drilldown_selection):
    if first_drilldown_selection == "region":
        with open("data/regions.txt") as f:
            options = literal_eval(f.read())
        return False, options, f"Please select {first_drilldown_selection}"
    elif first_drilldown_selection == "county":
        with open("data/counties.txt") as f:
            options = literal_eval(f.read())
        return False, options, f"Please select {first_drilldown_selection}"
    elif first_drilldown_selection == "category":
        with open("data/product_categories.txt") as f:
            options = literal_eval(f.read())
        return False, options, f"Please select product {first_drilldown_selection}"
    else:
        return True, [], "First, select view"


# 2nd visual ##########################################


@app.callback(
    Output(component_id="top10-sales-branch", component_property="figure"),
    Output(component_id="bottom10-sales-branch", component_property="figure"),
    Output(component_id="top10-qty-branch", component_property="figure"),
    Output(component_id="bottom10-qty-branch", component_property="figure"),
    Input(component_id="branches-first-dropdown", component_property="value"),
    Input(component_id="branches-second-dropdown", component_property="value"),
)
def update_branches_performance(first_dropdown_selection, second_dropdown_selection):
    if first_dropdown_selection == 'branch':
        charts_labels = {
            "branch": "",
            "region": "",
            "county": "",
            "amount_in_gbp": "Sales in GBP",
            "qty": "Quantity sold",
        }
        sales_df = (
            visuals_pt2_df.groupby(first_dropdown_selection)
            .sum()
            .reset_index()
            .sort_values(by="amount_in_gbp", ascending=False)
        )
        top10_sales_df = sales_df.head(10)
        top10_sales_chart = px.bar(
            top10_sales_df,
            x=first_dropdown_selection,
            y="amount_in_gbp",
            title="Top 10 branches by sales",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)

        bottom10_sales_df = sales_df.tail(10)
        bottom10_sales_chart = px.bar(
            bottom10_sales_df,
            x=first_dropdown_selection,
            y="amount_in_gbp",
            title="Bottom 10 branches by sales",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)

        qty_df = (
            visuals_pt2_df.groupby(first_dropdown_selection)
            .sum()
            .reset_index()
            .sort_values(by="qty", ascending=False)
        )
        top10_qty_df = qty_df.head(10)
        top10_qty_chart = px.bar(
            top10_qty_df,
            x=first_dropdown_selection,
            y="qty",
            title="Top 10 branches by sold products",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)

        bottom10_qty_df = qty_df.tail(10)
        bottom10_qty_chart = px.bar(
            bottom10_qty_df,
            x=first_dropdown_selection,
            y="qty",
            title="Bottom 10 branches by sold products",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)

        return (
            top10_sales_chart,
            bottom10_sales_chart,
            top10_qty_chart,
            bottom10_qty_chart,
        )
    elif first_dropdown_selection != 'branch' and second_dropdown_selection is not None:
        charts_labels = {
            "branch": "",
            "region": "",
            "county": "",
            "amount_in_gbp": "Sales in GBP",
            "qty": "Quantity sold",
        }
        sales_df = (
            visuals_pt2_df[visuals_pt2_df[first_dropdown_selection] == second_dropdown_selection]
            .sort_values(by="amount_in_gbp", ascending=False)
        )       
        top10_sales_df = sales_df.head(10)
        top10_sales_chart = px.bar(
            top10_sales_df,
            x='branch',
            y="amount_in_gbp",
            title=f"Top 10 by sales: {second_dropdown_selection}",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)
        
        bottom10_sales_df = sales_df.tail(10)
        bottom10_sales_chart = px.bar(
            bottom10_sales_df,
            x='branch',
            y="amount_in_gbp",
            title=f"Bottom 10 by sales: {second_dropdown_selection}",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)

        qty_df = (
            visuals_pt2_df[visuals_pt2_df[first_dropdown_selection] == second_dropdown_selection]
            .sort_values(by="qty", ascending=False)
        )        

        top10_qty_df = qty_df.head(10)
        top10_qty_chart = px.bar(
            top10_qty_df,
            x='branch',
            y="qty",
            title=f"Top 10 by sold quantity: {second_dropdown_selection}",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)
        
        bottom10_qty_df = qty_df.tail(10)
        bottom10_qty_chart = px.bar(
            bottom10_qty_df,
            x='branch',
            y="qty",
            title=f"Bottom 10 by sold quantity: {second_dropdown_selection}",
            labels=charts_labels,
        ).update_layout(title_x=0.5, title_y=0.85)
        
        
        return top10_sales_chart, bottom10_sales_chart, top10_qty_chart, bottom10_qty_chart
    else:
        return {}, {}, {}, {}

#       2nd visual dropdown list logic ################
@app.callback(
    Output(component_id="branches-second-dropdown", component_property="disabled"),
    Output(component_id="branches-second-dropdown", component_property="options"),
    Output(component_id="branches-second-dropdown", component_property="placeholder"),
    Input(component_id="branches-first-dropdown", component_property="value"),
)
def update_second_drilldown(first_drilldown_selection):
    if first_drilldown_selection == "region":
        with open("data/regions.txt") as f:
            options = literal_eval(f.read())
        return False, options, f"Please select {first_drilldown_selection}"
    elif first_drilldown_selection == "county":
        with open("data/counties.txt") as f:
            options = literal_eval(f.read())
        return False, options, f"Please select {first_drilldown_selection}"
    else:
        return True, [], "First, select view"

# run
if __name__ == '__main__':
    app.run_server(debug=True)