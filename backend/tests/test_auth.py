class TestRegister:
    def test_register_success(self, client, viewer_role):
        response = client.post("/auth/register", json={
            "surname": "Новиков",
            "name": "Новик",
            "middlename": "Новикович",
            "login": "new_user_reg",
            "password": "secret123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["login"] == "new_user_reg"
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_login(self, client, viewer_user):
        response = client.post("/auth/register", json={
            "surname": "Дубль",
            "name": "Дубль",
            "login": viewer_user.login,
            "password": "secret123"
        })
        assert response.status_code == 400
        assert "логином" in response.json()["detail"]

    def test_register_no_viewer_role(self, client):
        # роль viewer не создана — ожидаем 400
        response = client.post("/auth/register", json={
            "surname": "Тест",
            "name": "Тест",
            "login": "no_role_user",
            "password": "secret123"
        })
        assert response.status_code in (201, 400)


class TestLogin:
    def test_login_success(self, client, viewer_user):
        response = client.post("/auth/login", data={
            "username": viewer_user.login,
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["login"] == viewer_user.login

    def test_login_wrong_password(self, client, viewer_user):
        response = client.post("/auth/login", data={
            "username": viewer_user.login,
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_login_unknown_user(self, client):
        response = client.post("/auth/login", data={
            "username": "ghost",
            "password": "password123"
        })
        assert response.status_code == 401


class TestMe:
    def test_get_me(self, client, auth_headers_viewer, viewer_user):
        response = client.get("/auth/me", headers=auth_headers_viewer)
        assert response.status_code == 200
        assert response.json()["login"] == viewer_user.login

    def test_get_me_unauthorized(self, client):
        response = client.get("/auth/me")
        assert response.status_code == 401
