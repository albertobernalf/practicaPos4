from django.shortcuts import render
import MySQLdb
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearAdmisionForm
from datetime import datetime
from admisiones.models import Ingresos
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast, Coalesce
import pyodbc
import psycopg2
#from datetime import datetime, timezone
#from datetime import timezone as TZ

import pytz
import tzlocal
from datetime import datetime



from sitios.models import  HistorialDependencias
from usuarios.models import Usuarios
from planta.models import Planta

# Create your views here.


def menuAcceso(request):
    print("Ingreso a acceso")

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)
    context = {}
    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    return render(request, "inicio/accesoPrincipal1.html", context)

def validaAcceso(request):
    print("Hola Entre a validar el acceso Principal")

    context = {}
    username = request.POST["username"].strip()
    print("username=", username)
    contrasena = request.POST["password"]
    #perfilConseguido = request.POST["seleccion1"]
    sede = request.POST["seleccion2"]
    Sede = sede
    print("Sede Mayuscula = ", Sede)
    print(contrasena)
    #print("perfilConseguido= ", perfilConseguido)
    print("sede= ", sede)
    context = {}
    context['Documento'] = username
    context['Username'] = username
    #context['Perfil'] = perfilConseguido
    context['Sede'] = sede

    # Variables que tengo en context : Documento, Perfil , Sede,   sedes ,NombreSede

    print (context['Documento'])

    # Consigo la sede Nombre

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for id, nombre  in cur.fetchall():
        nombreSede.append({'id':id , 'nombre' : nombre})

    miConexion.close()
    print("ESTA ES EL NOMBRE DE LA SEDE :")
    print (nombreSede[0]['nombre'])

    context['NombreSede'] =  nombreSede[0]['nombre']

    # esta consulta por que se pierde de otras pantallas

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes


    #miConexion0 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion0 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur0 = miConexion0.cursor()
    comando = 'select p.id  Username_id , p.nombre profesional , p."sedesClinica_id" from planta_planta p where p.documento = ' + "'"  + username + "'"
    cur0.execute(comando)
    print(comando)
    planta = []
    profesional = ''

    for Username_id, profesional, sedesClinica_id in cur0.fetchall():
        planta.append({'Username_id': Username_id, 'profesional': profesional, 'sedesClinica_id': sedesClinica_id})
        context['Username_id'] = Username_id
        profesional = profesional

    context['Profesional'] = profesional
    print ("Profesional = ", context['Profesional'] )
    miConexion0.close()

    if planta == []:


        context['Error'] = "Personal invalido ! "
        print("Entre por personal No encontrado")

        miConexion0.close()

        return render(request, "inicio/accesoPrincipal1.html", context)

    else:


        #miConexion1 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexion1 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        cur1 = miConexion1.cursor()
        comando = "select p.contrasena contrasena from planta_planta p where p.documento ='" + username + "'" + " AND contrasena = '" + contrasena +"'"
        cur1.execute(comando)

        plantaContrasena = []



        for contrasena in cur1.fetchall():
            plantaContrasena.append({'contrasena': contrasena})

        if plantaContrasena == []:
            miConexion1.close()
            context['Error'] = "Contraseña invalida ! "
            return render(request, "inicio/accesoPrincipal1.html", context)
        else:
            print("OJOOO ya valide CONTRASENA")
            #Aqui ya se valido username y contraseña OK

            #miConexion2 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
            miConexion2 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
            cur2 = miConexion2.cursor()
            #comando = "select perf.tiposPlanta_id  perfil from planta_planta p , planta_perfilesplanta perf , planta_tiposPlanta tp where  p.sedesClinica_id = perf.sedesClinica_id and  p.sedesClinica_id ='" + str(sede) + "' AND p.documento =  '" + str(username) + "' AND perf.planta_id = p.id AND  perf.tiposPlanta_id = " + str(perfilConseguido)

            #comando = 'select gralusu."perfilesClinicaId_id"  perfil from planta_planta p, seguridad_perfilesclinica perf, seguridad_perfilesgralusu  gralusu where p."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND p.documento = ' + "'"  +  str(username) + "'" + ' and p.id = gralusu."plantaId_id" AND gralusu."perfilesClinicaId_id" = perf.id AND gralusu."perfilesClinicaId_id" = '  + str(perfilConseguido)
            comando =  'select perfcli.id perfil1 from seguridad_perfilesgralusu gral, sitios_sedesClinica sedes, seguridad_perfilesclinica perfcli, planta_planta planta where planta."sedesClinica_id" = sedes.id and planta.id=gral."plantaId_id" and perfcli.id = gral."perfilesClinicaId_id" and sedes.id = ' + "'" +  str(sede) + "'" +   ' AND  planta.documento = ' + "'" + str(username) + "'"
            print(comando)
            cur2.execute(comando)

            perfil = []

            for perfil1 in cur2.fetchall():
                perfil.append({'perfil1': perfil1})
                
            print ("OJOOO esto es perfil", perfil)
            miConexion2.close()

            if perfil == []:

                print ("Entre Perfil No autorizado para la sede!")
                context['Error'] = "Perfil No autorizado para la sede! "
                return render(request, "inicio/accesoPrincipal1.html", context)

            else:

                ingresos = []

                #miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexionx = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curx = miConexionx.cursor()


                detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and   sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + str(Sede) + '  AND  deptip.id = dep."dependenciasTipo_id" and dep."serviciosSedes_id" = ser.id AND i."salidaDefinitiva" = ' + "'" +  'N' + "'" +  ' and tp.id = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id"'
                print(detalle)

                curx.execute(detalle)

                for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
                    ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                                     'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                                     'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                                     'DxActual': dxActual})

                miConexionx.close()
                print(ingresos)
                context['Ingresos'] = ingresos

                # Combo de Servicios
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" +  str(sede) + "'" + ' AND sed."servicios_id" = ser.id'
                curt.execute(comando)
                print(comando)

                servicios = []
                servicios.append({'id':'' , 'nombre': ''})

                for id, nombre in curt.fetchall():
                    servicios.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(servicios)

                context['Servicios'] = servicios

                # Fin combo servicios

                # Combo de SubServicios
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" +  str(
                    sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
                curt.execute(comando)
                print(comando)

                subServicios = []
                subServicios.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    subServicios.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(subServicios)

                context['SubServicios'] = subServicios

                # Fin combo SubServicios

                # Combo TiposDOc
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
                curt.execute(comando)
                print(comando)

                tiposDoc = []
                #tiposDoc.append({'id': '', 'nombre': ''})



                for id, nombre in curt.fetchall():
                    tiposDoc.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDoc)

                context['TiposDoc'] = tiposDoc

                # Fin combo TiposDOc

                # Combo Habitaciones
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                #comando = 'SELECT id ,nombre FROM sitios_dependencias where "sedesClinica_id" = ' + "'"  + str(Sede) +"'"  + ' AND "dependenciasTipo_id" = 2'
                comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
                curt.execute(comando)
                print(comando)

                habitaciones = []
                habitaciones.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    habitaciones.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(habitaciones)

                context['Habitaciones'] = habitaciones


                # Fin combo Habitaciones

                # Combo Especialidades
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                comando = "SELECT id ,nombre FROM clinico_Especialidades"
                curt.execute(comando)
                print(comando)

                especialidades = []
                especialidades.append({'id': '', 'nombre': ''})


                for id, nombre in curt.fetchall():
                    especialidades.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(especialidades)

                context['Especialidades'] = especialidades

                # Fin combo Especialidades



                # Combo EspecialidadesMedicos

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' +"'"  + str(username) + "'"
                curt.execute(comando)
                print(comando)

                especialidadesMedicos = []
                especialidadesMedicos.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    especialidadesMedicos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(especialidadesMedicos)

                context['EspecialidadesMedicos'] = especialidadesMedicos

                # Fin combo EspecialidadesMedicos


                # Combo Medicos
                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()
                #comando = 'SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p."sedesClinica_id" = perf."sedesClinica_id" and  perf."sedesClinica_id" = ' + "'"  + str(Sede) + "'" +  ' AND perf."tiposPlanta_id" = 1 and p.id = perf."planta_id"'
                comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str('MEDICO') + "'" +  ' and med.planta_id = p.id'

                curt.execute(comando)
                print(comando)

                medicos = []
                medicos.append({'id': '', 'nombre': ''})


                for id, nombre in curt.fetchall():
                    medicos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(medicos)

                context['Medicos'] = medicos

                # Fin combo Medicos

                # Combo TiposFolio

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

                curt.execute(comando)
                print(comando)

                tiposFolio = []
                tiposFolio.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposFolio.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposFolio)

                context['TiposFolio'] = tiposFolio

                # Fin combo TiposFolio

                # Combo TiposUsuario

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

                curt.execute(comando)
                print(comando)

                tiposUsuario = []
                # tiposUsuario.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposUsuario.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposUsuario)

                context['TiposUsuario'] = tiposUsuario

                # Fin combo Tipos Usuario

                # Combo TiposDocumento

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

                curt.execute(comando)
                print(comando)

                tiposDocumento = []
                #tiposDocumento.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    tiposDocumento.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDocumento)

                context['TiposDocumento'] = tiposDocumento

                # Fin combo TiposDocumento

                # Combo Centros

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

                curt.execute(comando)
                print(comando)

                centros = []

                for id, nombre in curt.fetchall():
                    centros.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(tiposDocumento)

                context['Centros'] = centros

                # Fin combo Centros

                # Combo Diagnosticos

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

                curt.execute(comando)
                print(comando)

                diagnosticos = []
                diagnosticos.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    diagnosticos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(diagnosticos)

                context['Diagnosticos'] = diagnosticos

                # Fin combo Diagnosticos

                # Combo Departamentos

                #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

                curt.execute(comando)
                print(comando)

                departamentos = []
                # tiposDocumento.append({'id': '', 'nombre': ''})

                for id, nombre in curt.fetchall():
                    departamentos.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(departamentos)

                context['Departamentos'] = departamentos

                # Fin combo Departamentos

                # Combo Ciudades

                #iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

                curt.execute(comando)
                print(comando)

                ciudades = []


                for id, nombre in curt.fetchall():
                    ciudades.append({'id': id, 'nombre': nombre})

                miConexiont.close()
                print(ciudades)

                context['Ciudades'] = ciudades

                # Fin combo Ciudades

                # Combo Modulos

                # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

                curt.execute(comando)
                print(comando)

                modulos = []

                for id, nombre, nomenclatura, logo in curt.fetchall():
                    modulos.append({'id': id, 'nombre': nombre,'nomenclatura':nomenclatura, 'logo':logo})

                miConexiont.close()
                print(modulos)

                context['Modulos'] = modulos

                # Fin combo Modulos

                # Combo PermisosGrales

                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                #comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
                comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(username) + "'"

                curt.execute(comando)
                print(comando)

                permisosGrales = []

                for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
                    permisosGrales.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo,'modulo_id':modulo_id, 'modulo_nombre':modulo_nombre })

                miConexiont.close()
                print(permisosGrales)

                context['PermisosGrales'] = permisosGrales


                # Fin Combo PermisosGrales

                # Combo PermisosDetalle

                miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
                curt = miConexiont.cursor()

                comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'"  + username + "'"

                curt.execute(comando)
                print(comando)

                permisosDetalle = []

                for id, nombre, nomenclatura, logo , nombreOpcion , nombreElemento in curt.fetchall():
                    permisosDetalle.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion':nombreOpcion, 'nombreElemento':nombreElemento})

                miConexiont.close()
                print(permisosDetalle)

                context['PermisosDetalle'] = permisosDetalle

                # Fin Combo PermisosDetalle

                print (perfil[0])

    return render(request, "inicio/PantallaPrincipal.html", context)


