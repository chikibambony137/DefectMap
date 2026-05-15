import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useDefectStore = defineStore("defects", {
  state: () => ({
    defects: [],
    loading: false,
  }),

  actions: {
    async fetchDefects() {
      this.loading = true;
      try {
        const res = await apiRequest("/defects/geo");
        if (res) this.defects = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async addDefect(defect) {
      const res = await apiRequest("/defects", {
        method: "POST",
        body: JSON.stringify(defect),
      });
      if (res?.ok) await this.fetchDefects();
    },

    async updateDefect(defect, defectId) {
      const res = await apiRequest(`/defects/${defectId}`, {
        method: "PUT",
        body: JSON.stringify(defect),
      });
      if (res?.ok) await this.fetchDefects();
      else console.error("updateDefect error");
    },

    async removeDefect(defectId) {
      const res = await apiRequest(`/defects/${defectId}`, {
        method: "DELETE",
      });
      if (res?.ok) {
        await this.fetchDefects();
        alert("Успешно удалено!");
      } else console.error("removeDefect error");
    },
  },
});