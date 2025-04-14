from django.contrib import admin
from .models import UseCase, HubCategory, HubLink, ServerHost

@admin.register(UseCase)
class UseCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)


admin.site.register(HubCategory)
admin.site.register(HubLink)
admin.site.register(ServerHost)