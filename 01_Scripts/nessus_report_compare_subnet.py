import pandas as pd
from datetime import date
import os

CURR = os.path.join('04_Processing', 'processed_nessus_subnet.xlsx') 
BASE = os.path.join('03_Baselines', 'baseline_nessus_subnet.xlsx') 
OUT  = 'vuln_change_report_subnet.xlsx'
TODAY = date.today().strftime('%Y-%m-%d')

def prep(df):
    df['Name'] = df['Name'].fillna('').astype(str).str.strip()
    df['Hosts'] = df['Host'].fillna('')
    df['Host Count'] = df['Hosts'].apply(lambda s: len([h for h in str(s).split(',') if h.strip()]))
    return df[df['Name'] != '']

df_c, df_b = prep(pd.read_excel(CURR)), prep(pd.read_excel(BASE))
names_c, names_b = set(df_c['Name']), set(df_b['Name'])
rows = []

for n in sorted(names_c - names_b):
    r = df_c[df_c['Name']==n].iloc[0]
    rows.append({'Date': TODAY, 'Status': 'NEW', 'Score': r['CVSS v3.0 Base Score'], 'Risk': r['Risk'], 'Name': n, 'Hosts': r['Hosts'], 'Action': 'Create'})

for n in sorted(names_b - names_c):
    r = df_b[df_b['Name']==n].iloc[0]
    rows.append({'Date': 'Prior', 'Status': 'FIXED', 'Score': r['CVSS v3.0 Base Score'], 'Risk': r['Risk'], 'Name': n, 'Hosts': r['Hosts'], 'Action': 'Remove'})

for n in sorted(names_c & names_b):
    rc, rb = df_c[df_c['Name']==n].iloc[0], df_b[df_b['Name']==n].iloc[0]
    diff = "Host Count Changed" if rc['Host Count'] != rb['Host Count'] else ""
    rows.append({'Date': 'Prior', 'Status': 'STABLE', 'Score': rc['CVSS v3.0 Base Score'], 'Risk': rc['Risk'], 'Name': n, 'Hosts': rc['Hosts'], 'Action': 'Update' if diff else 'Keep', 'Notes': diff})

report_df = pd.DataFrame(rows)
with pd.ExcelWriter(OUT, engine='xlsxwriter') as writer:
    report_df.to_excel(writer, index=False)
    wb, ws = writer.book, writer.sheets['Sheet1']
    f_new, f_rem, f_upd = wb.add_format({'bg_color': '#C6EFCE'}), wb.add_format({'bg_color': '#FFC7CE'}), wb.add_format({'bg_color': '#FFEB9C'})
    col = chr(ord('A') + report_df.columns.get_loc('Action'))
    ws.conditional_format(f'A2:Z{len(rows)+1}', {'type':'formula','criteria':f'=${col}2="Create"','format':f_new})
    ws.conditional_format(f'A2:Z{len(rows)+1}', {'type':'formula','criteria':f'=${col}2="Remove"','format':f_rem})
    ws.conditional_format(f'A2:Z{len(rows)+1}', {'type':'formula','criteria':f'=${col}2="Update"','format':f_upd})
print(f"Subnet report saved to {OUT}")