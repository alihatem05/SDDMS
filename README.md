# SDDMS – Student Data CSV Management System

SDDMS (Student Data CSV Management System) is a Python-based project for validating, processing, and organizing CSV files containing student records. It automatically checks for data quality issues, enforces constraints (like GPA ranges, name formats, valid grades), and sorts files into clean or quarantined directories based on validation results.

✨ Features

✅ Automated Setup – creates required input/output folders.

✅ Config-driven – flexible validation rules defined in data.json.

✅ CSV Validation – enforces column headers, data types, ranges, and formats.

✅ File Sorting – clean files go to processed/clean, invalid files go to processed/quarantined.

✅ Logging – detailed logs written to log.txt for debugging and tracking.

✅ Extensible – easily add new rules or extend schema in data.json.
