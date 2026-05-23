<template>
  <div class="row">
    <div class="column q-pa-md q-px-xl" style="gap: 10px">
      <div class="row justify-end" style="gap: 20px">
        <q-btn
          size="sm"
          icon="add"
          color="positive"
          @click="isAddEquipmentVisible = !isAddEquipmentVisible"
        />
        <q-btn size="sm" icon="edit" color="primary" @click="updateEquipment" />
        <q-btn size="sm" icon="delete" color="negative" @click="delEquipment" />
      </div>

      <q-table
        flat
        bordered
        title="Приборы"
        dense
        selection="single"
        v-model:selected="selectedRows"
        :rows="store.items"
        :columns="columns"
        :loading="store.loading"
        row-key="id"
        @row-click="onRowClick"
        style="max-height: 550px; overflow-y: auto"
      >
        <!-- имя статуса вместо id -->
        <template #body-cell-status_id="props">
          <q-td :props="props">{{ statusName(props.row.status_id) }}</q-td>
        </template>
        <!-- имя производителя вместо id -->
        <template #body-cell-manufacturer_id="props">
          <q-td :props="props">{{
            manufacturerName(props.row.manufacturer_id)
          }}</q-td>
        </template>
      </q-table>
    </div>

    <div class="q-px-md" style="width: 500px" v-if="selectedEquipment">
      <h3 class="text-black" style="font-size: 20px">
        {{ selectedEquipment.serial_number }} {{ selectedEquipment.model }}
        {{ selectedEquipment.status_id === activeStatusId ? "🟢" : "🔴" }}
      </h3>
      <p>Дата установки: {{ selectedEquipment.installation_date }}</p>
      <p>
        Производитель: {{ manufacturerName(selectedEquipment.manufacturer_id) }}
      </p>
      <p>Статус: {{ statusName(selectedEquipment.status_id) }}</p>

      <div v-if="equipmentDefects && equipmentDefects.length">
        <div v-for="defect in equipmentDefects" :key="defect.id">
          <p>Дефект: {{ defect.title }}</p>
          <p>- {{ defect.description }}</p>
        </div>
      </div>
      <div v-else-if="equipmentDefects === null">Загрузка...</div>
      <div v-else>Нет дефектов</div>

      <yandex-map
        style="max-height: 400px; max-width: 400px"
        :center="[selectedEquipment.latitude, selectedEquipment.longitude]"
        :points="[
          {
            coords: [selectedEquipment.latitude, selectedEquipment.longitude],
            name: selectedEquipment.model,
            color:
              selectedEquipment.status_id === activeStatusId ? 'green' : 'red',
          },
        ]"
      />
    </div>

    <q-dialog v-model="isAddEquipmentVisible">
      <AddEquipment @close="isAddEquipmentVisible = false" />
    </q-dialog>

    <q-dialog v-model="isUpdateEquipmentVisible">
      <UpdateEquipment
        @close="isUpdateEquipmentVisible = false"
        :equipment="selectedEquipment"
      />
    </q-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import YandexMap from "src/components/YandexMap.vue";
import AddEquipment from "src/components/AddEquipment.vue";
import UpdateEquipment from "src/components/UpdateEquipment.vue";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { useEquipmentStatusStore } from "src/stores/useEquipmentStatusStore";
import { useManufacturerStore } from "src/stores/useManufacturerStore";
import { apiRequest } from "src/stores/api";

const $q = useQuasar();
const store = useEquipmentStore();
const statusStore = useEquipmentStatusStore();
const manufacturerStore = useManufacturerStore();

onMounted(() => {
  store.fetchEquipment();
  if (!statusStore.statuses.length) statusStore.fetchEquipmentStatuses();
  if (!manufacturerStore.manufacturers.length)
    manufacturerStore.fetchManufacturers();
});

const statusName = (id) =>
  statusStore.statuses.find((s) => s.id === id)?.name ?? id;
const manufacturerName = (id) =>
  manufacturerStore.manufacturers.find((m) => m.id === id)?.name ?? id;

const activeStatusId = computed(
  () => statusStore.statuses.find((s) => s.name === "Активен")?.id,
);

const selectedRows = ref([]);
const selectedEquipment = ref(null);
const equipmentDefects = ref(null);

const onRowClick = async (event, row) => {
  selectedRows.value = [row];
  selectedEquipment.value = row;
  equipmentDefects.value = null;
  const res = await apiRequest(`/defects/?skip=0&equipment_id=${row.id}`);
  equipmentDefects.value = res ? await res.json() : [];
};

const isAddEquipmentVisible = ref(false);
const isUpdateEquipmentVisible = ref(false);

const updateEquipment = () => {
  if (selectedEquipment.value) {
    isUpdateEquipmentVisible.value = true;
  } else {
    $q.notify({
      type: "warning",
      message: "Выберите прибор",
      position: "top",
    });
  }
};

const delEquipment = () => {
  if (!selectedEquipment.value) {
    $q.notify({
      type: "warning",
      message: "Выберите прибор",
      position: "top",
    });
    return;
  }

  $q.dialog({
    title: "Подтверждение",
    message: `Вы уверены, что хотите удалить ${selectedEquipment.value.model}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      await store.removeEquipment(selectedEquipment.value.id);
      selectedEquipment.value = null;
      selectedRows.value = [];

      $q.notify({
        type: "positive",
        message: "Успешно удалено!",
        position: "top",
      });
    } catch (error) {
      $q.notify({
        type: "negative",
        message: error.message || "Не удалось удалить прибор",
        position: "top",
      });
    }
  });
};

// prettier-ignore
const columns = [
  { name: "serial_number",    align: "center", label: "Серийный номер",  field: "serial_number",   sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "model",            align: "center", label: "Модель",          field: "model",           sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "manufacturer_id",  align: "center", label: "Производитель",   field: "manufacturer_id", sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "location_address", align: "center", label: "Адрес установки", field: "location_address",sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "installation_date",align: "center", label: "Дата установки",  field: (row) => new Date(row.installation_date).toLocaleDateString(), sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "status_id",        align: "center", label: "Статус",          field: "status_id",       sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
];
</script>

<style scoped>
:deep(.q-table th:first-child),
:deep(.q-table td:first-child) {
  display: none;
}
</style>
