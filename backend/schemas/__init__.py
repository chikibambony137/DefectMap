# User
from .user import (
    UserBase, UserCreate, UserUpdate, UserInDB, UserRegister,
    UserResponse, UserWithRole
)

# Role
from .role import RoleBase, RoleCreate, RoleResponse

# Equipment
from .equipment import (
    EquipmentBase, EquipmentCreate, EquipmentUpdate,
    EquipmentResponse, EquipmentWithStats
)

# EquipmentStatus
from .equipment_status import (
    EquipmentStatusBase, EquipmentStatusCreate, EquipmentStatusResponse
)

# Manufacturer
from .manufacturer import (
    ManufacturerBase, ManufacturerCreate, ManufacturerUpdate, ManufacturerResponse
)

# Defect
from .defect import (
    DefectBase, DefectCreate, DefectUpdate,
    DefectResponse, DefectWithRelations, DefectGeoResponse
)

# DefectType
from .defect_type import (
    DefectTypeBase, DefectTypeCreate, DefectTypeUpdate, DefectTypeResponse
)

# DefectStatus
from .defect_status import (
    DefectStatusBase, DefectStatusCreate, DefectStatusResponse
)

# Criticality
from .criticality import CriticalityBase, CriticalityCreate, CriticalityResponse

# Auth
from .auth import Token, TokenData, LoginRequest, LoginResponse

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserInDB", "UserRegister",
    "UserResponse", "UserWithRole",
    # Role
    "RoleBase", "RoleCreate", "RoleResponse",
    # Equipment
    "EquipmentBase", "EquipmentCreate", "EquipmentUpdate",
    "EquipmentResponse", "EquipmentWithStats",
    # EquipmentStatus
    "EquipmentStatusBase", "EquipmentStatusCreate", "EquipmentStatusResponse",
    # Manufacturer
    "ManufacturerBase", "ManufacturerCreate", "ManufacturerUpdate", "ManufacturerResponse",
    # Defect
    "DefectBase", "DefectCreate", "DefectUpdate",
    "DefectResponse", "DefectWithRelations", "DefectGeoResponse",
    # DefectType
    "DefectTypeBase", "DefectTypeCreate", "DefectTypeUpdate", "DefectTypeResponse",
    # DefectStatus
    "DefectStatusBase", "DefectStatusCreate", "DefectStatusResponse",
    # Criticality
    "CriticalityBase", "CriticalityCreate", "CriticalityResponse",
    # Auth
    "Token", "TokenData", "LoginRequest", "LoginResponse"
]