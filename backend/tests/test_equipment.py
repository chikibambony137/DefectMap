from datetime import date


class TestGetEquipment:
    def test_get_list(self, client, auth_headers_viewer, equipment):
        response = client.get("/equipment/", headers=auth_headers_viewer)
        assert response.status_code == 200
        assert any(e["id"] == equipment.id for e in response.json())

    def test_filter_by_status(self, client, auth_headers_viewer, equipment):
        response = client.get(
            f"/equipment/?status_id={equipment.status_id}",
            headers=auth_headers_viewer
        )
        assert response.status_code == 200
        assert all(e["status_id"] == equipment.status_id
                   for e in response.json())

    def test_unauthorized(self, client):
        response = client.get("/equipment/")
        assert response.status_code == 401


class TestGetEquipmentById:
    def test_get_existing(self, client, auth_headers_viewer, equipment):
        response = client.get(f"/equipment/{equipment.id}",
                              headers=auth_headers_viewer)
        assert response.status_code == 200
        assert response.json()["serial_number"] == equipment.serial_number

    def test_get_nonexistent(self, client, auth_headers_viewer):
        response = client.get("/equipment/99999",
                              headers=auth_headers_viewer)
        assert response.status_code == 404


class TestCreateEquipment:
    def test_engineer_can_create(self, client,
                                 auth_headers_engineer,
                                 manufacturer, equipment_status):
        response = client.post("/equipment/",
                               headers=auth_headers_engineer,
                               json={
                                    "serial_number": "SN-NEW-001",
                                    "model": "NewModel",
                                    "manufacturer_id": manufacturer.id,
                                    "location_address": "г. Тест, ул. тест, 1",
                                    "installation_date": "2024-01-01",
                                    "status_id": equipment_status.id,
                                    "latitude": 55.0,
                                    "longitude": 37.0
                                })
        assert response.status_code == 201
        assert response.json()["serial_number"] == "SN-NEW-001"

    def test_duplicate_serial(self, client, auth_headers_engineer, equipment,
                              equipment_status, manufacturer):
        response = client.post("/equipment/",
                               headers=auth_headers_engineer,
                               json={
                                    "serial_number": equipment.serial_number,
                                    "model": "AnotherModel",
                                    "manufacturer_id": manufacturer.id,
                                    "location_address": "г. Тест, ул. друг, 2",
                                    "installation_date": "2024-01-01",
                                    "status_id": equipment_status.id,
                                    "latitude": 55.0,
                                    "longitude": 37.0
                                })
        assert response.status_code == 400

    def test_viewer_cannot_create(self, client, auth_headers_viewer,
                                  manufacturer, equipment_status):
        response = client.post("/equipment/",
                               headers=auth_headers_viewer,
                               json={
                                    "serial_number": "SN-FORBIDDEN",
                                    "model": "Model",
                                    "manufacturer_id": manufacturer.id,
                                    "location_address": "г. Тест, 1",
                                    "installation_date": "2024-01-01",
                                    "status_id": equipment_status.id,
                                    "latitude": 55.0,
                                    "longitude": 37.0
                                })
        assert response.status_code == 403


class TestUpdateEquipment:
    def test_engineer_can_update(self, client,
                                 auth_headers_engineer,
                                 equipment):
        response = client.put(
            f"/equipment/{equipment.id}",
            headers=auth_headers_engineer,
            json={"model": "UpdatedModel"}
        )
        assert response.status_code == 200
        assert response.json()["model"] == "UpdatedModel"

    def test_update_nonexistent(self, client, auth_headers_engineer):
        response = client.put(
            "/equipment/99999",
            headers=auth_headers_engineer,
            json={"model": "X"}
        )
        assert response.status_code == 404


class TestDeleteEquipment:
    def test_admin_can_delete_equipment_without_defects(
        self, client, db, auth_headers_admin, manufacturer, equipment_status
    ):
        from models.equipment import Equipment
        eq = Equipment(
            serial_number="SN-TO-DELETE",
            model="DeleteMe",
            manufacturer_id=manufacturer.id,
            location_address="г. Тест",
            installation_date=date(2024, 1, 1),
            status_id=equipment_status.id,
            latitude=1.0,
            longitude=1.0
        )
        db.add(eq)
        db.commit()
        db.refresh(eq)

        response = client.delete(f"/equipment/{eq.id}",
                                 headers=auth_headers_admin)
        assert response.status_code == 204

    def test_cannot_delete_equipment_with_defects(
        self, client, auth_headers_admin, equipment, defect
    ):
        response = client.delete(
            f"/equipment/{equipment.id}", headers=auth_headers_admin
        )
        assert response.status_code == 400

    def test_viewer_cannot_delete(self, client, auth_headers_viewer,
                                  equipment):
        response = client.delete(
            f"/equipment/{equipment.id}", headers=auth_headers_viewer
        )
        assert response.status_code == 403
