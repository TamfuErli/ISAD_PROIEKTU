import pytest
from controller.pagina_kontrola import app
from pytest_mock import mocker

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_erabiltzaile_datuak(client):
    mocker.patch('controller.erabiltzaile_kudeaketa.sortuErabiltzailea', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.aldatuErabiltzailea', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzaileaOnartua', return_value=1)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzailea_logeatu', return_value=True)
    
    response = client.post('/submit_registration', data={'erabiltzailea': 'test', 'posta': " pato@gmail.com   ", 'password': 'test'})
    response = client.post('/submit_datuak', data={'izenBerria': 'test', 'emailBerria': "adibide@email.com" })
    
    assert response.status_code == 302
    assert response.location == 'http://localhost/aldatu_datuak'
    
def test_aldatu_erabiltzaile_datuak_admin(client):
    mocker.patch('controller.erabiltzaile_kudeaketa.aldatuErabiltzailea', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzaileaOnartua', return_value=1)  
    
    response = client.post('/update_user', data={'posta': 'test@gmail.com', 'izena': "" })
    
    assert response.status_code == 302
    assert response.location == 'http://localhost/aldatu_datuak'
     
    
                                                