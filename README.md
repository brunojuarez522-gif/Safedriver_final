# SafeDriver - Ecosistema Digital (2026)

# Sistema Inteligente de Prevención de Fatiga y Seguridad Vial

SafeDriver es un sistema inteligente desarrollado para prevenir accidentes ocasionados por fatiga o microsueños en conductores. El proyecto integra un backend desarrollado con FastAPI, una aplicación móvil en Flutter, un módulo de simulación IoT y una simulación gráfica en Godot 2D que representa el estado de los conductores en tiempo real.

Este proyecto fue desarrollado para el curso de **Desarrollo Basado en Plataformas**.

---

# Integrantes

- Aisha Huamán
- Eduardo Laurente
- Bruno Juárez
- José Manuel Castro

---

# Arquitectura del Proyecto

El ecosistema está dividido en cuatro módulos principales:

## Backend
API REST desarrollada con **Python**, **FastAPI**, **SQLAlchemy** y autenticación mediante **JWT**.

Funciones principales:
- Gestión de conductores.
- Gestión de vehículos.
- Registro de telemetría.
- Detección de alertas de fatiga.
- Documentación mediante Swagger.

## Mobile
Aplicación desarrollada con **Flutter** que permite:

- Iniciar sesión.
- Visualizar conductores.
- Consultar vehículos.
- Supervisar alertas.
- Monitorear información del sistema.

## IoT Industrial
Módulo encargado de simular el envío de información proveniente de sensores como:

- Frecuencia cardíaca.
- Parpadeos.
- Velocidad.
- Estado del conductor.

## Simulación Godot 2D
Simulación desarrollada en **Godot Engine** que representa visualmente el estado de varios conductores.

La simulación muestra:

- Vehículos en movimiento.
- Alertas visuales.
- Alertas sonoras.
- Estados Normal, Advertencia y Crítico.

---

# Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Flutter
- Dart
- Godot 4
- Git
- GitHub

---

# Requisitos

Antes de ejecutar el proyecto es necesario tener instalado:

- Python 3.10 o superior
- Flutter SDK
- Godot Engine 4
- Git

---

# ▶️ Ejecución del Backend

## 1. Ingresar a la carpeta backend

```bash
cd backend
```

## 2. Crear un entorno virtual (solo la primera vez)

### Windows

```bash
python -m venv venv
```

### Linux

```bash
python3 -m venv venv
```

## 3. Activar el entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux

```bash
source venv/bin/activate
```

## 4. Instalar las dependencias

```bash
pip install fastapi uvicorn[standard] sqlalchemy python-multipart "python-jose[cryptography]" "passlib[bcrypt]"
```

## 5. Ejecutar el servidor

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Una vez iniciado correctamente, abrir el navegador en:

```
http://localhost:8000/docs
```

para acceder a la documentación Swagger.

---

# 📱 Ejecución de la aplicación Flutter

Abrir una nueva terminal.

Ingresar a la carpeta:

```bash
cd mobile
```

Descargar dependencias:

```bash
flutter pub get
```

Ejecutar la aplicación:

```bash
flutter run
```

o en Google Chrome:

```bash
flutter run -d chrome
```

---

# 🎮 Ejecución de la simulación en Godot

1. Abrir Godot Engine.
2. Seleccionar **Import**.
3. Buscar el archivo:

```
simulation/project.godot
```

4. Importar el proyecto.
5. Ejecutar la escena principal.

> **Importante:** Antes de iniciar la simulación, el backend debe estar ejecutándose para que las alertas puedan actualizarse correctamente.

---

# 🔐 Credenciales de prueba

Usuario: admin

Contraseña: safedriver123


---

# 🚨 Estados de alerta

La simulación presenta tres estados:

🟢 **Normal**

- El conductor se encuentra en condiciones normales.
- El vehículo mantiene su velocidad.

🟠 **Advertencia**

- Se detectan señales de fatiga.
- Se muestra una alerta visual.
- El vehículo reduce ligeramente su velocidad.

🔴 **Crítico**

- Se detecta un posible microsueño.
- Se activa una alarma sonora.
- El vehículo reduce considerablemente su velocidad.

---

# 📂 Estructura del proyecto

```
backend/
mobile/
iot_industrial/
simulation/
README.md
docker-compose.yml
```

---

# ⚠️ Problemas comunes

### El backend no inicia

Verificar que el entorno virtual esté activado e instalar nuevamente las dependencias.

### Flutter no ejecuta

Ejecutar:

```bash
flutter pub get
```

antes de utilizar:

```bash
flutter run
```

### Godot no muestra información

Verificar que el backend esté ejecutándose correctamente en:

```
http://localhost:8000
```

---

# Observaciones

Para un funcionamiento correcto del sistema se recomienda iniciar los módulos en el siguiente orden:

1. Backend.
2. Aplicación Flutter.
3. Simulación Godot.

De esta manera, la simulación podrá consultar correctamente la información generada por la API y mostrar las alertas en tiempo real.