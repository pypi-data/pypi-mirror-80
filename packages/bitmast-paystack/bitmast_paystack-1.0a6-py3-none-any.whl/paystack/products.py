import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_product', 'list_products', 'update_product', 'fetch_product')


class ProductCommandRank(IntFlag):
    CREATE_PRODUCT = 127
    LIST_PRODUCTS = 131
    FETCH_PRODUCT = 137
    UPDATE_PRODUCT = 139


def create_product_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_PRODUCT_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)
    return response or NotImplemented


def list_products_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    url = bdo.url(PayStackRestUrl.LIST_PRODUCTS_URL)
    return requests.get(url=url, headers=bdo.header)


def fetch_product_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_PRODUCT_URL)
    product_id = data.get('product_id') or data.get('id')
    url += f'{product_id}'
    return requests.post(url=url, headers=bdo.header)


def update_product_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    product_id = data.get('product_id') or data.get('id')
    url = bdo.url(PayStackRestUrl.UPDATE_PRODUCT_URL)
    url += f'{product_id}'
    if 'product_id' in data:
        del data['product_id']
    elif 'id' in data:
        del data['id']
    return requests.put(url=url, data=json.dumps(data), headers=bdo.header)


create_product = Command(cmd=create_product_cmd, group=PayStackGatewayFlag.PRODUCTS,
                         rank=ProductCommandRank.CREATE_PRODUCT, label=None)
list_products = Command(cmd=list_products_cmd, group=PayStackGatewayFlag.PRODUCTS,
                        rank=ProductCommandRank.LIST_PRODUCTS, label=None)
fetch_product = Command(cmd=fetch_product_cmd, group=PayStackGatewayFlag.PRODUCTS,
                        rank=ProductCommandRank.FETCH_PRODUCT, label=None)
update_product = Command(cmd=update_product_cmd, group=PayStackGatewayFlag.PRODUCTS,
                         rank=ProductCommandRank.UPDATE_PRODUCT, label=None)
