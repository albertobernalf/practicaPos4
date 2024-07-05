from django.contrib import admin

# Register your models here.

from sitios.models import Departamentos, Ciudades, Centros, SedesClinica, DependenciasTipo, Dependencias,  ServiciosSedes, SubServiciosSedes, HistorialDependencias, Municipios, Paises, Localidades

@admin.register(SedesClinica)
class sedesClinicaAdmin(admin.ModelAdmin):


    list_display = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
    search_fields = ("id","departamentos","ciudades", "nombre","direccion", "telefono", "contacto","fechaRegistro")
    #Filtrar
    list_filter =('nombre', 'ciudades')


class CiudadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")

    # Filtrar
    list_filter = ('nombre',)


class DepartamentosAdmin(admin.ModelAdmin):


    list_display=("id","nombre")

    search_fields =("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

admin.site.register(Departamentos, DepartamentosAdmin)
admin.site.register(Ciudades, CiudadesAdmin)




@admin.register(Centros)
class centrosAdmin(admin.ModelAdmin):
        list_related_name = 'ciudadesDepartamentos'

        list_display = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        search_fields = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        # Filtrar
        list_filter = ('nombre','departamentos','ciudades','contacto')



@admin.register(ServiciosSedes)
class serviciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "servicios","nombre")
    search_fields = ("id","sedesClinica", "servicios","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "servicios",)


@admin.register(SubServiciosSedes)
class SubServiciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "serviciosSedes", "subServiciosSedes","nombre")
    search_fields = ("id","sedesClinica", "serviciosSedes","subServiciosSedes","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "serviciosSedes","subServiciosSedes")



@admin.register(DependenciasTipo)
class dependenciasTipoAdmin(admin.ModelAdmin):


    list_display = ("id","nombre")
    search_fields = ("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Dependencias)
class dependenciasAdmin(admin.ModelAdmin):


    list_display = ("id", "sedesClinica","serviciosSedes","subServiciosSedes","numero", "dependenciasTipo", "nombre", "descripcion")
    search_fields =  ("id", "sedesClinica","serviciosSedes","subServiciosSedes","numero", "dependenciasTipo", "nombre", "descripcion")
    #fields =  ("sedesClinica","subServicios", "dependenciasTipo","numero", "nombre", "descripcion")
    # Filtrar
    #list_filter = ('nombre', "sedesClinica","subServicios","numero", 'dependenciasTipo','descripcion')


@admin.register(HistorialDependencias)
class historialDependenciasAdmin(admin.ModelAdmin):


    list_display = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    fields = ( "dependencias", "tipoDoc", "documento", "consec", "fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    search_fields = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")


@admin.register(Municipios)
class municipiosAdmin(admin.ModelAdmin):


    list_display = ("id", "nombre", "municipioCodigoDian","departamento", "fechaRegistro")
    search_fields = ("id", "nombre", "municipioCodigoDian","departamento", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "municipioCodigoDian","departamento", "fechaRegistro")


@admin.register(Paises)
class paisAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "paisCodigoDian", "fechaRegistro")
    search_fields = ("id", "nombre", "paisCodigoDian",  "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "paisCodigoDian", "fechaRegistro")


@admin.register(Localidades)
class localidadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")
    search_fields = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")

admin.site.site_header = 'Clinica Vulnerable'
admin.site.index_title = 'Panel de control '
admin.site.site_title = 'Administracion'



