from django.contrib import admin

from .models import Transaction, Group, Category, Month

admin.site.register(Transaction)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(Month)
