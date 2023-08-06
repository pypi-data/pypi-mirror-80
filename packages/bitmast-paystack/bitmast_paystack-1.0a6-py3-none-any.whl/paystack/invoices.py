import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('create_invoice', 'list_invoices', 'view_invoice', 'verify_invoice',
           'send_notification', 'invoice_metrics', 'finalize_draft', 'update_invoice',
           'archive_invoice', 'mark_as_paid')


class InvoiceCommandRank(IntFlag):
    CREATE_INVOICE = 179
    LIST_INVOICES = 181
    VIEW_INVOICE = 191
    VERIFY_INVOICE = 193
    SEND_NOTIFICATION = 197
    INVOICE_METRICS = 199
    FINALIZE_DRAFT = 211
    FETCH_INVOICE = 223
    UPDATE_INVOICE = 227
    ARCHIVE_INVOICE = 229
    MARK_AS_PAID = 233


def create_invoice_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CREATE_INVOICE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_invoices_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_INVOICES_URL, params=query)
    return requests.get(url=url, headers=bdo.header)


def view_invoice_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.VIEW_INVOICE_URL)
    url += f'{query}'
    return requests.get(url=url, headers=bdo.header)


def verify_invoice_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.VERIFY_INVOICE_URL)
    url += f'{query}'
    return requests.get(url=url, headers=bdo.header)


def send_notification_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.SEND_NOTIFICATION_URL)
    url += f'{query}'
    return requests.post(url=url, headers=bdo.header)


def invoice_metrics_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.INVOICE_METRICS_URL)
    url += f'{query}'
    return requests.get(url=url, headers=bdo.header)


def finalize_draft_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    invoice_id = data.get('invoice_id') or data.get('id')
    url = bdo.url(PayStackRestUrl.FINALIZE_DRAFT_URL)
    url += f'{invoice_id}'
    if 'invoice_id' in data:
        del data['invoice_id']
    elif 'id' in data:
        del data['id']
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def update_invoice_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    invoice_id = data.get('invoice_id') or data.get('id')
    url = bdo.url(PayStackRestUrl.UPDATE_INVOICE_URL)
    url += f'{invoice_id}'
    if 'invoice_id' in data:
        del data['invoice_id']
    elif 'id' in data:
        del data['id']
    return requests.put(url=url, data=json.dumps(data), headers=bdo.header)


def archive_invoice_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.ARCHIVE_INVOICE_URL)
    url += f'{query}'
    return requests.post(url=url, headers=bdo.header)


def mark_as_paid_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    invoice_id = data.get('invoice_id') or data.get('id')
    url = bdo.url(PayStackRestUrl.MARK_AS_PAID_URL)
    url += f'{invoice_id}'
    if 'invoice_id' in data:
        del data['invoice_id']
    elif 'id' in data:
        del data['id']
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


create_invoice = Command(cmd=create_invoice_cmd, group=PayStackGatewayFlag.INVOICES,
                         rank=InvoiceCommandRank.CREATE_INVOICE, label=None)
list_invoices = Command(cmd=list_invoices_cmd, group=PayStackGatewayFlag.INVOICES,
                        rank=InvoiceCommandRank.LIST_INVOICES, label=None)
view_invoice = Command(cmd=view_invoice_cmd, group=PayStackGatewayFlag.INVOICES,
                       rank=PayStackGatewayFlag.INVOICES, label=None)
verify_invoice = Command(cmd=verify_invoice_cmd, group=PayStackGatewayFlag.INVOICES,
                         rank=InvoiceCommandRank.VERIFY_INVOICE, label=None)
send_notification = Command(cmd=send_notification_cmd, group=PayStackGatewayFlag.INVOICES,
                            rank=InvoiceCommandRank.SEND_NOTIFICATION, label=None)
invoice_metrics = Command(cmd=invoice_metrics_cmd, group=PayStackGatewayFlag.INVOICES,
                          rank=InvoiceCommandRank.INVOICE_METRICS, label=None)
finalize_draft = Command(cmd=finalize_draft_cmd, group=PayStackGatewayFlag.INVOICES,
                         rank=InvoiceCommandRank.FINALIZE_DRAFT, label=None)
update_invoice = Command(cmd=update_invoice_cmd, group=PayStackGatewayFlag.INVOICES,
                         rank=InvoiceCommandRank.UPDATE_INVOICE, label=None)
archive_invoice = Command(cmd=archive_invoice_cmd, group=PayStackGatewayFlag.INVOICES,
                          rank=InvoiceCommandRank.ARCHIVE_INVOICE, label=None)
mark_as_paid = Command(cmd=mark_as_paid_cmd, group=PayStackGatewayFlag.INVOICES,
                       rank=InvoiceCommandRank.MARK_AS_PAID, label=None)
