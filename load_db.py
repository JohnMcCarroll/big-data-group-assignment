import sqlite3
import pandas as pd
import os


if __name__ == "__main__":
    
    # Define table paths
    table1_path = "data/table-1-1.xlsx"
    table2_path = "data/table-2-1.xlsx"
    table3_path = "data/table-3.xlsx"

    db_name = 'educational_attainment_database.db'
    table_name1 = "attain01_2022"
    table_name2 = "attain02_2022"
    table_name3 = "attain03_2022"

    # Get the absolute path of the current file
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

    # Commit the changes
    conn.commit()

    # Query to retrieve the names of all tables in the database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # View each table
    for table_name in tables:
        print(f"\nContents of table {table_name[0]}:")
        df = pd.read_sql_query(f"SELECT * FROM {table_name[0]};", conn)
        print(df)

    conn.close()
