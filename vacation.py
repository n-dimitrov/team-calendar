import pandas as pd

month = "2024.06"

print(f"Month: {month}")
df = pd.read_csv(f"./data/{month}.csv", sep=';', encoding='utf-8')

# filter absence Vacation
df = df[df['Absence'] == 'Vacation']
df = df.groupby('Name')['Days'].sum().reset_index()

print(df)

# save to vacation.csv
df.to_csv(f"./data/{month}-vacation.csv", index=False, sep=';', encoding='utf-8')
print("Saved to vacation.csv")