import { defineStore } from 'pinia';
import { apiRequest } from './api';

export const useDefectCriticalitiesStore = defineStore('defectCriticalities', {
  state: () => ({
    defectCriticalities: []
  }),

  actions: {
    async fetchDefectCriticalities() {
      const res = await apiRequest('/criticalities');
      if (res) this.defectCriticalities = await res.json();
    }
  }
});
