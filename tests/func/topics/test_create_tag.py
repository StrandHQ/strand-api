import pytest

from tests.resources.MutationGenerator import MutationGenerator


class TestCreateTag:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, tag_factory):
        tag = tag_factory.build()

        mutation = MutationGenerator.create_tag(name=tag.name)
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTag'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, tag_factory):
        tag = tag_factory.build()

        mutation = MutationGenerator.create_tag(name=tag.name)
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200, response.content
        assert response.json()['data']['createTag']['tag']['name'] == tag.name
