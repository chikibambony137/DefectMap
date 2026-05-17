<template>
  <div class="column">
    <div class="row q-pa-md q-mx-xl" style="gap: 40px">
      <div class="column" style="gap: 10px; width: 800px">
        <div class="row justify-end" style="gap: 20px">
          <q-btn
            size="sm"
            icon="add"
            color="positive"
            @click="isAddUserVisible = !isAddUserVisible"
          />
          <q-btn size="sm" icon="delete" color="negative" @click="deleteUser" />
        </div>

        <q-table
          flat
          bordered
          title="Пользователи"
          dense
          :rows="userStore.users"
          :columns="columns"
          :loading="userStore.loading"
          row-key="id"
          v-model:selected="selectedRows"
          @row-click="onRowClick"
        />
      </div>

      <div v-if="selectedUser">
        <div class="row">
          <q-avatar size="72px">
            <img :src="avatarImg" />
          </q-avatar>

          <div class="q-mt-md text-primary">
            <b style="font-size: 16px">
              {{ selectedUser.surname }} {{ selectedUser.name }}
              {{ selectedUser.middlename ? selectedUser.middlename : "" }}
            </b>
            <p class="text-grey-7">
              {{
                selectedUser.role_id === 1
                  ? "Администратор"
                  : selectedUser.role_id === 2
                    ? "Инженер"
                    : "Наблюдатель"
              }}
            </p>
          </div>
        </div>

        <q-form class="q-gutter-xs q-mt-xl">
          <div class="row q-gutter-x-lg">
            <div style="min-width: 250px">
              <q-input
                filled
                v-model="selectedUser.surname"
                label="Фамилия"
                lazy-rules
                :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
              />

              <q-input
                filled
                v-model="selectedUser.name"
                label="Имя"
                lazy-rules
                :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
              />

              <q-input
                filled
                v-model="selectedUser.middlename"
                label="Отчество"
                lazy-rules
                hint="Необязательно"
              />
            </div>

            <div style="min-width: 250px">
              <q-input
                filled
                v-model="selectedUser.login"
                label="Логин"
                lazy-rules
                :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
              />

              <q-input
                filled
                type="password"
                v-model="newPassword"
                label="Пароль"
                lazy-rules
                :rules="[
                  (val) => (val !== null && val !== '') || 'Заполните поле',
                ]"
              />
            </div>
          </div>

          <div class="row justify-end q-my-md">
            <q-btn
              label="Обновить данные"
              @click="confirmChange"
              color="primary"
            />
          </div>
        </q-form>
      </div>
    </div>

    <Dialog
      @hide="isVisible = false"
      :type="dialogType"
      :visible="isVisible"
      @ok="okFunc"
      @cancel="cancelFunc"
      :title="title"
    ></Dialog>

    <q-dialog v-model="isAddUserVisible">
      <AddUser
        @close="isAddUserVisible = false"
        @cancel="isAddUserVisible = false"
        @registerSuccess="
          isAddUserVisible = false;
          userStore.fetchUsers();
        "
      />
    </q-dialog>
  </div>
</template>

<script setup>
import { useUserStore } from "src/stores/useUserStore";
import { onMounted, ref } from "vue";
import avatarImg from "src/assets/avatar.png";
import Dialog from "src/components/Dialog.vue";
import AddUser from "src/components/AddUser.vue";

const userStore = useUserStore();
onMounted(() => userStore.fetchUsers());

const selectedRows = ref([]);
const selectedUser = ref(null);
const onRowClick = (event, row, index) => {
  selectedRows.value = [row];
  selectedUser.value = row;
};

const newPassword = ref("");

const dialogType = ref("");
const okFunc = ref(null);
const cancelFunc = ref(null);
const title = ref("Dialog");
const isVisible = ref(false);

const confirmChange = () => {
  dialogType.value = "confirm";
  okFunc.value = submit;
  cancelFunc.value = () => {
    isVisible.value = false;
  };
  title.value = "Вы уверены, что хотите изменить текущие данные?";
  isVisible.value = true;
};

const successChange = () => {
  dialogType.value = "alert";
  okFunc.value = () => {
    isVisible.value = false;
  };
  title.value = "Данные успешно обновлены!";
  isVisible.value = true;
};

const submit = async () => {
  isVisible.value = false;

  const updateData = {
    surname: selectedUser.value.surname,
    name: selectedUser.value.name,
    middlename: selectedUser.value.middlename,
    login: selectedUser.value.login,
  };

  // Если заполнен новый пароль — добавляем его
  if (newPassword.value) {
    updateData.password = newPassword.value;
  }

  const success = await userStore.updateUser(updateData, selectedUser.value.id);
  if (success) {
    // Обновляем localStorage
    const updatedUser = await userStore.fetchUserById(selectedUser.value.id);
    if (updatedUser !== undefined || updatedUser !== null)
      localStorage.setItem("user", JSON.stringify(updatedUser));
    successChange();
  } else {
    alert("Ошибка при обновлении");
  }
};

const confirmDelete = () => {
  dialogType.value = "confirm";
  okFunc.value = () => {
    userStore.deleteUser(selectedUser.value.id);
    selectedUser.value = null;
  };
  cancelFunc.value = () => {
    isVisible.value = false;
  };
  title.value = `Вы уверены, что хотите удалить пользователя ${selectedUser.value.surname}
       ${selectedUser.value.name} ${selectedUser.value.middlename}?`;
  isVisible.value = true;
};

const deleteUser = () => {
  if (!selectedUser.value) {
    alert("Выберите пользователя!");
    return;
  }
  confirmDelete();
};

const isAddUserVisible = ref(false);

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
  },
];
</script>

<style></style>
