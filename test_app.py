from app import app

def test_contact_form():
    with app.test_client() as client:
        response = client.get("/contact")
        assert response.status_code == 200