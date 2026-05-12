<template>
  <q-card style="min-width: 450px">
    <q-card-section class="row items-center justify-between q-pb-none">
      <div class="text-h6">Добавить прибор</div>
      <q-btn icon="close" flat round dense @click="$emit('close')" />
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" class="q-gutter-sm">
        <q-input
          filled
          v-model="form.serial_number"
          label="Серийный номер"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-input
          filled
          v-model="form.model"
          label="Модель"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-input
          filled
          v-model="form.manufacturer"
          label="Производитель"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-input
          filled
          v-model="form.location_address"
          label="Адрес установки"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-input
          filled
          v-model="form.installation_date"
          label="Дата установки"
          type="date"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-select
          filled
          v-model="form.status"
          :options="statusOptions"
          label="Статус"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите статус']"
        />

        <q-card-actions align="right" class="q-pt-md">
          <q-btn flat label="Отмена" @click="$emit('close')" />
          <q-btn label="Добавить" type="submit" color="positive" />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref } from "vue";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { useYandexAddressGeocoder } from "src/composables/useYandexAddressGeocoder";

const { getCoordsByAddress } = useYandexAddressGeocoder();

const emit = defineEmits(["close"]);
const store = useEquipmentStore();

const statusOptions = [
  { label: "Активен", value: "active" },
  { label: "На обслуживании", value: "maintenance" },
  { label: "Выведен из эксплуатации", value: "decommissioned" },
];

const form = ref({
  serial_number: "",
  model: "",
  manufacturer: "",
  location_address: "",
  installation_date: "",
  status: null,
});

const onSubmit = async () => {
  const coords = await getCoordsByAddress(form.value.location_address);
  if (!coords) {
    console.log("address parsing error");
    return;
  }
  
  await store.addEquipment({
    ...form.value,
    latitude: coords.latitude,
    longitude: coords.longitude,
  });

  alert('Успешно добавлено!');

  emit("close");
};
</script>
