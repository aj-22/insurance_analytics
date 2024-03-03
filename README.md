## Project Details
- Data Simulator (Create synthetic data)
- Data Loader (Load data in database)
- Data Tracker (Transform and Track data using dbt)

## Set up the project

1. Set up SQL
   - From `sql_scripts`
   - Run `intialize.sql` in Microsoft SQL Server
   - Run `staging_tables.sql` in Microsoft SQL Server

2. Set up Dbt
   - Run `dbt seed`
   - Run `dbt run`

Only after executing the above steps move on the the next step

## Run Project

One time run: `python initial_load.py`

To create new data:
Enter data_simulator: `cd data_simulator`
Generate synthetic data: `python simulation.py`
Load synthetic data: `python realtime_load.py`

To run batch jobs:
Enter dbt project: `cd lambda`
Execute dbt job: `dbt run`

## Future Feature

Airflow to execute `realtime_load.py` on a minute basis and run batch jobs hourly basis.