# src/trivia/main.py

import sys
from functools import partial
from functionss import generar_preguntas_random, mezclar_opciones, generar_opciones, mostrar_pregunta, ejecutar_ronda
from reader import obtener_preguntas_csv
from decorators import tiempo_ejecucion_jugador  

# Predefinir la función de cantidad de preguntas a elegir del csv -> 5
calculate_default_score = partial(generar_preguntas_random, cantidad_preguntas=5)

def imprimirMensajeBienvenida() -> None:
    """
    Imprime un mensaje de bienvenida al juego de trivia y las opciones disponibles.
    """
    menuPrincipal = """
==================================================================
      ¡Bienvenidos al juego de Trivia más divertido!
==================================================================
¡Prepárate para un desafío de trivia lleno de diversión!

En este juego, tendrás la oportunidad de jugar una ronda con 5 preguntas al azar. 
Por cada respuesta correcta sumarás 10 puntos! :D
Pero por cada respuesta incorrecta sumarás 0 puntos :(

Elige una de las siguientes opciones para comenzar:

  1. Jugar ronda con todas las categorías al azar
  2. Finalizar el programa

===================================================================
===================================================================
    """
    print("\n", menuPrincipal)


def preguntar_continuar_juego(jenkins_mode=False) -> bool:
    """
    Pregunta al usuario si desea continuar jugando tras completar una ronda.

    Retorna:
        bool: True si el usuario elige continuar, False en caso contrario.
    """
    if jenkins_mode:
        return False  # Selecciona 'n' automáticamente en Jenkins
    
    respuesta = input("\n¿Quieres seguir jugando? (y/n): ").lower()
    return respuesta == 'y'


def imprimir_titulo_en_verde(titulo: str) -> None:
    """
    Imprime un título en color verde.

    Parámetros:
        titulo (str): El título a ser impreso en color verde.
    """
    ANSI_GREEN = "\033[92m"
    ANSI_RESET = "\033[0m"
    print(f"{ANSI_GREEN}{titulo}{ANSI_RESET}")

def obtener_respuestas_predefinidas() -> list:
    """
    Genera una lista de respuestas predefinidas para el modo de pruebas.

    Retorna:
        list: Lista de respuestas predefinidas.
    """
    return [1, 2, 1, 3, 2]  # Lista de índices predefinidos para las respuestas en el modo de prueba.


@tiempo_ejecucion_jugador
def ejecutar_juego_completo(preguntas: list, test_mode=False) -> None:
    """
    Ejecuta una ronda completa del juego de trivia, generando preguntas, 
    opciones y verificando respuestas.

    Parámetros:
        preguntas (list): Lista de preguntas obtenidas desde el archivo CSV.
    """
    preguntas_seleccionadas = list(calculate_default_score(preguntas))

    if not preguntas_seleccionadas:
        print("No se pudieron seleccionar preguntas aleatorias.")
        return

    opciones_todas_preguntas = [
        mezclar_opciones(generar_opciones(preguntas, pregunta)) 
        for pregunta in preguntas_seleccionadas
    ]

    respuestas_usuario = (
        obtener_respuestas_predefinidas() if test_mode 
        else [int(mostrar_pregunta(pregunta, opciones)) for pregunta, opciones in zip(preguntas_seleccionadas, opciones_todas_preguntas)]
    )

    resultados = ejecutar_ronda(preguntas_seleccionadas, opciones_todas_preguntas, respuestas_usuario)
    
    imprimir_titulo_en_verde("\nRESUMEN DEL JUEGO: ")
    for resultado in resultados:
        print(resultado)


if __name__ == "__main__":
    opcion = 0
    # Verifica si se está ejecutando en Jenkins mediante el argumento '--jenkins'
    jenkins_mode = '--jenkins' in sys.argv

    while True:

        imprimirMensajeBienvenida()
        try:
            # Selecciona la opción 1 automáticamente si estamos en Jenkins
            opcion = 1 if jenkins_mode else int(input("Seleccione la opción deseada: "))
            
            
            if opcion == 1:
                file_path = 'data/questions.csv'
                # Paso 1: Obtener preguntas desde el archivo CSV
                preguntas = obtener_preguntas_csv(file_path)

                if not preguntas:
                    print("No se encontraron preguntas en el archivo CSV.")
                    continue

                # Ejecutar el juego completo con el decorador
                ejecutar_juego_completo(preguntas,test_mode=jenkins_mode)

                # Preguntar si el usuario quiere continuar jugando
                if not preguntar_continuar_juego(jenkins_mode):
                    print("\nGracias por jugar. ¡Hasta la próxima!")
                    break

            elif opcion == 2:
                print("\n Su programa ha sido finalizado con éxito\n")
                break

            else:
                print("Debe ingresar números del 1 al 2")

        except ValueError:
            print("La opción ingresada no era correcta. Intente nuevamente con un número.")
