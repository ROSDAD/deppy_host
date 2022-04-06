from django.contrib import admin
from deppy.models import Users
from deppy.models import Chats,Sentiments
# Register your models here.

admin.site.register(Users)
admin.site.register(Chats)
admin.site.register(Sentiments)
