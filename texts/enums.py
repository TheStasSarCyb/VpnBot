from enum import Enum

class Bying_enum(Enum):
    days_pc_7 = "bying_proxy_pc_7"
    days_pc_30 = "bying_proxy_pc_30"
    days_pc_60 = "bying_proxy_pc_60"
    days_pc_90 = "bying_proxy_pc_90"
    days_phone_7 = "bying_proxy_phone_7"
    days_phone_30 = "bying_proxy_phone_30"
    days_phone_60 = "bying_proxy_phone_60"
    days_phone_90 = "bying_proxy_phone_90"

class Pay_methods(Enum):
    ACC = 'ACC'
    ACCP = 'ACCP'
    SBP = "SBP"
    CARD = "CARD"
    CARDP = "CARDP"
    SBPP = "SBPP"