import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Author: Kilian Jakstis
Create bar chart for race and educational attainment visualization
"""

db_name = 'educational_attainment_database.db'
table_3 = "table_3"
educ_level = "Groups"
educational_levels = {
    f"\"{educ_level}\" LIKE '%no diploma%'": "no hs diploma",
    f"\"{educ_level}\" LIKE '%GED%' OR \"{educ_level}\"  LIKE '%no degree%' OR \"{educ_level}\"  LIKE '%High school diploma%'": "high school",
    f"\"{educ_level}\" LIKE '%associate%'": "associates",
    f"\"{educ_level}\" LIKE '%Bachelor%'": "bachelors",
    f"\"{educ_level}\" LIKE '%Master%'": "masters",
    f"\"{educ_level}\" LIKE '%Doctorate%' OR \"{educ_level}\" LIKE '%Professional%'": "doctorate"
}
races = [
    "White(%)",
    "Black(%)",
    "Hispanic(%)",
    "Asian(%)",
    "Non-Hispanic_White(%)",
    "All_People(%)"
]
race_labels = [w[:-1 * len("(%)")] for w in races]
conn = sqlite3.connect(db_name)

# todo: read chunks of data, query
chunk_size = 3
def read_chunks(offset, chunk_size, educ_level, race_value):
    query = f"SELECT \"{race_value}\" " \
            f"FROM {table_3} " \
            f"WHERE {educ_level} " \
            # f"LIMIT {chunk_size} OFFSET {offset}"
    return pd.read_sql_query(query, conn)

x = np.arange(len(races))
width = 0.1
fig, ax = plt.subplots()

for i, race in enumerate(races):
    group_percentages = np.zeros(len(educational_levels))
    offset = 0
    for j, z in enumerate(educational_levels):
        # while true for chunking
        df_chunk = read_chunks(offset, chunk_size, z, race)
        group_percentages[j] += df_chunk.values.flatten().sum()
    offset += chunk_size
    ax.bar(x + i * width, group_percentages, width, label=race_labels[i])

conn.close()

# tidy up plot
ax.set_xticks(x + width / 2)
ax.set_xticklabels(educational_levels.values())
ax.set_xlabel("Educational Attainment")
ax.set_ylabel("Percentage of Demographic")
ax.set_title("Race and Educational Attainment")
plt.xticks(rotation=45)
ax.legend(title='Race')
plt.show()
