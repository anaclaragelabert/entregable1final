import unittest
import sys
import os

# Añade el directorio raíz del proyecto al sys.path para que Python pueda encontrar el módulo 'trivia'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ahora puedes importar desde el paquete trivia
from trivia.monads import unit, bind, MonadaResultado

# Definimos funciones de prueba para usar con bind
def sumar_dos(valor: int):
    return valor + 2, " +2"

def restar_cinco(valor: int):
    return valor - 5, " -5"

class TestMonada(unittest.TestCase):
    """
    Clase de pruebas unitarias para las funciones del módulo `monads`.
    Verifica el comportamiento de las funciones `unit` y `bind` en el contexto de una mónada.
    """
    
    def test_unit(self):
        """
        Prueba la función `unit`.

        Verifica que la función `unit` inicializa correctamente una mónada con un valor dado
        y una cadena de log vacía.
        """

        # Verifica que unit inicializa correctamente
        self.assertEqual(unit(10), (10, ""))
        self.assertEqual(unit(0), (0, ""))
        self.assertEqual(unit(-3), (-3, ""))

    def test_bind_suma(self):
        """
        Prueba la función `bind` con una función que suma un valor.

        Verifica que `bind` aplique la función `sumar_dos` al valor de la mónada inicial y
        combine el log inicial con el nuevo log generado por la función `sumar_dos`.
        """

        # Verifica el comportamiento de bind con una función que sume
        monada_inicial = (5, "Inicio")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (12, "Inicio +2"))

    def test_bind_resta(self):
        """
        Prueba la función `bind` con una función que resta un valor.

        Verifica que `bind` aplique la función `restar_cinco` al valor de la mónada inicial y
        combine el log inicial con el nuevo log generado por la función `restar_cinco`.
        """

        # Verifica el comportamiento de bind con una función que reste
        monada_inicial = (10, "Inicio")
        monada_final = bind(restar_cinco, monada_inicial)
        self.assertEqual(monada_final, (15, "Inicio -5"))
    

    def test_bind_con_valor_negativo(self):
        """
        Prueba la función `bind` con un valor inicial negativo.

        Verifica que `bind` aplique la función `sumar_dos` a un valor negativo y combine
        el log inicial con el nuevo log generado por la función `sumar_dos`.
        """

        # Verifica el comportamiento de bind con un valor inicial negativo
        monada_inicial = (-3, "Inicio")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (-4, "Inicio +2"))

    def test_bind_con_cadena_vacia(self):
        """
        Prueba la función `bind` con una cadena de log vacía.

        Verifica que `bind` aplique la función `sumar_dos` a un valor inicial con un log vacío
        y genere el nuevo log correctamente.
        """

        # Verifica el comportamiento de bind con un log inicial vacío
        monada_inicial = (0, "")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (2, " +2"))

if __name__ == '__main__':
    unittest.main()
