import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

"""
Author: Kilian Jakstis
Visualize year vs number of entrants of various educational levels
"""

db_name = 'educational_attainment_database.db'
table_2 = "table_2"
conn = sqlite3.connect(db_name)
index_col = "Groups"
educational_levels = {
    "None-8th": "no hs diploma",
    "9th-11th": "no hs diploma",
    "HS_Graduate": "high school",
    "Some_College": "high school",
    "Associates": "associates",
    "Bachelors": "bachelors",
    "Masters": "masters",
    "Professional": "doctorate",
    "Doctoral": "doctorate"
}
years_of_entry = {
    "2010 or later": 2020,
    "2000-2009": 2010,
    "1990-1999": 2000,
    "1980-1989": 1990,
    "1970-1979": 1980,
    "Before 1970": 1970
}
educ_levels_by_year = {level: [0 for i in range(len(years_of_entry))] for level in educational_levels.values()}

def read_chunks(offset_size, chunk_size, educ_level, year_value):
    query = f"SELECT \"{educ_level}\" " \
            f"FROM {table_2} " \
            f"WHERE \"{index_col}\"LIKE \'%{year_value}%\'" \
            f"LIMIT {chunk_size} OFFSET {offset_size}"
    return pd.read_sql_query(query, conn)

chunk = 3
for i, level in enumerate(educational_levels):
    for j, year in enumerate(years_of_entry):
        offset = 0
        summation = 0
        while True:
            data = read_chunks(offset, chunk, level, year)
            if data.empty:
                break
            summation += data.values.flatten()[0]
            offset += chunk
        educ_levels_by_year[educational_levels[level]][j] += summation

conn.close()

plt.figure(figsize=(10, 6))
x = list(years_of_entry.values())[::-1]
for y in educ_levels_by_year:
    plt.plot(x, educ_levels_by_year[y][::-1], label=y, linewidth=2)

plt.title('Year vs Educational Attainment of Entrants')
plt.xlabel('Year')
plt.ylabel('Number of Entrants (in thousands)')
plt.xlim(1965, 2025)
plt.grid(True)
plt.legend()
plt.savefig('entry_year_vs_attainment.png', format='png', dpi=300, bbox_inches='tight')
