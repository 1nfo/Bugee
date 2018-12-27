from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from peewee import CharField

from .base import Model


class User(Model):
    name = CharField(unique=True)
    password = CharField()

    attr_list = Model.attr_list + ('name',)

    def __str__(self):
        return str(self.name)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def login(self, password: str) -> bool:
        return self.password == password

    def add_recursive_budget(self, budget_name: str, amount: Decimal, start_date: date, delta: relativedelta):
        end_date = start_date + delta
        assert end_date > start_date
        return new_budget(user=self, name=budget_name, amount=amount, time_delta=delta,
                          start_date=start_date, end_date=end_date, recursive=True)

    def add_occasional_budget(self, budget_name: str, amount: Decimal, start_date: date, end_date: date):
        assert end_date > start_date
        return new_budget(user=self, name=budget_name, amount=amount,
                          start_date=start_date, end_date=end_date, recursive=False)

    def get_budget(self, name):
        budget = filter_budget(user=self, name=name, latest=True).get()
        if budget.recursive and not budget.is_active():
            budget.next_recursive()
            return self.get_budget(name)
        else:
            return budget

    def get_budget_by_id(self, bid):
        budget = filter_budget(id=bid).get()
        if budget.recursive and not budget.is_active():
            budget = budget.next_recursive()
            return self.get_budget_by_id(budget.id)
        else:
            return budget

    @property
    def budgets(self):
        return filter_budget(user=self, latest=True)


def new_budget(**kwargs):
    from .budget import Budget
    return Budget.create(**kwargs)


def filter_budget(*arg, **kwargs):
    from .budget import Budget
    return Budget.select().filter(*arg, **kwargs)
