import { defineStore } from "pinia";

export const useDefectStore = defineStore("defects", {
  state: () => ({
    defects: [],
    loading: false,
  }),

  actions: {
    async fetchDefects() {
      this.loading = true;
      try {
        const res = await fetch("http://localhost:8000/defects/geo", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (res.status === 401) {
          localStorage.removeItem("access_token");
          router.push("/login");
        }
        this.defects = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async addDefect(defect) {
      console.log(defect);
      const res = await fetch("http://localhost:8000/defects", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(defect),
      });
      const newDefect = await res.json();
      this.defects.push(newDefect);
    },

    async updateDefect(defect, defectId) {
      const res = await fetch(`http://localhost:8000/defects/${defectId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(defect),
      });
      if (res.ok) {
        this.fetchDefects();
      } 
      else console.log("error");
    },

    async removeDefect(defect) {
      const res = await fetch(
        `http://localhost:8000/defects/${defect.id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (res.ok) {
        this.fetchDefects();
        alert("Успешно удалено!");
      } else console.log("error");
    },
  },
});
