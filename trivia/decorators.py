# decorators.py
import time
from typing import Callable, Any

def tiempo_ejecucion(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.6f} seconds")
        return result
    return wrapper


def tiempo_ejecucion_jugador(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("¡La ronda ha comenzado!")
        start_time = time.time()  # Tiempo al inicio de la ronda
        result = func(*args, **kwargs)  # Ejecutar la función de la ronda
        end_time = time.time()  # Tiempo al finalizar la ronda
        tiempo_jugado = end_time - start_time
        print(f"Has completado la ronda en {tiempo_jugado:.2f} segundos.")
        return result
    return wrapper
