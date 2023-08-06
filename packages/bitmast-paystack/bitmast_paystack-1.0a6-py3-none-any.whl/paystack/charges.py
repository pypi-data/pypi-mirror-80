import json
from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, \
    PayStackRestUrl

__all__ = ('transaction_charge', 'submit_pin', 'submit_otp', 'submit_phone',
           'submit_birthday', 'check_pending_charge', 'initiate_bulk_charge',
           'list_bulk_charges', 'fetch_bulk_charge_batch', 'fetch_bulk_charges_in_batch',
           'pause_bulk_charge_batch', 'resume_bulk_charge_batch')


class ChargesCommandRank(IntFlag):
    CHARGE = 379
    SUBMIT_PIN = 383
    SUBMIT_OTP = 389
    SUBMIT_PHONE = 397
    SUBMIT_BIRTHDAY = 401
    CHECK_PENDING_CHARGE = 409


class BulkChargeCommandRank(IntFlag):
    INITIATE_BULK_CHARGE = 331
    LIST_BULK_CHARGES = 337
    FETCH_BULK_CHARGE_BATCH = 347
    FETCH_BULK_CHARGES_IN_BATCH = 349
    PAUSE_BULK_CHARGE_BATCH = 353
    RESUME_BULK_CHARGE_BATCH = 359


def charge_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.CHARGE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def submit_pin_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.SUBMIT_PIN_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def submit_otp_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.SUBMIT_OTP_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def submit_phone_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.SUBMIT_PHONE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def submit_birthday_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.SUBMIT_BIRTHDAY_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def check_pending_charge_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    reference = bdo.data()
    url = bdo.url(PayStackRestUrl.CHECK_PENDING_CHARGE_URL)
    url += f'{reference}/'
    return requests.post(url=url, headers=bdo.header)


def initiate_bulk_charge_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    data = bdo.data()
    url = bdo.url(PayStackRestUrl.INITIATE_BULK_CHARGE_URL)
    return requests.post(url=url, data=json.dumps(data), headers=bdo.header)


def list_bulk_charges_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.LIST_BULK_CHARGES_URL)
    return requests.post(url=url, params=query, headers=bdo.header)


def fetch_bulk_charge_batch_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_BULK_CHARGE_BATCH_URL)
    url += f'{query}'
    return requests.post(url=url, headers=bdo.header)


def fetch_bulk_charges_in_batch_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.FETCH_BULK_CHARGES_IN_BATCH_URL)
    return requests.post(url=url, params=query, headers=bdo.header)


def pause_bulk_charge_batch_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.PAUSE_BULK_CHARGE_BATCH_URL)
    url += f'{query}'
    return requests.post(url=url, headers=bdo.header)


def resume_bulk_charge_batch_cmd(**kwargs) -> Any:
    bdo = BusinessDataObject(**kwargs)
    query = bdo.data()
    url = bdo.url(PayStackRestUrl.RESUME_BULK_CHARGE_BATCH_URL)
    url += f'{query}'
    return requests.post(url=url, headers=bdo.header)


transaction_charge = Command(cmd=charge_cmd, group=PayStackGatewayFlag.CHARGE,
                             rank=ChargesCommandRank.CHARGE, label=None)
submit_pin = Command(cmd=submit_otp_cmd, group=PayStackGatewayFlag.CHARGE,
                     rank=ChargesCommandRank.SUBMIT_PIN, label=None)
submit_otp = Command(cmd=submit_otp_cmd, group=PayStackGatewayFlag.CHARGE,
                     rank=ChargesCommandRank.SUBMIT_OTP, label=None)
submit_phone = Command(cmd=submit_phone_cmd, group=PayStackGatewayFlag.CHARGE,
                       rank=ChargesCommandRank.SUBMIT_PHONE, label=None)
submit_birthday = Command(cmd=submit_birthday_cmd, group=PayStackGatewayFlag.CHARGE,
                          rank=ChargesCommandRank.SUBMIT_BIRTHDAY, label=None)
check_pending_charge = Command(cmd=check_pending_charge_cmd, group=PayStackGatewayFlag.CHARGE,
                               rank=ChargesCommandRank.CHECK_PENDING_CHARGE, label=None)

initiate_bulk_charge = Command(cmd=initiate_bulk_charge_cmd,
                               group=PayStackGatewayFlag.BULK_CHARGES,
                               rank=BulkChargeCommandRank.INITIATE_BULK_CHARGE, label=None)
list_bulk_charges = Command(cmd=list_bulk_charges_cmd,
                            group=PayStackGatewayFlag.BULK_CHARGES,
                            rank=BulkChargeCommandRank.LIST_BULK_CHARGES, label=None)
fetch_bulk_charge_batch = Command(cmd=fetch_bulk_charge_batch_cmd,
                                  group=PayStackGatewayFlag.BULK_CHARGES,
                                  rank=BulkChargeCommandRank.FETCH_BULK_CHARGE_BATCH,
                                  label=None)
fetch_bulk_charges_in_batch = Command(cmd=fetch_bulk_charges_in_batch_cmd,
                                      group=PayStackGatewayFlag.BULK_CHARGES,
                                      rank=BulkChargeCommandRank.FETCH_BULK_CHARGES_IN_BATCH,
                                      label=None)
pause_bulk_charge_batch = Command(cmd=pause_bulk_charge_batch_cmd,
                                  group=PayStackGatewayFlag.BULK_CHARGES,
                                  rank=BulkChargeCommandRank.PAUSE_BULK_CHARGE_BATCH,
                                  label=None)
resume_bulk_charge_batch = Command(cmd=resume_bulk_charge_batch_cmd,
                                   group=PayStackGatewayFlag.BULK_CHARGES,
                                   rank=BulkChargeCommandRank.RESUME_BULK_CHARGE_BATCH,
                                   label=None)
