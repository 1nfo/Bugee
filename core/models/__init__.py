from .budget import Budget
from .cost import Cost
from .user import User

all_models = {User, Budget, Cost}

__all__ = ['User', 'Budget', 'Cost']


def create_all_tables():
    from .base import DATABASE
    with DATABASE:
        DATABASE.create_tables(all_models)


create_all_tables()
