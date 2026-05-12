<template>
  <q-page class="flex flex-center bg-red">
    <q-splitter
      v-model="splitterModel"
      :limits="[10, 50]"
      class="fit"
      @update:model-value="onSplitterResize"
    >
      <template v-slot:before>
        <div class="q-pa-md bg-green" style="min-height: 92dvh;">

        </div>
      </template>

      <template v-slot:after>

          <div class="map-wrapper">
            <YandexMap ref="mapRef"></YandexMap>
          </div>

      </template>
    </q-splitter>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import YandexMap from "src/components/YandexMap.vue";

const mapRef = ref(null)
const splitterModel = ref(25)

const onSplitterResize = () => {
  // Сообщаем карте, что размер изменился
  mapRef.value?.invalidateSize()
}
</script>

<style scoped>
.map-wrapper {
  height: 92dvh;
  width: 100%;
  overflow: hidden;
}
</style>