def escogeAcceso(request, Sede, Username, Profesional, Documento, NombreSede, escogeModulo ):
    print ("Entre Escoge Acceso")

    username = Username
    sede = Sede
    #perfilConseguido = Perfil
    profesional = Profesional
    documento = Documento
    nombreSede = NombreSede
    escogeModulo = escogeModulo

    print("username = ", username)
    print("sede= ", sede)
    print("escogeModulo= ", escogeModulo)
    print("documento= ", documento)
    print("nombreSede= ", nombreSede)
    print("profesional= ", profesional)

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(username) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)



    # Fin Combo PermisosGrales
    print("permisosGrales= ", permisosGrales)

    context = {}
    context['PermisosGrales'] = permisosGrales
    context['Documento'] = documento
    context['Username'] = username
    context['Profesional'] = profesional
    context['Sede'] = sede
    context['PermisosGrales'] = permisosGrales
    context['NombreSede'] = nombreSede

    # Combo Accesos usuario

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()

    #comando = "select opc.id id_opc, opc.perfilesClinicaId_id id_perfilesClinica,opc.modulosElementosDefId_id id_elmentosDef, elem_nombre, elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem where usu.estadoReg = 'A' and usu.plantaId_id =  planta.id and planta.documento = '" + str(username) + "' and opc.id = usu.perfilesclinicaOpcionesId_id and elem.id =opc.modulosElementosDefId_id and modelem.id = opc.modulosElementosDefId_id "
    comando = 'select opc.id id_opc, opc."perfilesClinicaId_id" id_perfilesClinica,opc."modulosElementosDefId_id" id_elmentosDef,modulos.nombre nombre_modulo ,elem.nombre nombre_defelemento , elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem , seguridad_perfilesclinica perfcli, seguridad_perfilesgralusu gralusu, seguridad_modulos modulos, sitios_sedesClinica  sedes where gralusu."perfilesClinicaId_id" = perfcli.id and usu."plantaId_id" = gralusu."plantaId_id" and usu."plantaId_id" =  planta.id and usu."estadoReg" = ' + "'" + 'A' + "'" + ' and  opc.id = usu."perfilesClinicaOpcionesId_id" and elem.id =opc."modulosElementosDefId_id" and modulos.id = perfcli."modulosId_id" and elem."modulosId_id" = perfcli."modulosId_id"  and sedes.id = planta."sedesClinica_id"  and planta.documento =  ' + "'" + '19465673' + "'"

    curt.execute(comando)
    print(comando)

    accesosUsuario = []

    for id_opc, id_perfilesClinica, id_elmentosDef, nombre_modulo ,nombre_defelemento, url, nombreElemento  in curt.fetchall():
            accesosUsuario.append({'id_opc': id_opc, 'id_perfilesClinica': id_perfilesClinica,'id_elmentosDef':id_elmentosDef, 'nombre_modulo':nombre_modulo,  'nombre_defelemento':nombre_defelemento, 'url':url,'nombreElemento':nombreElemento} )

    miConexiont.close()
    print(accesosUsuario )

    context['AccesosUsuario '] = accesosUsuario 

    # Fin Accesos usuario

    # aqui la manada de combos organizarlo segun necesidades

    ingresos = []

    # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexionx = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curx = miConexionx.cursor()

    detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and   sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + str(Sede) + '  AND  deptip.id = dep."dependenciasTipo_id" and dep."serviciosSedes_id" = ser.id AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id"'
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id'
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios

    # Combo TiposDOc
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    # tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo EspecialidadesMedicos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(username) + "'"
    curt.execute(comando)
    print(comando)

    especialidadesMedicos = []
    especialidadesMedicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidadesMedicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidadesMedicos)

    context['EspecialidadesMedicos'] = especialidadesMedicos

    # Fin combo EspecialidadesMedicos

    # Combo Medicos
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str('MEDICO') + "'" + ' and med.planta_id = p.id'

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos

    # Fin combo Medicos

    # Combo TiposFolio

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

    curt.execute(comando)
    print(comando)

    tiposFolio = []
    tiposFolio.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposFolio.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposFolio)

    context['TiposFolio'] = tiposFolio

    # Fin combo TiposFolio

    # Combo TiposUsuario

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

    curt.execute(comando)
    print(comando)

    tiposUsuario = []
    # tiposUsuario.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposUsuario.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposUsuario)

    context['TiposUsuario'] = tiposUsuario

    # Fin combo Tipos Usuario

    # Combo TiposDocumento

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

    curt.execute(comando)
    print(comando)

    tiposDocumento = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDocumento.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['TiposDocumento'] = tiposDocumento

    # Fin combo TiposDocumento

    # Combo Centros

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

    curt.execute(comando)
    print(comando)

    centros = []

    for id, nombre in curt.fetchall():
        centros.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['Centros'] = centros

    # Fin combo Centros

    # Combo Diagnosticos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

    curt.execute(comando)
    print(comando)

    diagnosticos = []
    diagnosticos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        diagnosticos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(diagnosticos)

    context['Diagnosticos'] = diagnosticos

    # Fin combo Diagnosticos

    # Combo Departamentos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

    curt.execute(comando)
    print(comando)

    departamentos = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        departamentos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(departamentos)

    context['Departamentos'] = departamentos

    # Fin combo Departamentos

    # Combo Ciudades

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

    curt.execute(comando)
    print(comando)

    ciudades = []

    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)

    context['Ciudades'] = ciudades

    # Fin combo Ciudades

    # Combo Modulos

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

    curt.execute(comando)
    print(comando)

    modulos = []

    for id, nombre, nomenclatura, logo in curt.fetchall():
        modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

    miConexiont.close()
    print(modulos)

    context['Modulos'] = modulos

    # Fin combo Modulos

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
        username) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    context['PermisosGrales'] = permisosGrales

    # Fin Combo PermisosGrales

    # Combo PermisosDetalle

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'"

    curt.execute(comando)
    print(comando)

    permisosDetalle = []

    for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
        permisosDetalle.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
             'nombreElemento': nombreElemento})

    miConexiont.close()
    print(permisosDetalle)

    context['PermisosDetalle'] = permisosDetalle

    # Fin Combo PermisosDetalle

    ## fin manada de combis




   # Aqui ya vienen las validaciones de permisos de acceso
    # Se valida el aaceso al Modulo


    if (escogeModulo == 'ADMISIONES'):
        print ("WENTRE ADMISIONES 4")
        return render(request, "admisiones/panelAdmisiones.html", context)

    if (escogeModulo == 'HISTORIA CLINICA'):
        print ("WENTRE PERMSISO HISTORIA CLINICA")
        return render(request, "clinico/panelClinico.html", context)


    return render(request, "panelVacio.html", context)

    
    
    




