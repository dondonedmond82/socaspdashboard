import panel as pn
import pandas as pd
import hvplot.pandas
import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import ctypes
import pyodbc

warnings.filterwarnings("ignore")


def insertImportation(anneemois, origine, provenance, marketeur, essence, jet, petrole, gazoil):
    # Replace with the full path to your .accdb file
    database_path = r'C:\projet\socasp\socasp_19_09_2025\database\socasp.accdb'

    # Create connection string
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        fr"DBQ={database_path};"    
    )

    # Connect to database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    
    # Insert a new employee
    sql_insert = "INSERT INTO importation (anneemois, origine, provenance, marketeur, essence, jet, petrole, gazoil) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (anneemois, origine, provenance, marketeur, essence, jet, petrole, gazoil)

    cursor.execute(sql_insert, values)
    conn.commit()

    # Example: Get all rows from a table
    cursor.execute("SELECT * from importation")  # Replace with your actual table name

    # for row in cursor.fetchall():
    #     print(row)

    cursor.close()
    conn.close()




def insertDistribution(anneemois, marketeur, essence, jet, petrole, gazoil):
    # Replace with the full path to your .accdb file
    database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

    # Create connection string
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        fr"DBQ={database_path};"    
    )

    # Connect to database
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    
    # Insert a new employee
    sql_insert = "INSERT INTO distribution (anneemois, marketeur, essence, jet, petrole, gazoil) VALUES (?, ?, ?, ?, ?, ?)"
    values = (anneemois, marketeur, essence, jet, petrole, gazoil)

    cursor.execute(sql_insert, values)
    conn.commit()

    # Example: Get all rows from a table
    cursor.execute("SELECT * from distribution")  # Replace with your actual table name

    # for row in cursor.fetchall():
    #     print(row)

    cursor.close()
    conn.close()