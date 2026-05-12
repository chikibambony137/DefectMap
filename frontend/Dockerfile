# Этап сборки
FROM node:24 AS build-stage
WORKDIR /app

# Сначала копируем ВСЁ, включая quasar.config.js
COPY . .

# Только потом устанавливаем зависимости
RUN npm install

RUN npx quasar build

# Этап раздачи статики
FROM nginx:stable-alpine AS production-stage
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]