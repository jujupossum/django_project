from django.contrib import admin
from manager.models import Client, Class, ClientProfile, StripeInfo, ClassHistory


class CLAdmin(admin.ModelAdmin):
    list_display = ('name', )

class CAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','company')
    
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ClassHistoryAdmin(admin.ModelAdmin):
    list_display =('name',)
    
class StripeInfoAdmin(admin.ModelAdmin):
    list_display = ('key',)
    
admin.site.register(Client, CAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(StripeInfo, StripeInfoAdmin)
admin.site.register(ClassHistory, ClassHistoryAdmin)