import unittest
from unittest.mock import mock_open, patch
import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trivia.reader import obtener_preguntas_csv

class TestReader(unittest.TestCase):

    @patch('trivia.reader.open', new_callable=mock_open, read_data="Show_Number,Air_Date,Round,Category,Value,Question,Answer\n1234,2022-01-01,Jeopardy!,Geografía,$200,¿Cuál es la capital de Francia?,París\n1235,2022-01-02,Jeopardy!,Historia,$400,¿Quién descubrió América?,Cristóbal Colón\n")
    @patch('trivia.reader.csv.reader')
    def test_obtener_preguntas_csv(self, mock_csv_reader, mock_open_file):
        obtener_preguntas_csv.cache_clear()  # Limpiar el caché antes del test
        mock_csv_reader.return_value = iter([
            ['Show_Number', 'Air_Date', 'Round', 'Category', 'Value', 'Question', 'Answer'],
            ['1234', '2022-01-01', 'Jeopardy!', 'Geografía', '$200', '¿Cuál es la capital de Francia?', 'París'],
            ['1235', '2022-01-02', 'Jeopardy!', 'Historia', '$400', '¿Quién descubrió América?', 'Cristóbal Colón'],
        ])
        
        preguntas = obtener_preguntas_csv("ruta/falsa.csv")
        mock_open_file.assert_called_once_with("ruta/falsa.csv", newline='', encoding='latin1')
        self.assertEqual(preguntas, [
            ('Geografía', '¿Cuál es la capital de Francia?', 'París'),
            ('Historia', '¿Quién descubrió América?', 'Cristóbal Colón'),
        ])

    @patch('trivia.reader.open', new_callable=mock_open, read_data="Show_Number,Air_Date,Round,Category,Value,Question,Answer\n")
    @patch('trivia.reader.csv.reader')
    def test_obtener_preguntas_csv_sin_preguntas(self, mock_csv_reader, mock_open_file):
        obtener_preguntas_csv.cache_clear()  # Limpiar el caché antes del test
        mock_csv_reader.return_value = iter([])

        preguntas = obtener_preguntas_csv("ruta/falsa.csv")
        self.assertEqual(preguntas, [])

    @patch('trivia.reader.open', side_effect=FileNotFoundError)
    @patch('trivia.reader.csv.reader')
    def test_obtener_preguntas_csv_archivo_no_encontrado(self, mock_csv_reader, mock_open_file):
        obtener_preguntas_csv.cache_clear()  # Limpiar el caché antes del test
        mock_csv_reader.side_effect = FileNotFoundError
        
        preguntas = obtener_preguntas_csv("ruta/falsa.csv")
        self.assertEqual(preguntas, [])
        mock_open_file.assert_called_once_with("ruta/falsa.csv", newline='', encoding='latin1')

if __name__ == '__main__':
    unittest.main()
