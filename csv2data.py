import pandas as pd

names = [
    'Bunis, Nikola (11523656/I)', 
    'Dimitrov, Nikolay (11306619/I)',
    'Georgieva, Diyana (11828118/I)',
    'Gligov, Iliyan (11306589/I)',
    'Gochev, Blagovest (11306482/I)',
    'Grigorov, Ladislav (11828133/I)',
    'Kalinov, Chavdar (11306551/I)',
    'Lyapova, Mariya (11504399/I)',
    'Marinova, Pavlina (11787376/I)',
    'Obretenov, Borislav (11306501/I)',
    'Sholev, Radoslav (11821857/I)',    
    'Vasilev, Ivan (11847188/I)',
    'Baruh, Ognian (11678180/I)',
    'Kostadinov, Zhivko (11828128/I)',
    'Yoncheva, Gabriela (11678182/I)',
    'Mihaylov, Zlatimir (11828135/I)',
    'Manchev, Martin (11828134/I)',
 ]

#load the data cvs file
df = pd.read_csv("text.csv", sep=';', encoding='utf-8')

# print(df)

df['Name_Valid'] = df['Name'].isin(names)
if not df['Name_Valid'].all():
    print("ERROR: Unknown name found")
    print(df[~df['Name_Valid']])

df['Days'] = df['Days'].str.replace(' Days', '').str.replace(' Day', '').astype(int)
df['Duration'] = df['Duration'].str.replace(' Days', '').str.replace(' Day', '').astype(int)

# df['From'] = pd.to_datetime(df['From'], format='%d.%m.%Y')
# df['To'] = pd.to_datetime(df['To'], format='%d.%m.%Y')

# delete REQUEST_NO column
df.drop('Request_no', axis=1, inplace=True)
df.drop('Name_Valid', axis=1, inplace=True)
df.drop('Date_of_request', axis=1, inplace=True)

# Obretenov, Borislav (11306501/I) -> Obretenov, Borislav
df['Name'] = df['Name'].str.extract(r'([\w\s,]+)')

# save to data.csv
df.to_csv("data.csv", index=False, sep=';', encoding='utf-8')
print("Saved to data.csv")