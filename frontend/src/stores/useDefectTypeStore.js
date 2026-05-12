import { defineStore } from "pinia";

export const useDefectTypeStore = defineStore("defectTypes", {
  state: () => ({
    defectTypes: []
  }),

  actions: {
    async fetchDefectTypes() {
      try {
        const res = await fetch("http://localhost:8000/defect-types", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (res.status === 401) {
          localStorage.removeItem("access_token");
          router.push("/login");
        }
        this.defectTypes = await res.json();
      } catch {
        console.log('defectTypes fetch error');
      }
    }
  },
});
