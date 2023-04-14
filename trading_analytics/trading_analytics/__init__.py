from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
    fs_io_manager
)
from dagster_snowflake_pandas import snowflake_pandas_io_manager
from dagster_snowflake import snowflake_resource
from . import api_assets

iex_api_job = define_asset_job("iex_cloud_api", selection=AssetSelection.all())

# Addition: a ScheduleDefinition the job it should run and a cron schedule of how frequently to run it
hourly_api_schedule = ScheduleDefinition(
    job = define_asset_job(name = 'iex_cloud_api'), cron_schedule="0 * * * *"  # every hour
)

defs = Definitions(
    assets= load_assets_from_package_module(api_assets, group_name='api_data'),
    schedules=[hourly_api_schedule],
    resources={
        "snowflake_io_manager": snowflake_pandas_io_manager.configured(
            {
                "account": {"env": "DATABASE_ACCOUNT"},  
                "user": {"env": "DATABSE_USERNAME"},  
                "password":{"env": "DATABASE_PASSWORD"}, 
                "database": {"env": "DATABASE_NAME"},
                "schema": {"env": "DATABASE_SCHEMA"}
            }
        ),
        "fs_io_manager": fs_io_manager,
        "snowflake_query": snowflake_resource.configured(
            {
                "account": {"env": "DATABASE_ACCOUNT"},  
                "user": {"env": "DATABSE_USERNAME"},  
                "password":{"env": "DATABASE_PASSWORD"}, 
                "database": {"env": "DATABASE_NAME"},
                "schema": {"env": "DATABASE_SCHEMA"}
            }
        )
    }
)