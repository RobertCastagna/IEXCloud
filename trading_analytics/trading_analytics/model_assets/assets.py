import requests as re
import os
import json
import csv
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime
from dagster import Definitions, asset, get_dagster_logger, OpExecutionContext, MetadataValue, SourceAsset, Output, file_relative_path
from sklearn.linear_model import LinearRegression
import sklearn

load_dotenv()


@asset(required_resource_keys={"snowflake_query"}, group_name = 'modelling', compute_kind='Model', description='Computes linear regression to predict close price')
def lin_regression_model(context: OpExecutionContext, equity_history_data):
    df = context.resources.snowflake_query.execute_query(
        (
        f"select * from equity_history_data order by AVGTOTALVOLUME desc"
        ),
        fetch_results=True,
        use_pandas_result=True
    )

    sklearn.linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True)
    x,y = df['PERATIO'], df['AVGTOTALVOLUME']

    # Create an instance of a linear regression model and fit it to the data with the fit() function:
    model = LinearRegression().fit(x, y) 

    # Obtain the coefficient of determination by calling the model with the score() function, then print the coefficient:
    r_sq = model.score(x, y)
    logger = get_dagster_logger()
    logger.info('coefficient of determination: ' + r_sq + ', intercept: ' + model.intercept_ + ', slope: ' + model.coef_)


    return df

@asset(required_resource_keys={"snowflake_query"}, group_name = 'modelling', compute_kind='Plot', description='display a plot of trading volume over time')
def plot_volume_by_ticker(context: OpExecutionContext, lin_regression_model):

    df = context.resources.snowflake_query.execute_query(
        (
        f"select * from lin_regression_model order by AVGTOTALVOLUME desc"
        ),
        fetch_results=True,
        use_pandas_result=True
    )
    
    fig = px.histogram(df[:10], x="SYMBOL", y='AVGTOTALVOLUME')
    fig.update_layout(bargap=0.2)
    save_chart_path = file_relative_path(__file__, "volume_by_ticker.html")
    fig.write_html(save_chart_path, auto_open=True)

    context.add_output_metadata({"plot_url": MetadataValue.url("file://" + save_chart_path)})