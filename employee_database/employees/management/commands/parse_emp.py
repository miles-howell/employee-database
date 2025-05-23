# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

import os
import csv
import pyodbc
import base64
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.text import slugify
from django.conf import settings

# Key for department codes
departments = ['Government Programs', 'Administration', 'Finance', 
                'Info Tech', 'Claims', 'Member Services', 'Medical', 'Marketing', 'Enrollment', 'Mailroom', '*Fax Numbers', '*Main Numbers', '*Main Numbers']
dept_codes = ['00', '501', '503', '504', '505', '506', '510', '511', '514', '515', '*', '***', '****']

# Returns the department name, given department code
def find_dept_name(code):
    for idx, val in enumerate(dept_codes):
        if code == val:
            return departments[idx]
    return 'Unknown'

# Returns a list containing all active employees with department names, sorted by department and Spv status
def query_and_process_data(db_path):
    conn_str = (
        'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={db_path}'
    )
    base_dir = settings.BASE_DIR

    pyodbc.pooling = False
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()

    emp = crsr.execute("""
        SELECT 
            [First Name], 
            [Last Name], 
            [Extension], 
            [Title], 
            [Dept lookup], 
            [Spv], 
            [Dept Head], 
            IIF([DOH_Post], [DOH], NULL) AS FilteredDOH, 
            IIF([DOB_Post], [Bday], NULL) AS FilteredBday
        FROM Employees
        WHERE Inactive = False
    """).fetchall()

    crsr.close()
    cnxn.close()

    # Replace department codes with names
    processed_data = []
    for i in emp:
        i = list(i)
        i[4] = find_dept_name(i[4])  # Replace dept code with name
        i[3] = str(i[3]) # Title to str   
        processed_data.append(i)

    # Sort by department, then by Spv status (True first)
    processed_data.sort(key=lambda x: (x[4], not x[6], not x[5], x[3]))

    # Drop the Spv value from the output data

    return processed_data

# Writes employee data to CSV file at './employees.csv'
def write_CSV(data, output_path):
    header = ['First Name', 'Last Name', 'Extension', 'Title', 'Department', 'Spv', 'Dept Head', 'FilteredDOH', 'FilteredBday']
    with open(output_path, 'w', newline="", encoding='utf-8') as fou:
        csv_writer = csv.writer(fou)
        csv_writer.writerow(header)
        csv_writer.writerows(data)
    return True

class Command(BaseCommand):
    help = 'Parses employee data from Access DB and writes to a CSV.'

    def handle(self, *args, **kwargs):
        db_path = r"\\chp-fs1\Groups\HR Data\HR Archive\Employee Database.mdb"

        # Adjust path to save CSV inside 'employee_database/mystaticfiles'
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # now points to 'employee_database'
        csv_path = os.path.join(base_dir, 'mystaticfiles', 'employees.csv')

        self.stdout.write(f"Looking for Access DB at: {db_path}")
        if not os.path.exists(db_path):
            self.stderr.write(self.style.ERROR(f"Database not found at: {db_path}"))
            return

        self.stdout.write("Connecting to database and retrieving employee data...")
        directory = query_and_process_data(db_path)
        write_CSV(directory, csv_path)
        self.stdout.write(self.style.SUCCESS(f'Employee data parsed and saved to {csv_path}'))

        # Run the import_employees command
        self.stdout.write("Running import_employees to update Django model...")
        call_command('import_emp', csv_path)
