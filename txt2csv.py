import re
import pandas as pd

def process_line(line):
    pattern = re.compile(r"""
        (?P<Name>[\w\s,()\/]+)\s+                  # Name with possible special characters
        (?P<Request_no>\d+)\s+                     # Request number
        (?P<Date_of_request>\d{2}\.\d{2}\.\d{4})\s+ # Date of request
        (?P<Status>\w+)\s+                         # Status
        (?P<From>\d{2}\.\d{2}\.\d{4})\s+           # From date
        (?P<To>\d{2}\.\d{2}\.\d{4})\s+             # To date
        (?P<Days>\d+\s+\w+)\s+                     # Days (number and unit)
        (?P<Duration>\d+\s+\w+)\s+                 # Duration (number and unit)
        (?P<Absence>Vacation|Illness\s+at\s+entry|Maternity\s+leave)\s+ # Absence
        (?P<Description>.+)                        # Description
    """, re.VERBOSE)

    # Match the line with the regex pattern
    match = pattern.match(line)

    # Extract the matched groups into a dictionary
    if match:
        parsed_data = match.groupdict() 
        return parsed_data
    else:
        print("No match pattern: ", line)   
        return None
    
# read the text file
with open("text.txt", "r") as f:
    lines = f.readlines()

# skipt empty lines
lines = [line.strip() for line in lines if line.strip()]

print("Lines: ", len(lines))

# process each line
data = []
for line in lines:
    parsed_data = process_line(line)
    if parsed_data:
        data.append(parsed_data)

df = pd.DataFrame(data)
print("Data lines:", len(df))
print(df)

df.to_csv("text.csv", index=False, sep=';', encoding='utf-8')
print("Saved to text.csv")
