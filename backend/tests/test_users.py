import pytest


class TestGetUsers:
    def test_admin_can_get_users(self, client, auth_headers_admin, admin_user):
        response = client.get("/users/", headers=auth_headers_admin)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_viewer_cannot_get_users(self, client, auth_headers_viewer):
        response = client.get("/users/", headers=auth_headers_viewer)
        assert response.status_code == 403

    def test_unauthorized_cannot_get_users(self, client):
        response = client.get("/users/")
        assert response.status_code == 401


class TestGetUserById:
    def test_get_existing_user(self, client, auth_headers_admin, viewer_user):
        response = client.get(f"/users/{viewer_user.id}", headers=auth_headers_admin)
        assert response.status_code == 200
        assert response.json()["id"] == viewer_user.id

    def test_get_nonexistent_user(self, client, auth_headers_admin):
        response = client.get("/users/99999", headers=auth_headers_admin)
        assert response.status_code == 404


class TestCreateUser:
    def test_admin_create_user(self, client, auth_headers_admin, engineer_role):
        response = client.post("/users/", headers=auth_headers_admin, json={
            "surname": "Новый",
            "name": "Пользователь",
            "login": "brand_new_user",
            "password": "pass1234",
            "role_id": engineer_role.id
        })
        assert response.status_code == 201
        assert response.json()["login"] == "brand_new_user"

    def test_duplicate_login(self, client, auth_headers_admin, viewer_user, viewer_role):
        response = client.post("/users/", headers=auth_headers_admin, json={
            "surname": "Дубль",
            "name": "Дубль",
            "login": viewer_user.login,
            "password": "pass1234",
            "role_id": viewer_role.id
        })
        assert response.status_code == 400

    def test_invalid_role(self, client, auth_headers_admin):
        response = client.post("/users/", headers=auth_headers_admin, json={
            "surname": "Тест",
            "name": "Тест",
            "login": "test_bad_role",
            "password": "pass1234",
            "role_id": 99999
        })
        assert response.status_code == 400

    def test_viewer_cannot_create_user(self, client, auth_headers_viewer, viewer_role):
        response = client.post("/users/", headers=auth_headers_viewer, json={
            "surname": "Тест",
            "name": "Тест",
            "login": "shouldfail",
            "password": "pass1234",
            "role_id": viewer_role.id
        })
        assert response.status_code == 403


class TestUpdateUser:
    def test_update_own_profile(self, client, auth_headers_viewer, viewer_user):
        response = client.put(
            f"/users/{viewer_user.id}",
            headers=auth_headers_viewer,
            json={"name": "Обновлённое имя"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Обновлённое имя"

    def test_update_password(self, client, auth_headers_viewer, viewer_user):
        response = client.put(
            f"/users/{viewer_user.id}",
            headers=auth_headers_viewer,
            json={"password": "newpass123"}
        )
        assert response.status_code == 200
        # Проверяем что новый пароль работает
        login_resp = client.post("/auth/login", data={
            "username": viewer_user.login,
            "password": "newpass123"
        })
        assert login_resp.status_code == 200


class TestDeleteUser:
    def test_admin_delete_user(self, client, db, auth_headers_admin, engineer_role):
        from core.security import get_password_hash
        from models.user import User
        tmp = User(
            surname="Удалить",
            name="Меня",
            login="to_delete_user",
            hashed_password=get_password_hash("pass"),
            role=engineer_role
        )
        db.add(tmp)
        db.commit()
        db.refresh(tmp)

        response = client.delete(f"/users/{tmp.id}", headers=auth_headers_admin)
        assert response.status_code == 204

    def test_admin_cannot_delete_self(self, client, auth_headers_admin, admin_user):
        response = client.delete(f"/users/{admin_user.id}", headers=auth_headers_admin)
        assert response.status_code == 400

    def test_viewer_cannot_delete(self, client, auth_headers_viewer, viewer_user):
        response = client.delete(f"/users/{viewer_user.id}", headers=auth_headers_viewer)
        assert response.status_code == 403
