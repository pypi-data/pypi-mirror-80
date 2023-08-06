import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ()


class PaymentCommandRank(IntFlag):
    CREATE_PAGE = 149
    LIST_PAGES = 151
    FETCH_PAGE = 157
    UPDATE_PAGE = 163
    CHECK_SLUG_AVAILABILITY = 167
    ADD_PRODUCTS = 173


def create_page_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_PAGE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_pages_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_REFUNDS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def fetch_page_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    slug = data.get('reference') or data.get('page_id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.FETCH_PAGE_URL)
    url += f'{slug}'
    return requests.get(url=url, headers=bdo.header)


def update_page_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    slug = data.get('reference') or data.get('page_id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.FETCH_PAGE_URL)
    url += f'{slug}'
    if 'reference' in data:
        del data['reference']
    elif 'page_id' in data:
        del data['page_id']
    elif 'slug' in data:
        del data['slug']
    return requests.put(url=url, data=json.dumps(data), headers=bdo.header)


def check_slug_availability_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    slug = data.get('reference') or data.get('page_id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.CHECK_SLUG_AVAILABILITY_URL)
    url += f'{slug}'
    return requests.get(url, headers=bdo.header)


def add_products_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    slug = data.get('reference') or data.get('page_id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.ADD_PRODUCTS_URL)
    url += f'{slug}/product/'
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


create_page = Command(cmd=create_page_cmd, group=PayStackGatewayFlag.PAYMENT_PAGES,
                      rank=PaymentCommandRank.CREATE_PAGE, label=None)
list_pages = Command(cmd=list_pages_cmd, group=PayStackGatewayFlag.PAYMENT_PAGES,
                     rank=PaymentCommandRank.LIST_PAGES, label=None)
fetch_page = Command(cmd=fetch_page_cmd, group=PayStackGatewayFlag.PAYMENT_PAGES,
                     rank=PaymentCommandRank.FETCH_PAGE, label=None)
update_page = Command(cmd=update_page_cmd, group=PayStackGatewayFlag.PAYMENT_PAGES,
                      rank=PaymentCommandRank.UPDATE_PAGE, label=None)
check_slug_availability = Command(cmd=check_slug_availability_cmd,
                                  group=PayStackGatewayFlag.PAYMENT_PAGES,
                                  rank=PaymentCommandRank.CHECK_SLUG_AVAILABILITY, label=None)
add_products = Command(cmd=add_products_cmd, group=PayStackGatewayFlag.PAYMENT_PAGES,
                       rank=PaymentCommandRank.ADD_PRODUCTS, label=None)
