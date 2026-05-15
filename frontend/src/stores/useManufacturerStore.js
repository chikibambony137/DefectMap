import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useManufacturerStore = defineStore("manufacturers", {
  state: () => ({
    manufacturers: [],
  }),

  actions: {
    async fetchManufacturers() {
      const res = await apiRequest("/manufacturers");
      if (res) this.manufacturers = await res.json();
    },

    async addManufacturer(data) {
      const res = await apiRequest("/manufacturers", {
        method: "POST",
        body: JSON.stringify(data),
      });
      if (res?.ok) await this.fetchManufacturers();
    },

    async updateManufacturer(data, id) {
      const res = await apiRequest(`/manufacturers/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
      if (res?.ok) await this.fetchManufacturers();
    },

    async removeManufacturer(id) {
      const res = await apiRequest(`/manufacturers/${id}`, {
        method: "DELETE",
      });
      if (res?.ok) {
        await this.fetchManufacturers();
        alert("Успешно удалено!");
      }
    },
  },
});