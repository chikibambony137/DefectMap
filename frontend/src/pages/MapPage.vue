<template>
  <q-page class="flex flex-center">
    <q-splitter
      v-model="splitterModel"
      :limits="[20, 50]"
      class="fit"
      @update:model-value="onSplitterResize"
    >
      <template v-slot:before>
        <div class="q-pa-md">
          <div class="column q-pa-md q-mx-xl" style="gap: 10px">
            <div class="row justify-end" style="gap: 20px">
              <q-btn
                size="sm"
                icon="add"
                color="positive"
                @click="isAddDefectVisible = !isAddDefectVisible"
              ></q-btn>

              <q-btn
                size="sm"
                icon="edit"
                color="primary"
                @click="updateDefect"
              ></q-btn>

              <q-btn
                size="sm"
                icon="delete"
                color="negative"
                @click="delDefect"
              ></q-btn>
            </div>

            <q-table
              flat
              bordered
              title="Дефекты"
              dense
              selection="single"
              v-model:selected="selectedRows"
              :rows="store.defects"
              :columns="columns"
              :loading="store.loading"
              row-key="id"
              @row-click="onRowClick"
              style="max-height: 550px; overflow-y: auto"
            />
          </div>
        </div>
      </template>

      <template v-slot:after>
        <div class="map-wrapper">
          <YandexMap
            ref="mapRef"
            :center="
              selectedDefect
                ? [selectedDefect.latitude, selectedDefect.longitude]
                : [55.751574, 37.573856]
            "
            :points="mapPoints"
          ></YandexMap>
        </div>
      </template>
    </q-splitter>

    <q-dialog v-model="isAddDefectVisible">
      <AddDefect
        @close="isAddDefectVisible = false"
        @added="store.fetchDefects()"
      />
    </q-dialog>

    <q-dialog v-model="isUpdateDefectVisible">
      <UpdateDefect
        @close="isUpdateDefectVisible = false"
        @updated="store.fetchDefects()"
        :defect="fullDefect"
      />
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import YandexMap from "src/components/YandexMap.vue";
import { useDefectStore } from "src/stores/useDefectStore";
import AddDefect from "src/components/AddDefect.vue";
import UpdateDefect from "src/components/UpdateDefect.vue";

const mapRef = ref(null);
const splitterModel = ref(50);

const onSplitterResize = () => {
  // Сообщаем карте, что размер изменился
  mapRef.value?.invalidateSize();
};

const store = useDefectStore();
onMounted(() => {
  store.fetchDefects();
});

const isAddDefectVisible = ref(false);
const isUpdateDefectVisible = ref(false);
const fullDefect = ref(null);

const updateDefect = async () => {
  if (!selectedDefect.value) {
    alert("Выберите дефект!");
    return;
  }
  // загрузить полный объект с equipment_id, criticality_id и т.д.
  const res = await fetch(
    `http://localhost:8000/defects/${selectedDefect.value.id}`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    },
  );
  fullDefect.value = await res.json();
  isUpdateDefectVisible.value = true;
};

const delDefect = () => {
  if (!selectedDefect.value) alert("Выберите дефект!");
  else {
    if (
      confirm(
        `Вы уверены, что хотите удалить дефект ${selectedDefect.value.equipment_model} \'${selectedDefect.value.title}\'?`,
      )
    )
      store.removeDefect(selectedDefect.value);
  }
};

const mapPoints = computed(() => {
  if (!store.defects || !store.defects.length) return [];
  return store.defects.map((defect) => ({
    coords: [defect.latitude, defect.longitude],
    name: defect.equipment_model,
    color:
      defect.criticality === "high"
        ? "red"
        : defect.criticality === "medium"
          ? "yellow"
          : defect.criticality === "low"
            ? "green"
            : "gray",
  }));
});

const selectedRows = ref([]);
const selectedDefect = ref();
const onRowClick = (event, row, index) => {
  selectedRows.value = [row];
  selectedDefect.value = row;
};

const columns = [
  {
    name: "equipment_serial",
    align: "center",
    label: "Серийный номер",
    field: "equipment_serial",
    sortable: true,
    style:
      "min-width: 85px; max-width: 85px; word-break: break-word; white-space: normal;",
    headerStyle: "word-break: break-word; white-space: normal;",
  },
  {
    name: "equipment_model",
    align: "center",
    label: "Модель",
    field: "equipment_model",
    sortable: true,
    style: "word-break: break-word; white-space: normal;",
  },
  {
    name: "title",
    align: "center",
    label: "Наименование",
    field: "title",
    sortable: true,
    style: "word-break: break-word; white-space: normal;",
  },
  {
    name: "description",
    align: "center",
    label: "Описание",
    field: "description",
    sortable: true,
    style: "word-break: break-word; white-space: normal;",
  },
  {
    name: "status",
    align: "center",
    label: "Статус",
    field: "status",
    sortable: true,
    style: "word-break: break-word; white-space: normal;",
  },

  {
    name: "created_at",
    align: "center",
    label: "Дата создания",
    field: "created_at",
    sortable: true,
    style: "word-break: break-word; white-space: normal;",
  },
];
</script>

<style scoped>
.map-wrapper {
  height: 92dvh;
  width: 100%;
  overflow: hidden;
}
:deep(.q-table th:first-child),
:deep(.q-table td:first-child) {
  display: none;
}
</style>
