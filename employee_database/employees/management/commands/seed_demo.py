from django.core.management.base import BaseCommand
from employees.models import Employees
from django.utils import timezone
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with fake employee data for demo purposes."

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing employee data...")
        Employees.objects.all().delete()

        departments = [
            "Engineering", "Marketing", "Finance",
            "Customer Support", "Design", "Operations"
        ]
        titles = [
            "Software Engineer", "Marketing Coordinator", "Accountant",
            "Support Rep", "UI/UX Designer", "Ops Analyst"
        ]

        today = timezone.now().date()

        for i in range(25):
            first = fake.first_name()
            last = fake.last_name()
            dept = random.choice(departments)
            title = random.choice(titles)

            doh = fake.date_between(start_date="-10y", end_date="today")
            bday = fake.date_of_birth(minimum_age=22, maximum_age=60)

            emp = Employees(
                firstname=first,
                lastname=last,
                phone=fake.phone_number(),
                department=dept,
                title=title,
                head=random.choice([True, False, False, None]),  # 25% chance to be head
                spv=random.choice([True, False, None]),          # 33% chance to be spv
                doh=doh,
                bday=bday
            )

            emp.save()

        self.stdout.write(self.style.SUCCESS("✅ Demo employee data seeded successfully."))
