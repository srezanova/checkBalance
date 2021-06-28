import pytest

from checkBalance.data import initialize
from checkBalance.schema import schema


@pytest.mark.django_db
def test_user():
    initialize()
    query = """
      query {
        categories {
          group
          name
        }
      }
    """
    expected = {
        "categories": {"group": "Expense", "name": "Netflix"}
    }
    result = schema.execute(query)
    assert not result.errors
    assert result.data == expected

