import json

from flask import Blueprint, request
from flask_login import login_required, current_user

from app.handlers import (
    handle_new_recursive_budget,
    handle_new_occasional_budget,
    handle_upsert_cost,
    handle_cost_deleting
)
from app.utils import post_mapping

bp = Blueprint("budget_bp", __name__)


@bp.route("/user", methods=['GET'])
@login_required
@post_mapping(payload_type='JSON')
def user_resource():
    payload = {"username": current_user.name}
    return payload


@bp.route("/budgets", methods=['GET'])
@login_required
@post_mapping(payload_type='JSON')
def list_budgets():
    budgets = list(current_user.budgets)
    return {'budgets': budgets}


@bp.route("/budget/<budget_id>/costs", methods=['GET'])
@login_required
@post_mapping(payload_type='JSON')
def list_costs(budget_id):
    budget = current_user.get_budget_by_id(budget_id)
    return list(budget.costs)


@bp.route("/cost/<cost_id>", methods=['GET'])
@login_required
@post_mapping(payload_type='JSON')
def delete_cost(cost_id):
    return handle_cost_deleting(cost_id)


@bp.route("/budget/<budget_id>/costs", methods=['POST'])
@login_required
@post_mapping(payload_type='JSON')
def update_costs(budget_id):
    req = json.loads(request.data)
    response = None
    for r in req:
        response = handle_upsert_cost(budget_id, **r)
        if not response.result:
            break
    return response


@bp.route("/budget/occasional", methods=['POST'])
@login_required
@post_mapping(payload_type='JSON')
def new_occasional_budget():
    req = json.loads(request.data)
    result = handle_new_occasional_budget(**req)
    return result


@bp.route("/budget/recursive", methods=['POST'])
@login_required
@post_mapping(payload_type='JSON')
def new_recursive_budget():
    req = json.loads(request.data)
    result = handle_new_recursive_budget(**req)
    return result
