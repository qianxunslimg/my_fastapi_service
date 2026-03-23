FROM node:20-alpine AS deps

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS build

COPY . .
RUN npm run build

FROM deps AS dev

WORKDIR /app/frontend
RUN mkdir -p /app/frontend
EXPOSE 80

FROM nginx:1.27-alpine AS prod
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
COPY run.sh /run.sh
RUN chmod +x /run.sh
EXPOSE 80
CMD ["/run.sh"]