def retornarAdmision(request, Sede, Perfil, Username, Username_id, NombreSede):


    print ("Entre Retornar Admision")
    #Sede = request.POST["Sede"]
    print ("Sede = ", Sede)
    Sede = Sede.lstrip()
    sede = Sede
    #Perfil = request.POST["Perfil"]
    print ("Perfil = ",Perfil)
    Perfil = Perfil.lstrip()
    print("Perfil = ", Perfil)

    print ("Nombre dede = ", NombreSede)

    context = {}

    context['Sede'] = Sede
    context['Username'] = Username
    context['Username_id'] = Username_id
    context['NombreSede'] = NombreSede


    # Consigo la sede Nombre

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1

    # esta consulta por que se pierde de otras pantallas

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    ingresos = []

    #miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexionx = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curx = miConexionx.cursor()

    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  WHERE i.sedesClinica_id = dep.sedesClinica_id AND i.sedesClinica_id= '" + str(
        Sede) + "'   AND deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(
        sede) + "' AND sed.servicios_id = ser.id"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios


    # Combo TiposDOc
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo Medicos
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p , planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos
    context['Perfil'] = Perfil

    # Fin combo Medicos

    if (Perfil == 1):
        return render(request, "menuMedico.html", context)
    if (Perfil == 2):
        return render(request, "menuEnfermero.html", context)
    if (Perfil == 3):
        return render(request, "menuAuxiliar.html", context)
    if (Perfil == 4):
        return render(request, "citasMedicas/menuCitasMedicas.html", context)
    if (Perfil == 5):
        return render(request, "facturacion/menuFacturacion.html", context)
    if (Perfil == 6):
        print ("Entre por dende ERA")
        return render(request, "admisiones/panelAdmisiones.html", context)

    return render(request, "admisiones/panelAdmisiones.html", context)


