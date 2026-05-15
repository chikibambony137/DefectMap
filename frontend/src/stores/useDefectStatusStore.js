import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useDefectStatusStore = defineStore("defectStatuses", {
  state: () => ({
    statuses: [],
  }),

  actions: {
    async fetchDefectStatuses() {
      const res = await apiRequest("/defect-statuses");
      if (res) this.statuses = await res.json();
    },
  },
});