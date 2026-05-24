<template>
  <div class="bg-dark row justify-center items-center" style="height: 100dvh">
    <div
      class="q-pa-md bg-white rounded-borders"
      style="max-width: 600px; min-height: 400px"
    >
      <div class="text-h4 text-grey-10 row justify-center q-mt-lg">
        Регистрация
      </div>
      <q-form @submit="onSubmit" class="q-gutter-xs q-mt-xl">
        <div class="row q-gutter-x-lg">
          <div style="min-width: 250px">
            <q-input
              filled
              v-model="surname"
              label="Фамилия"
              lazy-rules
              :rules="nameRules"
            />

            <q-input
              filled
              v-model="name"
              label="Имя"
              lazy-rules
              :rules="nameRules"
            />

            <q-input
              filled
              v-model="middlename"
              label="Отчество"
              lazy-rules
              hint="Необязательно"
              :rules="middlenameRules"
            />
          </div>

          <div style="min-width: 250px">
            <q-input
              filled
              v-model="login"
              label="Логин"
              lazy-rules
              :rules="loginRules"
            />

            <q-input
              filled
              :type="showPassword1 ? 'text' : 'password'"
              v-model="password1"
              label="Пароль"
              lazy-rules
              :rules="passwordRules"
            >
              <template #append>
                <q-icon
                  :name="showPassword1 ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="showPassword1 = !showPassword1"
                />
              </template>
            </q-input>

            <q-input
              filled
              :type="showPassword2 ? 'text' : 'password'"
              v-model="password2"
              label="Повторите пароль"
              lazy-rules
              :rules="password2Rules"
            >
              <template #append>
                <q-icon
                  :name="showPassword2 ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="showPassword2 = !showPassword2"
                />
              </template>
            </q-input>
          </div>
        </div>

        <div class="row justify-end q-my-md">
          <q-btn
            label="Зарегистрироваться"
            type="submit"
            color="primary"
            :loading="isLoading"
          />
          <q-btn
            label="Авторизация"
            color="primary"
            flat
            class="q-ml-sm"
            @click="$router.push('/login')"
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

const surname = ref('');
const name = ref('');
const middlename = ref('');
const login = ref('');
const password1 = ref('');
const password2 = ref('');
const showPassword1 = ref(false);
const showPassword2 = ref(false);
const isLoading = ref(false);

// Только кириллица, дефис и пробел
const cyrillicRegex = /^[а-яёА-ЯЁ\s-]+$/;
// Логин: латиница, цифры, _, от 3 до 20 символов
const loginRegex = /^[a-zA-Z0-9_]{3,20}$/;
// Пароль: минимум 8 символов, хотя бы одна буква и одна цифра
const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;

const nameRules = [
  (val) => (val && val.trim().length > 0) || 'Заполните поле',
  (val) => cyrillicRegex.test(val?.trim()) || 'Только кириллица',
  (val) => val?.trim().length >= 2 || 'Минимум 2 символа',
  (val) => val?.trim().length <= 50 || 'Максимум 50 символов'
];

const middlenameRules = [
  (val) =>
    !val ||
    val.trim().length === 0 ||
    cyrillicRegex.test(val.trim()) ||
    'Только кириллица'
];

const loginRules = [
  (val) => (val && val.trim().length > 0) || 'Заполните поле',
  (val) =>
    loginRegex.test(val?.trim()) || 'Латиница, цифры и _, от 3 до 20 символов'
];

const passwordRules = [
  (val) => (val !== null && val !== '') || 'Заполните поле',
  (val) => val?.length >= 8 || 'Минимум 8 символов',
  (val) => passwordRegex.test(val) || 'Минимум одна буква и одна цифра'
];

const password2Rules = [
  (val) => (val !== null && val !== '') || 'Повторите пароль',
  (val) => val === password1.value || 'Пароли не совпадают'
];

const onSubmit = async() => {
  isLoading.value = true;
  try {
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        surname: surname.value.trim(),
        name: name.value.trim(),
        middlename: middlename.value.trim(),
        login: login.value.trim(),
        password: password1.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка регистрации');
    }

    $q.notify({
      type: 'positive',
      message: 'Регистрация прошла успешно!',
      position: 'top'
    });
    router.push('/login');
  } catch (error) {
    // eslint-disable-next-line
    console.error('Register error:', error);
    $q.notify({
      type: 'negative',
      message: error.message || 'Ошибка при регистрации',
      position: 'top'
    });
  } finally {
    isLoading.value = false;
  }
};
</script>
