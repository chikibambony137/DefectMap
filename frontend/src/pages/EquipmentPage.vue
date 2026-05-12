<template>
  <div class="row">
    <div class="column q-pa-md q-px-xl" style="gap: 10px">
      <div class="row justify-end" style="gap: 20px">
        <q-btn
          size="sm"
          icon="add"
          color="positive"
          @click="isAddEquipmentVisible = !isAddEquipmentVisible"
        ></q-btn>

        <q-btn
          size="sm"
          icon="edit"
          color="primary"
          @click="updateEquipment"
        ></q-btn>

        <q-btn
          size="sm"
          icon="delete"
          color="negative"
          @click="delEquipment"
        ></q-btn>
      </div>

      <div>
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
        />
      </div>
    </div>

    <div class="q-px-md" style="width: 500px" v-if="selectedEquipment">
      <h3 class="text-black" style="font-size: 20px">
        {{ selectedEquipment.serial_number }}
        {{ selectedEquipment.model }}
        {{ selectedEquipment.status === "active" ? "🟢" : "🔴" }}
      </h3>
      <p>Дата установки: {{ selectedEquipment.installation_date }}</p>
      <p>Производитель: {{ selectedEquipment.manufacturer }}</p>

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
            color: selectedEquipment.status === 'active' ? 'green' : 'red',
          },
        ]"
      ></yandex-map>
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
import YandexMap from "src/components/YandexMap.vue";
import AddEquipment from "src/components/AddEquipment.vue";
import UpdateEquipment from "src/components/UpdateEquipment.vue";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { onMounted, ref } from "vue";

const store = useEquipmentStore();
onMounted(() => store.fetchEquipment());

const selectedRows = ref([]);
const selectedEquipment = ref(null);
const equipmentDefects = ref(null);
const onRowClick = (event, row, index) => {
  selectedRows.value = [row];
  selectedEquipment.value = row;
  fetchDefects(selectedEquipment.value.id);
};

const fetchDefects = async (id) => {
  try {
    const res = await fetch(
      `http://localhost:8000/defects/?skip=0&equipment_id=${id}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      },
    );
    if (res.status === 401) {
      localStorage.removeItem("access_token");
      router.push("/login");
    }
    equipmentDefects.value = await res.json();
  } catch (error) {
    console.log("Ошибка! ", error);
  }
};

const isAddEquipmentVisible = ref(false);
const isUpdateEquipmentVisible = ref(false);

const updateEquipment = () => {
  if (selectedEquipment.value)
    isUpdateEquipmentVisible.value = !isUpdateEquipmentVisible.value;
  else alert("Выберите прибор!");
};

const delEquipment = () => {
  if (!selectedEquipment.value) alert("Выберите прибор!");
  else {
    if (
      confirm(
        `Вы уверены, что хотите удалить ${selectedEquipment.value.model}?`,
      )
    )
      store.removeEquipment(selectedEquipment.value);
  }
};

const columns = [
  {
    name: "serial_number",
    align: "center",
    label: "Серийный номер",
    field: "serial_number",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "model",
    align: "center",
    label: "Модель",
    field: "model",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "manufacturer",
    align: "center",
    label: "Производитель",
    field: "manufacturer",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "location_address",
    align: "center",
    label: "Адрес установки",
    field: "location_address",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "installation_date",
    align: "center",
    label: "Дата установки",
    field: "installation_date",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "status",
    align: "center",
    label: "Статус",
    field: "status",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
];
</script>

<style scoped>
:deep(.q-table th:first-child),
:deep(.q-table td:first-child) {
  display: none;
}
</style>