def retornarMen(request, Sede, Username,  Documento, NombreSede, Profesional):

    print("Voy a RETORNAR AL MENU")


    username = Username.strip()

    documento = Documento
    sede = Sede
    nombreSede = NombreSede
    profesional = Profesional
    context = {}
    print(username)


    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    context['Documento'] = username
    context['Username'] = username
    context['Sede'] = sede
    context['NombreSede'] = nombreSede
    context['Profesional'] = profesional


    ## desde aqui cargo ver que borrar arriba

    ingresos = []

    # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexionx = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curx = miConexionx.cursor()


    detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and   sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + str(
        Sede) + '  AND  deptip.id = dep."dependenciasTipo_id" and dep."serviciosSedes_id" = ser.id AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id"'
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id'
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios

    # Combo TiposDOc
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    # tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    # comando = 'SELECT id ,nombre FROM sitios_dependencias where "sedesClinica_id" = ' + "'"  + str(Sede) +"'"  + ' AND "dependenciasTipo_id" = 2'
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(
        Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo EspecialidadesMedicos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(
        username) + "'"
    curt.execute(comando)
    print(comando)

    especialidadesMedicos = []
    especialidadesMedicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidadesMedicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidadesMedicos)

    context['EspecialidadesMedicos'] = especialidadesMedicos

    # Fin combo EspecialidadesMedicos

    # Combo Medicos
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    # comando = 'SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p."sedesClinica_id" = perf."sedesClinica_id" and  perf."sedesClinica_id" = ' + "'"  + str(Sede) + "'" +  ' AND perf."tiposPlanta_id" = 1 and p.id = perf."planta_id"'
    comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(
        Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str(
        'MEDICO') + "'" + ' and med.planta_id = p.id'

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos

    # Fin combo Medicos

    # Combo TiposFolio

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

    curt.execute(comando)
    print(comando)

    tiposFolio = []
    tiposFolio.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposFolio.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposFolio)

    context['TiposFolio'] = tiposFolio

    # Fin combo TiposFolio

    # Combo TiposUsuario

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

    curt.execute(comando)
    print(comando)

    tiposUsuario = []
    # tiposUsuario.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposUsuario.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposUsuario)

    context['TiposUsuario'] = tiposUsuario

    # Fin combo Tipos Usuario

    # Combo TiposDocumento

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

    curt.execute(comando)
    print(comando)

    tiposDocumento = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDocumento.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['TiposDocumento'] = tiposDocumento

    # Fin combo TiposDocumento

    # Combo Centros

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

    curt.execute(comando)
    print(comando)

    centros = []

    for id, nombre in curt.fetchall():
        centros.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['Centros'] = centros

    # Fin combo Centros

    # Combo Diagnosticos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

    curt.execute(comando)
    print(comando)

    diagnosticos = []
    diagnosticos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        diagnosticos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(diagnosticos)

    context['Diagnosticos'] = diagnosticos

    # Fin combo Diagnosticos

    # Combo Departamentos

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

    curt.execute(comando)
    print(comando)

    departamentos = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        departamentos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(departamentos)

    context['Departamentos'] = departamentos

    # Fin combo Departamentos

    # Combo Ciudades

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

    curt.execute(comando)
    print(comando)

    ciudades = []

    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)

    context['Ciudades'] = ciudades

    # Fin combo Ciudades

    # Combo Modulos

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

    curt.execute(comando)
    print(comando)

    modulos = []

    for id, nombre, nomenclatura, logo in curt.fetchall():
        modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

    miConexiont.close()
    print(modulos)

    context['Modulos'] = modulos

    # Fin combo Modulos

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
        username) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    context['PermisosGrales'] = permisosGrales

    # Fin Combo PermisosGrales

    # Combo PermisosDetalle

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()

    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'"

    curt.execute(comando)
    print(comando)

    permisosDetalle = []

    for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
        permisosDetalle.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
             'nombreElemento': nombreElemento})

    miConexiont.close()
    print(permisosDetalle)

    context['PermisosDetalle'] = permisosDetalle

    # Fin Combo PermisosDetalle


    return render(request, "inicio/PantallaPrincipal.html", context)



def validaPassword(request, username, contrasenaAnt,contrasenaNueva,contrasenaNueva2):
    print("Entre ValidaPassword" )
    username = request.POST["username"]
    contrasenaAnt = request.POST["contrasenaAnt"]
    contrasenaNueva = request.POST["contrasenaNueva"]
    contrasenaNueva2 = request.POST["contrasenaNueva2"]

    print(username)
    print(contrasenaAnt)
    print(contrasenaNueva)
    print(contrasenaNueva2)
    context = {}

    if (contrasenaNueva2 != contrasenaNueva):
        dato = "No coinciden las contraseñas ! "
        context['Error'] = "No coincideln las contraseñas ! "
        print(context)

        return HttpResponse(dato)


    #miConexion1 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion1 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur1 = miConexion1.cursor()
    comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
    print(comando)
    cur1.execute(comando)

    UsuariosHc = []

    for documento, contrasena in cur1.fetchall():
        UsuariosHc = {'username': documento, 'contrasena': contrasena}

    miConexion1.close()
    print(UsuariosHc)

    if UsuariosHc == []:

        dato = "Personal invalido ! "
        context['Error'] = "Personal invalido ! "
        print(context)

        return HttpResponse(dato)
        #return render(request, "accesoPrincipal1.html", context)

    else:
        miConexion1 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "' AND contrasena = '" + str(contrasenaAnt) + "'"
        print(comando)
        cur1.execute(comando)

        ContrasenaHc = []
        for documento, contrasena in cur1.fetchall():
            ContrasenaHc = {'username': documento, 'contrasena': contrasena}
        miConexion1.close()

        if ContrasenaHc == []:
            dato = "Contraseña Invalida ! "
            context['Error'] = "Contraseña Invalida ! "
            print(context)

            return HttpResponse(dato)

        else:

            miConexion1 =psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
            cur1 = miConexion1.cursor()
            comando = "UPDATE planta_planta SET contrasena = '" +  str(contrasenaNueva) + "' WHERE documento = '" + str(username) + "'"
            print(comando)
            cur1.execute(comando)
            miConexion1.commit()
            miConexion1.close()
            context['Error'] = "Contraseña Actualizada ! "
            dato = "Contraseña Actualizada !"
            print(context)
            #return HttpResponse(context, safe=False)
            return HttpResponse(dato)
            #return render(request, "accesoPrincipal1.html", context)


    #return JsonResponse(UsuariosHc, safe=False)

