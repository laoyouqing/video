from django.contrib import admin

# Register your models here.
from users.models import Area, Address, User

admin.site.register(Area)
admin.site.register(Address)
admin.site.register(User)