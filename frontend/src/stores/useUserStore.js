import { defineStore } from 'pinia';
import { apiRequest } from './api';

export const useUserStore = defineStore('users', {
  state: () => ({
    users: [],
    loading: false
  }),

  actions: {
    async fetchUsers() {
      this.loading = true;
      try {
        const res = await apiRequest('/users');
        if (res) this.users = await res.json();
      } finally {
        this.loading = false;
      }
    },

    async getMyUser() {
      this.loading = true;
      try {
        const res = await apiRequest('/auth/me');
        if (res?.ok) return await res.json();
        return null;
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

    async addUser(user) {
      const res = await apiRequest('/users', {
        method: 'POST',
        body: JSON.stringify(user)
      });

      if (res?.ok) {
        const newUser = await res.json();
        this.users.push(newUser);
      } else
        throw new Error(res.data?.detail || 'Ошибка при добавлении пользователя');
    },

    async updateUser(user, userId) {
      const res = await apiRequest(`/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(user)
      });
      if (!res?.ok)
        throw new Error(res.data?.detail || 'Ошибка при обновлении пользователя');
      else this.fetchUsers();
    },

    async deleteUser(userId) {
      const res = await apiRequest(`/users/${userId}`, {
        method: 'DELETE'
      });
      if (!res?.ok) {
        throw new Error(res.data?.detail || 'Ошибка при удалении пользователя');
      } else this.fetchUsers();
    }
  }
});
