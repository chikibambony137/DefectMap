import { defineStore } from 'pinia';
import { useDefectStore } from './useDefectStore';
import { useQuasar } from 'quasar';

export const useWebSocketStore = defineStore('websocket', {
  state: () => ({
    ws: null
  }),

  actions: {
    connect() {
      const $q = useQuasar();
      const wsUrl = 'ws://localhost:8000/ws';
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const inner = JSON.parse(data.data);
          const defectsStore = useDefectStore();

          if (data.event === 'created') {
            defectsStore.fetchDefects();
            $q.notify({
              type: 'positive',
              message: `Добавлен новый дефект: ${inner.equipment_serial_number} ${inner.equipment_model} - ${inner.title}`,
              position: 'top'
            });
          }

          if (data.event === 'deleted') {
            defectsStore.fetchDefects();
            $q.notify({
              type: 'negative',
              message: `Дефект удалён: ${inner.equipment_serial_number} ${inner.equipment_model} - ${inner.title}`,
              position: 'top'
            });
          }

          if (data.event === 'updated') {
            defectsStore.fetchDefects();
            $q.notify({
              type: 'positive',
              message: `Дефект обновлён: ${inner.equipment_serial_number} ${inner.equipment_model} - ${inner.title}`,
              position: 'top'
            });
          }

        } catch {
          $q.notify({
            type: 'error',
            message: `'Failed to parse WS message: ${event.data}`,
            position: 'top'
          });
        }
      };

      // eslint-disable-next-line
      this.ws.onopen = () => console.log('🔌 WebSocket connected');
      // eslint-disable-next-line
      this.ws.onerror = (error) => console.error('WebSocket error:', error);

      this.ws.onclose = (event) => {
        // 1001 = сервер закрыл (LOCAL_MODE), не реконнектим
        if (this._intentionalClose || event.code === 1001) return;
        // eslint-disable-next-line
        console.warn('🔌 WebSocket disconnected, reconnecting in 3s...');
        setTimeout(() => this.connect(), 3000);
      };
    },

    disconnect() {
      this.ws?.close();
    }
  }
});
