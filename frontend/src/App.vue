<template>
  <router-view />
</template>
<script setup>
import { useWebSocketStore } from './stores/webSocket';
import { onMounted, onUnmounted } from 'vue';

onMounted(() => {
  const wsStore = useWebSocketStore();
  wsStore.connect();
});

onUnmounted(() => {
  const wsStore = useWebSocketStore();
  wsStore.disconnect();
});
</script>
