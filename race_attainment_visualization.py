import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# todo: actually add in data chunking properly (instead of summing ig)

##### setup

db_name = 'educational_attainment_database.db'
table_name3clean = "attain03_2022_clean"
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
educational_levels = {
    f"\"{column_names3[0]}\" LIKE '%no diploma%'": "no hs diploma",
    f"\"{column_names3[0]}\" LIKE '%GED%' OR \"{column_names3[0]}\"  LIKE '%no degree%' OR \"{column_names3[0]}\"  LIKE '%High school diploma%'": "high school",
    f"\"{column_names3[0]}\" LIKE '%associate%'": "associates",
    f"\"{column_names3[0]}\" LIKE '%Bachelor%'": "bachelors",
    f"\"{column_names3[0]}\" LIKE '%Master%'": "masters",
    f"\"{column_names3[0]}\" LIKE '%Doctorate%' OR \"{column_names3[0]}\" LIKE '%Professional%'": "doctorate"
}
races = ['white_percent', 'black_percent', 'hispanic_percent', 'asian_percent', 'nonhispanicwhite_percent',
         'allpeople_percent']
race_labels = [w[:-1 * len("_percent")] for w in races]
conn = sqlite3.connect(db_name)

##### replicating bar chart from assignment 1

# read chunks of data, query
chunk_size = 1
def read_chunks(offset, chunk_size, educ_level, race_value):
    query = f"SELECT SUM(\"{race_value}\") " \
            f"FROM {table_name3clean} " \
            f"WHERE {educ_level} " \
            # f"LIMIT {chunk_size} OFFSET {offset}"
    return pd.read_sql_query(query, conn)

# chart info
x = np.arange(len(races))
width = 0.1
fig, ax = plt.subplots()

# iterate and query
for i, race in enumerate(races):
    group_percentages = np.zeros(len(educational_levels))
    offset = 0
    for j, z in enumerate(educational_levels):
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

##### same info but grouping by race, color coded by educ level

# chunk_size = 1
# def read_chunks(offset, chunk_size, educ_level):
#     query = f"SELECT SUM(\"{races[0]}\"), SUM(\"{races[1]}\"), SUM(\"{races[2]}\"), SUM(\"{races[3]}\"), " \
#             f"SUM(\"{races[4]}\"), SUM(\"{races[5]}\") " \
#             f"FROM {table_name} " \
#             f"WHERE {educ_level} " \
#             # f"LIMIT {chunk_size} OFFSET {offset}"
#     return pd.read_sql_query(query, conn)
#
# # chart info
# x = np.arange(len(races))
# width = 0.1
# fig, ax = plt.subplots()
#
# for i, educ_level in enumerate(educational_levels):
#     group_percentages = np.zeros(len(races))
#     offset = 0
#     df_chunk = read_chunks(offset, chunk_size, educ_level)
#     # while True:
#     #     df_chunk = read_chunks(offset, chunk_size, educ_level)
#     #     if df_chunk.empty:
#     #         break
#     group_percentages += df_chunk.values.flatten()
#     offset += chunk_size
#     ax.bar(x + i * width, group_percentages, width, label=educational_levels[educ_level])
#
# conn.close()
#
# ax.set_xticks(x + width / 2)
# ax.set_xticklabels(race_labels)
# ax.set_xlabel("Race")
# ax.set_ylabel("Percentage of demographic")
# ax.set_title("Race and Educational Attainment")
# plt.xticks(rotation=45)
# ax.legend(title="Highest Education Level Completed")
# plt.show()
