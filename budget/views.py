from django.utils.functional import cached_property
from graphene_django.views import GraphQLView
from .loaders import TransactionByCategoryLoader, CategoryByTransactionLoader

class GQLContext:

    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def transactions_by_category_id_loader(self):
        return TransactionByCategoryLoader()

    @cached_property
    def  categories_by_transaction_ids_loader(self):
        return CategoryByTransactionLoader()

class CustomGraphQLView(GraphQLView):

    def get_context(self, request):
        return GQLContext(request)