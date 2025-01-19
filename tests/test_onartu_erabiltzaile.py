import pytest
from controller.pagina_kontrola import app
from pytest_mock import mocker

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
def test_erabiltzailea_onartu(client):
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzaileaOnartua', return_value=False)
    mocker.patch('controller.erabiltzaile_kudeaketa.bilatuErabiltzailea', return_value=False)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzailea_logeatu', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.Erabiltzailea.adminDa', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.sortuErabiltzailea', return_value=True)
    
    response = client.post('/submit_registration', data={ 'erabiltzailea': 'test', 'password': 'test','posta': "test2@gmail.com" })
    response = client.post('/submit_login', data={'posta': "admin" , 'password': 'admin'})
    response = client.post('/onartu_erabiltzaile', data={'posta':"test2@gmail.com"}) 
    
    assert response.status_code == 302
    assert response.location == 'http://localhost/eskaerak'
    
    
    
    
   