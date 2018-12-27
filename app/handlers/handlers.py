import traceback

from flask_login import login_user, current_user

from app.handlers.message import ResponseType, Response
from app.specs import mappings
from app.utils import pre_mapping
from core.models import User, Budget, Cost


@pre_mapping(mappings.login)
def handle_register(username=None, password=None) -> Response:
    if username is None or password is None:
        return Response(False, ResponseType.InvalidInput)
    try:
        user = User.create(name=username, password=password)
    except BaseException as e:
        return Response(False, ResponseType.InvalidData, e)
    return Response(True, ResponseType.Success, user)


@pre_mapping(mappings.login)
def handle_login(username=None, password=None, remember_me=False) -> Response:
    if username is None or password is None:
        return Response(False, ResponseType.InvalidInput)
    user = User.get_or_none(name=username)
    if user is None:
        return Response(False, ResponseType.UsernameNotExists)
    if not user.login(password):
        return Response(False, ResponseType.IncorrectPassword)
    try:
        login_user(user, remember=remember_me)
    except BaseException as e:
        return Response(False, ResponseType.InvalidData, e)
    return Response(True, ResponseType.Success)


@pre_mapping(mappings.new_occasional_budget, handler=User.add_occasional_budget)
def handle_new_occasional_budget(**kwargs):
    try:
        budget = current_user.add_occasional_budget(**kwargs)
    except Exception as e:
        # TODO trackback
        traceback.print_tb(e.__traceback__)
        traceback.format_exc()
        result = Response(False, ResponseType.InvalidData, traceback.format_exc())
    else:
        # TODO
        print("Created budget: %d" % budget.id)
        result = Response(True, ResponseType.Success, budget)
    return result


@pre_mapping(mappings.new_recursive_budget, handler=User.add_recursive_budget)
def handle_new_recursive_budget(**kwargs):
    try:
        budget = current_user.add_recursive_budget(**kwargs)
    except Exception as e:
        # TODO tracback?
        traceback.print_tb(e.__traceback__)
        result = Response(False, ResponseType.InvalidData, traceback.format_exc())
    else:
        # TODO
        print("Created budget: %d" % budget.id)
        result = Response(True, ResponseType.Success, budget)
    return result


@pre_mapping(mappings.upsert_costs, handler=Budget.upsert_cost)
def handle_upsert_cost(budget_id, **kwargs):
    try:
        budget = current_user.get_budget_by_id(budget_id)
        res = budget.upsert_cost(**kwargs)
        assert res
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        result = Response(False, ResponseType.InvalidData, traceback.format_exc())
    else:
        result = Response(True, ResponseType.Success)
    return result


def handle_cost_deleting(cost_id):
    try:
        res = Cost.delete().where(Cost.id == cost_id).execute()
        assert res
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        result = Response(False, ResponseType.InvalidData, traceback.format_exc())
    else:
        result = Response(True, ResponseType.Success)
    return result


def handle_user_loading(user_id):
    return User.get(id=user_id)
