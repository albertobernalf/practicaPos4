from django.contrib import admin

# Register your models here.

from usuarios.models import TiposDocumento, TiposUsuario, Usuarios, UsuariosContacto


@admin.register(TiposDocumento)
class tiposDocumentoAdmin(admin.ModelAdmin):

    list_display=("id","abreviatura","nombre")
    search_fields =("id","abreviatura","nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(TiposUsuario)
class tiposUsuarioAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(Usuarios)
class usuariosAdmin(admin.ModelAdmin):

    list_display = ("id","tipoDoc","documento","nombre","genero","centrosC","tiposUsuario","direccion","telefono","contacto")
    search_fields =("id","tipoDoc","documento","nombre","genero","centrosC","tiposUsuario","direccion","telefono","contacto")
    # Filtrar
    list_filter = ('genero','tiposUsuario')

@admin.register(UsuariosContacto)
class usuariosContactoAdmin(admin.ModelAdmin):

    list_display = ("id","tipoDoc","documento","nombre","direccion","telefono","correo", "tipoDocPaciente","documentoPaciente", "consecPaciente")
    search_fields =  ("id","tipoDoc","documento","nombre","direccion","telefono","correo", "tipoDocPaciente","documentoPaciente", "consecPaciente")
    # Filtrar
    list_filter =  ("id","tipoDoc","documento","nombre","direccion","telefono","correo", "tipoDocPaciente","documentoPaciente", "consecPaciente")