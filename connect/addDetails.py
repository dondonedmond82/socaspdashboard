import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import ctypes
import pyodbc

warnings.filterwarnings("ignore")


def insertOrigine(origine_one, origine_two):
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
    sql_insert = "INSERT INTO origine (origine_one, origine_two) VALUES (?, ?)"
    values = (origine_one, origine_two)

    cursor.execute(sql_insert, values)
    conn.commit()

    cursor.close()
    conn.close()




def insertProvenance(provenance_one, provenance_two):
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
    sql_insert = "INSERT INTO provenance (provenance_one, provenance_two) VALUES (?, ?)"
    values = (provenance_one, provenance_two)

    cursor.execute(sql_insert, values)
    conn.commit()

    cursor.close()
    conn.close()



def insertMarketeur(marketeur_one, marketeur_two):
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
    sql_insert = "INSERT INTO marketeur (marketeur_one, marketeur_two) VALUES (?, ?)"
    values = (marketeur_one, marketeur_two)

    cursor.execute(sql_insert, values)
    conn.commit()

    cursor.close()
    conn.close()



def insertAccount(username, password_one, password_two):
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
    sql_insert = "INSERT INTO account (username, password_one, password_two) VALUES (?, ?, ?)"
    values = (username, password_one, password_two)

    cursor.execute(sql_insert, values)
    conn.commit()

    cursor.close()
    conn.close()


