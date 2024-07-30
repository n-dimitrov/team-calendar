
import pandas as pd
import re

line = "Bunis, Nikola (11523656/I) 194469 07.11.2023 Approved 02.01.2024 02.01.2024 1 Day 1 Day Vacation Vacation"
# line = "Lyapova, Mariya (11504399/I) 198084 25.01.2024 Approved 04.12.2023 08.01.2024 5 Days 22 Days Illness at entry Illness at entry 45 days before birth"
line = "Georgieva, Diyana (11828118/I) 196245 07.12.2023 Approved 03.12.2023 01.01.2024 0 Day 17 Days Illness at entry Illness at entry"
# Define the regex pattern
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
    df = pd.DataFrame([parsed_data])

    print(df)
else:
    print("No match found")