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

