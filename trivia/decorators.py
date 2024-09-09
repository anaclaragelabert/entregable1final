# decorators.py
import time
from typing import Callable, Any

def tiempo_ejecucion(func: Callable) -> Callable:
    """
    Un decorador que mide y muestra el tiempo de ejecución de una función.

    Parámetros:
        func (Callable): La función a decorar.

    Retorna:
        Callable: La función decorada.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\nFunction '{func.__name__}' executed in {end_time - start_time:.6f} seconds")
        return result
    return wrapper


def tiempo_ejecucion_jugador(func: Callable) -> Callable:
    """
    Un decorador que muestra el tiempo de ejecución del jugador durante el juego.

    Parámetros:
        func (Callable): La función a decorar.

    Retorna:
        Callable: La función decorada.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("\n¡La ronda ha comenzado!")
        start_time = time.time()  # Tiempo al inicio de la ronda
        result = func(*args, **kwargs)  # Ejecutar la función de la ronda
        end_time = time.time()  # Tiempo al finalizar la ronda
        tiempo_jugado = end_time - start_time
        print(f"\nHas completado la ronda en {tiempo_jugado:.2f} segundos.")
        return result
    return wrapper
