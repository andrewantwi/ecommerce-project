from enum import Enum

class DepartmentEnum(str, Enum):
    OPTOMETRY = "optometry"
    GYNAECOLOGY = "gynaecology"
    GENERAL = "general"
    CARDIOLOGY = "cardiology"
    NEUROLOGY = "neurology"
    PEDIATRICS = "pediatrics"
    ORTHOPEDICS = "orthopedics"