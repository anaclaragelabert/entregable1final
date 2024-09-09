# Trivia Game

Un juego de trivia en Python que permite a los usuarios jugar una ronda de preguntas, con puntuaciones calculadas y registro de tiempos de ejecución. El juego lee preguntas desde un archivo CSV, genera preguntas aleatorias, y muestra opciones al usuario.

## Estructura del Proyecto

El proyecto está compuesto por varias carpetas y archivos de Python, cada uno con una función específica:

    Carpeta data:
        Contiene el archivo.csv
    
    Carpeta src:
        Carpeta tests: 
            Contiene los archivos de Python que contienen las pruebas unitarias.
                - testsdecorators.py
                - testsfunciones.py
                - testsmain.py
                - testsmonads.py
                - testsreader.py

        Carpeta trivia:
            Contiene los archivos de Python que permiten que funcione Trivia Game.
                - reader.py: Contiene funciones para leer preguntas desde un archivo CSV.
                - monads.py: Implementa funciones para manejar el estado de la monada en el juego.
                - main.py: El archivo principal que ejecuta el juego, maneja la interacción con el usuario y coordina el flujo del juego.
                - functionss.py: Contiene funciones auxiliares para generar preguntas, opciones, y calcular puntuaciones.
                - decorators.py: Define decoradores para medir el tiempo de ejecución de las funciones.

## Uso

El juego se ejecuta desde el archivo main.py

Una vez ejecutado, selecciona una opción:

    1. Jugar una ronda con preguntas al azar.
    2. Finalizar el programa.

## Estructura del Código

reader.py

    obtener_preguntas_csv(csv_file: str) -> list: Lee un archivo CSV y devuelve una lista de tuplas con el formato (Categoría Pregunta, Respuesta).

monads.py

    bind(func: Callable[[int], MonadaResultado], monada: MonadaResultado) -> MonadaResultado: Acumula el estado del puntaje y los logs.
    
    unit(valor: int) -> MonadaResultado: Inicializa el estado de la monada.

main.py

    imprimirMensajeBienvenida(): Imprime el mensaje de bienvenida al juego.
    
    preguntar_continuar_juego() -> bool: Pregunta al usuario si desea continuar jugando.
    
    imprimir_titulo_en_verde(titulo: str): Imprime un título en color verde.
    
    ejecutar_juego_completo(preguntas: list): Ejecuta una ronda completa del juego de trivia.

functions.py

    generar_preguntas_random(preguntas: List[Tuple[str, str, str]], cantidad_preguntas: int) -> Generator[Tuple[str, str, str], None, None]: Genera preguntas aleatorias.
    
    generar_opciones(preguntas: List[Tuple[str, str, str]], pregunta_actual: Tuple[str, str, str]) -> List[str]: Genera opciones de respuesta.
    
    mezclar_opciones(opciones: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]: Mezcla las opciones de respuesta.
    
    calcular_puntaje(respuestas_correctas: int) -> int: Calcula el puntaje total.
    
    mostrar_pregunta(pregunta: Tuple[str, str, str], opciones: List[str]) -> str: Muestra una pregunta y recoge la respuesta del usuario.
    
    verificar_respuesta(pregunta: Tuple[str, str, str], respuesta_usuario: int, opciones: List[str]) -> MonadaResultado: Verifica la respuesta del usuario.
    
    procesar_pregunta(pregunta: Tuple[str, str, str], opciones: List[str], respuesta_usuario: int) -> Callable[[MonadaResultado], MonadaResultado]: Procesa una pregunta y actualiza el estado de la monada.
    
    ejecutar_ronda(preguntas: List[Tuple[str, str, str]], opciones: List[List[str]], respuestas_usuario: List[int]) -> List[str]: Ejecuta una ronda de preguntas y calcula resultados.

decorators.py

    tiempo_ejecucion(func: Callable) -> Callable: Mide el tiempo de ejecución de una función.
    
    tiempo_ejecucion_jugador(func: Callable) -> Callable: Mide el tiempo de ejecución del jugador durante el juego.

## Conjunto de pruebas

**Asi como está el código no va a permitir que se ejecuten los siguientes archivos:**
    
    testfunciones.py
    testmain.py

Para poder ejecutar testfunciones.py se debe de cambiar los imports del archivo functionss.py a los siguientes:

    import random
    from itertools import chain
    from typing import List, Tuple, Callable, Generator
    from trivia.monads import unit, bind, MonadaResultado
    from trivia.decorators import tiempo_ejecucion

Para poder ejecutar testmain.py se debe de cambiar los imports del archivo main.py a los siguientes:

    from functools import partial
    from trivia.functionss import generar_preguntas_random, mezclar_opciones, generar_opciones, mostrar_pregunta, ejecutar_ronda
    from trivia.reader import obtener_preguntas_csv
    from trivia.decorators import tiempo_ejecucion_jugador  

**OBS:** Para poder volver a ejecutar el archivo main.py, se debe volver a los imports anteriores en los archivos mencionados 
(es simplemente sacarle el trivia. a los from que lo tienen)

### Breve resumen pruebas unitarias
testreader.py:

    Objetivo: Prueba la función obtener_preguntas_csv del módulo reader.
    Verificaciones:
        - Lectura correcta del CSV con preguntas.
        - Manejo de CSV vacío.
        - Manejo de errores como FileNotFoundError.

testmonads.py:

    Objetivo: Prueba las funciones de la implementación de mónadas, como unit y bind.
    Verificaciones:
        - Correcta inicialización de la mónada con unit.
        - Aplicación de funciones con bind y combinación de logs.

testmain.py:

    Objetivo: Prueba las funciones principales del juego de trivia en el módulo main.
    Verificaciones:
        - Función preguntar_continuar_juego para entradas de usuario.
        - imprimir_titulo_en_verde para la correcta impresión del título.
        - ejecutar_juego_completo para la secuencia de ejecución del juego, con funciones relacionadas como calculate_default_score, generar_opciones, etc.

testfunciones.py:

    Objetivo: Prueba las funciones auxiliares del juego de trivia en el módulo functionss.
    Verificaciones:
        - Generación aleatoria de preguntas.
        - Creación y mezcla de opciones.
        - Verificación de respuestas.
        - Ejecución de rondas.

testdecorators.py:

    Objetivo: Prueba los decoradores definidos en el módulo decorators.
    Verificaciones:
        - tiempo_ejecucion para medir y mostrar el tiempo de ejecución de una función.
        - tiempo_ejecucion_jugador para medir y mostrar el tiempo de ejecución de una ronda y notificar al jugador.
