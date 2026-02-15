from django.contrib import admin
from .models import quotations, contacts

# Register your models here.
admin.site.register(quotations)
admin.site.register(contacts)
