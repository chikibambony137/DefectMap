<template>
  <div class="row q-pa-xl" style="gap: 20px">
    <div class="column items-center">
      <q-avatar size="72px">
        <img :src="avatarImg" />
      </q-avatar>

      <p>
        {{
          currentUser.role_id === 1
            ? "Администратор"
            : currentUser.role_id === 2
              ? "Инженер"
              : "Наблюдатель"
        }}
      </p>
    </div>

    <q-form @submit="onSubmit" class="q-gutter-xs">
      <div class="row q-gutter-x-lg">
        <div style="min-width: 250px">
          <q-input
            filled
            v-model="currentUser.surname"
            label="Фамилия"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
          />

          <q-input
            filled
            v-model="currentUser.name"
            label="Имя"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
          />

          <q-input
            filled
            v-model="currentUser.middlename"
            label="Отчество"
            lazy-rules
            hint="Необязательно"
          />
        </div>

        <div style="min-width: 250px">
          <q-input
            filled
            v-model="currentUser.login"
            label="Логин"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
          />

          <q-input
            filled
            type="password"
            v-model="newPassword"
            label="Новый пароль"
            lazy-rules
          />
        </div>
      </div>

      <div class="row justify-end q-my-md">
        <q-btn label="Изменить данные" type="submit" color="primary" />
        <q-btn
          label="Выход"
          color="primary"
          flat
          class="q-ml-sm"
          @click="logOut"
        />
      </div>
    </q-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import avatarImg from "src/assets/avatar.png";
import { useUserStore } from "src/stores/useUserStore";

const router = useRouter();
const userStore = useUserStore();

const currentUser = ref({
  surname: "",
  name: "",
  middlename: "",
  login: "",
  role_id: null,
});

const newPassword = ref("");

onMounted(async () => {
  const userData = JSON.parse(localStorage.getItem("user"));
  const userId = userData?.id;
  if (userId) {
    const user = await userStore.fetchUserById(userId);
    if (user) {
      currentUser.value = user;
    }
  }
});

const onSubmit = async () => {
  const updateData = {
    surname: currentUser.value.surname,
    name: currentUser.value.name,
    middlename: currentUser.value.middlename,
    login: currentUser.value.login,
  };

  // Если заполнен новый пароль — добавляем его
  if (newPassword.value) {
    updateData.password = newPassword.value;
  }

  const success = await userStore.updateUser(updateData, currentUser.value.id);
  if (success) {
    alert("Данные обновлены");
    // Обновляем localStorage
    const updatedUser = await userStore.fetchUserById(currentUser.value.id);
    localStorage.setItem("user", JSON.stringify(updatedUser));
  } else {
    alert("Ошибка при обновлении");
  }
};

const logOut = () => {
  localStorage.clear();
  router.push("/login");
};
</script>

<style></style>
