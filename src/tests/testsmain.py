import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trivia.main import imprimirMensajeBienvenida, preguntar_continuar_juego, imprimir_titulo_en_verde,  ejecutar_juego_completo, calculate_default_score
#from trivia.functionss import generar_preguntas_random, mezclar_opciones, generar_opciones, mostrar_pregunta, ejecutar_ronda


class TestMain(unittest.TestCase):
    """
    Clase de pruebas unitarias para las funciones del módulo 'trivia.main'.
    Utiliza unittest y unittest.mock para verificar el comportamiento de funciones
    relacionadas con la ejecución principal del juego de trivia.
    """

    @patch('builtins.input', return_value='y')
    def test_preguntar_continuar_juego_si(self, mock_input):
        """
        Prueba la función `preguntar_continuar_juego` cuando el usuario elige continuar.

        1. Simula la entrada del usuario con 'y'.
        2. Verifica que la función devuelva True, indicando que el usuario desea continuar.
        """

        # Simulamos que el usuario ingresa 'y' para continuar jugando
        respuesta = preguntar_continuar_juego()
        self.assertTrue(respuesta)

    @patch('builtins.input', return_value='n')
    def test_preguntar_continuar_juego_no(self, mock_input):
        """
        Prueba la función `preguntar_continuar_juego` cuando el usuario elige no continuar.

        1. Simula la entrada del usuario con 'n'.
        2. Verifica que la función devuelva False, indicando que el usuario no desea continuar.
        """

        # Simulamos que el usuario ingresa 'n' para no continuar jugando
        respuesta = preguntar_continuar_juego()
        self.assertFalse(respuesta)

    @patch('builtins.print')
    def test_imprimir_titulo_en_verde(self, mock_print):
        """
        Prueba la función `imprimir_titulo_en_verde`.

        1. Verifica que la función imprime el título en verde usando códigos ANSI.
        2. Comprueba que `print` sea llamado con el formato correcto.
        """

        # Verifica que el título se imprime en verde
        titulo = "Test Título"
        imprimir_titulo_en_verde(titulo)
        ANSI_GREEN = "\033[92m"
        ANSI_RESET = "\033[0m"
        mock_print.assert_called_once_with(f"{ANSI_GREEN}{titulo}{ANSI_RESET}")

    @patch('trivia.main.calculate_default_score')
    @patch('trivia.main.mezclar_opciones')
    @patch('trivia.main.generar_opciones')
    @patch('trivia.main.mostrar_pregunta')
    @patch('trivia.main.ejecutar_ronda')
    def test_ejecutar_juego_completo(self, mock_ejecutar_ronda, mock_mostrar_pregunta, mock_generar_opciones, mock_mezclar_opciones, mock_calculate_default_score):
        """
        Prueba la función `ejecutar_juego_completo`.

        1. Simula el comportamiento de las funciones `calculate_default_score`, `generar_opciones`, `mezclar_opciones`, `mostrar_pregunta`, y `ejecutar_ronda`.
        2. Verifica que se llamen estas funciones con los parámetros correctos y en el orden esperado.
        """
        
        # Simulamos las preguntas y opciones generadas
        preguntas_mock = [("Geografía", "¿Cuál es la capital de Francia?", "París")]
        mock_calculate_default_score.return_value = preguntas_mock
        mock_generar_opciones.return_value = ["París", "Madrid", "Londres", "Berlín"]
        mock_mezclar_opciones.return_value = ["París", "Madrid", "Londres", "Berlín"]
        mock_mostrar_pregunta.return_value = "1"

        # Ejecuta el juego
        ejecutar_juego_completo(preguntas_mock)

        # Verifica que se llamaron las funciones correctas
        mock_calculate_default_score.assert_called_once_with(preguntas_mock)
        mock_generar_opciones.assert_called()
        mock_mezclar_opciones.assert_called()
        mock_mostrar_pregunta.assert_called()
        mock_ejecutar_ronda.assert_called()

if __name__ == '__main__':
    unittest.main()
