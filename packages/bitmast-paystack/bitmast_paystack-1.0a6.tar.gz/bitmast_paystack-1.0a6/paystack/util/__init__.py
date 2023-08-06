from enum import IntFlag, Enum
from typing import Any, Sequence, Mapping
from datetime import datetime
import sys
import re
from functools import singledispatch
from paystack.config import ConfigManager
from functools import wraps
import logging
import json
from paystack.errors import PyPayStackError


class TransactionChannelFlag(IntFlag):
    CARD = 2
    BANK = 3
    CARD_OR_BANK = 5
    USSD = 7


class ApprovedCurrenciesFlag(IntFlag):
    NGN = 2
    USD = 3
    EUR = 5
    GBP = 7


class PayStackGatewayFlag(IntFlag):
    TRANSACTIONS = 2
    CUSTOMERS = 3
    SUBACCOUNTS = 5
    PLANS = 7
    SUBSCRIPTIONS = 11
    PRODUCTS = 13
    PAYMENT_PAGES = 17
    INVOICES = 23
    SETTLEMENTS = 29
    TRANSFER_RECIPIENTS = 31
    TRANSFERS = 37
    TRANSFERS_CONTROL = 41
    BULK_CHARGES = 43
    CONTROL_PANEL = 47
    CHARGE = 53
    REFUNDS = 59
    VERIFICATION = 61
    MISCELLANEOUS = 67


