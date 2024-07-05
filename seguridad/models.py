from django.db import models

# Create your models here.
import planta
import sitios.models
from sitios.models import SedesClinica

#from planta.models import Planta

class Modulos(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    nomenclatura = models.CharField(max_length=20)
    logo = models.CharField(max_length=120, default='', unique=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

class ModulosElementos(models.Model):

        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=20)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre


class ModulosElementosDef(models.Model):

        id = models.AutoField(primary_key=True)
        modulosId = models.ForeignKey('Modulos', default=1, on_delete=models.PROTECT, null=True)
        modulosElementosId = models.ForeignKey('ModulosElementos', default=1, on_delete=models.PROTECT, null=True)
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)
        url =  models.CharField(max_length=50)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre


class Perfiles (models.Model):
        id  = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre

class PerfilesOpciones(models.Model):

        id  = models.AutoField(primary_key=True)
        perfilesId = models.ForeignKey('Perfiles', default=1, on_delete=models.PROTECT, null=True)
        modulosElementosDefId = models.ForeignKey('ModulosElementosDef', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.estadoReg


class PerfilesClinica(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        modulosId = models.ForeignKey('Modulos', default=1, on_delete=models.PROTECT, null=True)
        #sedesClinicaId = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
        sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True, related_name='SedesClinicaSeguridad')
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre

class PerfilesClinicaOpciones(models.Model):
        id = models.AutoField(primary_key=True)
        perfilesClinicaId = models.ForeignKey('PerfilesClinica', default=1, on_delete=models.PROTECT, null=True)
        modulosElementosDefId = models.ForeignKey('ModulosElementosDef', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return (str(self.perfilesClinicaId) + str(' ') + str(self.modulosElementosDefId))


class PerfilesUsu(models.Model):
    SI = 'S'
    NO = 'N'
    TIPO_CHOICES = (
        (SI, 'Si'),
        (NO, 'No'),
    )
    id = models.AutoField(primary_key=True)
    plantaId = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    perfilesClinicaOpcionesId = models.ForeignKey('PerfilesClinicaOpciones', default=1, on_delete=models.PROTECT, null=True)
    adicion = models.CharField(max_length=1, default='S', editable=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return str(self.perfilesClinicaOpcionesId)

class PerfilesGralUsu(models.Model):

        id = models.AutoField(primary_key=True)
        plantaId = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
        perfilesClinicaId = models.ForeignKey('PerfilesClinica', default=1, on_delete=models.PROTECT,
                                                      null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return str(self.perfilesClinicaId)