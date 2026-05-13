<template>
  <div class="bg-dark row justify-center items-center" style="height: 100dvh">
    <div
      class="q-pa-md bg-white rounded-borders"
      style="max-width: 400px; min-width: 400px; min-height: 400px"
    >
      <div class="text-h4 text-grey-10 row justify-center q-mt-lg">
        Авторизация
      </div>
      <q-form @submit="onSubmit" class="q-gutter-md q-mt-lg">
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
          v-model="password"
          label="Пароль"
          lazy-rules
          :rules="[(val) => (val !== null && val !== '') || 'Заполните поле']"
        />

        <div class="row justify-end q-mt-xl">
          <q-btn label="Войти" type="submit" color="primary" />
          <q-btn
            label="Регистрация"
            color="primary"
            flat
            class="q-ml-sm"
            @click="$router.push('/registration')"
          />
        </div>
      </q-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const login = ref("");
const password = ref("");

const onSubmit = async () => {
  try {
    // Отправка запроса на бэкенд
    const response = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        username: login.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (response.status === 401) {
      alert('Неверный логин или пароль!')
      return;
    }

    if (!response.ok) {
      throw new Error(data.detail || "Ошибка авторизации");
    }

    // Сохраняем токен
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("token_type", data.token_type);

    // Получаем данные пользователя
    await fetchUserData();

    handleSuccessConfirm();
  } catch (error) {
    console.error("Login error:", error);
  }
};

const fetchUserData = async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch("http://localhost:8000/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const userData = await response.json();
      // Сохраняем данные пользователя
      localStorage.setItem("user", JSON.stringify(userData));
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};

const handleSuccessConfirm = () => {
  router.push("/equipment");
};
</script>

<style scoped></style>
