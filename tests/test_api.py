import pytest
import os
from unittest.mock import patch, MagicMock
from app import create_app
from config import Config

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_post_ips_missing_token(client):
    """Testa criação sem passar token retorna 401"""
    response = client.post('/ips', json={"ip": "8.8.8.8"})
    assert response.status_code == 401
    assert b"Token est\xc3\xa1 faltando" in response.data or b"Token est" in response.data

def test_post_ips_invalid_token(client):
    """Testa criação com token errado retorna 401"""
    headers = {"Authorization": "Bearer token_falso"}
    response = client.post('/ips', json={"ip": "8.8.8.8"}, headers=headers)
    assert response.status_code == 401

@patch('app.routes.ip_routes.create_ip')
def test_post_ips_success(mock_create_ip, client):
    """Testa chamada de criação mockando o banco/api retorna 201"""
    mock_create_ip.return_value = {"ip": "8.8.8.8", "data": {"country": "US"}}
    
    headers = {"Authorization": f"Bearer {Config.SECRET_TOKEN}"}
    response = client.post('/ips', json={"ip": "8.8.8.8"}, headers=headers)
    
    assert response.status_code == 201
    assert response.get_json()["ip"] == "8.8.8.8"

@patch('app.routes.ip_routes.get_ips')
def test_get_ips_success(mock_get_ips, client):
    """Testa listagem paginada mockando o controller"""
    mock_get_ips.return_value = [{"ip": "8.8.8.8", "data": {}}]
    
    headers = {"Authorization": f"Bearer {Config.SECRET_TOKEN}"}
    response = client.get('/ips?page=1&limit=5', headers=headers)
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["page"] == 1
    assert json_data["limit"] == 5
    assert len(json_data["results"]) == 1
    assert json_data["results"][0]["ip"] == "8.8.8.8"
