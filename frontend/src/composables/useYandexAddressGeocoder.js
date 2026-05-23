export function useYandexAddressGeocoder() {
  const getCoordsByAddress = async(address) => {
    const apiKey = process.env.VITE_YANDEX_API_KEY;
    const url = `https://geocode-maps.yandex.ru/1.x/?apikey=${apiKey}&geocode=${encodeURIComponent(address)}&format=json`;

    const res = await fetch(url);
    const data = await res.json();

    const point =
      data.response.GeoObjectCollection.featureMember[0]?.GeoObject.Point.pos;
    if (!point) return null;

    const [longitude, latitude] = point.split(' ').map(Number);
    return { latitude, longitude };
  };

  return { getCoordsByAddress };
}