class PayStackRestUrl(Enum):
    INITIALIZE_TRANSACTION_URL = r'https://api.paystack.co/transaction/initialize/'
    VERIFY_TRANSACTION_URL = r'https://api.paystack.co/transaction/verify/'
    LIST_TRANSACTIONS_URL = r'https://api.paystack.co/transaction/'
    FETCH_TRANSACTION_URL = r'https://api.paystack.co/transaction/'
    CHANGE_AUTHORIZATION_URL = r'https://api.paystack.co/transaction/charge_authorization/'
    VIEW_TRANSACTION_TIMELINE_URL = r'https://api.paystack.co/transaction/timeline/'
    TRANSACTION_TOTALS_URL = r'https://api.paystack.co/transaction/totals/'
    EXPORT_TRANSACTIONS_URL = r'https://api.paystack.co/transaction/export/'
    REQUEST_REAUTHORIZATION_URL = \
        r'https://api.paystack.co/transaction/request_reauthorization/'
    CHECK_AUTHORIZATION_URL = r'https://api.paystack.co/transaction/check_authorization/'
    CREATE_CUSTOMER_URL = r'https://api.paystack.co/customer/'
    LIST_CUSTOMERS_URL = r'https://api.paystack.co/customer/'
    FETCH_CUSTOMER_URL = r'https://api.paystack.co/customer/'
    UPDATE_CUSTOMER_URL = r'https://api.paystack.co/customer/'
    CUSTOMER_ACCESS_CONTROL_URL = r'https://api.paystack.co/customer/set_risk_action/'
    DEACTIVATE_AUTHORIZATION_URL = \
        r'https://api.paystack.co/customer/deactivate_authorization/'
    CREATE_SUBACCOUNT_URL = r'https://api.paystack.co/subaccount/'
    LIST_SUBACCOUNTS_URL = r'https://api.paystack.co/subaccount/'
    FETCH_SUBACCOUNT_URL = r'https://api.paystack.co/subaccount/'
    UPDATE_SUBACCOUNT_URL = r'https://api.paystack.co/subaccount/'
    CREATE_PLAN_URL = r'https://api.paystack.co/plan/'
    LIST_PLANS_URL = r'https://api.paystack.co/plan/'
    FETCH_PLAN_URL = r'https://api.paystack.co/plan/'
    UPDATE_PLAN_URL = r'https://api.paystack.co/plan/'
    CREATE_SUBSCRIPTION_URL = r'https://api.paystack.co/subscription/'
    LIST_SUBSCRIPTIONS_URL = r'https://api.paystack.co/subscription/'
    FETCH_SUBSCRIPTION_URL = r'https://api.paystack.co/subscription/'
    DISABLE_SUBSCRIPTION_URL = r'https://api.paystack.co/subscription/'
    ENABLE_SUBSCRIPTION_URL = r'https://api.paystack.co/subscription/'
    CREATE_PRODUCT_URL = r'https://api.paystack.co/product/'
    LIST_PRODUCTS_URL = r'https://api.paystack.co/product/'
    FETCH_PRODUCT_URL = r'https://api.paystack.co/product/'
    UPDATE_PRODUCT_URL = r'https://api.paystack.co/product/'
    CREATE_PAGE_URL = r'https://api.paystack.co/page/'
    LIST_PAGES_URL = r'https://api.paystack.co/page/'
    FETCH_PAGE_URL = r'https://api.paystack.co/page/'
    UPDATE_PAGE_URL = r'https://api.paystack.co/page/'
    CHECK_SLUG_AVAILABILITY_URL = r'https://api.paystack.co/page/check_slug_availability/'
    ADD_PRODUCTS_URL = r'https://api.paystack.co/page/'
    CREATE_INVOICE_URL = r'https://api.paystack.co/paymentrequest/'
    LIST_INVOICES_URL = r'https://api.paystack.co/paymentrequest/'
    VIEW_INVOICE_URL = r'https://api.paystack.co/paymentrequest/'
    VERIFY_INVOICE_URL = r'https://api.paystack.co/paymentrequest/verify/'
    SEND_NOTIFICATION_URL = r'https://api.paystack.co/paymentrequest/notify/'
    INVOICE_METRICS_URL = r'https://api.paystack.co/paymentrequest/totals'
    FINALIZE_DRAFT_URL = r'https://api.paystack.co/paymentrequest/finalize/'
    FETCH_INVOICE_URL = r'https://api.paystack.co/paymentrequest/'
    UPDATE_INVOICE_URL = r'https://api.paystack.co/paymentrequest/'
    ARCHIVE_INVOICE_URL = r'https://api.paystack.co/paymentrequest/archive/'
    MARK_AS_PAID_URL = r'https://api.paystack.co/paymentrequest/'
    FETCH_SETTLEMENTS_URL = r'https://api.paystack.co/settlement/'
    CREATE_TRANSFER_RECIPIENT_URL = r'https://api.paystack.co/transferrecipient/'
    LIST_TRANSFER_RECIPIENTS_URL = r'https://api.paystack.co/transferrecipient/'
    UPDATE_TRANSFER_RECIPIENT_URL = r'https://api.paystack.co/transferrecipient/'
    DELETE_TRANSFER_RECIPIENT_URL = r'https://api.paystack.co/transferrecipient/'
    INITIATE_TRANSFER_URL = r'https://api.paystack.co/transfer/'
    LIST_TRANSFERS_URL = r'https://api.paystack.co/transfer/'
    FETCH_TRANSFER_URL = r'https://api.paystack.co/transfer/'
    FINALIZE_TRANSFER_URL = r'https://api.paystack.co/transfer/finalize_transfer/'
    INITIATE_BULK_TRANSFER_URL = r'https://api.paystack.co/transfer/bulk/'
    CHECK_BALANCE_URL = r'https://api.paystack.co/balance/'
    RESEND_TRANSFER_OTP_URL = r'https://api.paystack.co/transfer/resend_otp/'
    DISABLE_OTP_REQUIREMENT_URL = r'https://api.paystack.co/transfer/disable_otp/'
    FINALIZE_DISABLING_OTP_URL = r'https://api.paystack.co/transfer/disable_otp_finalize/'
    ENABLE_OTP_REQUIREMENT_URL = r'https://api.paystack.co/transfer/enable_otp/'
    INITIATE_BULK_CHARGE_URL = r'https://api.paystack.co/bulkcharge'
    LIST_BULK_CHARGES_URL = r'https://api.paystack.co/bulkcharge'
    FETCH_BULK_CHARGE_BATCH_URL = r'https://api.paystack.co/bulkcharge/'
    FETCH_BULK_CHARGES_IN_BATCH_URL = r'https://api.paystack.co/bulkcharge/'
    PAUSE_BULK_CHARGE_BATCH_URL = r'https://api.paystack.co/bulkcharge/pause/'
    RESUME_BULK_CHARGE_BATCH_URL = r'https://api.paystack.co/bulkcharge/resume/'
    FETCH_PAYMENT_SESSION_TIMEOUT_URL = \
        r'https://api.paystack.co/integration/payment_session_timeout/'
    UPDATE_PAYMENT_SESSION_TIMEOUT_URL = \
        r'https://api.paystack.co/integration/payment_session_timeout/'
    CHARGE_URL = r'https://api.paystack.co/charge/'
    SUBMIT_PIN_URL = r'https://api.paystack.co/charge/submit_pin/'
    SUBMIT_OTP_URL = r'https://api.paystack.co/charge/submit_otp/'
    SUBMIT_PHONE_URL = r'https://api.paystack.co/charge/submit_phone/'
    SUBMIT_BIRTHDAY_URL = r'https://api.paystack.co/charge/submit_birthday/'
    CHECK_PENDING_CHARGE_URL = r'https://api.paystack.co/charge/'
    CREATE_REFUND_URL = r'https://api.paystack.co/refund/'
    LIST_REFUNDS_URL = r'https://api.paystack.co/refund/'
    FETCH_REFUND_URL = r'https://api.paystack.co/refund/'
    RESOLVE_BVN_URL = r'https://api.paystack.co/bank/resolve_bvn/'
    BVN_MATCH_URL = r'https://api.paystack.co/bvn/match/'
    RESOLVE_ACCOUNT_NUMBER_URL = r'https://api.paystack.co/bank/resolve/'
    RESOLVE_CARD_BIN_URL = r'https://api.paystack.co/decision/bin//'
    RESOLVE_PHONE_NUMBER_URL = r'https://api.paystack.co/verifications/'
    LIST_BANKS_URL = r'https://api.paystack.co/bank/'


