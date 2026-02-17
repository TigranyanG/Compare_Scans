# Compare_Scans: Vulnerability Management & Change Tracking Pipeline

## 🛡️ Overview
`Compare_Scans` is a Python-based automation pipeline designed to streamline the vulnerability management lifecycle. By shifting from manual PDF summary reviews to automated raw CSV parsing, this tool provides a high-fidelity "Delta" (Change) report between weekly Nessus scans.

This project was developed to solve the "visibility gap" in standard security reporting, ensuring that newly discovered or persistent vulnerabilities are never overlooked due to report aggregation.

### 🚀 Key Impact
* **Efficiency:** Reduced manual report generation time by **95%** (from 2 hours down to 5 minutes).
* **Discovery:** Custom CSV parsing logic identified **critical CVEs** that were previously obscured in filtered PDF summaries.
* **Tracking:** Automated week-over-week "diff" logic to measure **remediation velocity** and identify stagnant risks.

---

## 📂 Project Structure
The pipeline follows a structured 6-stage data lifecycle to ensure auditability and data integrity:

* **`01_Scripts/`**: Core logic for preprocessing, CVSS-based prioritization, and comparison.
* **`02_Incoming_Scans/`**: Landing zone for new Nessus `.csv` exports.
* **`03_Baselines/`**: The "Source of Truth" representing the network state from the previous scan.
* **`04_Processing/`**: Temporary workspace for data normalization.
* **`05_Archive_Reports/`**: Automated storage for all generated Excel change reports.
* **`06_Archive_Baselines/`**: Version-controlled snapshots of previous network states.

---

## 🛠️ Features
* **Automated Delta Detection:** Flags vulnerabilities as `NEW`, `FIXED`, or `STABLE` (with host count updates).
* **Prioritized Reporting:** Automatically sorts findings by **CVSS 3.0 Score** and **Risk Level**.
* **Data Isolation:** Strictly separates global network scans from specific server subnets to prevent data contamination.
* **Audit Trail:** Every run generates a date-stamped archive of both the report and the baseline used.

---

## ⚙️ Installation & Usage

### Prerequisites
* Python 3.x
* Pandas & OpenPyXL (`pip install pandas openpyxl`)

### How to Run
1.  Place your new Nessus CSV exports into `02_Incoming_Scans`.
2.  Run the master pipeline:
    ```bash
    python run_pipeline.py
    ```
3.  Find your prioritized report in the main folder and a backed-up copy in `05_Archive_Reports`.

---

## 🔒 Security Note
This repository contains the **automation logic only**. No actual scan data, IP addresses, or sensitive network configurations are included. The `.gitignore` is configured to prevent the accidental upload of `.csv` or `.xlsx` files.