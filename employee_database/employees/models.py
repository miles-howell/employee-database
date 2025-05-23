from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

# Create your models here.

class Employees(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	slug = models.SlugField(blank=True)
	email = models.CharField(max_length=255, blank=True)
	head = models.BooleanField(blank=True, null=True)
	spv = models.BooleanField(blank=True, null=True)
	doh = models.DateField(blank=True, null=True)
	bday = models.DateField(blank=True, null=True)

	def save(self, *args, **kwargs):
		self.firstname = self.firstname.strip()
		self.lastname = self.lastname.strip()

		if not self.firstname or not self.lastname:
			raise ValueError("Firstname and lastname cannot be empty. ")

		if not self.slug:
			self.slug = slugify(f'{self.firstname} {self.lastname}')

		if not self.email and '*' not in self.department:
			self.email = (self.firstname[0]+self.lastname+"@coxhealthplans.com").lower()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.firstname} {self.lastname}"

class Analytics(models.Model):
	path = models.CharField(max_length=200)
	query_string = models.TextField(blank=True)
	ip_address =  models.GenericIPAddressField()
	user_agent = models.TextField()
	timestamp = models.DateTimeField(default=now)

	def __str__(self):
		return f"{self.ip_address} - {self.path} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"