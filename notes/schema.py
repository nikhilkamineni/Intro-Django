from graphene_django import DjangoObjectType
import graphene
from .models import PersonalNote as PersonalNoteModel


class PersonalNote(DjangoObjectType):
    """Describe which model we want to expose through GraphQL"""
    class Meta:
        model = PersonalNoteModel

        # Describe the data as a node in a graph for GraphQL
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    """Describe which records we want to show"""
    personalnotes = graphene.List(PersonalNote)

    def resolve_personalnotes(self, info):
        """Decide what notes to return."""
        user = info.context.user

        if user.is_anonymous:
            return PersonalNoteModel.objects.none()
        else:
            return PersonalNoteModel.objects.filter(user=user)


schema = graphene.Schema(query=Query)
