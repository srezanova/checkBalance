import graphene
from graphql_auth import mutations

import budget.schema
import budget.mutations
import users.schema


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    login = mutations.ObtainJSONWebToken.Field()


class Query(users.schema.Query, budget.schema.Query, graphene.ObjectType):
    pass


class Mutation(AuthMutation, budget.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
