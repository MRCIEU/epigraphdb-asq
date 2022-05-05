FROM node:12.4.0-alpine as build-stage
ARG VUE_APP_WEB_BACKEND_URL
ARG VUE_APP_GTAG_ID
RUN apk add --no-cache git make ncurses gawk
WORKDIR /app
RUN npm install @vue/cli -g
ENV VUE_APP_WEB_BACKEND_URL=${VUE_APP_WEB_BACKEND_URL}
ENV VUE_APP_GTAG_ID=${VUE_APP_GTAG_ID}
# Fix watch file size limit on remote server
ENV CHOKIDAR_USEPOLLING=1
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

FROM nginx:1.16.0-alpine as production-stage
ARG VUE_APP_WEB_BACKEND_URL
ARG VUE_APP_GTAG_ID
ENV VUE_APP_WEB_BACKEND_URL=${VUE_APP_WEB_BACKEND_URL}
ENV VUE_APP_GTAG_ID=${VUE_APP_GTAG_ID}
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