class PayStackProcessFlag(IntFlag):
    INITIALIZE_TRANSACTION = 3
    VERIFY_TRANSACTION = 5
    LIST_TRANSACTIONS = 7
    FETCH_TRANSACTION = 11
    CHANGE_AUTHORIZATION = 13
    VIEW_TRANSACTION_TIMELINE = 17
    TRANSACTION_TOTALS = 19
    EXPORT_TRANSACTIONS = 23
    REQUEST_REAUTHORIZATION = 29
    CHECK_AUTHORIZATION = 31
    CREATE_CUSTOMER = 37
    LIST_CUSTOMERS = 41
    FETCH_CUSTOMER = 43
    UPDATE_CUSTOMER = 47
    CUSTOMER_ACCESS_CONTROL = 53
    DEACTIVATE_AUTHORIZATION = 59
    CREATE_SUBACCOUNT = 61
    LIST_SUBACCOUNTS = 67
    FETCH_SUBACCOUNT = 71
    UPDATE_SUBACCOUNT = 73
    CREATE_PLAN = 79
    LIST_PLANS = 83
    FETCH_PLAN = 89
    UPDATE_PLAN = 97
    CREATE_SUBSCRIPTION = 101
    LIST_SUBSCRIPTIONS = 103
    FETCH_SUBSCRIPTION = 107
    DISABLE_SUBSCRIPTION = 109
    ENABLE_SUBSCRIPTION = 113
    CREATE_PRODUCT = 127
    LIST_PRODUCTS = 131
    FETCH_PRODUCT = 137
    UPDATE_PRODUCT = 139
    CREATE_PAGE = 149
    LIST_PAGES = 151
    FETCH_PAGE = 157
    UPDATE_PAGE = 163
    CHECK_SLUG_AVAILABILITY = 167
    ADD_PRODUCTS = 173
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
    FETCH_SETTLEMENTS = 239
    CREATE_TRANSFER_RECIPIENT = 241
    LIST_TRANSFER_RECIPIENTS = 251
    UPDATE_TRANSFER_RECIPIENT = 257
    DELETE_TRANSFER_RECIPIENT = 263
    INITIATE_TRANSFER = 269
    LIST_TRANSFERS = 271
    FETCH_TRANSFER = 277
    FINALIZE_TRANSFER = 281
    INITIATE_BULK_TRANSFER = 283
    CHECK_BALANCE = 293
    RESEND_TRANSFER_OTP = 307
    DISABLE_OTP_REQUIREMENT = 311
    FINALIZE_DISABLING_OTP = 313
    ENABLE_OTP_REQUIREMENT = 317
    INITIATE_BULK_CHARGE = 331
    LIST_BULK_CHARGES = 337
    FETCH_BULK_CHARGE_BATCH = 347
    FETCH_BULK_CHARGES_IN_BATCH = 349
    PAUSE_BULK_CHARGE_BATCH = 353
    RESUME_BULK_CHARGE_BATCH = 359
    FETCH_PAYMENT_SESSION_TIMEOUT = 367
    UPDATE_PAYMENT_SESSION_TIMEOUT = 373
    CHARGE = 379
    SUBMIT_PIN = 383
    SUBMIT_OTP = 389
    SUBMIT_PHONE = 397
    SUBMIT_BIRTHDAY = 401
    CHECK_PENDING_CHARGE = 409
    CREATE_REFUND = 419
    LIST_REFUNDS = 421
    FETCH_REFUND = 431
    RESOLVE_BVN = 433
    BVN_MATCH = 439
    RESOLVE_ACCOUNT_NUMBER = 443
    RESOLVE_CARD_BIN = 449
    RESOLVE_PHONE_NUMBER = 457
    LIST_BANKS = 461


