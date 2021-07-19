import graphene
from graphql_auth.schema import MeQuery
from graphql_auth import mutations

import budget.schema
import budget.mutations



class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()

    # django-graphql-jwt inheritances
    login = mutations.ObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()


class Query(MeQuery, budget.schema.Query, graphene.ObjectType):
    pass

class Mutation(AuthMutation, budget.mutations.Mutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
