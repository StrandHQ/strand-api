import graphene

from app.api.authorization import check_authorization
from app.topics.models import Discussion
from app.topics.types import (
    TopicType,
    TopicInputType,
    DiscussionType,
    DiscussionInputType,
    TagType,
    TagInputType,
    MarkDiscussionAsPendingClosedInputType,
    CloseDiscussionInputType)
from app.topics.validators import TopicValidator, DiscussionValidator, TagValidator


class CreateTopicMutation(graphene.Mutation):
    class Arguments:
        input = TopicInputType(required=True)

    topic = graphene.Field(TopicType)

    @check_authorization
    def mutate(self, info, input):
        tags = input.pop('tags', [])

        topic_validator = TopicValidator(data=input)
        topic_validator.is_valid(raise_exception=True)
        topic = topic_validator.save()

        topic.add_or_create_tags(tags)

        return CreateTopicMutation(topic=topic)


class CreateDiscussionMutation(graphene.Mutation):
    class Arguments:
        input = DiscussionInputType(required=True)

    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        discussion_validator = DiscussionValidator(data=input)
        discussion_validator.is_valid(raise_exception=True)
        discussion = discussion_validator.save()

        return CreateDiscussionMutation(discussion=discussion)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    @check_authorization
    def mutate(self, info, input):
        tag_validator = TagValidator(data=input)
        tag_validator.is_valid(raise_exception=True)
        tag = tag_validator.save()

        return CreateTagMutation(tag=tag)


class MarkDiscussionAsPendingClosed(graphene.Mutation):
    class Arguments:
        input = MarkDiscussionAsPendingClosedInputType(required=True)

    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        discussion = Discussion.objects.get(pk=input['id'])

        discussion.standby_to_auto_close()

        return MarkDiscussionAsPendingClosed(discussion=discussion)


class CloseDiscussionMutation(graphene.Mutation):
    class Arguments:
        input = CloseDiscussionInputType(required=True)

    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        discussion = Discussion.objects.get(pk=input['id'])

        discussion.mark_as_closed()
        discussion.save()

        return CloseDiscussionMutation(discussion=discussion)


class Mutation(graphene.ObjectType):
    create_topic = CreateTopicMutation.Field()
    create_discussion = CreateDiscussionMutation.Field()
    create_tag = CreateTagMutation.Field()

    mark_discussion_as_pending_closed = MarkDiscussionAsPendingClosed.Field()
    close_discussion = CloseDiscussionMutation.Field()
