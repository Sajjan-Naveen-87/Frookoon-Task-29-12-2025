from django.contrib import admin
from .models import User, Product, Vendor

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Vendor)