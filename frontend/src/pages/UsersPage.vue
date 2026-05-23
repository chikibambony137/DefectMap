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
              {{ selectedUser.middlename ?? "" }}
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

        <q-form ref="formRef" class="q-gutter-xs q-mt-xl">
          <div class="row q-gutter-x-lg">
            <div style="min-width: 250px">
              <q-input
                filled
                v-model="selectedUser.surname"
                label="Фамилия"
                lazy-rules
                :rules="nameRules"
              />

              <q-input
                filled
                v-model="selectedUser.name"
                label="Имя"
                lazy-rules
                :rules="nameRules"
              />

              <q-input
                filled
                v-model="selectedUser.middlename"
                label="Отчество"
                lazy-rules
                hint="Необязательно"
                :rules="middlenameRules"
              />
            </div>

            <div style="min-width: 250px">
              <q-input
                filled
                v-model="selectedUser.login"
                label="Логин"
                lazy-rules
                :rules="loginRules"
              />

              <q-input
                filled
                :type="showPassword ? 'text' : 'password'"
                v-model="newPassword"
                label="Новый пароль"
                hint="Оставьте пустым, чтобы не менять"
                lazy-rules
                :rules="newPasswordRules"
              >
                <template #append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>
          </div>

          <div class="row justify-end q-my-md">
            <q-btn
              label="Обновить данные"
              color="primary"
              :loading="isLoading"
              @click="confirmChange"
            />
          </div>
        </q-form>
      </div>
    </div>

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
import { useQuasar } from "quasar";
import avatarImg from "src/assets/avatar.png";
import AddUser from "src/components/AddUser.vue";

const $q = useQuasar();
const userStore = useUserStore();
onMounted(() => userStore.fetchUsers());

const formRef = ref(null);
const isLoading = ref(false);
const showPassword = ref(false);
const selectedRows = ref([]);
const selectedUser = ref(null);
const newPassword = ref("");

const onRowClick = (event, row) => {
  selectedRows.value = [row];
  selectedUser.value = { ...row }; // копия, чтобы не мутировать стор напрямую
  newPassword.value = "";
};

const cyrillicRegex = /^[а-яёА-ЯЁ\s-]+$/;
const loginRegex = /^[a-zA-Z0-9_]{3,20}$/;
const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;

const nameRules = [
  (val) => (val && val.trim().length > 0) || "Заполните поле",
  (val) => cyrillicRegex.test(val?.trim()) || "Только кириллические символы",
  (val) => val?.trim().length >= 2 || "Минимум 2 символа",
  (val) => val?.trim().length <= 50 || "Максимум 50 символов",
];

const middlenameRules = [
  (val) =>
    !val ||
    val.trim().length === 0 ||
    cyrillicRegex.test(val.trim()) ||
    "Только кириллические символы",
];

const loginRules = [
  (val) => (val && val.trim().length > 0) || "Заполните поле",
  (val) =>
    loginRegex.test(val?.trim()) || "Латиница, цифры и _, от 3 до 20 символов",
];

const newPasswordRules = [
  (val) => !val || val.length === 0 || val.length >= 8 || "Минимум 8 символов",
  (val) =>
    !val ||
    val.length === 0 ||
    passwordRegex.test(val) ||
    "Минимум одна буква и одна цифра",
];

const confirmChange = async () => {
  const valid = await formRef.value?.validate();
  if (!valid) return;

  $q.dialog({
    title: "Подтверждение",
    message: "Вы уверены, что хотите изменить данные пользователя?",
    cancel: true,
    persistent: true,
  }).onOk(submit);
};

const submit = async () => {
  isLoading.value = true;
  try {
    const updateData = {
      surname: selectedUser.value.surname.trim(),
      name: selectedUser.value.name.trim(),
      middlename: selectedUser.value.middlename?.trim() ?? "",
      login: selectedUser.value.login.trim(),
    };

    if (newPassword.value) {
      updateData.password = newPassword.value;
    }

    await userStore.updateUser(
      updateData,
      selectedUser.value.id,
    );

    await userStore.fetchUsers();
    newPassword.value = "";

    $q.notify({
      type: "positive",
      message: "Данные пользователя обновлены",
      position: "top",
    });
  } catch (error) {
    console.error("Ошибка при обновлении пользователя:", error);
    $q.notify({
      type: "negative",
      message: error.message || "Не удалось обновить данные",
      position: "top",
    });
  } finally {
    isLoading.value = false;
  }
};

const deleteUser = () => {
  if (!selectedUser.value) {
    $q.notify({
      type: "warning",
      message: "Выберите пользователя",
      position: "top",
    });
    return;
  }

  const { surname, name, middlename } = selectedUser.value;
  $q.dialog({
    title: "Подтверждение",
    message: `Вы уверены, что хотите удалить пользователя ${surname} ${name} ${middlename ?? ""}?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    try {
      await userStore.deleteUser(selectedUser.value.id);
      selectedUser.value = null;
      selectedRows.value = [];
      $q.notify({
        type: "positive",
        message: "Пользователь удалён",
        position: "top",
      });
    } catch (error) {
      $q.notify({
        type: "negative",
        message: error.message || "Не удалось удалить пользователя",
        position: "top",
      });
    }
  });
};

const isAddUserVisible = ref(false);

// prettier-ignore
const columns = [
  { name: "surname",    align: "center", label: "Фамилия", field: "surname",    sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "name",       align: "center", label: "Имя",     field: "name",       sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "middlename", align: "center", label: "Отчество", field: "middlename", sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "login",      align: "center", label: "Логин",   field: "login",      sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
  { name: "role_id",    align: "center", label: "Роль",    field: "role_id",    sortable: true, style: "min-width: 100px; max-width: 100px; word-break: break-word; white-space: normal;" },
];
</script>
