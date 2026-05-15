import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useEquipmentStatusStore = defineStore("equipmentStatuses", {
  state: () => ({
    statuses: [],
  }),

  actions: {
    async fetchEquipmentStatuses() {
      const res = await apiRequest("/equipment-statuses");
      if (res) this.statuses = await res.json();
    },
  },
});