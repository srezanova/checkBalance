import graphene
import graphql_jwt

import budget.schema.categories
import budget.schema.transactions
import budget.schema.months
import budget.schema.plans
import budget.mutations.categories
import budget.mutations.transactions
import budget.mutations.months
import budget.mutations.plans
import users.schema
import users.mutations


class AutMutation(users.mutations.Mutation, graphene.ObjectType):
    login = graphql_jwt.ObtainJSONWebToken.Field()


class Query(
        users.schema.Query,
        budget.schema.categories.Query,
        budget.schema.transactions.Query,
        budget.schema.months.Query,
        budget.schema.plans.Query,
        graphene.ObjectType):
    pass


class Mutation(
        AutMutation,
        budget.mutations.plans.Mutation,
        budget.mutations.transactions.Mutation,
        budget.mutations.months.Mutation,
        budget.mutations.categories.Mutation,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
