from datetime import datetime
import pytz

import pytest


class TestCreateReplyFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, slack_event_factory,
                             slack_user_factory, message_factory, reply_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)
        message_slack_user = slack_user_factory()
        message = message_factory(discussion=slack_channel.discussion,
                                  author=message_slack_user.user)
        message_slack_event = slack_event_factory(message=message)

        reply_slack_user = slack_user_factory()
        reply = reply_factory.build(message=message, author=reply_slack_user.user)
        reply_slack_event = slack_event_factory.build()

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, discussion_factory, slack_channel_factory, slack_event_factory,
                                   slack_user_factory, message_factory, reply_factory):
        discussion = discussion_factory(topic__is_private=False)
        slack_channel = slack_channel_factory.build()

        message_slack_user = slack_user_factory()
        message = message_factory(discussion=discussion,
                                  author=message_slack_user.user)
        message_slack_event = slack_event_factory(message=message)

        reply_slack_user = slack_user_factory()
        reply = reply_factory.build(message=message, author=reply_slack_user.user)
        reply_slack_event = slack_event_factory.build()

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, slack_channel_factory, slack_event_factory,
                                slack_user_factory, message_factory, reply_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        message_slack_user = slack_user_factory()
        message = message_factory(discussion=slack_channel.discussion,
                                  author=message_slack_user.user)
        message_slack_event = slack_event_factory(message=message)

        reply_slack_user = slack_user_factory.build()
        reply = reply_factory.build(message=message, author=reply_slack_user.user)
        reply_slack_event = slack_event_factory.build()

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_create_invalid_message_slack_event(self, auth_client, slack_channel_factory,
                                                slack_event_factory, slack_user_factory,
                                                message_factory, reply_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        message_slack_user = slack_user_factory()
        message = message_factory(discussion=slack_channel.discussion,
                                  author=message_slack_user.user)
        message_slack_event = slack_event_factory.build()

        reply_slack_user = slack_user_factory()
        reply = reply_factory.build(message=message, author=reply_slack_user.user)
        reply_slack_event = slack_event_factory.build()

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_channel_factory, slack_event_factory, slack_user_factory,
                   message_factory, reply_factory):
        slack_channel = slack_channel_factory(discussion__topic__is_private=False)

        message_slack_user = slack_user_factory()
        message = message_factory(discussion=slack_channel.discussion,
                                  author=message_slack_user.user)
        message_slack_event = slack_event_factory(message=message)

        reply_slack_user = slack_user_factory()
        reply = reply_factory.build(message=message, author=reply_slack_user.user)
        reply_slack_event = slack_event_factory.build()

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                time
                message {{
                  author {{
                    id
                  }}
                  discussion {{
                    participants {{
                      id
                    }}
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack']['reply']['time'] == \
            datetime.fromtimestamp(int(reply_slack_event.ts), tz=pytz.utc).isoformat()
        assert response.json()['data']['createReplyFromSlack']['reply']['message']['author']['id'] == \
            str(message.author.id)
        assert {'id': str(reply_slack_user.user.id)} in response.json()['data']['createReplyFromSlack']['reply'][
            'message']['discussion']['participants']
