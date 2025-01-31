# Register your models here.
from django.contrib import admin
from .models import MuscleGroup, Exercise

admin.site.register(MuscleGroup)
admin.site.register(Exercise)
