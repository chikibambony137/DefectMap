import { defineStore } from "pinia";

export const useUserStore = defineStore("users", {
  state: () => ({
    users: [],
    loading: false,
  }),

  actions: {
    async fetchUsers() {
      this.loading = true;
      try {
        const res = await fetch("http://localhost:8000/users", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        });
        if (res.status === 401) {
          localStorage.removeItem("access_token");
          router.push("/login");
        }
        this.users = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async addUser(user) {
      const res = await fetch("http://localhost:8000/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user),
      });
      const newUser = await res.json();
      this.users.push(newUser); // добавить в кэш
    },
    // ... update, delete
  },
});
