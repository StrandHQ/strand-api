import graphene
from graphene_django.types import DjangoObjectType

from app.dialogues.models import Message, Reply


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply


class MessageInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    discussion_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)


class ReplyInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    message_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)
