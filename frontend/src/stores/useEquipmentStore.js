import { defineStore } from "pinia";

export const useEquipmentStore = defineStore("equipment", {
  state: () => ({
    items: [],
    loading: false,
  }),

  actions: {
    async fetchEquipment() {
      this.loading = true;
      try {
        const res = await fetch("http://localhost:8000/equipment", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (res.status === 401) {
          localStorage.removeItem("access_token");
          router.push("/login");
        }
        this.items = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async addEquipment(equipment) {
      const res = await fetch("http://localhost:8000/equipment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(equipment),
      });
      const newItem = await res.json();
      this.items.push(newItem); // добавить в кэш
    },

    async updateEquipment(equipment, equipmentId) {
      console.log(equipment);
      const res = await fetch(`http://localhost:8000/equipment/${equipmentId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(equipment),
      });
      if (res.ok) this.fetchEquipment();
      else console.log("error");
    },

    async removeEquipment(equipment) {
      const res = await fetch(
        `http://localhost:8000/equipment/${equipment.id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (res.ok) {
        this.fetchEquipment();
        alert("Успешно удалено!");
      } else console.log("error");
    },
  },
});
