<template>
  <q-card style="min-width: 450px">
    <q-card-section class="row items-center justify-between q-pb-none">
      <div class="text-h6">Редактировать дефект</div>
      <q-btn icon="close" flat round dense @click="$emit('close')" />
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" class="q-gutter-sm">
        <q-select
          filled
          v-model="form.equipment_id"
          :options="equipmentOptions"
          label="Прибор"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите прибор']"
        />

        <q-input
          filled
          v-model="form.title"
          label="Наименование дефекта"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-input
          filled
          v-model="form.description"
          label="Описание"
          type="textarea"
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
        />

        <q-select
          filled
          v-model="form.defect_type_id"
          :options="typeOptions"
          label="Тип дефекта"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите тип']"
        />

        <q-select
          filled
          v-model="form.criticality_id"
          :options="criticalityOptions"
          label="Критичность"
          emit-value
          map-options
          lazy-rules
          :rules="[(val) => !!val || 'Выберите критичность']"
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
import { ref, computed, onMounted } from "vue";
import { useDefectStore } from "src/stores/useDefectStore";
import { useEquipmentStore } from "src/stores/useEquipmentStore";
import { useDefectTypeStore } from "src/stores/useDefectTypeStore";

const props = defineProps({
  defect: Object,
});

const emit = defineEmits(["close", "updated"]);
const defectStore = useDefectStore();
const equipmentStore = useEquipmentStore();
const defectTypeStore = useDefectTypeStore();

onMounted(() => {
  if (!equipmentStore.items.length) equipmentStore.fetchEquipment();
  if (!defectTypeStore.defectTypes.length) defectTypeStore.fetchDefectTypes();
});

const equipmentOptions = computed(() =>
  equipmentStore.items.map((eq) => ({
    label: `${eq.serial_number} — ${eq.model}`,
    value: eq.id,
  })),
);

const typeOptions = computed(() =>
  defectTypeStore.defectTypes.map((type) => ({
    label: `${type.description}`,
    value: type.id,
  })),
);

const criticalityOptions = [
  { label: "Высокая", value: 3 },
  { label: "Средняя", value: 2 },
  { label: "Низкая", value: 1 },
];

const statusOptions = [
  { label: "Открыт", value: "open" },
  { label: "В работе", value: "in_progress" },
  { label: "Закрыт", value: "closed" },
];

// копируем данные дефекта в форму, чтобы не мутировать пропс напрямую
const form = ref({
  equipment_id: props.defect?.equipment_id ?? null,
  title: props.defect?.title ?? "",
  description: props.defect?.description ?? "",
  criticality_id: props.defect?.criticality_id ?? null,
  status: props.defect?.status ?? null,
  defect_type_id: props.defect?.defect_type_id ?? null,
});

const onSubmit = async () => {
  await defectStore.updateDefect({...form.value}, props.defect.id);

  alert("Успешно обновлено!");
  emit("updated");
  emit("close");
};
</script>
