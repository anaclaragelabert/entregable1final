import unittest
from unittest.mock import mock_open, patch
from reader import obtener_preguntas_csv


class TestReader(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="Show_Number,Air_Date,Round,Category,Value,Question,Answer\n1234,2022-01-01,Jeopardy!,Geografía,$200,¿Cuál es la capital de Francia?,París\n1235,2022-01-02,Jeopardy!,Historia,$400,¿Quién descubrió América?,Cristóbal Colón\n")
    @patch('reader.csv.reader')
    def test_obtener_preguntas_csv(self, mock_csv_reader, mock_open_file):
        # Mockeamos la salida del CSV
        mock_csv_reader.return_value = [
            ['1234', '2022-01-01', 'Jeopardy!', 'Geografía', '$200', '¿Cuál es la capital de Francia?', 'París'],
            ['1235', '2022-01-02', 'Jeopardy!', 'Historia', '$400', '¿Quién descubrió América?', 'Cristóbal Colón'],
        ]
        
        # Llamamos la función con un archivo ficticio
        preguntas = obtener_preguntas_csv("ruta/falsa.csv")

        # Verificamos que el archivo se ha abierto correctamente
        mock_open_file.assert_called_once_with("ruta/falsa.csv", newline='', encoding='latin1')

        # Verificamos que las preguntas se han leído y transformado correctamente
        self.assertEqual(preguntas, [
            ('Geografía', '¿Cuál es la capital de Francia?', 'París'),
            ('Historia', '¿Quién descubrió América?', 'Cristóbal Colón'),
        ])

    @patch('builtins.open', new_callable=mock_open, read_data="Show_Number,Air_Date,Round,Category,Value,Question,Answer\n")
    @patch('reader.csv.reader')
    def test_obtener_preguntas_csv_sin_preguntas(self, mock_csv_reader, mock_open_file):
        # Mockeamos que el CSV no tiene preguntas, solo el encabezado
        mock_csv_reader.return_value = []

        # Llamamos la función
        preguntas = obtener_preguntas_csv("ruta/falsa.csv")

        # Verificamos que la función retorna una lista vacía si no hay preguntas
        self.assertEqual(preguntas, [])

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_obtener_preguntas_csv_archivo_no_encontrado(self, mock_open_file):
        # Simulamos que el archivo no existe
        preguntas = obtener_preguntas_csv("ruta/falsa.csv")

        # Verificamos que la función retorna una lista vacía si el archivo no existe
        self.assertEqual(preguntas, [])

        # Verificamos que se intentó abrir el archivo
        mock_open_file.assert_called_once_with("ruta/falsa.csv", newline='', encoding='latin1')


if __name__ == '__main__':
    unittest.main()
