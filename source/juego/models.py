from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Departamento(models.Model):
    COLOR_CHOICES = (
        ('info', 'azul'),
        ('success', 'verde'),
        ('warning', 'amarillo'),
        ('danger', 'rojo'),
        ('primary', 'morado'),)

    ICONOS_CHOICES = (
        ('desktop_windows', 'PC'),
        ('layers', 'CAPAS'),
        ('local_library', 'CAPACITACIÓN'),
        ('map', 'MAPA'),
        ('apps', 'APPS'),
        ('sms', 'MENSAJE'),)

    nombre = models.CharField(max_length=50)
    nombre_corto = models.CharField(max_length=5)
    color = models.CharField(max_length=20, default='primary', choices=COLOR_CHOICES)
    icono = models.CharField(max_length=20, default='apps', choices=ICONOS_CHOICES)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre_corto

    def get_absolute_url(self):
        return reverse_lazy('equipo_detail', kwargs={'pk': self.id})


class Colaborador(User):
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='colaboradores')
    coordinador = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradors"

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse_lazy('colaborador_detail', kwargs={'pk': self.id})

    def puntos_actual(self):
        puntuaciones = self.puntuaciones.count()
        if puntuaciones > 0:
            return round(sum(p.porcentaje for p in self.puntuaciones.all()) / puntuaciones, 2)
        return 0


class Valor(models.Model):
    nombre = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Valor"
        verbose_name_plural = "Valors"

    def __str__(self):
        return self.nombre


class Indicador(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='indicadores')
    valor = models.ForeignKey(Valor, on_delete=models.CASCADE, related_name='indicadores')

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

    def __str__(self):
        return '{} - {}'.format(self.departamento.nombre_corto, self.nombre)

    def puntos_semana(self, competencia=None):
        qs_semana = Semana.objects.all()
        if competencia:
            qs_semana = qs_semana.filter(competencia=competencia)
        qs_semana = qs_semana.annotate(
            puntos=models.Avg(
                'rubricas__punteos__porcentaje',
                filter=models.Q(rubricas__indicador=self))
            )
        return qs_semana


class Competencia(models.Model):
    valor = models.ForeignKey(Valor, on_delete=models.PROTECT, related_name='competencias')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name = "Competencia"
        verbose_name_plural = "Competencias"

    def __str__(self):
        return str(self.valor)

    def puntos_indicador(self, semana=None):
        qs_indicador = self.indicadores.all()
        qs_indicador.annotate(
            models.Avg(
                'puntuaciones__porcentaje',
                output_field=models.DecimalField(max_digits=5, decimal_places=2)
                )
            )
        return qs_indicador

    def puntos_colaborador(self, indicador=None):
        qs_colaborador = Colaborador.objects.filter(
            coordinador=False,
            puntuaciones__rubrica__semana__competencia=self)

        filtros = {}
        if indicador:
            filtros['puntuaciones__rubrica__indicador'] = indicador
            qs_colaborador = qs_colaborador.annotate(
                puntos=models.Avg(
                    'puntuaciones__porcentaje',
                    output_field=models.DecimalField(max_digits=5, decimal_places=2)
                    ),
                filter=models.Q(**filtros)
                )
        else:
            qs_colaborador = qs_colaborador.annotate(
                puntos=models.Avg(
                    'puntuaciones__porcentaje',
                    output_field=models.DecimalField(max_digits=5, decimal_places=2)
                    )
                )
        return qs_colaborador

    def puntos_equipo(self, indicador=None):
        qs_departamento = Departamento.objects.filter(
            colaboradores__puntuaciones__rubrica__semana__competencia=self)

        filtros = {}
        if indicador:
            filtros['colaboradores__puntuaciones__rubrica__indicador'] = indicador
            qs_departamento = qs_departamento.annotate(
                puntos=models.Avg(
                    'colaboradores__puntuaciones__porcentaje',
                    output_field=models.DecimalField(max_digits=5, decimal_places=2),
                    filter=models.Q(**filtros)
                    )
                )
        else:
            qs_departamento = qs_departamento.annotate(
                puntos=models.Avg(
                    'colaboradores__puntuaciones__porcentaje',
                    output_field=models.DecimalField(max_digits=5, decimal_places=2)
                    )
                )
        return qs_departamento


class Semana(models.Model):
    numero = models.PositiveIntegerField()
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, related_name='semanas')

    class Meta:
        verbose_name = "Semana"
        verbose_name_plural = "Semanas"

    def __str__(self):
        return '{} - {}'.format(self.competencia.valor, self.numero)

    def puntos_colaborador(self, indicador=None):
        qs_colaborador = Colaborador.objects.filter(
            coordinador=False,
            puntuaciones__rubrica__semana=self)

        filtros = {}
        if indicador:
            filtros['puntuaciones__rubrica__indicador'] = indicador
            qs_colaborador = qs_colaborador.annotate(
                puntos=models.Avg(
                    'puntuaciones__porcentaje',
                    output_field=models.DecimalField(max_digits=5, decimal_places=2)
                    ),
                filter=models.Q(**filtros))
        else:
            qs_colaborador = qs_colaborador.annotate(
                puntos=models.Avg('puntuaciones__porcentaje'))
        return qs_colaborador

    def puntos_equipo(self, indicador=None):
        filtros = {}

        qs_departamento = Departamento.objects.filter(
            colaboradores__puntuaciones__rubrica__semana=self)

        if indicador:
            filtros['colaboradores__puntuaciones__rubrica__indicador'] = indicador
            qs_departamento = qs_departamento.annotate(
                puntos=models.Avg(
                    'colaboradores__puntuaciones__porcentaje',
                    filter=models.Q(**filtros)))
        else:
            qs_departamento = qs_departamento.annotate(
                puntos=models.Avg('colaboradores__puntuaciones__porcentaje'))
        return qs_departamento


class Rubrica(models.Model):
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='rubricas')
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE, related_name='rubricas')

    class Meta:
        verbose_name = "Rubrica"
        verbose_name_plural = "Rubricas"
        unique_together = ('indicador', 'semana')

    def __str__(self):
        return '{} - {}'.format(self.indicador, self.semana)


class Punteo(models.Model):
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='puntuaciones')
    entregado_por = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name='asignaciones')
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE, related_name='punteos')
    punteo = models.PositiveIntegerField()
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    justificacion = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Punteo"
        verbose_name_plural = "Punteos"
        unique_together = ('colaborador', 'rubrica',)

    def __str__(self):
        return '{} - {}'.format(self.colaborador, self.rubrica)

    def save(self, *args, **kwargs):
        self.porcentaje = self.punteo / 5 * 100
        super(Punteo, self).save(*args, **kwargs)
