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
              />
              <q-btn
                size="sm"
                icon="edit"
                color="primary"
                @click="updateDefect"
              />
              <q-btn
                size="sm"
                icon="delete"
                color="negative"
                @click="delDefect"
              />
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
            v-if="mapReady"
            ref="mapRef"
            :center="
              selectedDefect
                ? [selectedDefect.latitude, selectedDefect.longitude]
                : [55.751574, 37.573856]
            "
            :points="mapPoints"
          />
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
import { ref, computed, onMounted } from 'vue';
import { useQuasar } from 'quasar';
import YandexMap from 'src/components/YandexMap.vue';
import AddDefect from 'src/components/AddDefect.vue';
import UpdateDefect from 'src/components/UpdateDefect.vue';
import { useDefectStore } from 'src/stores/useDefectStore';
import { apiRequest } from 'src/stores/api';

const $q = useQuasar();
const mapRef = ref(null);
const splitterModel = ref(50);
const onSplitterResize = () => mapRef.value?.invalidateSize();

const store = useDefectStore();
const mapReady = ref(false);
onMounted(async() => {
  await store.fetchDefects();
  mapReady.value = true;
});

const isAddDefectVisible = ref(false);
const isUpdateDefectVisible = ref(false);
const fullDefect = ref(null);
const selectedRows = ref([]);
const selectedDefect = ref(null);

const onRowClick = (event, row) => {
  selectedRows.value = [row];
  selectedDefect.value = row;
};

const updateDefect = async() => {
  if (!selectedDefect.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите дефект',
      position: 'top'
    });
    return;
  }
  const res = await apiRequest(`/defects/${selectedDefect.value.id}`);
  fullDefect.value = await res.json();
  isUpdateDefectVisible.value = true;
};

const delDefect = () => {
  if (!selectedDefect.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите дефект',
      position: 'top'
    });
    return;
  }

  $q.dialog({
    title: 'Подтверждение',
    message: `Вы уверены, что хотите удалить дефект ${selectedDefect.value.equipment_model} '${selectedDefect.value.title}'?`,
    cancel: true,
    persistent: true
  }).onOk(async() => {
    try {
      await store.removeDefect(selectedDefect.value.id);
      selectedDefect.value = null;
      selectedRows.value = [];

      $q.notify({
        type: 'positive',
        message: 'Успешно удалено!',
        position: 'top'
      });
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: error.message || 'Не удалось удалить дефект',
        position: 'top'
      });
    }
  });
};

const mapPoints = computed(() =>
  (store.defects ?? []).map((d) => ({
    coords: [d.latitude, d.longitude],
    name: d.equipment_model,
    color:
      d.criticality === 'high'
        ? 'red'
        : d.criticality === 'medium'
          ? 'yellow'
          : 'green'
  }))
);

// prettier-ignore
const columns = [
  { name: 'equipment_serial', align: 'center', label: 'Серийный номер', field: 'equipment_serial', sortable: true, style: 'min-width: 85px; max-width: 85px; word-break: break-word; white-space: normal;', headerStyle: 'word-break: break-word; white-space: normal;' },
  { name: 'equipment_model',  align: 'center', label: 'Модель',         field: 'equipment_model',  sortable: true, style: 'word-break: break-word; white-space: normal;' },
  { name: 'title',            align: 'center', label: 'Наименование',   field: 'title',            sortable: true, style: 'word-break: break-word; white-space: normal;' },
  { name: 'description',      align: 'center', label: 'Описание',       field: 'description',      sortable: true, style: 'word-break: break-word; white-space: normal;' },
  { name: 'status',           align: 'center', label: 'Статус',         field: 'status',           sortable: true, style: 'word-break: break-word; white-space: normal;' },
  { name: 'created_at',       align: 'center', label: 'Дата создания',  field: (row) => { const date = new Date(row.created_at); date.setHours(date.getHours() + 3); return date.toLocaleString(); }, sortable: true, style: 'word-break: break-word; white-space: normal;' }
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
