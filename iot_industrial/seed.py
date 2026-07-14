import requests
import time
import os
import sys

# ─── CONFIGURACIÓN (desde variables de entorno para Docker) ─────
API_URL_LOGIN       = os.getenv("API_URL_LOGIN", "http://backend:8000/token")
API_URL_CONDUCTORES = os.getenv("API_URL_CONDUCTORES", "http://backend:8000/conductores/")
API_URL_VEHICULOS   = os.getenv("API_URL_VEHICULOS", "http://backend:8000/vehiculos/")

USUARIO    = os.getenv("USUARIO", "admin")
CONTRASENA = os.getenv("CONTRASENA", "safedriver123")

# IDs de la flota de prueba a crear si no existen
FLOTA_IDS = [1, 2, 3]


def obtener_token() -> str:
    """Obtiene el JWT del backend, con reintentos (el backend puede tardar en estar listo)."""
    print(f"🔐 Seed solicitando JWT a {API_URL_LOGIN}...")
    intentos = 0
    while intentos < 15:
        try:
            resp = requests.post(
                API_URL_LOGIN,
                data={"username": USUARIO, "password": CONTRASENA},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=5
            )
            if resp.status_code == 200:
                print("✅ Token JWT obtenido exitosamente.\n")
                return resp.json()["access_token"]
            else:
                print(f"❌ Error obteniendo Token: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"⏳ Backend aún no disponible ({e}). Reintentando en 3s...")

        intentos += 1
        time.sleep(3)

    print("[CRÍTICO] No se pudo autenticar tras varios intentos.")
    sys.exit(1)


def inicializar_flota(token: str):
    """Crea conductores y vehículos de prueba si no existen todavía."""
    print("⚙️  Verificando e inicializando base de datos para pruebas...")
    headers = {"Authorization": f"Bearer {token}"}

    for i in FLOTA_IDS:
        resp = requests.get(f"{API_URL_CONDUCTORES}{i}", headers=headers, timeout=5)
        if resp.status_code == 404:
            print(f"   ➜ Creando Conductor {i} y su vehículo...")
            requests.post(API_URL_CONDUCTORES, json={
                "nombre": f"Conductor de Prueba {i}",
                "licencia": f"LIC-000{i}"
            }, headers=headers, timeout=5)
            requests.post(API_URL_VEHICULOS, json={
                "placa": f"TRK-90{i}",
                "modelo": "Volvo FH16 (Simulado)",
                "conductor_id": i
            }, headers=headers, timeout=5)
        else:
            print(f"   ✔ Conductor {i} ya existe, no se crea de nuevo.")

    print("✅ Base de datos lista con datos de prueba.\n")


if __name__ == "__main__":
    print("=" * 55)
    print("   🌱 SafeDriver — Siembra de Datos de Prueba 🌱")
    print("=" * 55)
    jwt = obtener_token()
    inicializar_flota(jwt)
    print("🏁 Siembra completada, este contenedor puede terminar.")
    sys.exit(0)