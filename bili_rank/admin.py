from django.contrib import admin

# Register your models here.
from .models import User_info, Submits

admin.site.register(User_info)
admin.site.register(Submits)