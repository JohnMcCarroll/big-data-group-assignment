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
educ_col = "Groups"
educational_levels = {
    f"\"{educ_col}\" LIKE '%no diploma%'": "no hs diploma",
    f"\"{educ_col}\" LIKE '%GED%' OR \"{educ_col}\"  LIKE '%no degree%' OR \"{educ_col}\"  LIKE '%High school diploma%'": "high school",
    f"\"{educ_col}\" LIKE '%associate%'": "associates",
    f"\"{educ_col}\" LIKE '%Bachelor%'": "bachelors",
    f"\"{educ_col}\" LIKE '%Master%'": "masters",
    f"\"{educ_col}\" LIKE '%Doctorate%' OR \"{educ_col}\" LIKE '%Professional%'": "doctorate"
}
races = [
    "White(%)",
    "Black(%)",
    "Hispanic(%)",
    "Asian(%)",
    "Non-Hispanic_White(%)",
    "All_People(%)"
]
race_labels = [w[:-1 * len('(%)')] for w in races]
conn = sqlite3.connect(db_name)

# reads in a few records at a time rather than all of them
def read_chunks(offset_size, chunk_size, educ_level, race_value):
    query = f"SELECT \"{race_value}\" " \
            f"FROM {table_3} " \
            f"WHERE {educ_level} " \
            f"LIMIT {chunk_size} OFFSET {offset_size}"
    return pd.read_sql_query(query, conn)

x = np.arange(len(races))
width = 0.1
fig, ax = plt.subplots()

# iteratively query and build up the bar chart
chunk = 3
for i, race in enumerate(races):
    group_percentages = np.zeros(len(educational_levels))
    for j, z in enumerate(educational_levels):
        offset = 0
        s = 0
        while True:
            df_chunk = read_chunks(offset, chunk, z, race)
            if df_chunk.empty:
                break
            s += df_chunk.values.flatten().sum()
            offset += chunk
        group_percentages[j] += s
    ax.bar(x + i * width, group_percentages, width, label=race_labels[i].replace('_', ' '))

conn.close()

# tidy up plot
ax.set_xticks(x + width / 2)
ax.set_xticklabels(educational_levels.values())
ax.set_xlabel("Educational Attainment")
ax.set_ylabel("Percentage of Demographic")
ax.set_title("Race and Educational Attainment")
plt.xticks(rotation=45)
ax.legend(title='Race')
plt.savefig('educational_attainment_vs_race.png', format='png', dpi=300, bbox_inches='tight')
