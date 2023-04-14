import json
import os

from dagster import load_assets_from_package_module
from . import api, model

API_ASSETS = "api"
MODEL_ASSETS = 'model'

api_assets = load_assets_from_package_module(package_module=api, group_name=API_ASSETS)

core_assets = load_assets_from_package_module(package_module=model, group_name=MODEL_ASSETS)

