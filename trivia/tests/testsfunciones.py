import unittest
from unittest.mock import patch
from itertools import chain

from functions import (
    generar_preguntas_random,
    generar_opciones,
    mezclar_opciones,
    calcular_puntaje,
    mostrar_pregunta,
    verificar_respuesta,
    procesar_pregunta,
    ejecutar_ronda,
)

class TestTrivia(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo para preguntas
        self.preguntas = [
            ("Ciencia", "¿Cuál es el planeta más cercano al Sol?", "Mercurio"),
            ("Ciencia", "¿Cuál es el elemento químico del oro?", "Oro"),
            ("Historia", "¿Quién descubrió América?", "Cristóbal Colón"),
            ("Historia", "¿En qué año cayó el Imperio Romano?", "476"),
            ("Ciencia", "¿Qué gas respiramos principalmente?", "Oxígeno"),
        ]

    @patch('random.sample')
    def test_generar_preguntas_random(self, mock_sample):
        mock_sample.return_value = [self.preguntas[0], self.preguntas[2]]
        generador = generar_preguntas_random(self.preguntas, 2)
        preguntas_generadas = list(generador)
        self.assertEqual(len(preguntas_generadas), 2)
        self.assertEqual(preguntas_generadas[0], self.preguntas[0])
        self.assertEqual(preguntas_generadas[1], self.preguntas[2])

    @patch('random.sample')
    def test_generar_opciones(self, mock_sample):
        mock_sample.side_effect = lambda x, y: x[:y]  # Simular el comportamiento de random.sample
        pregunta_actual = self.preguntas[0]
        opciones = generar_opciones(self.preguntas, pregunta_actual)
        self.assertIn("Mercurio", opciones)  # Respuesta correcta
        self.assertEqual(len(opciones), 3)

    @patch('random.shuffle')
    def test_mezclar_opciones(self, mock_shuffle):
        mock_shuffle.side_effect = lambda x: x  # No mezclar realmente
        opciones = mezclar_opciones(self.preguntas[:3])
        self.assertEqual(opciones, self.preguntas[:3])

    def test_calcular_puntaje(self):
        self.assertEqual(calcular_puntaje(5), 50)
        self.assertEqual(calcular_puntaje(0), 0)

    @patch('builtins.input', return_value='1')
    def test_mostrar_pregunta(self, mock_input):
        pregunta = self.preguntas[0]
        opciones = ["Mercurio", "Venus", "Marte"]
        respuesta = mostrar_pregunta(pregunta, opciones)
        self.assertEqual(respuesta, '1')

    def test_verificar_respuesta_correcta(self):
        pregunta = self.preguntas[0]
        opciones = ["Mercurio", "Venus", "Marte"]
        resultado, log = verificar_respuesta(pregunta, 1, opciones)
        self.assertEqual(resultado, 1)
        self.assertIn("¡Correcto!", log)

    def test_verificar_respuesta_incorrecta(self):
        pregunta = self.preguntas[0]
        opciones = ["Venus", "Marte", "Júpiter"]
        resultado, log = verificar_respuesta(pregunta, 1, opciones)
        self.assertEqual(resultado, 0)
        self.assertIn("Incorrecto", log)

    @patch('random.sample')
    @patch('random.shuffle')
    @patch('builtins.input', return_value='1')
    def test_ejecutar_ronda(self, mock_input, mock_shuffle, mock_sample):
        mock_sample.side_effect = lambda x, y: x[:y]  # Simular random.sample
        mock_shuffle.side_effect = lambda x: x  # No mezclar realmente

        preguntas = [self.preguntas[0], self.preguntas[1]]
        opciones = [["Mercurio", "Venus", "Marte"], ["Oro", "Plata", "Hierro"]]
        respuestas_usuario = [1, 1]

        logs = ejecutar_ronda(preguntas, opciones, respuestas_usuario)
        self.assertIn("¡Correcto!", logs[0])
        self.assertIn("Resultado final: 20", logs[1])

if __name__ == '__main__':
    unittest.main()
