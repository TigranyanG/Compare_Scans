import os
import shutil
import subprocess
from datetime import date

# --- DIRECTORY CONFIGURATION ---
BASE_DIR = os.getcwd()
SCRIPT_DIR = os.path.join(BASE_DIR, "01_Scripts")
INPUT_DIR  = os.path.join(BASE_DIR, "02_Incoming_Scans")
BASELN_DIR = os.path.join(BASE_DIR, "03_Baselines")
PROCES_DIR = os.path.join(BASE_DIR, "04_Processing")
# New Archive Folders
ARC_REPT_DIR = os.path.join(BASE_DIR, "05_Archive_Reports")
ARC_BASE_DIR = os.path.join(BASE_DIR, "06_Archive_Baselines")

TODAY = date.today().strftime('%Y-%m-%d')

# --- SCAN CONFIGURATION ---
SCANS = [
    {
        "name": "Complete_Range",
        "raw": os.path.join(INPUT_DIR, "nessus_scan_sample.csv"),
        "processed": os.path.join(PROCES_DIR, "processed_nessus.xlsx"),
        "baseline": os.path.join(BASELN_DIR, "baseline_nessus.xlsx"),
        "preprocess_script": "nessus_report_preprocess.py",
        "compare_script": "nessus_report_compare.py",
        "report": "vuln_change_report.xlsx"
    },
    {
        "name": "Server_Subnet",
        "raw": os.path.join(INPUT_DIR, "nessus_scan_sample_subnet.csv"),
        "processed": os.path.join(PROCES_DIR, "processed_nessus_subnet.xlsx"),
        "baseline": os.path.join(BASELN_DIR, "baseline_nessus_subnet.xlsx"),
        "preprocess_script": "subnet_nessus_report_preprocess.py",
        "compare_script": "nessus_report_compare_subnet.py",
        "report": "vuln_change_report_subnet.xlsx"
    }
]

def run_step(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    print(f"  --> Executing: {script_name}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Error in {script_name}:\n{result.stderr}")
        return False
    return True

def main():
    print(f"🛡️  Lake Forest College - Cyber Audit Pipeline | {TODAY}")
    print("="*55)

    for scan in SCANS:
        print(f"\n▶ STARTING: {scan['name']}")

        if not os.path.exists(scan['raw']):
            print(f"  ⚠️  Skipping: '{os.path.basename(scan['raw'])}' not found.")
            continue

        # 1. Preprocess (Creates Processed Excel)
        if not run_step(scan['preprocess_script']): continue

        # 2. Compare (Generates Report)
        # Note: If no baseline exists, we skip comparison and initialize baseline
        if os.path.exists(scan['baseline']):
            if not run_step(scan['compare_script']): continue
            
            # --- ARCHIVING LOGIC ---
            # A. Archive the Change Report with today's date
            archived_report_name = f"{TODAY}_{scan['report']}"
            shutil.copy(scan['report'], os.path.join(ARC_REPT_DIR, archived_report_name))
            
            # B. Archive the OLD Baseline (last week's state) before it's updated
            # We stamp it with today's date to show this was the baseline used ON this date.
            archived_baseline_name = f"{TODAY}_{os.path.basename(scan['baseline'])}"
            shutil.copy(scan['baseline'], os.path.join(ARC_BASE_DIR, archived_baseline_name))
            
            print(f"  ✨ SUCCESS: Report and Baseline archived.")
        else:
            print(f"  ℹ️  No baseline found. Initializing first baseline...")

        # 3. HANDOVER: Update the active baseline for next week
        shutil.move(scan['processed'], scan['baseline'])
        print(f"  ✅ Active baseline updated for next cycle.")

    print("\n" + "="*55)
    print("✅ Pipeline finished. Check Main folder for current reports.")

if __name__ == "__main__":
    main()