from django.contrib import admin
from .models import User, Watch, Asset

# Register your models here.
admin.site.register(User)
admin.site.register(Watch)
admin.site.register(Asset)
