import unittest
from unittest.mock import patch
from decorators import tiempo_ejecucion, tiempo_ejecucion_jugador
import time

class TestDecorators(unittest.TestCase):

    @patch('time.time', side_effect=[1, 2])  # Simula que la función tarda 1 segundo
    @patch('builtins.print')  # Intercepta la salida de print
    def test_tiempo_ejecucion(self, mock_print, mock_time):
        # Definimos una función de prueba
        @tiempo_ejecucion
        def funcion_prueba():
            return "resultado"
        
        # Llamamos a la función decorada
        resultado = funcion_prueba()

        # Verificamos el resultado de la función
        self.assertEqual(resultado, "resultado")
        
        # Verificamos que print haya sido llamado con el mensaje correcto
        mock_print.assert_called_with("Function 'funcion_prueba' executed in 1.000000 seconds")
    
    @patch('time.time', side_effect=[1, 2.5])  # Simula que la función tarda 1.5 segundos
    @patch('builtins.print')  # Intercepta la salida de print
    def test_tiempo_ejecucion_jugador(self, mock_print, mock_time):
        # Definimos una función de prueba
        @tiempo_ejecucion_jugador
        def funcion_prueba():
            return "resultado"
        
        # Llamamos a la función decorada
        resultado = funcion_prueba()

        # Verificamos el resultado de la función
        self.assertEqual(resultado, "resultado")
        
        # Verificamos que print haya sido llamado con los mensajes correctos
        mock_print.assert_any_call("¡La ronda ha comenzado!")
        mock_print.assert_any_call("Has completado la ronda en 1.50 segundos.")

if __name__ == '__main__':
    unittest.main()
