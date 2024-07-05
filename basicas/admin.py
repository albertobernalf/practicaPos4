from django.contrib import admin

# Register your models here.



from basicas.models import EstadoCivil,  Ocupaciones, CentrosCosto, Eventos, TiposFamilia, TiposContacto
from clinico.models import CausasExterna

@admin.register(EstadoCivil)
class estadoCivilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Ocupaciones)
class ocupacionesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(CentrosCosto)
class centrosCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(Eventos)
class eventosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","causasExterna")
    search_fields = ("id", "nombre","causasExterna")
    # Filtrar
    list_filter = ("id", "nombre","causasExterna")

@admin.register(TiposFamilia)
class tiposFamiliaCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(TiposContacto)
class tiposContactoCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)