import peewee

from core.settings import settings

DATABASE = peewee.SqliteDatabase(**{k: v for k, v in settings.db_setting.items()})


class Model(peewee.Model):
    class Meta:
        database = DATABASE

    attr_list = ('id',)

    def __repr__(self):
        return "<{type} {id}>".format(type=self.model_name, id=self.id)

    def to_dict(self):
        members = {k: getattr(self, k) for k in self.attr_list if hasattr(self, k)}
        return {self.model_name: members}

    @property
    def model_name(self):
        return type(self).__name__
