from enum import Enum, unique


@unique
class SheetName(Enum):
    AGILENT = "PVs Agilent 4UHV"
    COUNTING_PRU = "PVs Counting PRU"
    MBTEMP = "PVs MBTemp"
    MKS = "PVs MKS937b"
    SPIXCONV = "PVs SPIxCONV"

    @classmethod
    def has_key(cls, key: str):
        if not key or key.__class__ != str:
            return False
        return key.upper() in cls.__members__.keys()

    @classmethod
    def keys(cls):
        return [k for k in cls.__members__.keys()]

    @classmethod
    def from_key(cls, key: str):
        if not key:
            return None

        for member in cls:
            if member.name == key.upper():
                return member

        return None
