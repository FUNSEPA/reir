from django import forms
from django.contrib.auth.models import User
from juego import models as juego_m


class RubricaForm(forms.ModelForm):
    class Meta:
        model = juego_m.Rubrica
        fields = '__all__'


class PunteoForm(forms.ModelForm):
    # colaborador = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = juego_m.Punteo
        fields = '__all__'
        exclude = ('entregado_por', 'porcentaje',)

    def __init__(self, *args, **kwargs):
        super(PunteoForm, self).__init__(*args, **kwargs)
        self.fields['rubrica'].label_from_instance = lambda obj: '{} - Semana {}'.format(
            obj.indicador.nombre,
            obj.semana.numero)
