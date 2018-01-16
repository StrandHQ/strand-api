import pytest


class TestCreateUser:

    @pytest.mark.django_db
    def test_create_user_unauthenticated(self, client, user_factory):
        user = user_factory.build()
        mutation = f'''
          mutation {{
            createUser(input: {{email: "{user.email}", username: "{user.username}"}}) {{
              user {{
                username
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_user(self, auth_client, user_factory):
        user = user_factory.build()

        mutation = f'''
          mutation {{
            createUser(input: {{email: "{user.email}", username: "{user.username}"}}) {{
              user {{
                username
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser']['user']['username'] == user.username