def Modal(request, username, password):

        print("Entre a Modal")
        print(username)
        print(password)

        #miConexion1 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexion1 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
        print(comando)
        cur1.execute(comando)

        UsuariosHc = {}

        for documento, contrasena in cur1.fetchall():
            UsuariosHc = {'username': documento, 'contrasena': contrasena}

        miConexion1.close()
        print(UsuariosHc)
        return JsonResponse(UsuariosHc, safe=False)
        # return HttpResponse(UsuariosHc)



def buscarAdmision(request):
    context = {}


    print("Entre Buscar Admision" )
    BusTipoDoc = request.POST["busTipoDoc"]
    BusDocumento = request.POST["busDocumento"]
    BusHabitacion = request.POST["busHabitacion"]



    BusDesde = request.POST["busDesde"]
    BusHasta = request.POST["busHasta"]
    BusEspecialidad = request.POST["busEspecialidad"]
    print ("Especialidad = ", BusEspecialidad )
    BusMedico = request.POST["busMedico"]
    BusServicio = request.POST["busServicio"]
    BusPaciente = request.POST["busPaciente"]
    Perfil = request.POST['Perfil']

    Sede = request.POST["Sede"]
    context['Sede'] = Sede

    # Consigo la sede Nombre

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + Sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1


    Username = request.POST["Username"]
    context['Username'] = Username
    Username_id = request.POST["Username_id"]
    context['Username_id'] = Username_id




    print("Sede  = ", Sede)

    print("BusHabitacion= ", BusHabitacion)
    print("BusTipoDoc=", BusTipoDoc)
    print("BusDocumento=" , BusDocumento)
    print("BusDesde=", BusDesde)
    print("BusHasta=", BusHasta)
    print("La sede es = " , Sede)
    print("El busServicio = ", BusServicio)
    print("El busEspecialidad = ", BusEspecialidad)
    print("El busSMedico = ", BusMedico)
    print("El busSMedico = ", BusPaciente)

    ingresos = []

    # Combo de Servicios
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont =  psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios


    # Combo TiposDOc
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento"
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc


    # Combo Habitaciones
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
    curt.execute(comando)
    print(comando)

    especialidades = []
    especialidades.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidades)

    context['Especialidades'] = especialidades

    # Fin combo Especialidades

    # Combo Medicos
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')

    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos

    # Fin combo Medicos


    # Busco Nombre de Habitacion

    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_dependencias d WHERE d.id = '" + str(BusHabitacion) + "'"
    curt.execute(comando)
    print(comando)

    NombreHabitacion = ""


    for id, nombre in curt.fetchall():
        NombreHabitacion = nombre

    miConexiont.close()
    print("NombreHabitacion = ", NombreHabitacion)


    # Fin busco nombre de habitacion



    #miConexion1 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion1 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur1 = miConexion1.cursor()

    detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.sedesClinica_id= '" + str(Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"


    print(detalle)

    desdeTiempo = BusDesde[11:16]
    hastaTiempo = BusHasta[11:16]
    desdeFecha = BusDesde[0:10]
    hastaFecha = BusHasta[0:10]

    print ("desdeTiempo = ", desdeTiempo)
    print("desdeTiempo = " ,hastaTiempo)

    print (" desde fecha = " , desdeFecha)
    print("hasta "
          " = ", hastaFecha)


    if BusServicio != "":
      detalle = detalle + " AND  ser.id = '" + str(BusServicio) + "'"
    print(detalle)

    if BusDesde != "":
        detalle = detalle +  " AND i.fechaIngreso >= '" + str(desdeFecha) + " " + desdeTiempo + ":00'"
        print (detalle)

    if BusHasta != "":
        detalle = detalle + " AND i.fechaIngreso <=  '" + str(hastaFecha) + " " + hastaTiempo + ":00'"
        print(detalle)

    if BusHabitacion != "":
        detalle = detalle + " AND dep.id = '" + str(BusHabitacion) + "'"
        print(detalle)

    if BusTipoDoc != "":
            detalle = detalle + " AND i.tipoDoc_id= '" + str(BusTipoDoc) + "'"
            print(detalle)

    if BusDocumento != "":
                detalle = detalle + " AND u.documento= '" + str(BusDocumento) + "'"
                print(detalle)

    if BusPaciente != "":
        detalle = detalle + " AND u.nombre like '%" + str(BusPaciente) + "%'"
        print(detalle)

    if BusMedico != "":
        detalle = detalle + " AND i.medicoActual_id = '"  + str(BusMedico) + "'"
        print(detalle)


    if BusEspecialidad != "":
        detalle = detalle + " AND i.dxIngreso_id = '" + str(BusEspecialidad) + "'"
        print(detalle)




    cur1.execute(detalle)



    for tipoDoc, documento_id, nombre , consec, fechaIngreso,  fechaSalida, servicioNombreIng, camaNombreIng, dxActual  in cur1.fetchall():

        ingresos.append ({'tipoDoc' : tipoDoc, 'Documento': documento_id, 'Nombre': nombre , 'Consec': consec, 'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida, 'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng, 'DxActual': dxActual})

    miConexion1.close()
    print(ingresos)
    context['Ingresos'] = ingresos




    return render(request, "admisiones/panelAdmisiones.html", context)

def buscarServicios(request):
    context = {}
    Sede = request.GET["Sede"]
    print("Entre buscar  servicio =", Serv)
    print("Sede = ", Sede)
    # Combo de Servicios

    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                   password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT sed.id id ,sed.nombre nombre FROM  sitios_serviciosSedes sed Where sed."sedesClinica_id" =' + "'" + str(Sede) + "'"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    context['Sede'] = Sede

    return JsonResponse(json.dumps(servicios), safe=False)



def buscarSubServicios(request):
    context = {}
    Serv = request.GET["Serv"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  Subservicios del servicio  =",Serv)
    print ("Sede = ", Sede)

    # Combo de SubServicios
    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont =psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre FROM sitios_serviciosSedes sed ,sitios_subserviciossedes sub Where sed."sedesClinica_id" = ' + "'" + str(Sede) + "'" + '  and sed."sedesClinica_id" = sub."sedesClinica_id" and sed.id = sub."serviciosSedes_id" and sub."serviciosSedes_id" = ' + "'" + str(Serv) + "'"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios


    context['Sede'] = Sede


    return JsonResponse(json.dumps(subServicios), safe=False)



def buscarCiudades(request):
    context = {}
    Departamento = request.GET["Departamento"]

    print ("Entre buscar  Ciudades del Depto  =",Departamento)


    # Combo de Medicos Especialidades


    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_departamentos d, sitios_ciudades c WHERE c.departamentos_id = d.id and d.id = '" + str(Departamento) + "'"

    curt.execute(comando)
    print(comando)

    ciudades = []



    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)


    context['Ciudades'] = ciudades


    return JsonResponse(json.dumps(ciudades), safe=False)




