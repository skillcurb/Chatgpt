# Import libraries
from llama_index import SQLDatabase
from llama_index.indices.struct_store import (
    NLSQLTableQueryEngine,
    SQLTableRetrieverQueryEngine,
)
from sqlalchemy import create_engine, MetaData
import mysql.connector

# Create SQLALchemy engine and metadata
engine = create_engine("mysql+mysqlconnector://root: @localhost:3308/sqlalchemy")
metadata_obj = MetaData()

# Create tables
from sqlalchemy import Table, Column, String, Numeric, Date, ForeignKey

table_name = "car_brands"
car_brands_table = Table(
    table_name,
    metadata_obj,
    Column("brand", String(30), primary_key=True),
    Column("country", String(50), nullable=False)
)

table_name = "car_models"
car_models_table = Table(
    table_name,
    metadata_obj,
    Column("model", String(50), primary_key=True),
    Column("brand", String(30), ForeignKey("car_brands.brand"), nullable=False)
)

metadata_obj.create_all(engine)

# Insert data in the car_brands table
from sqlalchemy import insert

'''rows = [
    {"brand": "Citroen", "country": "France"},
    {"brand": "Hyundai", "country": "South Korea"},
    {"brand": "Jeep", "country": "USA"},
    {"brand": "Renault", "country": "France"},
    {"brand": "Volvo", "country": "German"}
]

for row in rows:
    stmt = insert(car_brands_table).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()
'''

# Insert data in the car_models table
'''rows = [
    {"model": "C3", "brand": "Citroen"},
    {"model": "C4", "brand": "Citroen"},
    {"model": "Creta", "brand": "Hyundai"},
    {"model": "HB20", "brand": "Hyundai"},
    {"model": "Santa Fé", "brand": "Hyundai"},
    {"model": "Tucson", "brand": "Hyundai"},
    {"model": "Compass", "brand": "Jeep"},
    {"model": "Renegade", "brand": "Jeep"},
    {"model": "Captur", "brand": "Renault"},
    {"model": "Duster", "brand": "Renault"},
    {"model": "Sandero", "brand": "Renault"},
    {"model": "V60", "brand": "Volvo"}
]
for row in rows:
    stmt = insert(car_models_table).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()
'''

# Configure OPENAI_API_KEY environment variable and api_key for openai library
import os
os.environ['OPENAI_API_KEY'] = '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'

import openai
openai.api_key="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"

# Connect llamindex to the MYSQL engine, naming the table we will use
sql_database = SQLDatabase(engine, include_tables=["car_brands", "car_models"])

# Create a structured store to offer a context to GPT
query_engine = NLSQLTableQueryEngine(sql_database)

# Invoke query_engine to ask a question and get answer
response = query_engine.query("Which car brands are from France?")
print(str(response))

# Invoke query_engine to ask a question and get answer
response = query_engine.query("Which car models are from Hyundai?")
print(str(response))

# Invoke query_engine to ask a question and get answer
response = query_engine.query("Which car models are produced in France?")
print(str(response))
print(str(response.metadata))

#Inserting Data into the table
response = query_engine.query("Insert a new row in the car_brands table having brand Toyota and Country USA")
print(str(response))

#Storing query results in new table
response = query_engine.query("Which car models are produced in France? Can you create a new table brand_models and store the result in it?")
print(str(response))
print(str(response.metadata))










