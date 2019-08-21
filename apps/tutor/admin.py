from django.contrib import admin

# Register your models here.
from tutor.models import Label, Tutor

admin.site.register(Tutor)
admin.site.register(Label)