import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_transfer_recipient', 'list_transfer_recipients',
           'update_transfer_recipient', 'delete_transfer_recipient', 'initiate_transfer',
           'list_transfers', 'fetch_transfer', 'finalize_transfer', 'initiate_bulk_transfer')


class TransferCommandRank(IntFlag):
    CREATE_TRANSFER_RECIPIENT = 241
    LIST_TRANSFER_RECIPIENTS = 251
    UPDATE_TRANSFER_RECIPIENT = 257
    DELETE_TRANSFER_RECIPIENT = 263
    INITIATE_TRANSFER = 269
    LIST_TRANSFERS = 271
    FETCH_TRANSFER = 277
    FINALIZE_TRANSFER = 281
    INITIATE_BULK_TRANSFER = 283


def create_transfer_recipient_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_TRANSFER_RECIPIENT_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_transfer_recipients_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_TRANSFER_RECIPIENTS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def delete_transfer_recipient_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    transfer_recipient_id = data.get('transfer_recipient_id') or data.get('id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.DELETE_TRANSFER_RECIPIENT_URL)
    url += f'{transfer_recipient_id}'
    return requests.delete(url=url, headers=bdo.header)


def update_transfer_recipient_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    transfer_recipient_id = data.get('transfer_recipient_id') or data.get('id') or data.get('slug')
    url = bdo.url(PayStackRestUrl.UPDATE_TRANSFER_RECIPIENT_URL)
    url += f'{transfer_recipient_id}'
    if 'transfer_recipient_id' in data:
        del data['transfer_recipient_id']
    elif 'id' in data:
        del data['id']
    elif 'slug' in data:
        del data['slug']
    return requests.put(url=url, data=json.dumps(data), headers=bdo.header)


def initiate_transfer_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.INITIATE_TRANSFER_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_transfers_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_TRANSFERS_URL)
    return requests.get(url=url, params=query, headers=bdo.header)


def fetch_transfer_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_TRANSFER_URL)
    transfer_id = data.get('transfer_id') or data.get('id') or data.get('slug')
    url += f'{transfer_id}'
    return requests.post(url=url, headers=bdo.header)


def finalize_transfer_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.FINALIZE_TRANSFER_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def initiate_bulk_transfer_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.INITIATE_BULK_TRANSFER_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


create_transfer_recipient = Command(cmd=create_transfer_recipient_cmd,
                                    group=PayStackGatewayFlag.TRANSFER_RECIPIENTS,
                                    rank=TransferCommandRank.CREATE_TRANSFER_RECIPIENT,
                                    label=None)
list_transfer_recipients = Command(cmd=list_transfer_recipients_cmd,
                                   group=PayStackGatewayFlag.TRANSFER_RECIPIENTS,
                                   rank=TransferCommandRank.LIST_TRANSFER_RECIPIENTS,
                                   label=None)
update_transfer_recipient = Command(cmd=update_transfer_recipient_cmd,
                                    group=PayStackGatewayFlag.TRANSFER_RECIPIENTS,
                                    rank=TransferCommandRank.UPDATE_TRANSFER_RECIPIENT,
                                    label=None)
delete_transfer_recipient = Command(cmd=delete_transfer_recipient_cmd,
                                    group=PayStackGatewayFlag.TRANSFER_RECIPIENTS,
                                    rank=TransferCommandRank.DELETE_TRANSFER_RECIPIENT,
                                    label=None)
initiate_transfer = Command(cmd=initiate_transfer_cmd, group=PayStackGatewayFlag.TRANSFERS,
                            rank=TransferCommandRank.INITIATE_TRANSFER,
                            label=None)
list_transfers = Command(cmd=list_transfers_cmd, group=PayStackGatewayFlag.TRANSFERS,
                         rank=TransferCommandRank.LIST_TRANSFERS,
                         label=None)
fetch_transfer = Command(cmd=fetch_transfer_cmd, group=PayStackGatewayFlag.TRANSFERS,
                         rank=TransferCommandRank.FETCH_TRANSFER,
                         label=None)
finalize_transfer = Command(cmd=finalize_transfer_cmd, group=PayStackGatewayFlag.TRANSFERS,
                            rank=TransferCommandRank.FINALIZE_TRANSFER,
                            label=None)
initiate_bulk_transfer = Command(cmd=initiate_bulk_transfer_cmd,
                                 group=PayStackGatewayFlag.TRANSFERS,
                                 rank=TransferCommandRank.INITIATE_BULK_TRANSFER, label=None)
