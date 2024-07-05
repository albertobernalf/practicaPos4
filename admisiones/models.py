from django.db import models
from django.utils.timezone import now

# Create your models here.

class Ingresos(models.Model):

    id           = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica')
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento')
    hClinica = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    consec    = models.IntegerField()
    fechaIngreso = models.DateTimeField( editable=True, null=True, blank=True)
    fechaSalida = models.DateTimeField(editable=True, null=True, blank=True)
    factura  = models.IntegerField(default=0)
    numcita  =  models.IntegerField(default=0)
    #serviciosIng = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id9')
    dependenciasIngreso = models.ForeignKey('sitios.Dependencias', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id0')
    dxIngreso = models.ForeignKey('clinico.Diagnosticos', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id3')
    medicoIngreso  =  models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id6')

    especialidadesMedicosIngreso =  models.ForeignKey('clinico.Especialidades', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='EspIng')

    #serviciosActual = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id10')
    dependenciasActual = models.ForeignKey('sitios.Dependencias', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    dxActual = models.ForeignKey('clinico.Diagnosticos', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id4')
    medicoActual =  models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id7')
    especialidadesMedicosActual = models.ForeignKey('clinico.Especialidades', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='EspAct')
    estadoSalida  = models.ForeignKey('clinico.EstadosSalida', blank=True,null= True, editable=True, on_delete=models.PROTECT)
   # serviciosSalida  = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id11')
    dependenciasSalida = models.ForeignKey('sitios.Dependencias', blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='id2')
    dxSalida = models.ForeignKey('clinico.Diagnosticos', blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='id5')
    medicoSalida =  models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='id8')
    especialidadesMedicosSalida = models.ForeignKey('clinico.Especialidades', blank=True,null= True, editable=True,  on_delete=models.PROTECT, related_name='EspSal')
    salidaClinica = models.CharField(max_length=1,default='N')

    salidaDefinitiva =  models.CharField(max_length=1,default='N')
    salidaMotivo = models.ForeignKey('clinico.TiposSalidas', blank=True,null= True, editable=True,  on_delete=models.PROTECT, related_name='EspSal')

    ViasIngreso  = models.ForeignKey('clinico.ViasIngreso', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    causasExterna = models.ForeignKey('clinico.CausasExterna', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    regimen = models.ForeignKey('clinico.Regimenes', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposCotizante =  models.ForeignKey('clinico.TiposCotizante', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    # supongo  tabla - ContratosPaciente(id, tipoDoc, documento, contrato, vigencia_desde, vigencia_hasta)
    # ContratosPacienteAdmisiones(id, tipoDoc, documento, contrato, consec)
    ViasEgreso = models.ForeignKey('clinico.ViasEgreso', blank=True, null=True, editable=True, on_delete=models.PROTECT)

    muerte =  models.CharField(max_length=1,default='N')
    fechaMuerte = models.DateTimeField(editable=True, null=True, blank=True)
    ActaDefuncion =  models.CharField(max_length=30,default='')
    medicoDefuncion = models.ForeignKey('clinico.Medicos', blank=True,null= True, editable=True, on_delete=models.PROTECT)

    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)



