import pytest


class TestSolveTopicFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, topic_factory, discussion_factory,
                             slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        discussion = discussion_factory(topic=topic)
        slack_channel = slack_channel_factory(discussion=discussion)
        time_end = discussion_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveTopicFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              topic {{
                discussion {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, user_factory, topic_factory, discussion_factory,
                                   slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        discussion = discussion_factory(topic=topic)
        slack_channel = slack_channel_factory.build(discussion=discussion)
        time_end = discussion_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveTopicFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              topic {{
                discussion {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, user_factory, topic_factory,
                                discussion_factory, slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        discussion = discussion_factory(topic=topic)
        slack_channel = slack_channel_factory(discussion=discussion)
        time_end = discussion_factory.build().time_end
        slack_solver = slack_user_factory.build()

        mutation = f'''
          mutation {{
            solveTopicFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              topic {{
                discussion {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, topic_factory, discussion_factory,
                   slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        discussion = discussion_factory(topic=topic)
        slack_channel = slack_channel_factory(discussion=discussion)
        time_end = discussion_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveTopicFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              topic {{
                discussion {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopicFromSlack']['topic'][
                   'solver']['id'] == str(slack_solver.user.id)
