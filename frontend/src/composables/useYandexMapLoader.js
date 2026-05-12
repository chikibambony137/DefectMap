// Флаг, чтобы отследить, началась ли уже загрузка API
let scriptLoadingInProgress = false;
// Promise, который будет ждать загрузки API
let loadScriptPromise = null;

export function useYandexMapLoader() {
  /**
   * Основная функция: загружает API Яндекс.Карт и возвращает Promise,
   * который разрешится, когда API станет доступен глобально (ymaps)
   * @param {string} apiKey - Ваш API-ключ для Яндекс.Карт
   * @returns {Promise}
   */
  const loadMapApi = (apiKey) => {
    // Если API уже загружен (объект ymaps существует), сразу возвращаем успешный Promise
    if (window.ymaps) {
      return Promise.resolve();
    }

    // Если загрузка уже идёт, возвращаем существующий Promise, чтобы не создавать новый скрипт
    if (scriptLoadingInProgress) {
      return loadScriptPromise;
    }

    // Отмечаем, что начинаем загрузку
    scriptLoadingInProgress = true;

    // Создаём новый Promise, который разрешится, когда скрипт загрузится и инициализируется
    loadScriptPromise = new Promise((resolve, reject) => {
      // Создаём тег <script>
      const script = document.createElement('script');
      // Формируем URL для загрузки API с переданным ключом
      script.src = `https://api-maps.yandex.ru/2.1/?apikey=${apiKey}&lang=ru_RU`;
      // Асинхронный скрипт, чтобы не блокировать загрузку страницы
      script.async = true;

      // Обработчик успешной загрузки скрипта
      script.onload = () => {
        // API Яндекс.Карт загружается асинхронно, и после загрузки скрипта нужно дождаться готовности ymaps
        if (window.ymaps) {
          // Функция ymaps.ready выполнит переданный колбэк, когда API будет готов к работе
          window.ymaps.ready(() => {
            console.log('Yandex Maps API is ready');
            resolve();
          });
        } else {
          // Если по какой-то причине ymaps не появился — ошибка
          reject(new Error('Yandex Maps API failed to initialize'));
        }
      };

      // Обработчик ошибки загрузки скрипта
      script.onerror = () => {
        console.error('Failed to load Yandex Maps API script');
        scriptLoadingInProgress = false;
        reject(new Error('Failed to load Yandex Maps API script'));
      };

      // Добавляем скрипт в <head> страницы, тем самым запуская его загрузку
      document.head.appendChild(script);
    });

    return loadScriptPromise;
  };

  // Возвращаем функцию, чтобы использовать её в компоненте
  return { loadMapApi };
}