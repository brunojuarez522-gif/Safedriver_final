# ── Etapa 1: Construir la app Flutter para web ────────────────────
FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app
COPY . .

RUN flutter pub get
RUN flutter build web --release

# ── Etapa 2: Servir los archivos estáticos con Nginx ──────────────
FROM nginx:alpine

COPY --from=build /app/build/web /usr/share/nginx/html

EXPOSE 80