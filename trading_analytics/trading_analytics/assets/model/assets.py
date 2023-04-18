import requests as re
import os
import json
import csv
import pandas as pd
import numpy as np
import boto3
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from datetime import datetime
from dagster import Definitions, asset, get_dagster_logger, OpExecutionContext, MetadataValue, SourceAsset, Output, file_relative_path
from sklearn.linear_model import LinearRegression
import sklearn
load_dotenv()


@asset(required_resource_keys={"snowflake_query"}, compute_kind='Model', description='Computes linear regression to predict close price')
def lin_regression_model(context: OpExecutionContext, equity_history_data):
    df = context.resources.snowflake_query.execute_query(
        (
        f"select PERATIO, AVGTOTALVOLUME from equity_history_data order by AVGTOTALVOLUME desc"
        ),
        fetch_results=True,
        use_pandas_result=True
    )

    sklearn.linear_model.LinearRegression(fit_intercept=True)
    df1 = df.dropna()
    x = df1.PERATIO.values
    X = x.reshape(-1, 1)

    # Create an instance of a linear regression model and fit it to the data with the fit() function:
    model = LinearRegression().fit(X, df1.AVGTOTALVOLUME) 

    # Obtain the coefficient of determination by calling the model with the score() function, then print the coefficient:
    r_sq = model.score(X, df1.AVGTOTALVOLUME)
    
    #generate random PE RATIOS to feed to prediction model
    x_range = np.linspace(0, len(X), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    logger = get_dagster_logger()
    logger.info('coefficient of determination: ' + str(r_sq) + ', intercept: ' + str(model.intercept_) + ', slope: ' + str(model.coef_))

    return [df1, x_range, y_range]


@asset(compute_kind='Plot', description='display a plot of trading volume over time')
def plot_volume_by_ticker(context: OpExecutionContext, lin_regression_model):

    df1, x_range, y_range = lin_regression_model

    #generate line of best fit and prediction model
    fig = px.scatter(df1, x = 'PERATIO', y = 'AVGTOTALVOLUME', opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name = 'Regression Fit'))
    save_chart_path = file_relative_path(__file__, "volume_by_ticker.html")
    fig.write_html(save_chart_path, auto_open=True)

    context.add_output_metadata({"plot_url": MetadataValue.url("file://" + save_chart_path)})


@asset(compute_kind='s3', description='s3 read/write')
def s3_connection(lin_regression_model):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('ci-data-lake-dev')

    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()
        print(key, '<----------------------------------------')


