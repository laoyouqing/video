from django.contrib import admin

# Register your models here.
from store.models import Store, StoreImage

admin.site.register(Store)
admin.site.register(StoreImage)

