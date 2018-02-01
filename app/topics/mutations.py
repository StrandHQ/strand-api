import graphene

from app.api.authorization import check_authorization
from app.topics.models import Topic
from app.topics.validators import TopicValidator, DiscussionValidator, TagValidator
from app.topics.types import (
    TopicType,
    TopicInputType,
    DiscussionType,
    DiscussionInputType,
    SolveTopicInputType,
    TagType,
    TagInputType
)
from app.users.models import User


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


class SolveTopicMutation(graphene.Mutation):
    class Arguments:
        input = SolveTopicInputType(required=True)

    topic = graphene.Field(TopicType)
    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        topic = Topic.objects.get(pk=input['id'])
        solver = User.objects.get(pk=input['solver_id'])

        topic.discussion.mark_as_closed()
        topic.discussion.save()

        topic.mark_as_solved()
        topic.solver = solver
        topic.save()

        return SolveTopicMutation(topic=topic, discussion=topic.discussion)


class Mutation(graphene.ObjectType):
    create_topic = CreateTopicMutation.Field()
    create_discussion = CreateDiscussionMutation.Field()
    create_tag = CreateTagMutation.Field()

    solve_topic = SolveTopicMutation.Field()
