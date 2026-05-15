from .auth import router as auth_router
from .users import router as users_router
from .roles import router as roles_router
from .equipment import router as equipment_router
from .equipment_statuses import router as equipment_statuses_router
from .defects import router as defects_router
from .defect_types import router as defect_types_router
from .defect_statuses import router as defect_statuses_router
from .criticalities import router as criticalities_router
from .manufacturers import router as manufacturers_router

__all__ = [
    "auth_router",
    "users_router",
    "roles_router",
    "equipment_router",
    "equipment_statuses_router",
    "defects_router",
    "defect_types_router",
    "defect_statuses_router",
    "criticalities_router",
    "manufacturers_router",
]