class Descriptor:

    def __get__(self, instance, owner):
        return NotImplemented

    def __delete__(self, instance):
        raise RuntimeError('Selected attribute cannot be deleted')


class AllFieldsDescriptor(Descriptor):
    __slots__ = 'all_fields'

    def __init__(self):
        ordered_fields = sorted({
            'amount', 'authorization_code', 'bearer', 'callback_url', 'cancel_action',
            'cancel_action_url', 'channels', 'currency', 'customer', 'email', 'from',
            'invoice_limit', 'metadata', 'page', 'payment_page', 'perPage', 'plan',
            'quantity', 'queue', 'reference', 'settled', 'settlement', 'status',
            'subaccount', 'to', 'transaction_charge', 'transaction_id'},
            key=lambda x: x.lower())
        self.all_fields = {*ordered_fields}

    def __get__(self, instance, owner):
        return self.all_fields


class InitializeFieldDescriptor(Descriptor):
    __slots__ = 'initialize_fields'

    def __init__(self):
        self.initialize_fields = {'reference', 'callback_url', 'amount', 'email', 'plan',
                                  'invoice_limit', 'metadata', 'subaccount',
                                  'transaction_charge', 'bearer', 'channels', }

    def __get__(self, instance, owner):
        return self.initialize_fields


class VerifyFieldDescriptor(Descriptor):
    __slots__ = 'verify_fields'

    def __init__(self):
        self.verify_fields = {'reference', }

    def __get__(self, instance, owner):
        return self.verify_fields


class ListTransactionsFieldDescriptor(Descriptor):
    __slots__ = 'list_transactions_fields'

    def __init__(self):
        self.list_transactions_fields = {'perPage', 'page', 'customer', 'status', 'from', 'to',
                                         'amount'}

    def __get__(self, instance, owner):
        return self.list_transactions_fields


class FetchFieldDescriptor(Descriptor):
    __slots__ = 'fetch_fields'

    def __init__(self):
        self.fetch_fields = {'transaction_id', }

    def __get__(self, instance, owner):
        return self.fetch_fields


class ChangeAuthorizationFieldDescriptor(Descriptor):
    __slots__ = 'change_authorization_fields'

    def __init__(self):
        self.change_authorization_fields = {'reference', 'amount', 'currency', 'email',
                                            'plan', 'quantity', 'invoice_limit', 'metadata',
                                            'authorization_code', 'subaccount',
                                            'transaction_charge', 'bearer', 'queue'}

    def __get__(self, instance, owner):
        return self.change_authorization_fields


