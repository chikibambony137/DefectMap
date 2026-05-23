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

    <q-form ref="formRef" class="q-gutter-xs">
      <div class="row q-gutter-x-lg">
        <div style="min-width: 250px">
          <q-input
            filled
            v-model="currentUser.surname"
            label="Фамилия"
            lazy-rules
            :rules="nameRules"
          />

          <q-input
            filled
            v-model="currentUser.name"
            label="Имя"
            lazy-rules
            :rules="nameRules"
          />

          <q-input
            filled
            v-model="currentUser.middlename"
            label="Отчество"
            lazy-rules
            hint="Необязательно"
            :rules="middlenameRules"
          />
        </div>

        <div style="min-width: 250px">
          <q-input
            filled
            v-model="currentUser.login"
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
          label="Изменить данные"
          color="primary"
          :loading="isLoading"
          @click="confirmChange"
        />
        <q-btn
          label="Выход"
          color="primary"
          flat
          class="q-ml-sm"
          @click="confirmExit"
        />
      </div>
    </q-form>

    <CustomDialog
      @hide="isVisible = false"
      :type="dialogType"
      :visible="isVisible"
      @ok="okFunc"
      @cancel="cancelFunc"
      :title="title"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import avatarImg from 'src/assets/avatar.png';
import { useUserStore } from 'src/stores/useUserStore';
import CustomDialog from 'src/components/CustomDialog.vue';

const router = useRouter();
const userStore = useUserStore();
const $q = useQuasar();

const formRef = ref(null);
const isLoading = ref(false);
const showPassword = ref(false);

const currentUser = ref({
  surname: '',
  name: '',
  middlename: '',
  login: '',
  role_id: null
});

const newPassword = ref('');

onMounted(async() => {
  const user = await userStore.getMyUser();
  if (user) currentUser.value = user;
});

const cyrillicRegex = /^[а-яёА-ЯЁ\s-]+$/;
const loginRegex = /^[a-zA-Z0-9_]{3,20}$/;
const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;

const nameRules = [
  (val) => (val && val.trim().length > 0) || 'Заполните поле',
  (val) => cyrillicRegex.test(val?.trim()) || 'Только кириллические символы',
  (val) => val?.trim().length >= 2 || 'Минимум 2 символа',
  (val) => val?.trim().length <= 50 || 'Максимум 50 символов'
];

const middlenameRules = [
  (val) =>
    !val ||
    val.trim().length === 0 ||
    cyrillicRegex.test(val.trim()) ||
    'Только кириллические символы'
];

const loginRules = [
  (val) => (val && val.trim().length > 0) || 'Заполните поле',
  (val) =>
    loginRegex.test(val?.trim()) || 'Латиница, цифры и _, от 3 до 20 символов'
];

const newPasswordRules = [
  (val) => !val || val.length === 0 || val.length >= 8 || 'Минимум 8 символов',
  (val) =>
    !val ||
    val.length === 0 ||
    passwordRegex.test(val) ||
    'Минимум одна буква и одна цифра'
];

const dialogType = ref('');
const okFunc = ref(null);
const cancelFunc = ref(null);
const title = ref('Dialog');
const isVisible = ref(false);

const confirmChange = async() => {
  const valid = await formRef.value?.validate();
  if (!valid) return;

  dialogType.value = 'confirm';
  okFunc.value = submit;
  cancelFunc.value = () => {
    isVisible.value = false;
  };
  title.value = 'Вы уверены, что хотите изменить текущие данные?';
  isVisible.value = true;
};

const confirmExit = () => {
  dialogType.value = 'confirm';
  okFunc.value = logOut;
  cancelFunc.value = () => {
    isVisible.value = false;
  };
  title.value = 'Вы уверены, что хотите выйти?';
  isVisible.value = true;
};

const submit = async() => {
  isVisible.value = false;
  isLoading.value = true;
  try {
    const updateData = {
      surname: currentUser.value.surname.trim(),
      name: currentUser.value.name.trim(),
      middlename: currentUser.value.middlename?.trim() ?? '',
      login: currentUser.value.login.trim()
    };

    if (newPassword.value) {
      updateData.password = newPassword.value;
    }

    const success = await userStore.updateUser(
      updateData,
      currentUser.value.id
    );
    if (!success) throw new Error('Ошибка при обновлении');

    const updatedUser = await userStore.fetchUserById(currentUser.value.id);
    if (updatedUser) localStorage.setItem('user', JSON.stringify(updatedUser));

    $q.notify({
      type: 'positive',
      message: 'Данные успешно обновлены',
      position: 'top'
    });
  } catch (error) {
    console.error('Ошибка при обновлении профиля:', error);
    $q.notify({
      type: 'negative',
      message: error.message || 'Не удалось обновить данные',
      position: 'top'
    });
  } finally {
    isLoading.value = false;
  }
};

const logOut = () => {
  isVisible.value = false;
  localStorage.clear();
  router.push('/login');
};
</script>
