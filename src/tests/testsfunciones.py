import unittest
from unittest.mock import patch
from itertools import chain

import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trivia.functionss import generar_preguntas_random, generar_opciones, mezclar_opciones, calcular_puntaje, mostrar_pregunta, verificar_respuesta, procesar_pregunta, ejecutar_ronda


class TestTrivia(unittest.TestCase):
    """
    Clase de pruebas unitarias para las funciones del módulo 'trivia.functionss'.
    Utiliza unittest y unittest.mock para verificar el comportamiento de funciones
    relacionadas con la lógica del juego de trivia.
    """

    def setUp(self):
        """
        Configura los datos de ejemplo para las pruebas unitarias.
        """
       
        self.preguntas = [
            ("Ciencia", "¿Cuál es el planeta más cercano al Sol?", "Mercurio"),
            ("Ciencia", "¿Cuál es el elemento químico del oro?", "Oro"),
            ("Historia", "¿Quién descubrió América?", "Cristóbal Colón"),
            ("Historia", "¿En qué año cayó el Imperio Romano?", "476"),
            ("Ciencia", "¿Qué gas respiramos principalmente?", "Oxígeno"),
        ]

    @patch('random.sample')
    def test_generar_preguntas_random(self, mock_sample):
        """
        Prueba la función `generar_preguntas_random`.

        1. Simula el comportamiento de `random.sample` para devolver un conjunto fijo de preguntas.
        2. Verifica que la función `generar_preguntas_random` devuelva el número correcto de preguntas.
        3. Comprueba que las preguntas generadas coincidan con las esperadas.
        """

        mock_sample.return_value = [self.preguntas[0], self.preguntas[2]]
        generador = generar_preguntas_random(self.preguntas, 2)
        preguntas_generadas = list(generador)
        self.assertEqual(len(preguntas_generadas), 2)
        self.assertEqual(preguntas_generadas[0], self.preguntas[0])
        self.assertEqual(preguntas_generadas[1], self.preguntas[2])

    @patch('random.sample')
    def test_generar_opciones(self, mock_sample):
        """
        Prueba la función `generar_opciones`.

        1. Simula el comportamiento de `random.sample` para devolver un subconjunto fijo de opciones.
        2. Verifica que la función `generar_opciones` incluya la respuesta correcta en las opciones.
        3. Comprueba que el número de opciones generadas sea correcto.
        """

        mock_sample.side_effect = lambda x, y: x[:y]  # Simular el comportamiento de random.sample
        pregunta_actual = self.preguntas[0]
        opciones = generar_opciones(self.preguntas, pregunta_actual)
        self.assertIn("Mercurio", opciones)  # Respuesta correcta
        self.assertEqual(len(opciones), 3)

    @patch('random.shuffle')
    def test_mezclar_opciones(self, mock_shuffle):
        """
        Prueba la función `mezclar_opciones`.

        1. Simula el comportamiento de `random.shuffle` para no mezclar realmente las opciones.
        2. Verifica que la función `mezclar_opciones` devuelva las opciones en el mismo orden proporcionado.
        """

        mock_shuffle.side_effect = lambda x: x  # No mezclar realmente
        opciones = mezclar_opciones(self.preguntas[:3])
        self.assertEqual(opciones, self.preguntas[:3])

    def test_calcular_puntaje(self):
        """
        Prueba la función `calcular_puntaje`.

        1. Verifica que el cálculo del puntaje sea correcto para un número dado de respuestas correctas.
        """

        self.assertEqual(calcular_puntaje(5), 50)
        self.assertEqual(calcular_puntaje(0), 0)

    @patch('builtins.input', return_value='1')
    def test_mostrar_pregunta(self, mock_input):
        """
        Prueba la función `mostrar_pregunta`.

        1. Simula la entrada del usuario para seleccionar una opción.
        2. Verifica que la función `mostrar_pregunta` devuelva la respuesta correcta basada en la selección del usuario.
        """

        pregunta = self.preguntas[0]
        opciones = ["Mercurio", "Venus", "Marte"]
        respuesta = mostrar_pregunta(pregunta, opciones)
        self.assertEqual(respuesta, '1')

    def test_verificar_respuesta_correcta(self):
        """
        Prueba la función `verificar_respuesta` con una respuesta correcta.

        1. Verifica que la función devuelva el puntaje correcto y el mensaje apropiado cuando la respuesta del usuario es correcta.
        """

        pregunta = self.preguntas[0]
        opciones = ["Mercurio", "Venus", "Marte"]
        resultado, log = verificar_respuesta(pregunta, 1, opciones)
        self.assertEqual(resultado, 1)
        self.assertIn("¡Correcto!", log)

    def test_verificar_respuesta_incorrecta(self):
        """
        Prueba la función `verificar_respuesta` con una respuesta incorrecta.

        1. Verifica que la función devuelva un puntaje de 0 y el mensaje apropiado cuando la respuesta del usuario es incorrecta.
        """

        pregunta = self.preguntas[0]
        opciones = ["Venus", "Marte", "Júpiter"]
        resultado, log = verificar_respuesta(pregunta, 1, opciones)
        self.assertEqual(resultado, 0)
        self.assertIn("Incorrecto", log)

    @patch('random.sample')
    @patch('random.shuffle')
    @patch('builtins.input', return_value='1')
    def test_ejecutar_ronda(self, mock_input, mock_shuffle, mock_sample):
        """
        Prueba la función `ejecutar_ronda`.

        1. Simula el comportamiento de `random.sample` y `random.shuffle` para controlar el conjunto de preguntas y opciones.
        2. Simula la entrada del usuario para las respuestas.
        3. Verifica que la función `ejecutar_ronda` devuelva los mensajes correctos sobre el estado de las respuestas y el puntaje final.
        """

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