def buscarEspecialidadesMedicos(request):
    context = {}
    Esp = request.GET["Esp"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  Servicio =",Esp)
    print ("Sede = ", Sede)

    # Combo de Medicos Especialidades


    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()


    comando = 'SELECT m.id id, m.nombre nombre from clinico_medicos m, clinico_Especialidadesmedicos medesp,clinico_especialidades esp,sitios_sedesclinica sed,  planta_planta pla where esp.id = ' + "'" + str(Esp) + "'" + ' and esp.id=medesp.especialidades_id and pla."sedesClinica_id" = sed.id and pla.id = medesp.planta_id and pla."sedesClinica_id"=' + "'" + str(Sede) + "'" + ' order by m.nombre'

    curt.execute(comando)
    print(comando)

    medicosEspecialidades = []


    for id, nombre in curt.fetchall():
        medicosEspecialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicosEspecialidades)


    context['MedicosEspecialidades'] = medicosEspecialidades

    context['Sede'] = Sede

    return JsonResponse(json.dumps(medicosEspecialidades), safe=False)



def buscarHabitaciones(request):


    context = {}
    Exc = request.GET["Exc"]
    print ("Excluir = ", Exc)
    Serv = request.GET["Serv"]
    SubServ = request.GET["SubServ"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  servicio =",Serv)
    print("Entre buscar Subservicio =", SubServ)
    print ("Sede = ", Sede)


    # Busco la habitaciones de un Servicio

    #miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()

    if Exc == 'N':

      comando = "SELECT dep.id id ,dep.numero nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub , sitios_dependencias dep  Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and  dep.sedesClinica_id=sed.sedesClinica_id and dep.servicios_id = sub.servicios_id and dep.subServicios_id =sub.id  and dep.subServicios_id = '" +str(SubServ) + "'"

    else:


       comando = 'SELECT dep.id id ,dep.numero nombre   FROM sitios_serviciosSedes sed,  sitios_subserviciossedes sub , sitios_dependencias dep Where sed."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND sed."sedesClinica_id" = sub."sedesClinica_id" and sub."serviciosSedes_id" = sed.id and dep."sedesClinica_id"=sed."sedesClinica_id" and dep."serviciosSedes_id"= sed.id and dep."subServiciosSedes_id" = sub.id and dep."subServiciosSedes_id" = ' + "'" + str(SubServ) + "'"

    curt.execute(comando)
    print(comando)

    Habitaciones =[]




    for id, nombre in curt.fetchall():
        Habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(Habitaciones)
    context['Habitaciones'] = Habitaciones

    context['Sede'] = Sede



    return JsonResponse(json.dumps(Habitaciones), safe=False)



# aqui nuevo codigo cvrear admision DEF


def crearAdmisionDef(request):

    print("Entre a Craer Admision definitiva")

    if request.method == 'POST':
        print("EntrePost Graba Admision Def")
        data = {}
        context = {}


        #sedesClinica = request.POST['sedesClinica']
        sedesClinica = request.POST['Sede']
        Sede = request.POST['Sede']
        context['Sede'] = Sede



        print("Sedes Clinica = ", sedesClinica)
        print ("Sede = ",Sede)


        Username = request.POST["Username"].strip()
        print(" Username = " , Username)
        context['Username'] = Username

        Username_id = request.POST["Username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id



        tipoDoc = request.POST['tipoDoc']
       # documento = request.POST['documento']
        documento = request.POST['busDocumentoSel']
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)
        #extraServicio = request.POST['extraServicio']
       #print("extraServicio = ", extraServicio)

        # Consigo el Id del Paciente Documento

        DocumentoId = Usuarios.objects.get(documento=documento)
        idPacienteFinal = DocumentoId.id

        print("idPacienteFinal", idPacienteFinal)



        consec = Ingresos.objects.all().filter(tipoDoc_id=tipoDoc).filter(documento_id=idPacienteFinal).aggregate(maximo=Coalesce(Max('consec'), 0))
        print("ultimo Ingreso = ", consec)
        consecAdmision = (consec['maximo'] + 1)
        print("ultimo ingreso = ", consecAdmision)

        fechaIngreso = request.POST['fechaIngreso']
        print("fechaIngreso = ", fechaIngreso)

        fechaIngreso = datetime.strptime(fechaIngreso, "%Y-%m-%dT%H:%M")
        print("fechaIngreso3 = ", fechaIngreso)

        fechaSalida = "0001-01-01 00:00:00"

        factura = 0
        numcita = 0
        dependenciasIngreso = request.POST['dependenciasIngreso']
        print("dependenciasIngreso =", dependenciasIngreso)
        #dependenciasActual = dependenciasIngreso
        dependenciasSalida = ""
        dxIngreso = request.POST['dxIngreso']
        print("dxIngreso =", dxIngreso)
        dxActual = dxIngreso
        dxSalida = ""
        estadoSalida = "1"

        medicoIngreso = request.POST['medicoIngreso']
        print("medicoIngreso =", medicoIngreso)
        medicoActual = medicoIngreso
        medicoSalida = ""
        salidaClinica = "N"
        salidaDefinitiva = "N"

        especialidadesMedicos = request.POST['busEspecialidad']

        especialidadesMedicosSalida = ""
        especialidadesMedicosActual = especialidadesMedicos


        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)


        fechaRegistro = fechaIngreso

        estadoReg = "A"
        print("estadoRegistro =", estadoReg)

        data[0] = "Ha ocurrido un error"

        # VAmos a guardar la Admision

        # Consigo ID de Documento

        documento_llave = Usuarios.objects.get(documento=documento)
        print("el id del dopcumento = ", documento_llave.id)

        usernameId = Planta.objects.get(documento=Username)
        print("el id del planta = ", usernameId.id)


        ## Primero creo la dependencia Actual asi :
        # Grabo Dependencia Actual


        grabo = Ingresos(
                         sedesClinica_id=Sede,
                         tipoDoc_id=tipoDoc,
                         documento_id=documento_llave.id,
                         consec=consecAdmision,
                         fechaIngreso=fechaIngreso,
                         fechaSalida=fechaSalida,
                         factura=factura,
                         numcita=numcita,
                         dependenciasIngreso_id=dependenciasIngreso,
                         dxIngreso_id=dxIngreso,
                         medicoIngreso_id=medicoIngreso,
                         especialidadesMedicosIngreso_id=especialidadesMedicos,
                        # dependenciasActual_id=grabo3.id,
                         dxActual_id = dxActual,
                         medicoActual_id=medicoActual,
                         especialidadesMedicosActual_id=especialidadesMedicosActual,
                         dependenciasSalida_id = dependenciasSalida,
                         dxSalida_id = dxSalida,
                         medicoSalida_id=medicoSalida,
                         especialidadesMedicosSalida_id="",
                         estadoSalida_id = estadoSalida,

                         salidaClinica = salidaClinica,
                         salidaDefinitiva=salidaDefinitiva,
                         fechaRegistro=fechaRegistro,
                         usuarioRegistro_id=usernameId.id,
                         estadoReg=estadoReg

        )
        print("Voy a fiu¿guardar la INFO")

        grabo.save()
        print("yA grabe 2", grabo.id)
        grabo.id
        print("yA grabe" , grabo.id)

        # Grabo Dependencia Historico

        print("Voy a guardar HISTORICO dependencias ")

        grabo2 = HistorialDependencias(
            tipoDoc_id=tipoDoc,
            documento_id=documento_llave.id,
            consec=consecAdmision,
            dependencias_id=dependenciasIngreso,
            disponibilidad='O',
            fechaRegistro=fechaRegistro,
            usuarioRegistro_id=usernameId.id,
            fechaLiberacion=null,
            fechaOcupacion=fechaRegistro,
            estadoReg=estadoReg

        )
        grabo2.save()

        print("Grabe HISTPRICO DEPENDENCIAS")

        # RUTINA ARMADO CONTEXT

        ingresos = []

        #miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexionx =  psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        curx = miConexionx.cursor()


        detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  , sitios_serviciosSedes sd WHERE  sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        ## ojo desde aquip


        # Combo PermisosGrales

        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
            username) + "'"

        curt.execute(comando)
        print(comando)

        permisosGrales = []

        for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
            permisosGrales.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
                 'modulo_nombre': modulo_nombre})

        miConexiont.close()
        print(permisosGrales)

        # Fin Combo PermisosGrales
        print("permisosGrales= ", permisosGrales)

        context = {}
        context['PermisosGrales'] = permisosGrales
        context['Documento'] = documento
        context['Username'] = username
        context['Profesional'] = profesional
        context['Sede'] = sede
        context['PermisosGrales'] = permisosGrales
        context['NombreSede'] = nombreSede

        # Combo Accesos usuario

        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        # comando = "select opc.id id_opc, opc.perfilesClinicaId_id id_perfilesClinica,opc.modulosElementosDefId_id id_elmentosDef, elem_nombre, elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem where usu.estadoReg = 'A' and usu.plantaId_id =  planta.id and planta.documento = '" + str(username) + "' and opc.id = usu.perfilesclinicaOpcionesId_id and elem.id =opc.modulosElementosDefId_id and modelem.id = opc.modulosElementosDefId_id "
        comando = 'select opc.id id_opc, opc."perfilesClinicaId_id" id_perfilesClinica,opc."modulosElementosDefId_id" id_elmentosDef,modulos.nombre nombre_modulo ,elem.nombre nombre_defelemento , elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem , seguridad_perfilesclinica perfcli, seguridad_perfilesgralusu gralusu, seguridad_modulos modulos, sitios_sedesClinica  sedes where gralusu."perfilesClinicaId_id" = perfcli.id and usu."plantaId_id" = gralusu."plantaId_id" and usu."plantaId_id" =  planta.id and usu."estadoReg" = ' + "'" + 'A' + "'" + ' and  opc.id = usu."perfilesClinicaOpcionesId_id" and elem.id =opc."modulosElementosDefId_id" and modulos.id = perfcli."modulosId_id" and elem."modulosId_id" = perfcli."modulosId_id"  and sedes.id = planta."sedesClinica_id"  and planta.documento =  ' + "'" + '19465673' + "'"

        curt.execute(comando)
        print(comando)

        accesosUsuario = []

        for id_opc, id_perfilesClinica, id_elmentosDef, nombre_modulo, nombre_defelemento, url, nombreElemento in curt.fetchall():
            accesosUsuario.append(
                {'id_opc': id_opc, 'id_perfilesClinica': id_perfilesClinica, 'id_elmentosDef': id_elmentosDef,
                 'nombre_modulo': nombre_modulo, 'nombre_defelemento': nombre_defelemento, 'url': url,
                 'nombreElemento': nombreElemento})

        miConexiont.close()
        print(accesosUsuario)

        context['AccesosUsuario '] = accesosUsuario

        # Fin Accesos usuario

        # aqui la manada de combos organizarlo segun necesidades

        ingresos = []

        # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexionx = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curx = miConexionx.cursor()
        detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and   sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + str(
            Sede) + '  AND  deptip.id = dep."dependenciasTipo_id" and dep."serviciosSedes_id" = ser.id AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id"'
        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        # Combo de Servicios
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
            sede) + "'" + ' AND sed."servicios_id" = ser.id'
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo de SubServicios
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
            sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
        curt.execute(comando)
        print(comando)

        subServicios = []
        subServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            subServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(subServicios)

        context['SubServicios'] = subServicios

        # Fin combo SubServicios

        # Combo TiposDOc
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        # tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' AND tip.nombre=' + "'" + str(
            'HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
        curt.execute(comando)
        print(comando)

        habitaciones = []
        habitaciones.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            habitaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(habitaciones)

        context['Habitaciones'] = habitaciones

        # Fin combo Habitaciones

        # Combo Especialidades
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        # Combo EspecialidadesMedicos

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()
        comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(
            username) + "'"
        curt.execute(comando)
        print(comando)

        especialidadesMedicos = []
        especialidadesMedicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidadesMedicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidadesMedicos)

        context['EspecialidadesMedicos'] = especialidadesMedicos

        # Fin combo EspecialidadesMedicos

        # Combo Medicos
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str(
            'MEDICO') + "'" + ' and med.planta_id = p.id'

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # Combo TiposFolio

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

        curt.execute(comando)
        print(comando)

        tiposFolio = []
        tiposFolio.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposFolio.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposFolio)

        context['TiposFolio'] = tiposFolio

        # Fin combo TiposFolio

        # Combo TiposUsuario

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

        curt.execute(comando)
        print(comando)

        tiposUsuario = []
        # tiposUsuario.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposUsuario.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposUsuario)

        context['TiposUsuario'] = tiposUsuario

        # Fin combo Tipos Usuario

        # Combo TiposDocumento

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

        curt.execute(comando)
        print(comando)

        tiposDocumento = []
        # tiposDocumento.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDocumento.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['TiposDocumento'] = tiposDocumento

        # Fin combo TiposDocumento

        # Combo Centros

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

        curt.execute(comando)
        print(comando)

        centros = []

        for id, nombre in curt.fetchall():
            centros.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['Centros'] = centros

        # Fin combo Centros

        # Combo Diagnosticos

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

        curt.execute(comando)
        print(comando)

        diagnosticos = []
        diagnosticos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            diagnosticos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(diagnosticos)

        context['Diagnosticos'] = diagnosticos

        # Fin combo Diagnosticos

        # Combo Departamentos

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

        curt.execute(comando)
        print(comando)

        departamentos = []
        # tiposDocumento.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            departamentos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(departamentos)

        context['Departamentos'] = departamentos

        # Fin combo Departamentos

        # Combo Ciudades

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

        curt.execute(comando)
        print(comando)

        ciudades = []

        for id, nombre in curt.fetchall():
            ciudades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(ciudades)

        context['Ciudades'] = ciudades

        # Fin combo Ciudades

        # Combo Modulos

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

        curt.execute(comando)
        print(comando)

        modulos = []

        for id, nombre, nomenclatura, logo in curt.fetchall():
            modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

        miConexiont.close()
        print(modulos)

        context['Modulos'] = modulos

        # Fin combo Modulos

        # Combo PermisosGrales

        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
            username) + "'"

        curt.execute(comando)
        print(comando)

        permisosGrales = []

        for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
            permisosGrales.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
                 'modulo_nombre': modulo_nombre})

        miConexiont.close()
        print(permisosGrales)

        context['PermisosGrales'] = permisosGrales

        # Fin Combo PermisosGrales

        # Combo PermisosDetalle

        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres",
                                       password="pass123")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'"

        curt.execute(comando)
        print(comando)

        permisosDetalle = []

        for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
            permisosDetalle.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
                 'nombreElemento': nombreElemento})

        miConexiont.close()
        print(permisosDetalle)

        context['PermisosDetalle'] = permisosDetalle

        # Fin Combo PermisosDetalle

        # FIN RUTINA ARMADO CONTEXT


    return render(request, "admisiones/panelAdmisiones.html", context)



