import csv
import sys
import pandas as pd
import dataframe_image as dfi

# import userinfo from file.csv in sys.argv[1]
input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

df = pd.DataFrame(users, columns=list(
    ['username', 'id', 'access_hash', 'name']))

# adding a gradient based on values in cell
# df_styled = df.style.background_gradient()
# df_styled = df.style.set_precision(2)
df_styled = df.style.hide_index()

dfi.export(df_styled, "mytable.png")
