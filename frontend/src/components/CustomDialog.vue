<template>
  <q-dialog v-model="isVisible">
    <q-card>
      <q-card-section>
        <div class="text-h6">{{ title }}</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        {{ body }}
      </q-card-section>

      <q-card-actions align="right" v-if="type === 'alert'">
        <q-btn flat
               label="OK"
               color="primary"
               @click="onOk" />
      </q-card-actions>

      <q-card-actions align="right" v-if="type === 'confirm'">
        <q-btn flat
               label="Отмена"
               color="primary"
               @click="onCancel" />
        <q-btn flat
               label="OK"
               color="primary"
               @click="onOk" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  type: {
    type: String,
    required: true
  },
  title: {
    type: String
  },
  body: {
    type: String
  },
  visible: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['ok', 'cancel', 'update:visible']);

const isVisible = ref(props.visible);

watch(() => props.visible, (val) => {
  isVisible.value = val;
});

watch(isVisible, (val) => {
  emit('update:visible', val);
});

const onOk = () => {
  isVisible.value = false;
  emit('ok');
};

const onCancel = () => {
  isVisible.value = false;
  emit('cancel');
};
</script>
