from datetime import date
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from peewee import CharField, ForeignKeyField, BooleanField, DateField, DecimalField, Field
from peewee import Check

from .base import Model, DATABASE
from .user import User


class TimeDeltaField(Field):
    field_type = 'TEXT'

    def db_value(self, value: relativedelta):
        return "{'years':%d,'months':%d,'weeks':%d,'days':%d}" % (value.years, value.months, value.weeks, value.days)

    def python_value(self, value: str):
        d = eval(value)
        return relativedelta(**d)


class Budget(Model):
    user = ForeignKeyField(User)
    name = CharField(constraints=[Check("LENGTH(name)>0")])
    amount = DecimalField(decimal_places=2, auto_round=True, constraints=[Check('amount>0')])
    time_delta = TimeDeltaField(default=relativedelta())
    start_date = DateField()
    end_date = DateField()
    recursive = BooleanField()
    latest = BooleanField(default=True)

    attr_list = Model.attr_list + ('name', 'balance', 'amount', 'start_date', 'end_date', 'recursive', 'time_delta', 'latest')

    def __str__(self):
        return str(self.name)

    def upsert_cost(self, amount: Decimal, cost_date: date, note: str, cost_id: int = None):
        assert self.start_date <= cost_date <= self.end_date
        if cost_id:
            return update_cost(amount=amount, cost_date=cost_date, note=note, cost_id=cost_id)
        return add_cost(budget=self, amount=amount, cost_date=cost_date, note=note)

    @property
    def costs(self):
        return filter_cost(budget=self)

    @property
    def balance(self):
        return lookup_balance(self)

    def is_active(self):
        return self.start_date <= date.today() < self.end_date

    @DATABASE.atomic()
    def next_recursive(self):
        if self.recursive:
            budget = self
            assert date.today() >= self.end_date
            budget.latest = False
            return budget.create(Òuser=budget.user, name=budget.name, amount=budget.amount,
                                 time_delta=budget.time_delta, start_date=budget.end_date,
                                 end_date=budget.end_date + budget.time_delta, recursive=True)
        else:
            raise Exception("not able to recur a non-recursive budget")


def add_cost(**kwargs):
    from .cost import Cost
    return Cost.create(**kwargs)


def filter_cost(*arg, **kwargs):
    from .cost import Cost
    return Cost.select().filter(*arg, **kwargs)


def update_cost(cost_id, **kwargs):
    from .cost import Cost
    return Cost.update(**kwargs).where(Cost.id == cost_id).execute()


def lookup_balance(budget: Budget):
    from .cost import Cost
    costs = Cost.select().where((Cost.budget == budget) &
                                (Cost.cost_date < budget.end_date) &
                                (Cost.cost_date >= budget.start_date))
    return budget.amount - sum(cost.amount for cost in costs)
