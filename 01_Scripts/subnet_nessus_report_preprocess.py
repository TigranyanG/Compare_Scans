import pandas as pd
import os

input_file = os.path.join('02_Incoming_Scans', 'nessus_scan_sample_subnet.csv')
output_file = os.path.join('04_Processing', 'processed_nessus_subnet.xlsx')

df = pd.read_csv(input_file)
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

filtered_df = df[df['Risk'].isin(['High', 'Critical', 'Medium'])]

aggregated = filtered_df.groupby(['Plugin ID', 'Name'], as_index=False).agg({
    'CVE': 'first', 'CVSS v3.0 Base Score': 'first', 'Risk': 'first',
    'Protocol': 'first', 'Port': 'first', 'Synopsis': 'first',
    'Description': 'first', 'Solution': 'first', 'See Also': 'first',
    'Host': lambda hosts: ', '.join(sorted(set(hosts.astype(str))))
})

aggregated['CVSS v3.0 Base Score'] = pd.to_numeric(aggregated['CVSS v3.0 Base Score'], errors='coerce')
aggregated.sort_values(by='CVSS v3.0 Base Score', ascending=False, inplace=True)
aggregated.to_excel(output_file, index=False)
print(f"Processed {len(aggregated)} subnet vulnerabilities.")