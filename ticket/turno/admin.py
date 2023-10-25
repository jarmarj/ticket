from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Turno, Municipio, Nivel, Asunto, Estatus, User, Qr


class TurnoAdmin(admin.ModelAdmin):
    list_display = ('turno', 'municipio', 'id')
    list_filter = ('municipio',)


class TurnoInline(admin.TabularInline):
    model = Turno
    extra = 1


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'municipio')
    inlines = [
        TurnoInline
    ]


admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Nivel)
admin.site.register(Asunto)
admin.site.register(Estatus)
admin.site.register(Turno,  TurnoAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Qr)
