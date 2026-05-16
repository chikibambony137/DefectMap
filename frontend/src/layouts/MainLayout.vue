<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="bg-primary glossy text-white q-px-xl">
        <q-btn flat round dense icon="menu" class="q-mr-sm">
          <q-menu>
            <q-list style="min-width: 200px">
              <q-item>
                <q-item-section>Главное меню</q-item-section>
              </q-item>
              <q-separator />

              <q-item
                clickable
                v-close-popup
                @click="$router.push('/equipment')"
              >
                <q-item-section>Приборы</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="$router.push('/map')">
                <q-item-section>Карта дефектов</q-item-section>
              </q-item>
              <q-separator />

              <q-item v-if="isUserAdmin" clickable v-close-popup @click="$router.push('/users')">
                <q-item-section>Пользователи</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>

        <q-avatar>
          <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
        </q-avatar>

        <q-toolbar-title>Optimetrik</q-toolbar-title>

        <q-btn flat round dense>
          <q-avatar class="bg-white q-m-md">
            <img :src="avatarImg" />
          </q-avatar>
          <q-menu>
            <div class="row no-wrap q-pa-md">
              <div
                class="row items-start justify-between"
                style="min-width: 220px"
              >
                <q-avatar size="72px">
                  <img :src="avatarImg" />
                </q-avatar>

                <div class="column" style="gap: 10px;">
                  <div class="text-subtitle1">
                    {{ userData.surname }} {{ userData.name[0] }}.
                    {{ userData.middlename[0] }}.
                  </div>

                  <q-btn
                    color="primary"
                    label="Профиль"
                    push
                    size="sm"
                    v-close-popup
                    @click="router.push('/profile')"
                  />

                  <q-btn
                    color="negative"
                    label="Выйти"
                    push
                    size="sm"
                    v-close-popup
                    @click="logOut"
                  />
                </div>
              </div>
            </div>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import avatarImg from 'src/assets/avatar.png'
const userData = JSON.parse(localStorage.getItem("user"));
import { useRouter } from "vue-router";

const router = useRouter();
const logOut = () => {
  localStorage.clear();
  router.push("/login");
};

const isUserAdmin = JSON.parse(localStorage.getItem('user')).role_id === 1;
</script>
