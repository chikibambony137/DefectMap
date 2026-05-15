import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useEquipmentStore = defineStore("equipment", {
  state: () => ({
    items: [],
    loading: false,
  }),

  actions: {
    async fetchEquipment() {
      this.loading = true;
      try {
        const res = await apiRequest("/equipment");
        if (res) this.items = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async addEquipment(equipment) {
      const res = await apiRequest("/equipment", {
        method: "POST",
        body: JSON.stringify(equipment),
      });
      if (res?.ok) await this.fetchEquipment();
    },

    async updateEquipment(equipment, equipmentId) {
      const res = await apiRequest(`/equipment/${equipmentId}`, {
        method: "PUT",
        body: JSON.stringify(equipment),
      });
      if (res?.ok) await this.fetchEquipment();
      else console.error("updateEquipment error");
    },

    async removeEquipment(equipmentId) {
      const res = await apiRequest(`/equipment/${equipmentId}`, {
        method: "DELETE",
      });
      if (res?.ok) {
        await this.fetchEquipment();
        alert("Успешно удалено!");
      } else console.error("removeEquipment error");
    },
  },
});