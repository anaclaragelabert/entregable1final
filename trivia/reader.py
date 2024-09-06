import csv
from functools import lru_cache

# Ruta al archivo CSV
file_path = 'datos/questions.csv'

@lru_cache(maxsize=1)
def obtener_preguntas_csv(csv_file):
    try:
        with open(csv_file, newline='', encoding='latin1') as file:
            lector = csv.reader(file)
            next(lector) # Saltamos la primera línea que contiene las cabeceras -> ['Show_Number', 'Air_Date', 'Round', 'Category', 'Value', 'Question', 'Answer']

            # Transformar cada fila en el formato (Category, Question, Answer) -> Se transforma en (fila[0], fila[1], fila[2])
            nueva_fila = lambda fila: (fila[3], fila[5], fila[6])

            # Usar map para aplicar la función a cada fila del CSV
            preguntas = map(nueva_fila, lector)
            
            return list(preguntas)
        
    except FileNotFoundError:
        return [] 
    