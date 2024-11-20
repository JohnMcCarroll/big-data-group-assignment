import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# name json data file "thread_data.json" in same dir
# prints summary table info, saves daily post barchart

with open("thread_data.json", "r") as file:
    data = json.load(file)

id_user = {"W0192CMQM6F": "John McCarroll", "U07J87Q7K6U": "Kilian Jakstis", "U01LH695G2C": "Willow Rose"}
msg_data = data["messages"]
user_post_data = {x: {} for x in id_user.values()}
date_format = '%m/%d/%y'

first_day = datetime.fromtimestamp(float(msg_data[0]["ts"]))
last_day = datetime.fromtimestamp(float(msg_data[-1]["ts"]))

date_range = {}
current = first_day
while current <= last_day:
    date_range[current.strftime(date_format)] = {u: 0 for u in id_user.keys()}
    current += timedelta(days=1)

for m in msg_data:
    if m["type"] == "message":
        date = datetime.fromtimestamp(float(m["ts"])).strftime(date_format)
        date_range[date][m["user"]] += 1

post_counts = {member: [] for member in id_user.keys()}
for date in date_range.keys():
    for member in id_user.keys():
        post_counts[member].append(date_range[date].get(member))
post_counts_values = [post_counts[member] for member in id_user]

for i, member in enumerate(id_user.values()):
    user_post_data[member]["max"] = max(post_counts_values[i])
    user_post_data[member]["min"] = min(post_counts_values[i])
    user_post_data[member]["total"] = sum(post_counts_values[i])
    user_post_data[member]["average"] = user_post_data[member]["total"] / len(date_range)

x = np.arange(len(date_range))
fig, ax = plt.subplots()
width = 0.2
for i, member in enumerate(id_user):
    plt.bar(x + i * width, post_counts[member], 0.2, label=id_user[member])

print("Summary table data:")
print(user_post_data)

max_posts = max([user_post_data[x]["max"] for x in id_user.values()])
ax.set_xticks(x + width)
ax.set_xticklabels(date_range.keys(), fontsize=8)
ax.set_yticks(range(0, max_posts + 1))
ax.set_xlabel("Date")
ax.set_ylabel("Number of Messages")
ax.set_title("Daily Slack Messages by Group Member")
plt.xticks(rotation=45)
ax.legend(title='Group Member')
plt.savefig('post_chart.png', format='png', dpi=300, bbox_inches='tight')
