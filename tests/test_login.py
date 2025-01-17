import pytest
from controller.pagina_kontrola import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client, mocker):
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzailea_logeatu', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzaileaOnartua', return_value=1)
    mocker.patch('controller.erabiltzaile_kudeaketa.Erabiltzailea.adminDa', return_value=False)

    response = client.post('/submit_login', data={'posta': 'test@example.com', 'password': 'correct_password'})
    assert response.status_code == 302
    assert response.location == 'http://localhost/home_loged'

def test_login_incorrect_password(client, mocker):
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzailea_logeatu', return_value=False)

    response = client.post('/submit_login', data={'posta': 'test@example.com', 'password': 'wrong_password'})
    assert response.status_code == 302
    assert response.location == 'http://localhost/login?error=Pasahitza%20okerra'

def test_login_unapproved_user(client, mocker):
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzailea_logeatu', return_value=True)
    mocker.patch('controller.erabiltzaile_kudeaketa.erabiltzaileaOnartua', return_value=0)

    response = client.post('/submit_login', data={'posta': 'test@example.com', 'password': 'correct_password'})
    assert response.status_code == 302
    assert response.location == 'http://localhost/login?error=Erabiltzailea%20ez%20dago%20onartuta'