import { defineStore } from 'pinia';
import { apiRequest } from './api';

export const useDefectTypeStore = defineStore('defectTypes', {
  state: () => ({
    defectTypes: []
  }),

  actions: {
    async fetchDefectTypes() {
      const res = await apiRequest('/defect-types');
      if (res) this.defectTypes = await res.json();
    }
  }
});
