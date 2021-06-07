import graphene
import budget.schema
from graphene_django import DjangoObjectType, DjangoListField
import accounts.schema
import graphql_jwt

class Query(accounts.schema.Query, budget.schema.Query, graphene.ObjectType):
    pass

class Mutation(accounts.schema.Mutation, budget.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)