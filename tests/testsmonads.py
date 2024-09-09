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
    
    def test_unit(self):
        # Verifica que unit inicializa correctamente
        self.assertEqual(unit(10), (10, ""))
        self.assertEqual(unit(0), (0, ""))
        self.assertEqual(unit(-3), (-3, ""))

    def test_bind_suma(self):
        # Verifica el comportamiento de bind con una función que sume
        monada_inicial = (5, "Inicio")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (12, "Inicio +2"))

    def test_bind_resta(self):
        # Verifica el comportamiento de bind con una función que reste
        monada_inicial = (10, "Inicio")
        monada_final = bind(restar_cinco, monada_inicial)
        self.assertEqual(monada_final, (15, "Inicio -5"))
    

    def test_bind_con_valor_negativo(self):
        # Verifica el comportamiento de bind con un valor inicial negativo
        monada_inicial = (-3, "Inicio")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (-4, "Inicio +2"))

    def test_bind_con_cadena_vacia(self):
        # Verifica el comportamiento de bind con un log inicial vacío
        monada_inicial = (0, "")
        monada_final = bind(sumar_dos, monada_inicial)
        self.assertEqual(monada_final, (2, " +2"))

if __name__ == '__main__':
    unittest.main()