# fin nuevo mcodigo crear admison DEF



def crearResponsables(request):
    print("Entre crear Responsables")
    pass


def UsuariosModal(request):
        print("Entre a buscar Usuario para la Modal")

        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']

        print ("documento = " , documento)
        print("tipodoc = " ,tipoDoc)



        miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        curt = miConexiont.cursor()
        comando = 'SELECT usu.nombre, usu.documento, usu.genero, usu.departamentos_id, usu.ciudades_id, usu.direccion, usu.telefono, usu.contacto, usu."centrosC_id", usu."tipoDoc_id", usu."tiposUsuario_id" FROM usuarios_usuarios usu WHERE usu."tipoDoc_id" = ' + "'"  + str(tipoDoc) + "'" + ' AND usu.documento = ' + "'" + str(documento) + "'"
        print(comando)
        curt.execute(comando)

        Usuarios = {}

        for nombre, documento, genero, departamentos_id, ciudades_id, direccion, telefono, contacto, centrosc_id, tipoDoc_id, tiposUsuario_id  in curt.fetchall():
            Usuarios = {'nombre': nombre, 'documento': documento, 'genero': genero,'departamento' : departamentos_id, 'ciudad': ciudades_id,  'direccion':  direccion, 'telefono' :telefono, 'contacto': contacto, 'centrosc_id':centrosc_id, 'tipoDoc_id':tipoDoc_id,'tiposUsuario_id':tiposUsuario_id}

        miConexiont.close()
        print(Usuarios)

        if Usuarios == '[]':
            datos = {'Mensaje' : 'Usuario No existe'}
            return JsonResponse(datos, safe=False)
        else:
            return JsonResponse(Usuarios, safe=False)




