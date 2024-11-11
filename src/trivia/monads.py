# src/trivia/monads.py

from typing import Tuple, Callable

# Definimos el tipo MonadaResultado como una tupla de un entero y una cadena
MonadaResultado = Tuple[int, str]

def bind(func: Callable[[int], MonadaResultado], monada: MonadaResultado) -> MonadaResultado:
    """
    Función 'bind' para la monada. Acumula el estado del puntaje y los logs.

    Parámetros:
        func (Callable[[int], MonadaResultado]): Una función que toma el puntaje y devuelve
        un nuevo estado de la monada.
        monada (MonadaResultado): El estado actual de la monada (puntaje, log).

    Retorna:
        MonadaResultado: El nuevo estado con el puntaje y los logs actualizados.
    """
    res = func(monada[0])  # Pasamos el estado actual (el puntaje) a la función
    nuevo_puntaje = monada[0] + res[0]  # Acumula el puntaje con el nuevo resultado
    nuevo_log = monada[1] + res[1]  # Acumula los logs
    return nuevo_puntaje, nuevo_log


def unit(valor: int) -> MonadaResultado:
    """
    Inicializa el estado de la monada.

    Parámetros:
        valor (int): El puntaje inicial.

    Retorna:
        MonadaResultado: El estado inicial con el puntaje y un log vacío.
    """
    return valor, ""
