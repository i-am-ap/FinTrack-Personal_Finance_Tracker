from django.contrib import admin

from .models import CustomUser, Data, limitData


admin.site.register(CustomUser)
admin.site.register(Data)
admin.site.register(limitData)

