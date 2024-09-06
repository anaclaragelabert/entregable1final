from typing import Tuple, Callable

# Definimos el tipo MonadaResultado como una tupla de un entero y una cadena
MonadaResultado = Tuple[int, str]

# Función bind para la monada, acumula correctamente el estado
def bind(func: Callable[[int], MonadaResultado], monada: MonadaResultado) -> MonadaResultado:
    res = func(monada[0])  # Pasamos el estado actual (el puntaje) a la función
    nuevo_puntaje = monada[0] + res[0]  # Acumula el puntaje con el nuevo resultado
    nuevo_log = monada[1] + res[1]  # Acumula los logs
    return nuevo_puntaje, nuevo_log

# Función unit para inicializar el estado de la monada
def unit(valor: int) -> MonadaResultado:
    return valor, ""