def guardarUsuariosModal(request):
    print("Entre a grabar Usuarios Modal")
    tipoDoc_id = request.POST["tipoDoc"]

    documento = request.POST["documento"]
    nombre = request.POST["nombre"]
    print("DOCUMENTO = " ,documento)
    print(nombre)
    genero = request.POST["genero"]
    departamento = request.POST["departamentos"]
    ciudad = request.POST["ciudades"]
    print ("departamento = ", departamento)
    print("ciudad = ", ciudad)

    direccion = request.POST["direccion"]
    telefono = request.POST["telefono"]
    contacto = request.POST["contacto"]
    centrosc_id = request.POST["centrosc"]
    tiposUsuario_id = request.POST["tiposUsuario"]
    print("DIRECCION = ", direccion)
    print("telefono = ", telefono)
    print("contacto = ", contacto)
    print("centrosc_id = ", centrosc_id)


    print(documento)
    print(tipoDoc_id)

    #miConexion11 =  MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
    miConexion11 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
    cur11 = miConexion11.cursor()
    comando = 'SELECT usu.id, usu."tipoDoc_id", usu.documento FROM usuarios_usuarios usu WHERE usu."tipoDoc_id" = ' + "'" + str(tipoDoc_id) + "'" + ' AND usu.documento = ' + "'" + str(documento) + "'"

    print(comando)
    cur11.execute(comando)

    Usuarios = []

    for id, tipoDoc_id, documento in cur11.fetchall():
        Usuarios.append({'id': id, 'tipoDoc_id': tipoDoc_id, 'documento': documento})

    miConexion11.close()

    if Usuarios == []:

         print("Entre a crear")
         #miConexion3 = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
         miConexion3 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
         cur3 = miConexion3.cursor()
         comando = 'insert into usuarios_usuarios (nombre, documento, genero, departamentos_id, ciudades_id, direccion, telefono, contacto, "centrosC_id", "tipoDoc_id", "tiposUsuario_id") values (' + "'" + nombre + "'" + ' , ' + "'" + documento + "'" + ', ' + "'" + genero + "'" + '  , ' + "'" + departamento + "'" +  '  , ' + "'" +  ciudad + "'" + '  , ' + "'" +  direccion + "'" + ', ' + "'" + telefono + "'" + ', ' + "'" + contacto + "'" + ', ' + "'" + centrosc_id + "'" +  ', ' + "'" + tipoDoc_id + "'" + ', ' + "'" + tiposUsuario_id + "'" + ')'
         print(comando)
         cur3.execute(comando)
         miConexion3.commit()
         miConexion3.close()
         return HttpResponse("Usuario Creado ! ")
    else:
        print("Entre a actualizar")
        #miConexion3 =  MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulner2able')
        miConexion3 = psycopg2.connect(host="192.168.79.129", database="vulner2", port="5432", user="postgres", password="pass123")
        cur3 = miConexion3.cursor()
        comando = 'update usuarios_usuarios set nombre = ' "'" + str(nombre) +  "'" +  ', direccion  = ' + "'" +  str(direccion) + "'" + ', genero = ' + "'" + str(genero) + "'"  + ', telefono= ' + "'" + str(telefono) + "'" +  ', contacto= ' + "'" +  str(contacto) + "'" +  ', "centrosC_id"= ' + "'" + str(centrosc_id) + "'" + ', "tiposUsuario_id" = ' + "'" + str(tiposUsuario_id) + "'" + ' WHERE "tipoDoc_id" = ' + str(tipoDoc_id) + ' AND documento = ' + "'" + str(documento) + "'"
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()


        miConexion3.close()
        return HttpResponse("Usuario Actualizado ! ")
