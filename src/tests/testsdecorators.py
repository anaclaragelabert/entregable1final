import unittest
from unittest.mock import patch
import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trivia.decorators import tiempo_ejecucion, tiempo_ejecucion_jugador
import time

class TestDecorators(unittest.TestCase):
    """
    Clase de pruebas unitarias para los decoradores definidos en el módulo 'trivia.decorators'.
    Utiliza unittest y unittest.mock para verificar el comportamiento de los decoradores
    `tiempo_ejecucion` y `tiempo_ejecucion_jugador`.
    """

    @patch('time.time', side_effect=[1, 2])  # Simula que la función tarda 1 segundo
    @patch('builtins.print')  # Intercepta la salida de print
    def test_tiempo_ejecucion(self, mock_print, mock_time):
        """
        Prueba el decorador `tiempo_ejecucion`.

        1. Define una función de prueba decorada con `tiempo_ejecucion`.
        2. Llama a la función decorada y verifica su resultado.
        3. Comprueba que `print` haya sido llamado con el mensaje correcto que indica
           el tiempo de ejecución de la función.
        """
         
        # Definimos una función de prueba
        @tiempo_ejecucion
        def funcion_prueba():
            return "resultado"
        
        # Llamamos a la función decorada
        resultado = funcion_prueba()

        # Verificamos el resultado de la función
        self.assertEqual(resultado, "resultado")
        
        # Verificamos que print haya sido llamado con el mensaje correcto
        mock_print.assert_called_with("\nFunction 'funcion_prueba' executed in 1.000000 seconds")
    
    @patch('time.time', side_effect=[1, 2.5])  # Simula que la función tarda 1.5 segundos
    @patch('builtins.print')  # Intercepta la salida de print
    def test_tiempo_ejecucion_jugador(self, mock_print, mock_time):
        """
        Prueba el decorador `tiempo_ejecucion_jugador`.

        1. Define una función de prueba decorada con `tiempo_ejecucion_jugador`.
        2. Llama a la función decorada y verifica su resultado.
        3. Comprueba que `print` haya sido llamado con los mensajes correctos que indican
           el inicio de la ronda y el tiempo de ejecución.
        """

        # Definimos una función de prueba
        @tiempo_ejecucion_jugador
        def funcion_prueba():
            return "resultado"
        
        # Llamamos a la función decorada
        resultado = funcion_prueba()

        # Verificamos el resultado de la función
        self.assertEqual(resultado, "resultado")
        
        # Verificamos que print haya sido llamado con los mensajes correctos
        mock_print.assert_any_call("\n¡La ronda ha comenzado!")
        mock_print.assert_any_call("\nHas completado la ronda en 1.50 segundos.")

if __name__ == '__main__':
    unittest.main()
