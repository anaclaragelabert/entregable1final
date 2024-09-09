import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trivia.main import imprimirMensajeBienvenida, preguntar_continuar_juego, imprimir_titulo_en_verde,  ejecutar_juego_completo, calculate_default_score
from trivia.functions import generar_preguntas_random, mezclar_opciones, generar_opciones, mostrar_pregunta, ejecutar_ronda


class TestMain(unittest.TestCase):
    '''
    @patch('builtins.print')
    def test_imprimirMensajeBienvenida(self, mock_print):
        # Ejecuta la función
        imprimirMensajeBienvenida()

        # Verifica que la función haya llamado a print con una cadena que contenga parte del mensaje de bienvenida
        found = False
        for call in mock_print.call_args_list:
            if "¡Bienvenidos al juego de Trivia más divertido!" in call[0][0]:
                found = True
                break
        self.assertTrue(found, "El mensaje de bienvenida no se imprimió correctamente")
    '''

    @patch('builtins.input', return_value='y')
    def test_preguntar_continuar_juego_si(self, mock_input):
        # Simulamos que el usuario ingresa 'y' para continuar jugando
        respuesta = preguntar_continuar_juego()
        self.assertTrue(respuesta)

    @patch('builtins.input', return_value='n')
    def test_preguntar_continuar_juego_no(self, mock_input):
        # Simulamos que el usuario ingresa 'n' para no continuar jugando
        respuesta = preguntar_continuar_juego()
        self.assertFalse(respuesta)

    @patch('builtins.print')
    def test_imprimir_titulo_en_verde(self, mock_print):
        # Verifica que el título se imprime en verde
        titulo = "Test Título"
        imprimir_titulo_en_verde(titulo)
        ANSI_GREEN = "\033[92m"
        ANSI_RESET = "\033[0m"
        mock_print.assert_called_once_with(f"{ANSI_GREEN}{titulo}{ANSI_RESET}")

    @patch('main.calculate_default_score')
    @patch('main.mezclar_opciones')
    @patch('main.generar_opciones')
    @patch('main.mostrar_pregunta')
    @patch('main.ejecutar_ronda')
    def test_ejecutar_juego_completo(self, mock_ejecutar_ronda, mock_mostrar_pregunta, mock_generar_opciones, mock_mezclar_opciones, mock_calculate_default_score):
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
    '''
    @patch('main.mostrar_pregunta')
    @patch('builtins.input', side_effect=["1"])
    def test_mostrar_pregunta(self, mock_input, mock_mostrar_pregunta):
        # Simulamos una pregunta con sus opciones
        pregunta_mock = ("Historia", "¿Quién descubrió América?", "Cristóbal Colón")
        opciones_mock = ["Cristóbal Colón", "Américo Vespucio", "Fernando de Magallanes"]

        # Simulamos que el usuario selecciona la primera opción
        mock_mostrar_pregunta.return_value = "1"

        # Llamamos la función que ejecuta mostrar_pregunta
        respuesta = mostrar_pregunta(pregunta_mock, opciones_mock)

        # Verificamos que la función retorne la opción correcta
        self.assertEqual(respuesta, "1")
        mock_mostrar_pregunta.assert_called_once_with(pregunta_mock, opciones_mock)
    '''

if __name__ == '__main__':
    unittest.main()
