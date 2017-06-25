from django.contrib import admin
from manager.models import ClassRoom, Client, Class, ClientProfile

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
    

admin.site.register(ClassRoom, CLAdmin)
admin.site.register(Client, CAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(ClientProfile, ClientProfileAdmin)
