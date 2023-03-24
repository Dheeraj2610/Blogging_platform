from django.contrib import admin
from core.models import registration,BlogPost,Comment
# Register your models here.

admin.site.register(registration)
admin.site.register(BlogPost)
admin.site.register(Comment)

