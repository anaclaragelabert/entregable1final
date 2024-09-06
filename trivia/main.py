from functools import partial
from functions import generar_preguntas_random, mezclar_opciones, generar_opciones, mostrar_pregunta, ejecutar_ronda
from reader import obtener_preguntas_csv
from decorators import tiempo_ejecucion_jugador  # Asegúrate de importar el decorador

# Predefinir la función de cantidad de preguntas a elegir del csv -> 5
calculate_default_score = partial(generar_preguntas_random, cantidad_preguntas=5)

def imprimirMensajeBienvenida() -> None:
    menuPrincipal = """
==================================================================
      ¡Bienvenidos al juego de Trivia más divertido!
==================================================================

¡Prepárate para un desafío de trivia lleno de diversión!

En este juego, tendrás la oportunidad de jugar una ronda con 5 preguntas al azar. 

Elige una de las siguientes opciones para comenzar:

  1. Jugar ronda con todas las categorías al azar
  2. Finalizar el programa

===================================================================
    """

    print("\n", menuPrincipal)

@tiempo_ejecucion_jugador # Decoramos toda la ejecución de la ronda
def ejecutar_juego_completo(preguntas: list) -> None:
    # Paso 2: Generar preguntas aleatorias
    preguntas_seleccionadas = list(calculate_default_score(preguntas))

    if not preguntas_seleccionadas:
        print("No se pudieron seleccionar preguntas aleatorias.")
        return

    # Paso 3: Generar opciones para cada pregunta
    opciones_todas_preguntas = [
        mezclar_opciones(generar_opciones(preguntas, pregunta)) 
        for pregunta in preguntas_seleccionadas
    ]

    # Recolectar respuestas del usuario
    respuestas_usuario = []
    for pregunta, opciones in zip(preguntas_seleccionadas, opciones_todas_preguntas):
        respuesta = mostrar_pregunta(pregunta, opciones)
        try:
            respuestas_usuario.append(int(respuesta))
        except ValueError:
            print("La opción ingresada no era correcta. Intente nuevamente con un número.")

    # Paso 4: Ejecutar la ronda y obtener los resultados
    resultados = ejecutar_ronda(preguntas_seleccionadas, opciones_todas_preguntas, respuestas_usuario)
    
    # Mostrar los resultados
    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    opcion = 0

    while opcion != 2:

        imprimirMensajeBienvenida()
        try:
            opcion = int(input("Seleccione la opción deseada: "))
            
            if opcion == 1:
                file_path = 'data/questions.csv'
                # Paso 1: Obtener preguntas desde el archivo CSV
                preguntas = obtener_preguntas_csv(file_path)

                if not preguntas:
                    print("No se encontraron preguntas en el archivo CSV.")
                    continue

                # Ejecutar el juego completo con el decorador
                ejecutar_juego_completo(preguntas)

            elif opcion == 2:
                print("\n Su programa ha sido finalizado con éxito\n")
                break

            else:
                print("Debe ingresar números del 1 al 2")

        except ValueError:
            print("La opción ingresada no era correcta. Intente nuevamente con un número.")