class ViewTransactionTimelineFieldDescriptor(Descriptor):
    __slots__ = 'view_transaction_timeline_fields'

    def __init__(self):
        self.view_transaction_timeline_fields = {'transaction_id', }

    def __get__(self, instance, owner):
        return self.view_transaction_timeline_fields


class TransactionTotalsFieldDescriptor(Descriptor):
    __slots__ = 'transaction_totals_fields'

    def __init__(self):
        self.transaction_totals_fields = {'from', 'to'}

    def __get__(self, instance, owner):
        return self.transaction_totals_fields


class ExportTransactionsFieldDescriptor(Descriptor):
    __slots__ = 'export_transactions_fields'

    def __init__(self):
        self.export_transactions_fields = {'from', 'amount', 'to', 'settled', 'payment_page',
                                           'customer', 'currency', 'settlement', 'status'}

    def __get__(self, instance, owner):
        return self.export_transactions_fields


class RequestReAuthorizationFieldDescriptor(Descriptor):
    __slots__ = 'request_reauthorization_fields'

    def __init__(self):
        self.request_reauthorization_fields = {'reference', 'authorization_code', 'amount',
                                               'currency', 'email', 'metadata'}

    def __get__(self, instance, owner):
        return self.request_reauthorization_fields


class CheckAuthorizationFieldDescriptor(Descriptor):
    __slots__ = 'check_authorization_fields'

    def __init__(self):
        self.check_authorization_fields = {'authorization_code', 'amount', 'email', 'currency'}

    def __get__(self, instance, owner):
        return self.check_authorization_fields


@singledispatch
def data_check(arg, **kwargs) -> Any:
    if not arg:
        raise RuntimeError("None value provided for validation")
    else:
        if callable(arg):
            return arg
        else:
            return NotImplemented


@data_check.register(bool)
def _(arg, **kwargs):
    return bool(arg)


@data_check.register(int)
def _(arg):
    int_min = -sys.maxsize - 1
    int_max = sys.maxsize
    try:
        return int(arg) if (arg < int_max) and (arg > int_min) else NotImplemented
    except ValueError:
        raise ValueError('Unable to process given data type as int. '
                         'Expected int, got %s' % type(arg))


@data_check.register(float)
def _(arg):
    float_max = float('inf')
    float_min = float('-inf')
    try:
        return arg if (arg < float_max) and (arg > float_min) else NotImplemented
    except ValueError:
        raise ValueError('Unable to process given data type as float. '
                         'Expected float, got %s' % type(arg))
    except Exception:
        raise Exception


@data_check.register(str)
def _(arg, pattern: str = None, length: int = None):
    if isinstance(arg, str) and bool(arg):
        result = None
        if bool(length) and len(arg) > length:
            return NotImplemented
        elif isinstance(pattern, str) and bool(pattern):
            result = arg if bool(re.match(pattern, arg)) else NotImplemented
        if not length and isinstance(pattern, str) and bool(pattern):
            result = arg if bool(re.match(pattern, arg)) else NotImplemented
        if not pattern and not length:
            return str(arg)
        return result


@data_check.register(datetime)
def _(arg):
    if isinstance(arg, datetime):
        return arg
    else:
        return NotImplemented


@data_check.register(dict)
def _(arg):
    if isinstance(arg, dict):
        return arg
    else:
        return NotImplemented


