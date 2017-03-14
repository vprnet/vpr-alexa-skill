"""
Tests for VPR's Amazon Alexa Skill
"""
from vpr_alexa.webapp import create_app

app = create_app()
client = app.test_client()

def test_welcome():
    response = client.get('/ask')
    assert response.status_code == 200

