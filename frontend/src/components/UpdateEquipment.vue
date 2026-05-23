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
          :rules="[
            (val) => (val && val.trim().length > 0) || 'Заполните поле',
            (val) => val.trim().length >= 3 || 'Минимум 3 символа',
            (val) => val.trim().length <= 50 || 'Максимум 50 символов',
          ]"
        />

        <q-input
          filled
          v-model="form.model"
          label="Модель"
          lazy-rules
          :rules="[
            (val) => (val && val.trim().length > 0) || 'Заполните поле',
            (val) => val.trim().length >= 2 || 'Минимум 2 символа',
            (val) => val.trim().length <= 100 || 'Максимум 100 символов',
          ]"
        />

        <q-select
          filled
          v-model="form.manufacturer_id"
          :options="manufacturerOptions"
          label="Производитель"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите производителя']"
        />

        <q-input
          filled
          v-model="form.location_address"
          label="Адрес установки"
          lazy-rules
          :rules="[
            (val) => (val && val.trim().length > 0) || 'Заполните поле',
            (val) => val.trim().length >= 5 || 'Введите полный адрес',
          ]"
        />

        <q-input
          filled
          v-model="form.installation_date"
          label="Дата установки"
          type="date"
          lazy-rules
          :rules="[
            (val) => (val && val.length > 0) || 'Укажите дату установки',
            (val) =>
              new Date(val) <= new Date() || 'Дата не может быть в будущем',
          ]"
        />

        <q-select
          filled
          v-model="form.status_id"
          :options="statusOptions"
          label="Статус"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите статус']"
        />

        <q-card-actions align="right" class="q-pt-md">
          <q-btn flat label="Отмена" @click="$emit('close')" />
          <q-btn
            label="Обновить"
            type="submit"
            color="positive"
            :loading="isLoading"
          />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useQuasar } from "quasar";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { useEquipmentStatusStore } from "src/stores/useEquipmentStatusStore";
import { useManufacturerStore } from "src/stores/useManufacturerStore";
import { useYandexAddressGeocoder } from "src/composables/useYandexAddressGeocoder";

const props = defineProps({ equipment: Object });
const emit = defineEmits(["close", "updated"]);

const { getCoordsByAddress } = useYandexAddressGeocoder();
const $q = useQuasar();
const store = useEquipmentStore();
const statusStore = useEquipmentStatusStore();
const manufacturerStore = useManufacturerStore();

const isLoading = ref(false);

onMounted(() => {
  if (!statusStore.statuses.length) statusStore.fetchEquipmentStatuses();
  if (!manufacturerStore.manufacturers.length)
    manufacturerStore.fetchManufacturers();
});

const statusOptions = computed(() =>
  statusStore.statuses.map((s) => ({ label: s.name, value: s.id })),
);

const manufacturerOptions = computed(() =>
  manufacturerStore.manufacturers.map((m) => ({ label: m.name, value: m.id })),
);

const form = ref({
  serial_number: props.equipment?.serial_number ?? "",
  model: props.equipment?.model ?? "",
  manufacturer_id: props.equipment?.manufacturer_id ?? null,
  location_address: props.equipment?.location_address ?? "",
  installation_date: props.equipment?.installation_date ?? "",
  status_id: props.equipment?.status_id ?? null,
});

const onSubmit = async () => {
  isLoading.value = true;
  try {
    const coords = await getCoordsByAddress(form.value.location_address);
    if (!coords) {
      $q.notify({
        type: "warning",
        message: "Не удалось определить координаты по указанному адресу",
        position: "top",
      });
      return;
    }

    await store.updateEquipment(
      {
        ...form.value,
        serial_number: form.value.serial_number.trim(),
        model: form.value.model.trim(),
        location_address: form.value.location_address.trim(),
        latitude: coords.latitude,
        longitude: coords.longitude,
      },
      props.equipment.id,
    );

    $q.notify({
      type: "positive",
      message: "Прибор успешно обновлён",
      position: "top",
    });

    emit("updated");
    emit("close");
  } catch (error) {
    console.error("Ошибка при обновлении прибора:", error);
    $q.notify({
      type: "negative",
      message: error.message || "Не удалось обновить прибор",
      position: "top",
    });
  } finally {
    isLoading.value = false;
  }
};
</script>
