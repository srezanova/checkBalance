import graphene
from graphql_auth.schema import MeQuery, UserQuery
from graphql_auth import mutations

import budget.schema
import budget.mutations



class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(MeQuery, UserQuery, budget.schema.Query, graphene.ObjectType):
    pass

class Mutation(AuthMutation, budget.mutations.Mutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)
