import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_subscription', 'list_subscriptions', 'fetch_subscription',
           'disable_subscription', 'enable_subscription')


class SubscriptionCommandRank(IntFlag):
    CREATE_SUBSCRIPTION = 101
    LIST_SUBSCRIPTIONS = 103
    FETCH_SUBSCRIPTION = 107
    DISABLE_SUBSCRIPTION = 109
    ENABLE_SUBSCRIPTION = 113


def create_subscription_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_SUBSCRIPTION_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_subscriptions_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_SUBSCRIPTIONS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def fetch_subscription_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_SUBSCRIPTION_URL)
    subscription_id = data.get('subscription_id') or data.get('id') or data.get('slug')
    url += f'{subscription_id}'
    return requests.post(url=url, headers=bdo.header)


def configure_subscription_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.DISABLE_SUBSCRIPTION_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


create_subscription = Command(cmd=create_subscription_cmd,
                              group=PayStackGatewayFlag.SUBSCRIPTIONS,
                              rank=SubscriptionCommandRank.CREATE_SUBSCRIPTION, label=None)
list_subscriptions = Command(cmd=list_subscriptions_cmd,
                             group=PayStackGatewayFlag.SUBSCRIPTIONS,
                             rank=SubscriptionCommandRank.LIST_SUBSCRIPTIONS, label=None)
fetch_subscription = Command(cmd=fetch_subscription_cmd, group=PayStackGatewayFlag.PRODUCTS,
                             rank=SubscriptionCommandRank.FETCH_SUBSCRIPTION, label=None)
disable_subscription = Command(cmd=configure_subscription_cmd,
                               group=PayStackGatewayFlag.PRODUCTS,
                               rank=SubscriptionCommandRank.DISABLE_SUBSCRIPTION, label=None)
enable_subscription = Command(cmd=configure_subscription_cmd,
                              group=PayStackGatewayFlag.PRODUCTS,
                              rank=SubscriptionCommandRank.ENABLE_SUBSCRIPTION, label=None)
