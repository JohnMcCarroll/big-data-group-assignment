import sqlite3
import pandas as pd
import os

"""
Authors: John McCarroll, Kilian Jakstis
Clean and load data into SQLite database
"""

def clean_3(df3):
    # clean formatting for table 3
    df_cleaned = df3.replace('', pd.NA).dropna()
    df_cleaned = df_cleaned.replace(['Z', r'^\s*$'], 0, regex=True)
    # fix col names
    column_names3 = ['educ_attainment',
                     "allpeople_number", "allpeople_percent",
                     "male_number", "male_percent",
                     "female_number", "female_percent",
                     "age25_34_number", "age25_34_percent",
                     "age35_54_number", "age35_54_percent",
                     "age55plus_number", "age55plus_percent",
                     "white_number", "white_percent",
                     "nonhispanicwhite_number", "nonhispanicwhite_percent",
                     "black_number", "black_percent",
                     "asian_number", "asian_percent",
                     "hispanic_number", "hispanic_percent"
                     ]
    df_cleaned.columns = column_names3
    return df_cleaned

if __name__ == "__main__":
    
    # Define table paths
    table1_path = "data/table-1-1.xlsx"
    table2_path = "data/table-2-1.xlsx"
    table3_path = "data/table-3.xlsx"

    db_name = 'educational_attainment_database_python.db'
    table_name1 = "attain01_2022"
    table_name2 = "attain02_2022"
    table_name3 = "attain03_2022"
    table_name3clean = "attain03_2022_clean"

    # Get full paths to excel files
    current_file_path = os.path.abspath(__file__)
    root_folder = os.path.dirname(current_file_path)
    table1_full_path = os.path.join(root_folder, table1_path)
    table2_full_path = os.path.join(root_folder, table2_path)
    table3_full_path = os.path.join(root_folder, table3_path)

    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    
    # Load table data to SQLite database
    df = pd.read_excel(table1_full_path)
    df.to_sql(table_name1, conn, if_exists='replace', index=False)
    df = pd.read_excel(table2_full_path)
    df.to_sql(table_name2, conn, if_exists='replace', index=False)
    df = pd.read_excel(table3_full_path)
    df.to_sql(table_name3, conn, if_exists='replace', index=False)
    # new table
    df = clean_3(df)
    df.to_sql(table_name3clean, conn, if_exists='replace', index=False)

    # Commit the changes
    conn.commit()

    # Query to retrieve the names of all tables in database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # View each table
    for table_name in tables:
        print(f"\nContents of table {table_name[0]}:")
        df = pd.read_sql_query(f"SELECT * FROM {table_name[0]};", conn)
        print(df)

    conn.close()
