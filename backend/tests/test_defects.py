class TestGetDefects:
    def test_get_list(self, client, auth_headers_viewer, defect):
        response = client.get("/defects/", headers=auth_headers_viewer)
        assert response.status_code == 200
        assert any(d["id"] == defect.id for d in response.json())

    def test_filter_by_status(self, client, auth_headers_viewer, defect):
        response = client.get(
            f"/defects/?status_id={defect.status_id}",
            headers=auth_headers_viewer
        )
        assert response.status_code == 200
        assert all(d["status_id"] == defect.status_id for d in response.json())

    def test_filter_by_equipment(self, client, auth_headers_viewer, defect):
        response = client.get(
            f"/defects/?equipment_id={defect.equipment_id}",
            headers=auth_headers_viewer
        )
        assert response.status_code == 200
        assert all(d["equipment_id"] == defect.equipment_id
                   for d in response.json())

    def test_unauthorized(self, client):
        response = client.get("/defects/")
        assert response.status_code == 401


class TestGetDefectById:
    def test_get_existing(self, client, auth_headers_viewer, defect):
        response = client.get(f"/defects/{defect.id}",
                              headers=auth_headers_viewer)
        assert response.status_code == 200
        assert response.json()["id"] == defect.id

    def test_get_nonexistent(self, client, auth_headers_viewer):
        response = client.get("/defects/99999", headers=auth_headers_viewer)
        assert response.status_code == 404


class TestCreateDefect:
    def test_engineer_can_create(self, client, auth_headers_engineer,
                                 equipment, defect_status,
                                 defect_type, criticality):
        response = client.post("/defects/",
                               headers=auth_headers_engineer,
                               json={
                                    "title": "Новый дефект",
                                    "description": "Описание нового дефекта",
                                    "equipment_id": equipment.id,
                                    "status_id": defect_status.id,
                                    "defect_type_id": defect_type.id,
                                    "criticality_id": criticality.id
                                })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Новый дефект"

    def test_invalid_equipment(self, client, auth_headers_engineer,
                               defect_status, defect_type, criticality):
        response = client.post("/defects/", headers=auth_headers_engineer,
                               json={
                                    "title": "Дефект",
                                    "description": "Описание",
                                    "equipment_id": 99999,
                                    "status_id": defect_status.id,
                                    "defect_type_id": defect_type.id,
                                    "criticality_id": criticality.id
                                })
        assert response.status_code == 400

    def test_viewer_cannot_create(self, client, auth_headers_viewer,
                                  equipment, defect_status,
                                  defect_type, criticality):
        response = client.post("/defects/", headers=auth_headers_viewer, json={
            "title": "Дефект",
            "description": "Описание",
            "equipment_id": equipment.id,
            "status_id": defect_status.id,
            "defect_type_id": defect_type.id,
            "criticality_id": criticality.id
        })
        assert response.status_code == 403


class TestUpdateDefect:
    def test_engineer_can_update(self, client, auth_headers_engineer, defect):
        response = client.put(
            f"/defects/{defect.id}",
            headers=auth_headers_engineer,
            json={"title": "Обновлённый дефект"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Обновлённый дефект"

    def test_update_nonexistent(self, client, auth_headers_engineer):
        response = client.put(
            "/defects/99999",
            headers=auth_headers_engineer,
            json={"title": "Х"}
        )
        assert response.status_code == 404

    def test_viewer_cannot_update(self, client, auth_headers_viewer, defect):
        response = client.put(
            f"/defects/{defect.id}",
            headers=auth_headers_viewer,
            json={"title": "Попытка"}
        )
        assert response.status_code == 403


class TestDeleteDefect:
    def test_admin_can_delete(self, client, db, auth_headers_admin,
                              equipment, defect_status, defect_type,
                              criticality, engineer_user):
        from models.defect import Defect
        d = Defect(
            title="К удалению",
            description="Удали меня",
            equipment_id=equipment.id,
            status_id=defect_status.id,
            defect_type_id=defect_type.id,
            criticality_id=criticality.id,
            user_id=engineer_user.id
        )
        db.add(d)
        db.commit()
        db.refresh(d)

        response = client.delete(f"/defects/{d.id}",
                                 headers=auth_headers_admin)
        assert response.status_code == 204

    def test_engineer_cannot_delete(self, client,
                                    auth_headers_engineer, defect):
        response = client.delete(
            f"/defects/{defect.id}", headers=auth_headers_engineer
        )
        assert response.status_code == 403


class TestDefectsGeo:
    def test_geo_returns_coords(self, client, auth_headers_viewer, defect):
        response = client.get("/defects/geo", headers=auth_headers_viewer)
        assert response.status_code == 200
        data = response.json()
        if data:
            assert "latitude" in data[0]
            assert "longitude" in data[0]
