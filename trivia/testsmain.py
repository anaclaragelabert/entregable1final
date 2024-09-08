import unittest
from unittest.mock import patch, MagicMock
from functions import mostrar_pregunta
from reader import obtener_preguntas_csv
from main import imprimirMensajeBienvenida, ejecutar_juego_completo

class TestMain(unittest.TestCase):

    @patch('builtins.print')
    def test_imprimirMensajeBienvenida(self, mock_print):
        # Ejecuta la función
        imprimirMensajeBienvenida()

        # Verifica que la función haya llamado a print con el menú correcto
        mock_print.assert_called_once()
        self.assertIn("¡Bienvenidos al juego de Trivia más divertido!", mock_print.call_args[0][0])

    @patch('builtins.input', side_effect=["1"])
    @patch('main.obtener_preguntas_csv')
    @patch('main.ejecutar_juego_completo')
    def test_ejecutar_juego_completo(self, mock_juego_completo, mock_obtener_preguntas_csv, mock_input):
        # Mockeamos la salida del CSV para que retorne algunas preguntas
        preguntas_mock = [
            ("Geografía", "¿Cuál es la capital de Francia?", "París"),
            ("Historia", "¿Quién descubrió América?", "Cristóbal Colón"),
            ("Ciencia", "¿Qué planeta es conocido como el planeta rojo?", "Marte")
        ]
        mock_obtener_preguntas_csv.return_value = preguntas_mock

        # Simulamos que el usuario elige la opción 1 y se ejecuta el juego completo
        with patch('builtins.input', side_effect=["1", "2", "3", "1", "1"]):  # Simulamos respuestas del usuario
            ejecutar_juego_completo(preguntas_mock)
        
        # Verificamos que las preguntas se han obtenido y el juego ha sido ejecutado
        mock_obtener_preguntas_csv.assert_called_once()
        mock_juego_completo.assert_called_once_with(preguntas_mock)

    @patch('builtins.input', side_effect=["1", "0", "2"])
    @patch('main.obtener_preguntas_csv')
    @patch('main.ejecutar_juego_completo')
    def test_juego_opcion_invalida(self, mock_juego_completo, mock_obtener_preguntas_csv, mock_input):
        # Probar una opción de menú inválida y luego ejecutar el juego correctamente
        preguntas_mock = [
            ("Geografía", "¿Cuál es la capital de Francia?", "París"),
        ]
        mock_obtener_preguntas_csv.return_value = preguntas_mock

        # Simulamos la opción 0 inválida y luego elige 2 para salir
        with patch('builtins.input', side_effect=["0", "2"]):
            from main import main
            main()  # Ejecutamos el ciclo principal

        mock_juego_completo.assert_not_called()

    @patch('builtins.input', side_effect=["1", "2", "3"])
    @patch('main.mostrar_pregunta')
    def test_mostrar_pregunta(self, mock_mostrar_pregunta):
        # Simulamos una pregunta con sus opciones
        pregunta_mock = ("Historia", "¿Quién descubrió América?", "Cristóbal Colón")
        opciones_mock = ["Cristóbal Colón", "Américo Vespucio", "Fernando de Magallanes"]

        # Simulamos que el usuario selecciona la primera opción
        mock_mostrar_pregunta.return_value = "1"

        # Llamamos la función con mocks
        respuesta = mostrar_pregunta(pregunta_mock, opciones_mock)

        # Verificamos que la función retorne la opción correcta
        self.assertEqual(respuesta, "1")
        mock_mostrar_pregunta.assert_called_once_with(pregunta_mock, opciones_mock)

if __name__ == '__main__':
    unittest.main()
