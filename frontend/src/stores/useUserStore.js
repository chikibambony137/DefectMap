import { defineStore } from "pinia";
import { apiRequest } from "./api";

export const useUserStore = defineStore("users", {
  state: () => ({
    users: [],
    loading: false,
  }),

  actions: {
    async fetchUsers() {
      this.loading = true;
      try {
        const res = await apiRequest("/users");
        if (res) this.users = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async fetchUserById(userId) {
      this.loading = true;
      try {
        const res = await apiRequest(`/users/${userId}`);
        if (res?.ok) return await res.json();
        return null;
      } finally {
        this.loading = false;
      }
    },

    async updateUser(user, userId) {
      const res = await apiRequest(`/users/${userId}`, {
        method: "PUT",
        body: JSON.stringify(user),
      });
      return res?.ok || false;
    },

    async addUser(user) {
      const res = await apiRequest("/users", {
        method: "POST",
        body: JSON.stringify(user),
      });
      if (res?.ok) {
        const newUser = await res.json();
        this.users.push(newUser);
      }
    },
  },
});