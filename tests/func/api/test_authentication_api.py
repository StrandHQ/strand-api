import pytest


class TestAPIAuthentication:

    @pytest.mark.django_db
    def test_email_auth(self, user_factory, client):
        user = user_factory()

        data = {'email': user.email, 'password': 'mypass123!'}
        response = client.post('/auth-token', data)

        assert response.status_code == 200, response.content
        assert response.json()['token']

    @pytest.mark.django_db
    def test_username_auth(self, user_factory, client):
        user = user_factory()

        data = {'username': user.username, 'password': 'mypass123!'}
        response = client.post('/auth-token', data)

        assert response.status_code == 400
        assert response.json() == {
            'email': [
                'This field is required.'
            ]
        }
