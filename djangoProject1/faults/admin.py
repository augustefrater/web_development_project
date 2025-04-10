from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FaultCase, FaultImage, Profile

admin.site.register(FaultCase)
admin.site.register(FaultImage)
admin.site.register(Profile)
