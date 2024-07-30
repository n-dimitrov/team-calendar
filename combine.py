import pandas as pd
import os

month = "06"
target_file = "./data/data.csv"
# if file exists, load it
if os.path.exists(target_file):
    target_df = pd.read_csv(target_file, sep=';', encoding='utf-8') 
else:
    # Name;Status;From;To;Days;Duration;Absence;Description
    target_df = pd.DataFrame(columns=['Month', 'Name', 'Status', 'From', 'To', 'Days', 'Duration', 'Absence', 'Description']) 


print(f"Month: {month}")
df = pd.read_csv(f"./data/2024.{month}.csv", sep=';', encoding='utf-8')

df['Month'] = month
# df['Description'] = df['Short description'] + ' ' + df['Comment']

print(df)

# copy df to target_df
target_df = pd.concat([target_df, df], ignore_index=True)

# save to data.csv
target_df.to_csv(target_file, index=False, sep=';', encoding='utf-8')
print("Saved to data.csv")
