import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Connect to database
db_name = 'educational_attainment_database.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
table2_name = 'attain02_2022'

# Remove first four rows of the table
delete_query = f"""
DELETE FROM {table2_name} 
WHERE rowid IN (
    SELECT rowid FROM {table2_name}
    ORDER BY rowid ASC
    LIMIT 4
);
"""
cursor.execute(delete_query)

# Query to get dataframe of table 2
query = f"SELECT * FROM attain02_2022;"
df2 = pd.read_sql_query(query, conn)

# Set first row as column names
df2.columns = df2.iloc[0]
df2 = df2.drop(0)
df2 = df2.reset_index(drop=True)

# Rename the first column
df2.columns.values[0] = "Group"

# Plot Occupation Data
indices = [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
df2.set_index('Group', inplace=True)
df_subset = df2.iloc[indices]
# Convert strings to numeric
df_subset.iloc[:, 0:] = df_subset.iloc[:, 0:].replace(',', '', regex=True).apply(pd.to_numeric)
# Divide by the respective totals to get percentages
df_subset.iloc[:, 1:] = df_subset.iloc[:, 1:].div(df_subset['Total'], axis=0)
# Drop Total column
df_subset = df_subset.drop(columns=['Total'], errors='ignore')
# Create bar chart
ax = df_subset.plot(kind='bar', stacked=False, figsize=(14, 7), width=0.7)
ax.set_ylim(0, 0.5)
ax.set_ylabel('Percentage of Employees (%)')
# Set y axis as %
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
ax.set_title('Educational Attainment vs Occupation')
ax.set_xlabel('Occupation')
# Clean x labels
ax.set_xticklabels([label.get_text().strip() for label in ax.get_xticklabels()], rotation=45, ha='right', fontsize=8)
ax.legend(title='Educational Attainment', bbox_to_anchor=(1, 1), loc='upper left')
plt.tight_layout()
plt.savefig('educational_attainment_vs_occupation.png', format='png', dpi=300, bbox_inches='tight')
