# src/trivia/reader.py

import csv
from functools import lru_cache

# Ruta al archivo CSV
file_path = 'datos/questions.csv'

@lru_cache(maxsize=1)
def obtener_preguntas_csv(csv_file: str) -> list:
    """
    Lee un archivo CSV de preguntas y transforma cada fila en una tupla que contiene 
    la categoría, la pregunta y la respuesta.

    Parámetros:
        csv_file (str): La ruta al archivo CSV que contiene las preguntas.

    Retorna:
        list: Una lista de tuplas con el formato (Categoría, Pregunta, Respuesta).
    """
    try:
        with open(csv_file, newline='', encoding='latin1') as file:
            lector = csv.reader(file)
            
            # Intentamos saltar la cabecera solo si existen filas
            try:
                next(lector)  # Saltamos la primera línea que contiene las cabeceras
            except StopIteration:
                return []  # Si no hay más filas, retornamos una lista vacía

            # Transformar cada fila en una tupla (Categoría, Pregunta, Respuesta)
            nueva_fila = lambda fila: (fila[3], fila[5], fila[6])
            preguntas = map(nueva_fila, lector)
            
            return list(preguntas)
        
    except FileNotFoundError:
        return [] 
