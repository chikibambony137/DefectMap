import pytest


class TestGetManufacturers:
    def test_get_list(self, client, auth_headers_viewer, manufacturer):
        response = client.get("/manufacturers/", headers=auth_headers_viewer)
        assert response.status_code == 200
        assert any(m["id"] == manufacturer.id for m in response.json())

    def test_unauthorized(self, client):
        response = client.get("/manufacturers/")
        assert response.status_code == 401


class TestGetManufacturerById:
    def test_get_existing(self, client, auth_headers_viewer, manufacturer):
        response = client.get(
            f"/manufacturers/{manufacturer.id}", headers=auth_headers_viewer
        )
        assert response.status_code == 200
        assert response.json()["name"] == manufacturer.name

    def test_get_nonexistent(self, client, auth_headers_viewer):
        response = client.get("/manufacturers/99999", headers=auth_headers_viewer)
        assert response.status_code == 404


class TestCreateManufacturer:
    def test_engineer_can_create(self, client, auth_headers_engineer):
        response = client.post("/manufacturers/", headers=auth_headers_engineer, json={
            "name": "Новый производитель",
            "phone": "+79009998877",
            "email": "new@manufacturer.ru",
            "address": "г. Санкт-Петербург, ул. Новая, 5"
        })
        assert response.status_code == 201
        assert response.json()["name"] == "Новый производитель"

    def test_viewer_cannot_create(self, client, auth_headers_viewer):
        response = client.post("/manufacturers/", headers=auth_headers_viewer, json={
            "name": "Запрещено",
            "phone": "+79001112233",
            "email": "forbidden@test.ru",
            "address": "г. Тест, 1"
        })
        assert response.status_code == 403


class TestUpdateManufacturer:
    def test_engineer_can_update(self, client, auth_headers_engineer, manufacturer):
        response = client.put(
            f"/manufacturers/{manufacturer.id}",
            headers=auth_headers_engineer,
            json={"name": "Обновлённый производитель"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Обновлённый производитель"

    def test_update_nonexistent(self, client, auth_headers_engineer):
        response = client.put(
            "/manufacturers/99999",
            headers=auth_headers_engineer,
            json={"name": "X"}
        )
        assert response.status_code == 404


class TestDeleteManufacturer:
    def test_admin_can_delete_without_equipment(self, client, db, auth_headers_admin):
        from models.manufacturer import Manufacturer
        m = Manufacturer(
            name="УдалитьМеня",
            phone="+79000000000",
            email="delete@me.ru",
            address="г. Удалённый, 0"
        )
        db.add(m)
        db.commit()
        db.refresh(m)

        response = client.delete(f"/manufacturers/{m.id}", headers=auth_headers_admin)
        assert response.status_code == 204
