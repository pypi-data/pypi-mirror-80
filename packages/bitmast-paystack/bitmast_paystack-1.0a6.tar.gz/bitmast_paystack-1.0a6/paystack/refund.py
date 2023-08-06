import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_refund', 'list_refunds', 'fetch_refund')


class RefundCommandRank(IntFlag):
    CREATE_REFUND = 419
    LIST_REFUNDS = 421
    FETCH_REFUND = 431


def create_refund_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_REFUND_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_refunds_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_REFUNDS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def fetch_refund_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    transaction_id = data.get('reference') or data.get('transaction_id')
    url = bdo.url(PayStackRestUrl.FETCH_REFUND_URL)
    url += f'{transaction_id}'
    return requests.get(url=url, headers=bdo.header)


create_refund = Command(cmd=create_refund_cmd, group=PayStackGatewayFlag.REFUNDS,
                        rank=RefundCommandRank.CREATE_REFUND, label=None)
list_refunds = Command(cmd=list_refunds_cmd, group=PayStackGatewayFlag.VERIFICATION,
                       rank=RefundCommandRank.LIST_REFUNDS, label=None)
fetch_refund = Command(cmd=fetch_refund_cmd, group=PayStackGatewayFlag.VERIFICATION,
                       rank=RefundCommandRank.FETCH_REFUND, label=None)
