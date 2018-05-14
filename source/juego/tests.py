from django.test import TestCase
from juego import models as juego_m


class SemanaTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.semana = juego_m.Semana.objects.first()

    def test_puntos_colaborador(self):
        qs = self.semana.puntos_colaborador().values('first_name', 'puntos')
        liza = qs.first()
        self.assertEqual(liza['first_name'], 'Liza')

        resultado_esperado = round(2.5 / 5 * 100, 2)
        self.assertEqual(liza['puntos'], resultado_esperado)

    def test_puntos_colaborador_indicador(self):
        indicador = juego_m.Indicador.objects.first()
        qs = self.semana.puntos_colaborador(indicador=indicador).values('first_name', 'puntos')
        liza = qs.first()
        self.assertEqual(liza['first_name'], 'Liza')

        resultado_esperado = round(3 / 5 * 100, 2)
        self.assertEqual(liza['puntos'], resultado_esperado)

    def test_puntos_equipo(self):
        qs = self.semana.puntos_equipo().values('nombre_corto', 'puntos')
        tpe = qs.first()
        self.assertEqual(tpe['nombre_corto'], 'TPE')

        resultado_esperado = round(2 / 5 * 100, 2)
        self.assertEqual(tpe['puntos'], resultado_esperado)

    def test_puntos_equipo_indicador(self):
        indicador = juego_m.Indicador.objects.first()
        qs = self.semana.puntos_equipo(indicador=indicador).values('nombre_corto', 'puntos')
        tpe = qs.first()
        self.assertEqual(tpe['nombre_corto'], 'TPE')

        resultado_esperado = round(2.5 / 5 * 100, 2)
        self.assertEqual(tpe['puntos'], resultado_esperado)


class CompetenciaTest(TestCase):
    """Test del modelo :class:`Competencia`"""

    fixtures = ['test.json']

    def setUp(self):
        self.competencia = juego_m.Competencia.objects.first()

    def test_puntos_equipo(self):
        semanas = self.competencia.puntos_equipo().values()
        tpe = semanas.first()
        self.assertEqual(tpe['nombre_corto'], 'TPE')

        resultado_esperado = round(2.625 / 5 * 100, 2)
        self.assertEqual(tpe['puntos'], resultado_esperado)

    def test_puntos_colaborador(self):
        qs = self.competencia.puntos_colaborador().values()
        liza = qs.first()
        self.assertEqual(liza['first_name'], 'Liza')

        resultado_esperado = round(2.75 / 5 * 100, 2)
        self.assertEqual(liza['puntos'], resultado_esperado)

    # def test_puntos_indicador(self):
    #     indicadores = self.competencia.puntos_indicador().values()
    #     puntualidad = indicadores.first()
    #     self.assertEqual(puntualidad['nombre'], 'Puntualidad')


class IndicadorTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.indicador = juego_m.Indicador.objects.first()
        self.competencia = juego_m.Competencia.objects.first()

    def test_semana(self):
        semanas = self.indicador.puntos_semana(self.competencia).values()
        uno = semanas.get(id=2)
        self.assertEqual(uno['numero'], 2)

        resultado_esperado = round(3.5 / 5 * 100, 2)
        self.assertEqual(uno['puntos'], resultado_esperado)
