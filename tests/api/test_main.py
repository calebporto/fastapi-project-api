from fastapi.testclient import TestClient

def test_get_main(client: TestClient) -> None:
    response = client.get('/')
    body = response.json()
    assert response.status_code == 200
    assert body['api_name'] == 'ibvg_api'