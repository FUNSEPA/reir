from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin

from juego import models as juego_m
from juego import forms as juego_f


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['competencia'] = juego_m.Competencia.objects.get(
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now())
        context['equipos'] = juego_m.Departamento.objects.all()
        context['indicadores'] = []
        context['equipos_chart'] = []
        for equipo in context['equipos']:
            lista_e = []
            for i in juego_m.Indicador.objects.filter(departamento=equipo):
                puntos = context['competencia'].puntos_equipo(indicador=i).filter(id=equipo.id).first().puntos
                lista_e.append({
                    'indicador': i.nombre,
                    'puntos': puntos})
            context['equipos_chart'].append({'nombre': equipo.nombre_corto, 'id': equipo.id, 'datos': lista_e})
        return context


class ColaboradorListView(LoginRequiredMixin, ListView):
    model = juego_m.Colaborador
    template_name = 'juego/colaborador_list.html'

    def get_queryset(self):
        return self.model.objects.filter(coordinador=False)


class ColaboradorDetailView(LoginRequiredMixin, DetailView):
    model = juego_m.Colaborador
    template_name = 'juego/colaborador_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ColaboradorDetailView, self).get_context_data(**kwargs)
        competencia = juego_m.Competencia.objects.get(
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now())
        try:
            context['puntos'] = competencia.puntos_colaborador().get(id=self.object.id).puntos
            semanas = competencia.semanas.all().order_by('numero')
            context['semanas'] = [s.puntos_colaborador().filter(id=self.object.id).values('puntos').first() for s in semanas]
        except:
            context['semanas'] = competencia.semanas.all()
        return context


class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = juego_m.Colaborador
    template_name = 'juego/colaborador_form.html'
    fields = ('first_name', 'last_name', 'departamento', 'coordinador', 'username', 'password')


class IndicadorCreateView(LoginRequiredMixin, CreateView):
    model = juego_m.Indicador
    template_name = 'juego/indicador_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('indicador_list')


class IndicadorListView(LoginRequiredMixin, ListView):
    model = juego_m.Indicador
    template_name = 'juego/indicador_list.html'


class RubricaCreateView(LoginRequiredMixin, CreateView):
    model = juego_m.Rubrica
    template_name = 'juego/rubrica_add.html'
    form_class = juego_f.RubricaForm

    def get_success_url(self):
        return reverse_lazy('rubrica_list')


class RubricaListView(LoginRequiredMixin, ListView):
    model = juego_m.Rubrica
    template_name = 'juego/rubrica_list.html'


class PunteoCreateView(LoginRequiredMixin, CreateView):
    model = juego_m.Punteo
    template_name = 'juego/punteo_add.html'
    form_class = juego_f.PunteoForm

    def get_form_class(self):
        return self.form_class

    def get_form(self, *args, **kwargs):
        form = super(PunteoCreateView, self).get_form(*args, **kwargs)
        qs_colaborador = form.fields['colaborador'].queryset
        qs_rubrica = form.fields['rubrica'].queryset

        form.fields['colaborador'].queryset = qs_colaborador.filter(
            departamento=self.request.user.colaborador.departamento,
            coordinador=False)
        form.fields['rubrica'].queryset = qs_rubrica.filter(
            indicador__departamento=self.request.user.colaborador.departamento)
        return form

    def form_valid(self, form):
        form.instance.entregado_por = self.request.user.colaborador
        return super(PunteoCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.colaborador.get_absolute_url()


class PunteoDetailView(LoginRequiredMixin, DetailView):
    model = juego_m.Punteo
    template_name = 'juego/punteo_detail.html'


class EquipoDetailView(LoginRequiredMixin, DetailView):
    model = juego_m.Departamento
    template_name = 'juego/equipo_detail.html'


class EquipoListView(LoginRequiredMixin, ListView):
    model = juego_m.Departamento
    template_name = 'juego/equipo_list.html'
