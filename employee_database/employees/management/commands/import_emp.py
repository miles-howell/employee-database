# Copyright (c) 2025 Miles H. (Planned Pixel Studio)
# Licensed for personal or educational use only.
# Commercial use, redistribution, or resale requires a paid license.
# Contact: miles@plannedpixel.com

import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from employees.models import Employees
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime

class Command(BaseCommand):
    help = 'Import or update employees from a CSV file. Defaults to mystaticfiles/employees.csv if no path is given.'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            nargs='?',
            default=None,
            type=str,
            help='Optional path to the CSV file'
        )

    # Utility to generate a unique slug
    def generate_unique_slug(self, first_name, last_name):
        base_slug = slugify(f"{first_name} {last_name}")
        slug = base_slug
        n = 1
        while Employees.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{n}"
            n += 1
        return slug

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # If no path is provided, default to mystaticfiles/employees.csv
        if not csv_file:
            static_path = os.path.join(settings.BASE_DIR, 'mystaticfiles', 'employees.csv')
            self.stdout.write(f"No path provided. Using default: {static_path}")
            csv_file = static_path

        # Check if the file exists
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"❌ File not found: {csv_file}"))
            return

        seen_keys = set()

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                first_name = row['First Name'].strip()
                last_name = row['Last Name'].strip()
                phone = row['Extension'].strip()
                department = row['Department'].strip()
                title = row['Title'].strip()
                spv = row['Spv'].strip()
                head = row['Dept Head'].strip()
                raw_doh = row['FilteredDOH'].strip()
                raw_bday = row['FilteredBday'].strip()

                doh = None
                bday = None

                if raw_doh:
                    try:
                        parsed_date = datetime.strptime(raw_doh.split()[0], '%Y-%m-%d')
                        doh = parsed_date.date()
                    except ValueError as e:
                        print(f"Date parse error: {raw_doh} - {e}")
                if raw_bday:
                    try:
                        parsed_date = datetime.strptime(raw_bday.split()[0], '%Y-%m-%d')
                        bday = parsed_date.date()
                    except ValueError as e:
                        print(f"Date parse error: {raw_bday} - {e}")

                # Fix missing names: if last_name is blank, try to split first_name
                if not last_name:
                    parts = first_name.split()
                    if len(parts) > 1:
                        first_name = parts[0]
                        last_name = " ".join(parts[1:])
                    else:
                        last_name = "Unknown"

                # Skip rows where first name is still empty
                if not first_name:
                    self.stderr.write(self.style.ERROR(f"⚠️ Skipping row with missing first name: {row}"))
                    continue

                slug = self.generate_unique_slug(first_name, last_name)
                seen_keys.add((first_name, last_name))

                employee, created = Employees.objects.update_or_create(
                    firstname=first_name,
                    lastname=last_name,
                    defaults={
                        'phone': phone,
                        'department': department,
                        'title': title,
                        'slug': slug,
                        'spv': spv,
                        'head': head,
                        'doh': doh,
                        'bday': bday,
                    }
                )
                action = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f"{action}: {employee}"))

        # Delete employees not in the current CSV
        seen_q = Q()
        for fn, ln in seen_keys:
            seen_q |= Q(firstname=fn, lastname=ln)

        to_delete = Employees.objects.exclude(seen_q)
        deleted_count = to_delete.count()
        to_delete.delete()

        self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} employee(s) not found in CSV."))
        self.stdout.write(self.style.SUCCESS('✅ Import complete!'))
