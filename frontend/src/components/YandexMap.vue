<template>
  <div class="fit">
    <q-circular-progress
      v-if="loading"
      indeterminate
      rounded
      size="50px"
      color="red"
      class="absolute-center"
    />
    <div id="map" class="fit"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { useYandexMapLoader } from 'src/composables/useYandexMapLoader';

const props = defineProps({
  center: {
    type: Array,
    default: () => [55.751574, 37.573856]
  },
  points: {
    type: Array,
    default: () => []
  }
});

const { loadMapApi } = useYandexMapLoader();
const loading = ref(true);
let map = null;
let clusterer = null;

const initMap = () => {
  const container = document.getElementById('map');
  if (
    !container ||
    container.clientWidth === 0 ||
    container.clientHeight === 0
  ) {
    setTimeout(initMap, 50);
    return;
  }

  map = new window.ymaps.Map('map', {
    center: props.center,
    zoom: 10,
    controls: ['zoomControl', 'fullscreenControl']
  });

  clusterer = new window.ymaps.Clusterer({
    preset: 'islands#invertedVioletClusterIcons',
    groupByCoordinates: false,
    zoomMargin: 20,
    minClusterSize: 2,
    clusterDisableClickZoom: false,
    clusterOpenBalloonOnClick: true,
    clusterIconColor: 'black',
    clusterNumbers: ['#FFFFFF']
  });

  addPointsToMap();
};

onMounted(async() => {
  try {
    await loadMapApi(process.env.VITE_YANDEX_API_KEY);
    loading.value = false;
    initMap();
  } catch (error) {
    console.error('Ошибка загрузки карты:', error);
  }
});

const addPointsToMap = () => {
  if (!map || !clusterer) return;
  if (props.points && props.points.length) {
    const placemarks = props.points.map(
      (point) =>
        new window.ymaps.Placemark(
          point.coords,
          { hintContent: point.name, balloonContent: `${point.name}` },
          { preset: getPlacemarkColor(point.color) }
        )
    );
    clusterer.add(placemarks);
    map.geoObjects.add(clusterer);
  }
};

const getPlacemarkColor = (color) => {
  if (color === 'red') return 'islands#redIcon';
  if (color === 'orange') return 'islands#orangeIcon';
  if (color === 'yellow') return 'islands#yellowIcon';
  if (color === 'green') return 'islands#greenIcon';
  
  return 'islands#grayIcon';
};

// Следим за изменением центра карты и перемещаем карту
watch(
  () => props.center,
  (newCenter) => {
    if (map && newCenter && newCenter.length === 2) {
      map.setCenter(newCenter, 12); // зум 12, можно настроить
    }
  },
  { deep: true, immediate: false } // immediate = false, чтобы не вызывать при старте, иначе map ещё не создан
);

// Если массив points изменится – обновляем метки (очищаем и добавляем заново)
watch(
  () => props.points,
  (newPoints) => {
    if (map && clusterer) {
      clusterer.removeAll(); // удалить старые метки
      if (newPoints && newPoints.length) {
        const placemarks = newPoints.map(
          (point) =>
            new window.ymaps.Placemark(
              point.coords,
              {
                hintContent: point.name,
                balloonContent: `${point.name}`
              },
              { preset: getPlacemarkColor(point.color) }
            )
        );
        clusterer.add(placemarks);
      }
    }
  },
  { deep: true }
);

const invalidateSize = () => {
  if (map) {
    map.container.fitToViewport();
  }
};

defineExpose({ invalidateSize });
</script>
