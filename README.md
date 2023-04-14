# IEXCloud - S&P500 Trading Analytics Project

## OVERVIEW
This repository contains pieces of my project to utilize IEX Cloud API to build two market analysis tools:

### Equal Weight S&P500 Portfolio
- The goal was to display an equal weight s&p500 portfolio.

### Momentum Trading S&P500 Portfolio
- The goal was to analyse the One-Year, Six-Month, Three-Month and One-Month percentile changes in price and output a weighted average score (hqm_score) to rank the top 10% of stocks in terms of momentum growth.

## Tech Stack
In this project I have used the following resources:
- **Python** for data manipulation and analysis
- **IEX Cloud: REST API** for batch API calls
- **Redis** for testing analytics tools by caching real-time data
- **psycopg2** database adapter to connect to PostgreSQL database hosted on AWS

New Version: refers to folder 'trading_analytics' only.  
adding:
- **Dagster** for workflow orchestration
- **Snowflake** for continual data storage for analytics
- **scikit-learn** ml models  
removing:
- **Redis**
- **psycopg2**
