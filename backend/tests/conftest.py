import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from api.dependencies import get_db
from core.database import Base
from core.security import get_password_hash
from models.user import User
from models.role import Role
from models.equipment import Equipment
from models.manufacturer import Manufacturer
from models.defect import Defect
from models.defect_status import DefectStatus
from models.defect_type import DefectType
from models.equipment_status import EquipmentStatus
from models.defect_criticality import DefectCriticality
from datetime import date
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# --- Справочные данные ---

@pytest.fixture()
def viewer_role(db):
    role = Role(name="viewer")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture()
def engineer_role(db):
    role = Role(name="engineer")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture()
def admin_role(db):
    role = Role(name="admin")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture()
def viewer_user(db, viewer_role):
    user = User(
        surname="Иванов",
        name="Иван",
        middlename="Иванович",
        login="viewer_user",
        hashed_password=get_password_hash("password123"),
        role=viewer_role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def engineer_user(db, engineer_role):
    user = User(
        surname="Петров",
        name="Пётр",
        middlename="Петрович",
        login="engineer_user",
        hashed_password=get_password_hash("password123"),
        role=engineer_role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def admin_user(db, admin_role):
    user = User(
        surname="Сидоров",
        name="Сидор",
        middlename="Сидорович",
        login="admin_user",
        hashed_password=get_password_hash("password123"),
        role=admin_role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_token(client, login: str, password: str = "password123") -> str:
    response = client.post(
        "/auth/login",
        data={"username": login, "password": password}
    )
    return response.json()["access_token"]


@pytest.fixture()
def viewer_token(client, viewer_user):
    return get_token(client, viewer_user.login)


@pytest.fixture()
def engineer_token(client, engineer_user):
    return get_token(client, engineer_user.login)


@pytest.fixture()
def admin_token(client, admin_user):
    return get_token(client, admin_user.login)


@pytest.fixture()
def auth_headers_viewer(viewer_token):
    return {"Authorization": f"Bearer {viewer_token}"}


@pytest.fixture()
def auth_headers_engineer(engineer_token):
    return {"Authorization": f"Bearer {engineer_token}"}


@pytest.fixture()
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# --- Данные для тестов ---

@pytest.fixture()
def manufacturer(db):
    m = Manufacturer(
        name="ТестПроизводитель",
        phone="+79001234567",
        email="test@manufacturer.ru",
        address="г. Москва, ул. Тестовая, 1"
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@pytest.fixture()
def equipment_status(db):
    s = EquipmentStatus(name="Активен")
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@pytest.fixture()
def equipment(db, manufacturer, equipment_status):
    eq = Equipment(
        serial_number="SN-TEST-001",
        model="TestModel",
        manufacturer_id=manufacturer.id,
        location_address="г. Москва, ул. Тестовая, 1",
        installation_date=date(2023, 1, 1),
        status_id=equipment_status.id,
        latitude=55.75,
        longitude=37.61
    )
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return eq


@pytest.fixture()
def defect_status(db):
    s = DefectStatus(name="Открыт")
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@pytest.fixture()
def defect_type(db):
    t = DefectType(name="Механический", description="Механический дефект")
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@pytest.fixture()
def criticality(db):
    c = DefectCriticality(name="Средняя", weight=2)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@pytest.fixture()
def defect(db, equipment, defect_status, defect_type, criticality, engineer_user):
    d = Defect(
        title="Тестовый дефект",
        description="Описание тестового дефекта",
        equipment_id=equipment.id,
        status_id=defect_status.id,
        defect_type_id=defect_type.id,
        criticality_id=criticality.id,
        user_id=engineer_user.id
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d
