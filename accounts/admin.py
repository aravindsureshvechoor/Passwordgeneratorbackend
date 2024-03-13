from django.contrib import admin

# Register your models here.
from .models import User, saved_password, secureKeys

admin.site.register(User)
admin.site.register(saved_password)
admin.site.register(secureKeys)