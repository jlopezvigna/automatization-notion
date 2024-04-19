# TODO: Update python 3.11 in AWS
# from enum import StrEnum
from enum import Enum


class StatusPropertyClass(str, Enum):
    NEW = 'New'
    ACTIVE = 'Active'
    RESOLVED = 'Resolved'
