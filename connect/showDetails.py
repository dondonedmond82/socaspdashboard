import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import ctypes
import pyodbc

warnings.filterwarnings("ignore")

def dataOrigine():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_19_09_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT origine_one, origine_two from origine"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./type/origine_data.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))
        

def dataProvenance():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT provenance_one, provenance_two from provenance"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./type/provenance_data.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))



def dataMarketeur():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT marketeur_one, marketeur_two from marketeur"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./type/marketeur_data.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))



def dataAccount():

    try:
        # Replace with the full path to your .accdb file
        database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

        #  Create connection string
        conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
        conn = pyodbc.connect(conn_str)

        # Your SQL query
        query = "SELECT username, password_one, password_two from account"

        # Load result into DataFrame directly
        df = pd.read_sql(query, conn)

        # Always good to close connection
        conn.close()

        # Write to Excel file
        df.to_excel('./type/account_data.xlsx', index=False)

    except Exception as Ex:
        print("%s"%(Ex))


def exportUser():

    # Replace with the full path to your .accdb file
    database_path = r'C:\projet\socasp\socasp_06_08_2025\database\socasp.accdb'

    #  Create connection string
    conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" fr"DBQ={database_path};")
    conn = pyodbc.connect(conn_str)

    # Your SQL query
    query = "SELECT username, password_one from account"

    # Load result into DataFrame directly
    df = pd.read_sql(query, conn)
 
    thisdict = dict(df)

    with open("credentials.json", "w") as final:
        json.dump(thisdict, final)

    # Always good to close connection
    conn.close()

    cursor.close()
    conn.close()