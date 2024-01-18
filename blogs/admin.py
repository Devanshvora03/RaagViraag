from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Categories)
admin.site.register(Post)
admin.site.register(SidebarContent)
admin.site.register(AboutContent)
admin.site.register(AdminInfo)