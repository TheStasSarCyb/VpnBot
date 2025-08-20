from enum import Enum

class Bying_enum(Enum):
    days_30 = "bying_proxy_30"
    days_60 = "bying_proxy_60"
    days_90 = "bying_proxy_90"

class Pay_methods(Enum):
    SBP = "SBP"
    CARD = "CARD"
    CARDP = "CARD"
    SBPP = "SBPP"