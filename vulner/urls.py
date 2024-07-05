"""vulner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf  import settings
from django.conf.urls.static import  static

from django.urls import path, include
from camara import  views as viewsCamara

from Reportes import views as viewsReportes

from admisiones import views as viewsAdmisiones

from usuarios import views as viewsUsuarios

from django.conf  import settings
from django.conf.urls.static import  static
from clinico import views as viewsClinico
#from mecanicosPacientes import views as viewsmecanicosPacientes



urlpatterns = [
    path('admin/', admin.site.urls),

    # Primero Reporteador

    path('chaining/', include('smart_selects.urls')),
    path('medicalReport/', viewsReportes.menuAcceso),

    #path('validaAcceso/', viewsReportes.validaAcceso),
    path('salir/', viewsReportes.salir),
    path('pantallaSubgrupos/<str:username>, <str:sedeSeleccionada>, <str:grupo>', viewsReportes.pantallaSubgrupos),
    path('emergenteGrupos/<str:username>, <str:sedeSeleccionada>, <str:grupo>', viewsReportes.emergenteGrupos),
    path('combo/<str:username>, <str:sedeSeleccionada>, <str:grupo>, <str:subGrupo>', viewsReportes.combo),
    #path('/combo/<str:username>, <str:sedeSeleccionada>, <str:grupo>, <str:subGrupo>', views.combo),

    # path('contrasena/<str:documento>', views.contrasena),

    ## Invoca Reporte

    path('Reporte1/<str:numreporte>,<str:username>,<str:sedeSeleccionada>,<str:grupo>,<str:subGrupo>',
         viewsReportes.Reporte1PdfView.as_view()),
    # path('Reporte2/<str:numreporte>,<str:username>,<str:sedeSeleccionada>,<str:grupo>,<str:subGrupo>', views.Reporte1PdfView.as_view()),

    # Fin Reporteador

    # Acceso al Programa General Clinico

    path('menu/', viewsCamara.menu),
    # path('menuAcceso/validaAcceso/', views.validaAcceso),
    path('contrasena/<str:documento>', viewsCamara.contrasena),
    # path('salir/validaAcceso/', views.validaAcceso),

    # HISTORIA CLINICA

    # path('accesoEspecialidadMedico/historiaView/<str:documento>', viewsClinico.nuevoView.as_view()),
    # path('historia1View/', viewsClinico.historia1View),
    # path('historiaExamenesView/', viewsClinico.historiaExamenesView),
    # path('consecutivo_folios/', viewsClinico.consecutivo_folios),
    # path('buscaExamenes/', viewsClinico.buscaExamenes),
    path('motivoSeñas/', viewsClinico.motivoSeñas),
    path('subjetivoSeñas/', viewsClinico.subjetivoSeñas),
    path('motivoInvidente/', viewsClinico.motivoInvidente),
    # path('resMotivoInvidente/', viewsClinico.s),
    path('reconocerAudio/', viewsCamara.reconocerAudio),
    path('reproduceAudio/', viewsCamara.reproduceAudio),
    path('accesoEspecialidadMedico/<str:documento>', viewsCamara.accesoEspecialidadMedico),
    path('crearHistoriaClinica/', viewsClinico.crearHistoriaClinica),
    # path('crearHistoriaClinica1/', viewsClinico.crearHistoriaClinica1.as_view()),
    path('buscarAdmisionClinico/', viewsClinico.buscarAdmisionClinico),
    path('cargaPanelMedico/', viewsClinico.cargaPanelMedico),
    path('buscarAntecedentes/', viewsClinico.buscarAntecedentes),

    # Actividaes Mecanicas

    path('prueba/', viewsClinico.prueba),
    #   path('manejoLuz/', viewsmecanicosPacientes.manejoLuz.as_view()),
    #  path('ambienteMusical/', viewsmecanicosPacientes.ambienteMusical.as_view()),
    path('camara/', viewsCamara.camara),
    path('leeAudio/', viewsCamara.leeAudio),

    path('chaining/', include('smart_selects.urls')),

    # Acceso global

    path('medicalSocial/', viewsAdmisiones.menuAcceso),

    # Admisiones

    path('validaAcceso/', viewsAdmisiones.validaAcceso),
    #path('menuAccesoClinico/', viewsAdmisiones.menuAcceso),
    path('validaAccesoClinico/', viewsAdmisiones.validaAcceso),
    path('escoge/', viewsAdmisiones.escogeAcceso),
    path('escoge/<str:Sede>,<str:Username>,<str:Profesional>,<str:Documento>,<str:NombreSede>,<str:escogeModulo>', viewsAdmisiones.escogeAcceso),

    path('retornarAdmision/<str:Sede>, <str:Perfil> , <str:Username>, <str:Username_id>, <str:NombreSede>',
         viewsAdmisiones.retornarAdmision),

    path('retornarMen/<str:Sede>,<str:Username>,<str:Documento>,<str:NombreSede>,<str:Profesional>', viewsAdmisiones.retornarMen),
    path('grabar1/<str:username>,<str:contrasenaAnt>,<str:contrasenaNueva>,<str:contrasenaNueva2>',
         viewsAdmisiones.validaPassword),
    path('findOne/<str:username> , <str:password> , <str:tipoDoc>/', viewsAdmisiones.Modal),
    # path('buscarAdmision/<str:BusHabitacion>,<str:BusTipoDoc>,<str:BusDocumento>,<str:BusPaciente>,<str:BusDesde>,<str:BusHasta>', viewsAdmisiones.buscarAdmision),
    path('buscarAdmision/', viewsAdmisiones.buscarAdmision),

    path('buscarEspecialidadesMedicos/', viewsAdmisiones.buscarEspecialidadesMedicos),
    path('buscarCiudades/', viewsAdmisiones.buscarCiudades),
    path('buscarHabitaciones/', viewsAdmisiones.buscarHabitaciones),
    path('buscarSubServicios/', viewsAdmisiones.buscarSubServicios),
    # path('crearAdmision/<str:Sede>,<str:Perfil>, <str:Username>, <str:Username_id>', viewsAdmisiones.crearAdmision.as_view()),
    path('crearAdmisionDef/', viewsAdmisiones.crearAdmisionDef),

    path('findOneUsuario/', viewsAdmisiones.UsuariosModal),
    path('guardarUsuariosModal/', viewsAdmisiones.guardarUsuariosModal),

    path('crearResponsables/', viewsAdmisiones.crearResponsables),

    # Facturacion

    # Citas Medicas

    # Usuarios

    path('crearUsuarios/', viewsUsuarios.crearUsuarios),
    # Fin Acceso al Programa General Clinico

]


if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

# Añadir
admin.site.site_header = 'Administracion Medical Report'
admin.site.site_title = "Portal de Medical Report"
admin.site.index_title = "Bienvenidos al portal de administración Medical Report"
