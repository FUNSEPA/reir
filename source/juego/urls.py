from django.urls import path
from juego import views as juego_v

urlpatterns = [
    path('colaborador/', juego_v.ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaborador/add/', juego_v.ColaboradorCreateView.as_view(), name='colaborador_add'),
    path('colaborador/<int:pk>/', juego_v.ColaboradorDetailView.as_view(), name='colaborador_detail'),

    path('indicador/', juego_v.IndicadorListView.as_view(), name='indicador_list'),
    path('indicador/add/', juego_v.IndicadorCreateView.as_view(), name='indicador_add'),

    path('rubrica/', juego_v.RubricaListView.as_view(), name='rubrica_list'),
    path('rubrica/add/', juego_v.RubricaCreateView.as_view(), name='rubrica_add'),

    path('punteo/add/', juego_v.PunteoCreateView.as_view(), name='punteo_add'),
    path('punteo/<int:pk>/', juego_v.PunteoDetailView.as_view(), name='punteo_detail'),

    path('equipo/', juego_v.EquipoListView.as_view(), name='equipo_list'),
    path('equipo/<int:pk>/', juego_v.EquipoDetailView.as_view(), name='equipo_detail'),

    path('', juego_v.HomeView.as_view(), name='home'),
]
