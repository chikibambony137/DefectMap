<template>
  <div class="column q-px-xl">
    <div class="q-pa-md q-mx-xl" style="max-width: 700px;">
      <q-table
        flat
        bordered
        title="Пользователи"
        dense
        :rows="store.users"
        :columns="columns"
        :loading="store.loading"
        row-key="id"
        @row-click="onRowClick"
      />
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from "src/stores/useUserStore";
import { onMounted, ref } from "vue";

const store = useUserStore();
onMounted(() => store.fetchUsers());

const selectedUser = ref(null);
const onRowClick = (event, row, index) => {
  selectedUser.value = row;
};


const columns = [
  {
    name: "surname",
    align: "center",
    label: "Фамилия",
    field: "surname",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "name",
    align: "center",
    label: "Имя",
    field: "name",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "middlename",
    align: "center",
    label: "Отчество",
    field: "middlename",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "login",
    align: "center",
    label: "Логин",
    field: "login",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  },
  {
    name: "role_id",
    align: "center",
    label: "Роль",
    field: "role_id",
    sortable: true,
    style:
      "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;",
  }
];
</script>

<style>

</style>