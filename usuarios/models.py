from django.db import models
from django.utils.timezone import now
from smart_selects.db_fields import ChainedForeignKey
from sitios.models import Departamentos, Ciudades
from basicas.models import EstadoCivil


# Create your models here.


class TiposDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    abreviatura= models.CharField(max_length=2)
    nombre = models.CharField(max_length=50)
    tiposDocCodigoDian = models.CharField(max_length=15, default='')
    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __str__(self):
        return self.nombre

class TiposUsuario(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
 #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __str__(self):
        return self.nombre

class Usuarios(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    TIPO_CHOICES= (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )
    id = models.AutoField(primary_key=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #documento =  models.IntegerField(unique=True)
    documento = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=TIPO_CHOICES,)
    centrosC = models.ForeignKey('sitios.Centros', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    tiposUsuario = models.ForeignKey('usuarios.TiposUsuario', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    correo = models.EmailField()
    fechaNacio = models.DateTimeField(default=now, editable=False)
    pais = models.ForeignKey('sitios.Paises', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    municipio = models.ForeignKey('sitios.Municipios', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    localidad = models.ForeignKey('sitios.Localidades', blank=True, null=True, editable=True, on_delete=models.PROTECT)

    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',  show_all=False)

    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    contacto  = models.CharField(max_length=50)
    estadoCivil = models.ForeignKey('basicas.EstadoCivil', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ocupacion = models.ForeignKey('basicas.Ocupaciones', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to="fotos", null=True)

    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class UsuariosContacto(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    TIPO_CHOICES= (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )
    id = models.AutoField(primary_key=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT ,related_name ='tipoDoc0')
    documento = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=TIPO_CHOICES,)
    fechaNacio = models.DateTimeField(default=now, editable=False)
    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',  show_all=False)
    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    correo = models.EmailField()
    tipoDocPaciente= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT ,related_name ='tipoDoc1')
    documentoPaciente = models.ForeignKey('usuarios.Usuarios', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    consecPaciente    = models.IntegerField()
    tiposFamilia= models.ForeignKey('basicas.TiposFamilia', blank=True,null= True, editable=True, on_delete=models.PROTECT)

    tiposContacto = models.ForeignKey('basicas.TiposContacto', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

