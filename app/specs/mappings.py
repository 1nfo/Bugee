login = {
    'key_mappings': {
        'username': 'username',
        'password': 'password',
        'remember_me': 'remember_me',
    }
}

new_recursive_budget = {
    'key_mappings': {
        'budget_name': 'budgetName',
        'amount': 'amount',
        'start_date': 'startdate',
        'delta': {'timeunit': 'howlong'}
    },
    'value_mappings': {
        'budget_name': 'str',
        'amount': 't_decimal',
        'start_date': 't_date',
        'delta': 't_delta'
    }
}

new_occasional_budget = {
    'key_mappings': {
        'budget_name': 'budgetName',
        'amount': 'amount',
        'start_date': 'startdate',
        'end_date': 'enddate'
    },
    'value_mappings': {
        'budget_name': 'str',
        'amount': 't_decimal',
        'start_date': 't_date',
        'end_date': 't_date'
    }
}

upsert_costs = {
    'key_mappings': {
        'cost_id': 'id',
        'amount': 'amount',
        'cost_date': 'date',
        'note': 'note'
    },
    'value_mappings': {
        'cost_id': 't_nullable_id',
        'amount': 't_decimal',
        'cost_date': 't_date_string',
        'note': 'str'
    }
}
