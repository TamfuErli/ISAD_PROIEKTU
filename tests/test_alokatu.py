import unittest
from unittest.mock import patch, MagicMock
from flask import session
from your_application import app, film_kudeaketa, erabiltzaile_kudeaketa

class TestAlokatu(unittest.TestCase):

    def setUp(self):
        # Configurar el entorno de pruebas
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.client.testing = True

        # Crear una sesión de prueba
        with self.client.session_transaction() as sess:
            sess['sPosta'] = 'test@example.com'

    @patch('your_application.film_kudeaketa.alokatutakoFilmak')
    @patch('your_application.film_kudeaketa.billatuPelikula')
    def test_alokairu(self, mock_billatuPelikula, mock_alokatutakoFilmak):
        # Configurar los mocks
        mock_alokatutakoFilmak.return_value = [MagicMock(getKodeFilm=lambda: 1)]
        mock_billatuPelikula.return_value = [(1, 'Test Film', '/path/to/poster.jpg', 'Description', 7.5, '2023-01-01', 1)]

        # Hacer una solicitud GET a la ruta /alokairu
        response = self.client.get('/alokairu')

        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Film', response.data)
        self.assertIn(b'2023-01-01', response.data)
        self.assertIn(b'/path/to/poster.jpg', response.data)

    @patch('your_application.erabiltzaile_kudeaketa.gehituAlokairua')
    def test_submit_alokairu(self, mock_gehituAlokairua):
        # Configurar el mock
        mock_gehituAlokairua.return_value = {'success': True}

        # Hacer una solicitud POST a la ruta /submit_alokairu
        response = self.client.post('/submit_alokairu', data={'kodeFilma': 1})

        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 302)  # Redirección
        self.assertEqual(response.location, 'http://localhost/home_loged')

        # Verificar que el mock fue llamado correctamente
        mock_gehituAlokairua.assert_called_once_with('test@example.com', '1')

if __name__ == '__main__':
    unittest.main()