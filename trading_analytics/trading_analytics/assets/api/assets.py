
import requests as re
import os
import json
import csv
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime
from dagster import Definitions, asset, get_dagster_logger, OpExecutionContext, MetadataValue, SourceAsset, Output, file_relative_path

load_dotenv()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@asset(io_manager_key='fs_io_manager', compute_kind='API', description='Gets a list of equities in ishares core s&p us stock market ETF')
def get_equity_info(context: OpExecutionContext):
    url = "https://www.ishares.com/us/products/239724/ishares-core-sp-total-us-stock-market-etf/1467271812596.ajax?fileType=csv&fileName=iShares-Core-SP-Total-US-Stock-Market-ETF_fund&dataType=fund"
    r = re.get(url)

    lines = [line.strip() for line in r.text.split('\n') if line.strip()]
    csv_res = [line for line in csv.reader(lines)]
    etf_holdings = csv_res[8:]

    # take a sample set of data (total ~3300) and pass list to api
    df_etf_holdings = pd.DataFrame.from_records(etf_holdings[1:-1], columns=etf_holdings[0])[:500]
    
    context.add_output_metadata(
        {
            "num_records": len(df_etf_holdings),
            "preview": MetadataValue.md(df_etf_holdings.head().to_markdown())
        }
    )

    return df_etf_holdings


@asset(io_manager_key="snowflake_io_manager", compute_kind='API', description='hits iexcloud api to return financial data on a list of given tickers') 
def batch_api_quote_data(context: OpExecutionContext, get_equity_info):

    #api call for new data
    base_url = 'https://sandbox.iexapis.com/v1'
    api_token = '&token=' + str(os.environ['API_KEY'])

    #preparing list of tickers for batch call into groups of 100
    symbol_groups = list(chunks(get_equity_info['Ticker'], 100))
    symbol = []
    for x in range(0, len(symbol_groups)):
        symbol.append(','.join(symbol_groups[x]))
    case_list = {}

    for y in symbol:
        quote = re.get(base_url + f'/stock/market/batch?symbols={y}&types=quote' + api_token).json()

        for ticker in quote:
            case_list[ticker] = quote[ticker]['quote']

    df = pd.DataFrame(case_list).T

    #metadata for Dagit UI
    context.add_output_metadata(
        {
            "new_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )
    return df


@asset(required_resource_keys={"snowflake_query"},io_manager_key="snowflake_io_manager", compute_kind='Snowflake', description='append new results')
def equity_history_data(context: OpExecutionContext, batch_api_quote_data):

    top_stories_stored_query = context.resources.snowflake_query.execute_query(
        (
            " SELECT * FROM batch_api_quote_data UNION select * from equity_history_data"
        ),
        fetch_results=True,
        use_pandas_result=True
    )

    context.add_output_metadata(
        {
            "num_records": len(top_stories_stored_query),
        }
    )
    return top_stories_stored_query


