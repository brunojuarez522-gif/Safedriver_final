# SafeDriver - Ecosistema Digital

## Sistema Inteligente de Prevención de Fatiga y Seguridad Vial

SafeDriver es un sistema desarrollado para la prevención de accidentes ocasionados por fatiga o microsueños en conductores. El proyecto integra un backend desarrollado con FastAPI, una aplicación móvil en Flutter, un módulo IoT basado en MQTT y una simulación desarrollada en Godot 2D.

Proyecto desarrollado para el curso de Desarrollo Basado en Plataformas.

---

# Integrantes

- Aisha Huamán
- Eduardo Laurente
- Bruno Juárez
- José Manuel Castro

---

# Arquitectura del proyecto

El ecosistema está compuesto por los siguientes módulos:

## Backend

API REST desarrollada con FastAPI que administra conductores, vehículos, telemetría y alertas mediante autenticación JWT.

## Mobile

Aplicación desarrollada en Flutter para visualizar la información enviada por el backend.

## IoT Industrial

Módulo encargado de simular el envío de datos mediante MQTT.

Los principales archivos son:

- `driver_sim.py`: simula el comportamiento del conductor y genera datos de telemetría.
- `mqtt_sender.py`: publica la información simulada al broker MQTT.
- `mqtt_bridge.py`: recibe los mensajes MQTT y los envía al backend mediante solicitudes HTTP.

## Simulación

Interfaz desarrollada en Godot 2D que representa el estado de los vehículos mediante alertas visuales y sonoras.

---

# Tecnologías utilizadas

- Python
- FastAPI
- Flutter
- Godot 4
- MQTT
- Docker
- SQLite
- SQLAlchemy
- JWT
- Git

---

# Requisitos

Para ejecutar el proyecto es necesario tener instalado:

- Git
- Docker Desktop
- Docker Compose

Si se desea modificar el proyecto también se recomienda instalar Python, Flutter SDK y Godot Engine.

---

# Clonar el repositorio

```bash
git clone https://github.com/brunojuarez522-gif/Safedriver_final.git
```

Ingresar a la carpeta del proyecto:

```bash
cd Safedriver_final
```

---

# Ejecución del proyecto mediante Docker

Desde la carpeta principal ejecutar:

```bash
docker compose up --build
```

Este comando construye e inicia automáticamente los siguientes servicios:

- Backend
- MQTT Bridge
- MQTT Sender

Durante la construcción de los contenedores, Docker instala automáticamente las dependencias definidas en `requirements.txt` del backend y `requisitos.txt` del módulo IoT.

---

# Acceso al Backend

Una vez iniciado Docker, la documentación de la API estará disponible en:

```
http://localhost:8000/docs
```

---

# Aplicación Flutter

Para ejecutar la aplicación:

```bash
cd mobile
flutter pub get
flutter run
```

También puede ejecutarse en Google Chrome:

```bash
flutter run -d chrome
```

---

# Simulación en Godot

# Opción A: Ejecución Rápida con Ejecutable

1. Diríjase a la sección de [Releases de este repositorio](https://github.com/brunojuarez522-gif/Safedriver_final/releases).
2. Descargue el archivo **`SafeDriver_Windows.zip`** de la versión v1.0.
3. Descomprima el contenido
4. Doble clic sobre **`SafeDriver_Sim.exe`**

# Opción B: Ejecución desde el Código Fuente

1. Abrir Godot Engine.
2. Importar el proyecto ubicado en:

```
simulation/project.godot
```
3. Click en Escena/Abrir escena 
4. Seleccionar panel_de_control.tscn
5. Click en "Abrir"
6. Click en "Reproducir proyecto" o presionar F5

Antes de iniciar la simulación, verificar que el backend esté ejecutándose mediante Docker.

---

# Credenciales de prueba

Usuario:

```
admin
```

Contraseña:

```
safedriver123
```

---

# Estructura del proyecto

```
backend/
mobile/
iot_industrial/
simulation/
docker-compose.yml
README.md
```