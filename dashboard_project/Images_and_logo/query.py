import mysql.connector
from getpass import getpass
import pandas as pd
import streamlit as st

##connection
password = getpass("Enter your password: ")
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password=f'{password}',  #
    db='phone_pulse'
)

cursor = conn.cursor()


@st.cache_resource
def view_all_data(df: str):
    cursor.execute(f"SELECT * FROM {df}")
    data = cursor.fetchall()
    return data


@st.cache_resource
def extract_column(df: str):
    cursor.execute(f'''
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{df}';
    ''')
    here = []
    smiles = cursor.fetchall()
    for smile in smiles:
        here.append(smile[0])
    return here


@st.cache_resource
def data_frame(df: str):
    result1 = view_all_data(df)
    result2 = extract_column(df)
    result = pd.DataFrame(result1, columns=result2)
    return result
