import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_plan', 'list_plans', 'update_plan', 'fetch_plan')


class PlanCommandRank(IntFlag):
    CREATE_PLAN = 79
    LIST_PLANS = 83
    FETCH_PLAN = 89
    UPDATE_PLAN = 97


def create_plan_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_PLAN_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_plans_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_PLANS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def fetch_plan_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_PRODUCT_URL)
    plan_id = data.get('plan_id') or data.get('id') or data.get('slug')
    url += f'{plan_id}'
    return requests.post(url=url, headers=bdo.header)


def update_plan_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    plan_id = data.get('plan_id') or data.get('id')
    url = bdo.url(PayStackRestUrl.UPDATE_PRODUCT_URL)
    url += f'{plan_id}'
    if 'plan_id' in data:
        del data['plan_id']
    elif 'id' in data:
        del data['id']
    elif 'slug' in data:
        del data['slug']
    return requests.put(url=url, data=json.dumps(data), headers=bdo.header)


create_plan = Command(cmd=create_plan_cmd, group=PayStackGatewayFlag.PLANS,
                      rank=PlanCommandRank.CREATE_PLAN, label=None)
list_plans = Command(cmd=list_plans_cmd, group=PayStackGatewayFlag.PLANS,
                     rank=PlanCommandRank.LIST_PLANS, label=None)
fetch_plan = Command(cmd=fetch_plan_cmd, group=PayStackGatewayFlag.PLANS,
                     rank=PlanCommandRank.FETCH_PLAN, label=None)
update_plan = Command(cmd=update_plan_cmd, group=PayStackGatewayFlag.PLANS,
                      rank=PlanCommandRank.UPDATE_PLAN, label=None)
