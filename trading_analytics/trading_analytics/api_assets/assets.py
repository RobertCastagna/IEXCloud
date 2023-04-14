
import requests as re
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dagster import Definitions, asset, get_dagster_logger, OpExecutionContext, MetadataValue

load_dotenv()

# ------------- TEMP INPUT PARMAS ------------- #
ticker='aapl'
# --------------------------------------------- #


@asset(io_manager_key="snowflake_io_manager") 
def aapl_quote_data(context: OpExecutionContext):
    base_url = 'https://sandbox.iexapis.com/v1'
    api_token = '?token=' + str(os.environ['API_KEY'])
    quote = re.get(base_url + f'/stock/{ticker}/quote' + api_token)
    now = datetime.now()

    df = pd.DataFrame(quote.json(), index = [now])

    logger = get_dagster_logger()
    logger.info(df.columns)
    
    context.add_output_metadata(
        {
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )
    return df

