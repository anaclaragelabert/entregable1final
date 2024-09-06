import random
from itertools import chain
from typing import List, Tuple, Callable, Generator
from monads import unit, bind, MonadaResultado
from decorators import tiempo_ejecucion

# Función que genera preguntas aleatorias
def generar_preguntas_random(preguntas: List[Tuple[str, str, str]], cantidad_preguntas: int) -> Generator[Tuple[str, str, str], None, None]:
    preguntas_seleccionadas = random.sample(preguntas, cantidad_preguntas)
    for pregunta in preguntas_seleccionadas:
        yield pregunta

# Función para generar opciones de respuesta
def generar_opciones(preguntas: List[Tuple[str, str, str]], pregunta_actual: Tuple[str, str, str]) -> List[str]:
    respuesta_correcta = pregunta_actual[2]
    categoria_actual = pregunta_actual[0]

    # Filtrar preguntas que tengan la misma categoría pero una respuesta incorrecta
    respuestas_incorrectas = list(
        filter(
            lambda pregunta: pregunta[2] != respuesta_correcta and pregunta[0] == categoria_actual,
            preguntas
        )
    )

    if len(respuestas_incorrectas) < 2:
        # Si no hay suficientes respuestas incorrectas en la misma categoría, añadir respuestas incorrectas de otras categorías
        nuevas_incorrectas = list(
            filter(
                lambda pregunta: pregunta[2] != respuesta_correcta,
                preguntas
            )
        )
        nuevas_incorrectas = random.sample(nuevas_incorrectas, min(2, len(nuevas_incorrectas)))
        opciones = list(chain(nuevas_incorrectas, [pregunta_actual]))
    else:
        # Seleccionar 2 respuestas incorrectas de la misma categoría
        respuestas_seleccionadas = random.sample(respuestas_incorrectas, 2)
        opciones = list(chain([pregunta_actual], respuestas_seleccionadas))

    # Extraer solo las respuestas de las opciones
    return [opcion[2] for opcion in mezclar_opciones(opciones)]

# Función para mezclar las opciones de respuesta
def mezclar_opciones(opciones: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    opciones_copiadas = opciones[:]
    random.shuffle(opciones_copiadas)
    return opciones_copiadas

# Función para calcular el puntaje basado en respuestas correctas
def calcular_puntaje(respuestas_correctas: int) -> int:
    return respuestas_correctas * 10

# Función para mostrar una pregunta y sus opciones
def mostrar_pregunta(pregunta: Tuple[str, str, str], opciones: List[str]) -> str:
    print(f"\nCategoría: {pregunta[0]}")
    print(f"\nPregunta: {pregunta[1]}")

    for indice, opcion in enumerate(opciones):
        print(f"{indice + 1}. {opcion}")

    respuesta_usuario = input("\nIngrese su respuesta (1, 2, 3): ")

    if respuesta_usuario not in {'1', '2', '3'}:
        print("\nOpción inválida. Su respuesta debe ser 1, 2 o 3.")
        return mostrar_pregunta(pregunta, opciones)
    
    return respuesta_usuario


# Función para verificar la respuesta del usuario
def verificar_respuesta(pregunta: Tuple[str, str, str], respuesta_usuario: int, opciones: List[str]) -> MonadaResultado:
    es_correcto = opciones[respuesta_usuario - 1].lower() == pregunta[2].lower()
    log = f"\nCategoría: {pregunta[0]}\nPregunta: {pregunta[1]}\n"

    if es_correcto:
        log += "¡Correcto!\n"
        return 1, log  # Retorna 1 punto si es correcto
    else:
        log += f"Incorrecto. La respuesta correcta era: {pregunta[2]}\n"
        return 0, log  # Retorna 0 puntos si es incorrecto

# Función para procesar la respuesta del usuario y actualizar el estado de la monada
def procesar_pregunta(pregunta: Tuple[str, str, str], opciones: List[str], respuesta_usuario: int) -> Callable[[MonadaResultado], MonadaResultado]:
    return lambda estado: bind(lambda _: verificar_respuesta(pregunta, respuesta_usuario, opciones), estado)

# Función para ejecutar una ronda de preguntas y calcular resultados
@tiempo_ejecucion
def ejecutar_ronda(preguntas: List[Tuple[str, str, str]], opciones: List[List[str]], respuestas_usuario: List[int]) -> List[str]:
    resultado_final = unit(0)  # Inicializa con 0 puntos
    
    # Procesar cada pregunta y actualizar el estado de la monada
    procesos = [procesar_pregunta(pregunta, opciones[i], respuestas_usuario[i]) for i, pregunta in enumerate(preguntas)]
    
    # Acumular los resultados en la monada
    for proceso in procesos:
        resultado_final = proceso(resultado_final)

    # Extraer los logs del resultado final
    logs = resultado_final[1]
    
    # Calcular puntaje total (resultado_final[0] contiene los puntos acumulados)
    puntaje_total = calcular_puntaje(resultado_final[0])

    return [logs] + [f"\nResultado final: {puntaje_total}\n"]


"""
CHEQUEAR QUE LOS FOR QUE USAMOS NO AFECTEN ALGO EXTERIOR
"""