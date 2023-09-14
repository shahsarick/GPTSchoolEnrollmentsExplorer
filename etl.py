# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 13:12:55 2023

@author: Sarick
"""

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table

# This code replaces the database tables with new data.
# In a production environment, appending would be used instead of replacing.
# Future improvements include logging, cronjob setup, and orchestration.


def validate_schema(data_frame, table):
    """
    Validate existing table schema before replacing.
    :param data_frame: DataFrame containing the new data
    :param table: Table object representing the database table
    """
    dtype_mapping = {
        "int64": "BIGINT",
        "object": "TEXT",
        "float64": "FLOAT"
    }

    for column in table.columns[1:]:
        assert column.name in data_frame.columns, \
            f"Column {column.name} not found in the new file"
        
        try:
            assert dtype_mapping[str(data_frame[column.name].dtype).lower()] \
                == str(column.type).upper(), f"Column {column.name} type mismatch"
        except KeyError:
            assert isinstance(
                data_frame[column.name].dtype, type(column.type)
            ), f"Column {column.name} type mismatch"


def load_data(data_frame, table, engine):
    """
    Load data into a database table.
    :param data_frame: DataFrame containing the new data
    :param table: Table object representing the database table
    :param engine: SQLAlchemy engine object
    """
    validate_schema(data_frame, table)
    data_frame.to_sql(table.name, engine, if_exists="replace")


def county_demographics_load(file_path, table, disk_engine):
    """
    Load county demographics data.
    :param file_path: File path to the Excel data
    :param table: Table object representing the database table
    :param disk_engine: SQLAlchemy engine object
    """
    demographics_df = pd.read_excel(file_path, skiprows=[0, 1, 2, 3])
    demographics_df.reset_index(inplace=True, drop=True)
    load_data(demographics_df, table, disk_engine)


def enrollments_load(file_path, sep, encoding, table, disk_engine):
    """
    Load enrollments data.
    :param file_path: File path to the CSV data
    :param sep: Separator used in the CSV file
    :param encoding: File encoding
    :param table: Table object representing the database table
    :param disk_engine: SQLAlchemy engine object
    """
    enrollments_df = pd.read_csv(file_path, sep=sep, encoding=encoding)
    load_data(enrollments_df, table, disk_engine)


if __name__ == "__main__":
    disk_engine = create_engine("sqlite:///my_lite_store.db")
    metadata = MetaData()

    enrollments = Table("enrollments", metadata, autoload_with=disk_engine)
    county_demographics = Table(
        "county_demographics", metadata, autoload_with=disk_engine
    )

    county_demographics_load(
        "California_DemographicsByCounty_sample.xlsx", county_demographics, disk_engine
    )
    enrollments_load("filesenrps.asp.tsv", "\t", "latin-1", enrollments, disk_engine)
