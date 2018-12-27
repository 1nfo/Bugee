from peewee import Check
from peewee import ForeignKeyField, DateField, DecimalField, TextField

from core.models.base import Model
from core.models.budget import Budget


class Cost(Model):
    budget = ForeignKeyField(Budget)
    amount = DecimalField(decimal_places=2, auto_round=True)
    cost_date = DateField()
    note = TextField(default='')

    attr_list = Model.attr_list + ('amount', 'cost_date', 'note')

    def __str__(self):
        return '$%s %s' % (self.amount, str(self.cost_date))