class PayStackData:
    # set up the lookup table
    initialize_fields = InitializeFieldDescriptor()
    verify_fields = VerifyFieldDescriptor()
    list_transactions_fields = ListTransactionsFieldDescriptor()
    fetch_fields = FetchFieldDescriptor()
    change_authorization_fields = ChangeAuthorizationFieldDescriptor()
    view_transaction_timeline_fields = ViewTransactionTimelineFieldDescriptor()
    transaction_totals_fields = TransactionTotalsFieldDescriptor()
    export_transactions_fields = ExportTransactionsFieldDescriptor()
    request_reauthorization_fields = RequestReAuthorizationFieldDescriptor()
    check_authorization_fields = CheckAuthorizationFieldDescriptor()
    all_fields = AllFieldsDescriptor()

    @classmethod
    def validate(cls, field: str, value: Any, formatter: str = None, length: int = None) -> \
            Any:
        """
        Provide validation of the various page transaction fields.
        Listed fields for PayStack api 2.0 will include:
        'amount'
        'authorization_code'
        'bearer'
        'callback_url'
        'cancel_action'
        'cancel_action_url'
        'channels'
        'currency'
        'customer'
        'email'
        'from'
        'invoice_limit'
        'metadata'
        'page'
        'payment_page'
        'perPage'
        'plan'
        'quantity'
        'queue'
        'reference'
        'settled'
        'settlement'
        'status'
        'subaccount'
        'to'
        'transaction_charge'
        'transaction_id'

        :param field: Given field to validate
        :param value: The given value being validated
        :param formatter: The regex pattern used to validate the data if it is string based
        or to be validated by regex pattern
        :param length: total number of characters or approved length for the data
        :return: bool
        """
        result = False

        def _check_amount(amt, **kwargs):
            return data_check(float(amt))

        def _check_authorization_code(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)

        def _check_bearer(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return data_check(data, pattern=r'bearer', length=data_length)

        def _check_callback_url(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|' \
                              r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                return data_check(data, pattern=url_pattern, length=data_length)

        def _check_cancel_action(data, **kwargs):
            return data_check(data)

        def _check_cancel_action_url(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|' \
                              r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                return data_check(data, pattern=url_pattern, length=data_length)

        def _check_channels(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return data_check(data, pattern=r'(card)|(bank)', length=data_length)

        def _check_currency(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return data_check(data, pattern=r'(NGN)|(USD)|(EUR)|(GBP)', length=data_length)

        def _check_customer(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                customer_pattern = r'^\w+$'
                return data_check(data, pattern=customer_pattern, length=data_length)

        def _check_email(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
                return data_check(data, pattern=email_pattern, length=data_length)

        def _check_from(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            if isinstance(data, str) and isinstance(pattern, str) and bool(pattern) and \
                    bool(data):
                _date = datetime.strptime(data, pattern)
                return data_check(_date)
            elif isinstance(data, datetime):
                return data_check(data)

        def _check_invoice_limit(data, **kwargs):
            return data_check(int(data))

        def _check_metadata(data, **kwargs):
            return data_check(data)

        def _check_page(data, **kwargs):
            return data_check(int(data))

        def _check_payment_page(data, **kwargs):
            return data_check(int(data))

        def _check_per_page(data, **kwargs):
            return data_check(int(data))

        def _check_plan(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and bool(pattern):
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return NotImplemented

        def _check_quantity(data, **kwargs):
            return data_check(float(data))

        def _check_queue(data, **kwargs):
            return data_check(bool(data))

        def _check_reference(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and pattern:
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return NotImplemented

        def _check_settled(data, **kwargs):
            return data_check(bool(data))

        def _check_settlement(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and pattern:
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return data_check(data, pattern=r'^\w+$', length=data_length)

        def _check_status(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and pattern:
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return data_check(data, pattern=r'^\w+$', length=data_length)

        def _check_subaccount(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and pattern:
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return NotImplemented

        def _check_to(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            if isinstance(data, str) and isinstance(pattern, str) and bool(pattern) and \
                    bool(data):
                _date = datetime.strptime(data, pattern)
                return data_check(_date)
            elif isinstance(data, datetime):
                return data_check(data)

        def _check_transaction_charge(data, **kwargs):
            return data_check(float(data))

        def _check_transaction_id(data, **kwargs):
            pattern = kwargs.get('pattern', None)
            data_length = kwargs.get('length', None)
            if isinstance(pattern, str) and pattern:
                return data_check(data, pattern=pattern, length=data_length)
            else:
                return NotImplemented

        functions = (_check_amount, _check_authorization_code, _check_bearer,
                     _check_callback_url, _check_cancel_action, _check_cancel_action_url,
                     _check_channels, _check_currency, _check_customer, _check_email,
                     _check_from, _check_invoice_limit, _check_metadata, _check_page,
                     _check_payment_page, _check_per_page, _check_plan, _check_quantity,
                     _check_queue, _check_reference, _check_settled, _check_settlement,
                     _check_status, _check_subaccount, _check_to, _check_transaction_charge,
                     _check_transaction_id)
        ordered_functions = sorted(functions, key=lambda x: x.__name__.lower())
        function_lookup = dict(zip(sorted(cls.all_fields), ordered_functions))
        if field in cls.all_fields:
            checker = function_lookup[field]
            return checker(value, pattern=formatter)


class BusinessDataObject:
    # define a data structure holding elements that can be updated only through a defined
    # interface

    def __init__(self, config: Any = None, **kwargs):
        self._data = dict()
        self.__bon__ = None
        self._header = None

        if not self.__bon__:
            name = kwargs.get('name') or kwargs.get('business_object_name')
            self.__bon__ = name or self.__class__.__qualname__
        if not self._data.get('key'):
            # get keys from config aliases
            key_aliases = config.option('named_fields', 'key').split('|')
            api_key = None
            for k in key_aliases:
                if k in kwargs:
                    api_key = kwargs.pop(k)
                    self._data.update({k: api_key})

            self._data['key'] = api_key or config.option('system', 'secret_key')
        if not self.header:
            if 'authorization' in kwargs and 'conttentype' in kwargs and 'cache' in kwargs:
                authorization = kwargs.pop('authorization')
                conttentype = kwargs.pop('contenttype')
                cache = kwargs.pop('cache')
                header = {
                    'authorization': authorization,
                    'content-type': conttentype,
                    'cache-control': cache
                }
                self._header = header
            else:
                contenttype = config.option('http', 'content-type')
                cache = config.option('http', 'cache-control')
                api_key = self._data.get('key')
                auth = config.option('http', 'authorization')
                header = {
                    'authorization': f'{auth} {api_key}',
                    'content-type': contenttype,
                    'cache-control': cache
                }
                self._header = header
        self._data.update(**kwargs)

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

    def update(self, **kwargs):
        self._data.update(**kwargs)

    def data(self):
        return self._data

    def url(self, transaction_type, params=None):
        _url = None
        if isinstance(transaction_type, Enum) and transaction_type in PayStackRestUrl:
            _url = transaction_type.value
        elif isinstance(transaction_type, str) and transaction_type in PayStackRestUrl.__members__.keys():
            _url = PayStackRestUrl.__members__[transaction_type]
        query_params = None
        if isinstance(params, Sequence):
            query_params = tuple(params)
        elif isinstance(params, dict):
            query_params = tuple(params.items())
        if query_params:
            _param = ''
            for name, value in params:
                _param += f'{name}/{value}/'
            _url += _param
        return _url

    @property
    def header(self):
        return self._header


def networklog(*, level=logging.WARNING, error=None, message=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config = ConfigManager()
            logging.basicConfig(filename=config.option('logging', 'log'))
            logger = logging.getLogger(func.__name__)
            try:
                return func(*args, **kwargs)
            except error:
                logmsg = "%s: %s" % (error, message) if error and message else \
                    (error, str(error))
                logger.log(level, logmsg)
            except PyPayStackError:
                paystack_error = PyPayStackError(*args, **kwargs)
                logging.warning("Request: %s\nResponse: %s" % (
                    paystack_error.request, paystack_error.response))
            except:
                logger.log(level, sys.exc_info()[0])

        return wrapper

    return decorate


def parser(*, encoder=None, target=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            outcome = func(*args, **kwargs)
            if hasattr(target, '__init__'):
                if isinstance(outcome, Mapping):
                    return target.__init__(**outcome)
                elif isinstance(outcome, str) and not encoder:
                    try:
                        params = json.loads(outcome)
                        return target(**params)
                    except ValueError:
                        logging.warning(ValueError)
                elif outcome and callable(encoder):
                    return encoder(outcome)
            else:
                return BusinessDataObject(**outcome)

        return wrapper

    return decorate
