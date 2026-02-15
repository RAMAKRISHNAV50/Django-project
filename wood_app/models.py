from django.db import models

# Create your models here.
class quotations(models.Model):
    name = models.CharField(max_length=50, null=False)
    mail = models.EmailField(max_length=50, null=False)
    mobile = models.BigIntegerField()
    # DB column in MySQL is `service` (singular) — map the model field `services` to it
    services = models.CharField(max_length=100, null=False, db_column='service')
    # ensure a sensible default so inserts won't fail if DB column is added later
    budget = models.IntegerField(default=0)
    note = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.name} — {self.services}"


# `contacts` model exists in migration 0002_contacts — add the model class so
# the codebase matches the migration history and enables saving from the
# contact form.
class contacts(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>: {self.subject}"

