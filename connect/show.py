import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import ctypes
import pyodbc

warnings.filterwarnings("ignore")

def dataImportation():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_19_09_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT origine, provenance, marketeur, essence, jet, petrole, gazoil, anneemois from importation"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./data/importation.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))
        

def dataDistribution():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT marketeur, essence, jet, petrole, gazoil, anneemois  from distribution"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./data/distribution.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))


