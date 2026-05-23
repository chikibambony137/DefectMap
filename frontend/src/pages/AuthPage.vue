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
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          label="Пароль"
          lazy-rules
          :rules="[(val) => (val !== null && val !== '') || 'Заполните поле']"
        >
          <template #append>
            <q-icon
              :name="showPassword ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="showPassword = !showPassword"
            />
          </template>
        </q-input>

        <div class="row justify-end q-mt-xl">
          <q-btn
            label="Войти"
            type="submit"
            color="primary"
            :loading="isLoading"
          />
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';

const router = useRouter();
const $q = useQuasar();

const login = ref('');
const password = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const onSubmit = async() => {
  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: login.value,
        password: password.value
      })
    });

    const data = await response.json();

    if (response.status === 401) {
      $q.notify({
        type: 'negative',
        message: 'Неверный логин или пароль',
        position: 'top'
      });
      return;
    }

    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка авторизации');
    }

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('token_type', data.token_type);

    await fetchUserData();

    router.push('/equipment');
  } catch (error) {
    console.error('Login error:', error);
    $q.notify({
      type: 'negative',
      message: error.message || 'Не удалось выполнить вход',
      position: 'top'
    });
  } finally {
    isLoading.value = false;
  }
};

const fetchUserData = async() => {
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch('http://localhost:8000/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.ok) {
      const userData = await response.json();
      localStorage.setItem('user', JSON.stringify(userData));
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
};
</script>
