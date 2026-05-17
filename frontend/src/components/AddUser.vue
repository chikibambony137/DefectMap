<template>
  <q-card
    class="q-pa-md bg-white rounded-borders"
    style="max-width: 600px; min-height: 400px"
  >
    <q-card-section class="text-h4 text-grey-10 row justify-center">
      Регистрация пользователя
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" class="q-gutter-xs">
        <div class="row q-gutter-x-lg">
          <div style="min-width: 250px">
            <q-input
              filled
              v-model="surname"
              label="Фамилия"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
            />

            <q-input
              filled
              v-model="name"
              label="Имя"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
            />

            <q-input
              filled
              v-model="middlename"
              label="Отчество"
              lazy-rules
              hint="Необязательно"
            />
          </div>

          <div style="min-width: 250px">
            <q-input
              filled
              v-model="login"
              label="Логин"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Заполните поле']"
            />

            <q-input
              filled
              type="password"
              v-model="password1"
              label="Пароль"
              lazy-rules
              :rules="[
                (val) => (val !== null && val !== '') || 'Заполните поле',
              ]"
            />

            <q-input
              filled
              type="password"
              v-model="password2"
              label="Пароль"
              lazy-rules
              :rules="[
                (val) => (val !== null && val !== '') || 'Повторите пароль',
              ]"
            />
          </div>
        </div>

        <div class="row justify-end q-my-md">
          <q-btn label="Зарегистрировать пользователя" type="submit" color="primary" />
          <q-btn label="Отмена" flat @click="emit('cancel')" color="primary" />
        </div>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(['registerSuccess', 'cancel'])

const surname = ref("");
const name = ref("");
const middlename = ref("");
const login = ref("");
const password1 = ref("");
const password2 = ref("");

const onSubmit = async () => {
  try {
    if (password1.value !== password2.value) {
      alert("Ошибка! Пароли не совпадают");
      return;
    }

    // Отправка запроса на бэкенд
    const response = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        surname: surname.value,
        name: name.value,
        middlename: middlename.value,
        login: login.value,
        password: password1.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка регистрации");
    }

    handleSuccessConfirm();
  } catch (error) {
    console.error("Register error:", error);
  }
};

const handleSuccessConfirm = () => {
  window.confirm("Успешная регистрация!");
  emit('registerSuccess');
};
</script>

<style></style>
