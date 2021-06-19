from collections import defaultdict
from promise import Promise
from promise.dataloader import DataLoader
from .models import Category, Transaction, Month

class TransactionByCategoryLoader(DataLoader):
    def batch_load_fn(self, category_ids):
        transactions_by_category_ids = defaultdict(list)

        for transaction in Transaction.objects.filter(category_id__in=category_ids).iterator():
            transactions_by_category_ids[transaction.category_id].append(transaction)

        return Promise.resolve([transactions_by_category_ids.get(category_id, []) for category_id in category_ids])

class CategoryByTransactionLoader(DataLoader):
    def batch_load_fn(self, transaction_ids):
        categories_by_transaction_ids = defaultdict(list)

        for category in Category.objects.filter(transaction_id__in=transaction_ids).iterator():
            categories_by_transaction_ids[category.transaction_id].append(category)

        return Promise.resolve([categories_by_transaction_ids.get(transaction_id, []) for transaction_id in transaction_ids])
