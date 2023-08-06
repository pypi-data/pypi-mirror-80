from enum import IntFlag
import requests
import json
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, PayStackRestUrl, BusinessDataObject
from typing import Any

__all__ = ('create_subaccount', 'list_subaccounts', 'fetch_subaccount', 'update_subaccount',
           'AccountCommandRank')


class AccountCommandRank(IntFlag):
    CREATE = 2
    LIST_SUBACCOUNTS = 3
    FETCH = 5
    UPDATE = 7


class AccountBusinessObject(BusinessDataObject):

    def __init__(self, **kwargs):
        super(AccountBusinessObject, self).__init__(**kwargs)


def create_subaccount_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_SUBACCOUNT_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)
    

def list_subaccount_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query_data = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_SUBACCOUNTS_URL)
    return requests.get(url=url, params=query_data, headers=bdo.header)
    

def fetch_subaccount_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    url = bdo.url(PayStackRestUrl.FETCH_SUBACCOUNT_URL)
    account_id = bdo.data().get('account_id')
    url += f'{account_id}/'
    return requests.get(url=url, headers=bdo.header)


def update_subaccount_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.UPDATE_SUBACCOUNT_URL)
    return requests.put(url, data=json.dumps(data), headers=bdo.header)


create_subaccount = Command(cmd=create_subaccount_cmd, group=PayStackGatewayFlag.SUBACCOUNTS,
                            rank=AccountCommandRank.CREATE, label=None)

list_subaccounts = Command(cmd=list_subaccount_cmd, group=PayStackGatewayFlag.SUBACCOUNTS,
                           rank=AccountCommandRank.LIST_SUBACCOUNTS, label=None)

fetch_subaccount = Command(cmd=fetch_subaccount_cmd, group=PayStackGatewayFlag.SUBACCOUNTS,
                           rank=AccountCommandRank.CREATE, label=None)

update_subaccount = Command(cmd=create_subaccount_cmd,
                            group=PayStackGatewayFlag.SUBACCOUNTS,
                            rank=AccountCommandRank.UPDATE, label=None)
