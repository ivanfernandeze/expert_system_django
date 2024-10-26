

from django.contrib import admin
from .models import Destino

@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
