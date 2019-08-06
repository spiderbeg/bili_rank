from django.contrib import admin

# Register your models here.
from .models import User, User_info, Submits

admin.site.register(User)
admin.site.register(User_info)
admin.site.register(Submits)
