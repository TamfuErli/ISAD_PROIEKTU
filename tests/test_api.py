import unittest
from controller import film_kudeaketa

# Kontsolan python -m unittest tests/test_api.py egin exekutatzeko

class TestApi(unittest.TestCase):
    def test_gehituFilma(self):
        film_kudeaketa.gehituFilma(0, "test", "test", "test", 1.0, "2022-01-01", 0) # Datu-basean kodeFilma existitzen bada, ez du berriro sortuko 
        self.assertEqual(film_kudeaketa.gehituEskaera(0, 1), True) # Datu-basean horrelakorik existitzerakoan, None aterako da
        self.assertEqual(film_kudeaketa.gehituEskaera(0, 1), False)

if __name__ == '__main__':
    unittest.main()