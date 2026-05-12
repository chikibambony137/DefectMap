<template>
  <q-card style="min-width: 450px">
    <q-card-section class="row items-center justify-between q-pb-none">
      <div class="text-h6">Редактировать прибор</div>
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
          <q-btn label="Обновить" type="submit" color="positive" />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref } from "vue";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { useYandexAddressGeocoder } from "src/composables/useYandexAddressGeocoder";

const props = defineProps({
  equipment: Object,
});

const { getCoordsByAddress } = useYandexAddressGeocoder();

const emit = defineEmits(["close"]);
const store = useEquipmentStore();

const statusOptions = [
  { label: "Активен", value: "active" },
  { label: "На обслуживании", value: "maintenance" },
  { label: "Выведен из эксплуатации", value: "decommissioned" },
];

// копируем данные дефекта в форму, чтобы не мутировать пропс напрямую
const form = ref({
  serial_number: props.equipment?.serial_number,
  model: props.equipment?.model,
  manufacturer: props.equipment?.manufacturer,
  location_address: props.equipment?.location_address,
  installation_date: props.equipment?.installation_date,
  status: props.equipment?.status,
});

const onSubmit = async () => {
  const coords = await getCoordsByAddress(form.value.location_address);
  if (!coords) {
    console.log("address parsing error");
    return;
  }

  await store.updateEquipment(
    {
      ...form.value,
      latitude: coords.latitude,
      longitude: coords.longitude,
    },
    props.equipment.id,
  );

  alert("Успешно обновлено!");

  emit("close");
};
</script>
