from enum import IntFlag
from typing import Any
import requests
from toolkit.behaviour.command import Command
from paystack.util import PayStackGatewayFlag, BusinessDataObject, PayStackRestUrl


__all__ = ('fetch_settlements',)


class SettlementCommandRank(IntFlag):
    FETCH_SETTLEMENTS = 239


def fetch_settlements_cmd(**kwargs) -> Any:
    settlement = BusinessDataObject(**kwargs)
    query = settlement.data()
    url = settlement.url(PayStackRestUrl.FETCH_SETTLEMENTS_URL)
    return requests.get(url=url, params=query, headers=settlement.header)


fetch_settlements = Command(cmd=fetch_settlements_cmd,
                            group=PayStackGatewayFlag.SETTLEMENTS,
                            rank=SettlementCommandRank.FETCH_SETTLEMENTS, label=None)
