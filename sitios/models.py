from django.db import models
from django.utils.timezone import now


from smart_selects.db_fields import GroupedForeignKey
from smart_selects.db_fields import ChainedForeignKey
#from django.db.models import UniqueConstraint

# Create your models here.




class Departamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    departamentoCodigoDian = models.CharField(max_length=15, default ='')
    pais = models.ForeignKey('sitios.Paises', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Ciudades(models.Model):
        id = models.AutoField(primary_key=True)
        departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name = 'ciudades')
        nombre = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
   #     usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre

class SedesClinica(models.Model):
    id = models.AutoField(primary_key=True)

    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                 show_all=False)
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    contacto = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
 #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1,default='A', editable=False)

    def __str__(self):
        return self.nombre




class Centros(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)

        ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                     show_all=False)


        ubicacion = models.CharField(max_length=50, default='')
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
     #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)


        def __str__(self):
                return self.nombre


class DependenciasTipo(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)


        def __str__(self):
             return self.nombre

class ServiciosSedes(models.Model):

    id = models.AutoField(primary_key= True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    servicios = models.ForeignKey('clinico.Servicios', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    class Meta:
        #constraints = [
          #  unique_together(fields=['sedesClinica', 'servicios'], name='Constraint_ServiciosSedes')

           unique_together = ('sedesClinica', 'servicios',)

          #  models.db.UniqueConstraint(fields=['sedesClinica', 'servicios'],
           #                         name='Constraint_ServiciosSedes')
        #]



    def __str__(self):
                return self.nombre


class SubServiciosSedes(models.Model):

    id = models.AutoField(primary_key= True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    serviciosSedes = ChainedForeignKey(ServiciosSedes, chained_field='sedesClinica', chained_model_field='sedesClinica',
                                  show_all=False)
    subServiciosSedes = models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    class Meta:
        unique_together = ('sedesClinica', 'serviciosSedes','subServiciosSedes',)
        #constraints = [
         #   models.UniqueConstraint(fields=['sedesClinica', 'servicios','subServicios'], name='Constraint_SubServiciosSedes')
        #]



    def __str__(self):
             return self.nombre


class Dependencias(models.Model):
    LIBRE = 'L'
    OCUPADA = 'O'
    TIPO_CHOICES = (
        (LIBRE, 'LIBRE'),
        (OCUPADA, 'OCUPADA'),
       # (DESINFECCION, 'DESINFECCION'),
    )
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    dependenciasTipo= models.ForeignKey('sitios.DependenciasTipo', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    serviciosSedes = models.ForeignKey('sitios.ServiciosSedes', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name ='serviciosSedes1')
    #servicios = ChainedForeignKey(ServiciosSedes, chained_field='serviciosSedes', chained_model_field='serviciosSedes',  show_all=False, related_name="dos")
    #subServicios = ChainedForeignKey(ServiciosSedes, chained_field='servicios', chained_model_field='servicios', show_all=False)
    subServiciosSedes = models.ForeignKey('sitios.SubServiciosSedes', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    numero =  models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoDepAct')
    consec = models.IntegerField()
    fechaOcupacion = models.DateTimeField(default=now, editable=True)
    fechaLiberacion = models.DateTimeField(default=now, editable=True)
    disponibilidad = models.CharField(max_length=1, default='L', choices=TIPO_CHOICES, )
    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    #class Meta:

    #  unique_together = ('sedesClinica', 'serviciosSedes', 'subServicios','numero','dependenciasTipo')

       #constraints = [
        #   models.UniqueConstraint(fields=[ 'sedesClinica', 'serviciosSedes','servicios','subServicios','numero','dependenciasTipo'], name='Constraint_dependencias')
       # ]

    def __str__(self):
        return self.nombre


class HistorialDependencias(models.Model):
    LIBRE = 'L'
    OCUPADA = 'O'
    TIPO_CHOICES = (
        (LIBRE, 'LIBRE'),
        (OCUPADA, 'OCUPADA'),
    )

    id = models.AutoField(primary_key=True)
    dependencias = models.ForeignKey('sitios.Dependencias', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True,null= True, editable=True, on_delete=models.PROTECT,
                                  related_name='DocumentohistorialDep')

    consec	= models.IntegerField()
    fechaOcupacion = models.DateTimeField(default=now, editable=True)
    fechaLiberacion = models.DateTimeField(default=now, editable=True)
    disponibilidad = models.CharField(max_length=1, default='L', choices=TIPO_CHOICES, )
    fechaRegistro = models.DateTimeField(default=now, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)



class Municipios(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    municipioCodigoDian = models.CharField(max_length=15 , default ='')
    departamento = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre



class Paises(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    paisCodigoDian = models.CharField(max_length=15 , default ='')
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Localidades(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    localidadCodigoDian = models.CharField(max_length=15 , default ='')
    municipio = models.ForeignKey('sitios.Municipios', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre