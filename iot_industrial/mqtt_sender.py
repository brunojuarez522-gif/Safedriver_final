import paho.mqtt.client as mqtt
import json
import time
import random
import requests

# ─── CONFIGURACIÓN MQTT Y API ────────────────────────────────────
BROKER = "broker.hivemq.com"
PORT = 1883

API_URL_LOGIN       = "http://localhost:8000/token"
API_URL_CONDUCTORES = "http://localhost:8000/conductores/"

USUARIO    = "admin"
CONTRASENA = "safedriver123"

# ─── FUNCIONES PARA OBTENER CONDUCTORES DINÁMICOS ────────────────

def obtener_token() -> str:
    """Hace login en el backend para poder consultar los conductores."""
    try:
        resp = requests.post(
            API_URL_LOGIN,
            data={"username": USUARIO, "password": CONTRASENA},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        else:
            print(f"❌ Error de autenticación en el transmisor: {resp.text}")
            exit(1)
    except Exception as e:
        print(f"[CRÍTICO] El transmisor no pudo conectar al backend: {e}")
        exit(1)

def obtener_ids_disponibles() -> list:
    """Trae la lista de IDs de conductores reales desde la base de datos."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(API_URL_CONDUCTORES, headers=headers)
        if resp.status_code == 200:
            conductores = resp.json()
            ids = [c["id"] for c in conductores]
            return ids
        else:
            print(f"⚠️ Error al obtener conductores. Usando ID 1 por defecto.")
            return [1]
    except Exception as e:
        print(f"⚠️ Falló conexión: {e}. Usando ID 1 por defecto.")
        return [1]


# ─── LEER SENSORES DE CABINA SIMULADOS ───────────────────────────

def leer_sensores_cabina(conductor_id: int) -> dict:
    frecuencia_parpadeo = round(random.uniform(3.0, 22.0), 1)
    base_fatiga = max(0.0, (12.0 - frequency_parpadeo) / 12.0) if 'frequency_parpadeo' in locals() else max(0.0, (12.0 - frecuencia_parpadeo) / 12.0)
    nivel_fatiga = round(min(1.0, base_fatiga + random.uniform(-0.05, 0.1)), 2)
    velocidad_kmh = round(random.uniform(40.0, 110.0), 1)

    return {
        "conductor_id": conductor_id,
        "frecuencia_parpadeo": frecuencia_parpadeo,
        "nivel_fatiga": nivel_fatiga,
        "velocidad_kmh": velocidad_kmh,
        "timestamp": time.time()
    }


# ─── INICIAR PROCESO DE SENSORIZACIÓN ────────────────────────────

def iniciar_sensor():
    client = mqtt.Client()
    print("🔌 Conectando al Broker MQTT (HiveMQ)...")
    client.connect(BROKER, PORT)
    
    # Mapeamos los conductores que creaste en la app o en la DB
    ids_conductores = obtener_ids_disponibles()
    print(f"📊 Conductores detectados para simular: {ids_conductores}")
    print("-" * 55)
    
    ciclo = 0
    while True:
        ciclo += 1
        
        # 🎲 Selecciona un conductor aleatorio de la lista real
        conductor_actual = random.choice(ids_conductores)
        
        # Simulamos que el ID del vehículo coincide con el ID del conductor
        vehiculo_actual = conductor_actual 
        
        # El tópico ahora cambia dinámicamente según el vehículo elegido al azar
        topic_dinamico = f"safedriver/telemetria/vehiculos/{vehiculo_actual}"
        
        # Genera los datos simulados
        payload = leer_sensores_cabina(conductor_actual)
        
        # Publica el mensaje en el Broker
        client.publish(topic_dinamico, json.dumps(payload))
        
        print(f"[TX {ciclo:04d}] Envió -> Vehículo/Cond: {vehiculo_actual} | "
              f"Fatiga: {payload['nivel_fatiga']} | Vel: {payload['velocidad_kmh']} km/h")
        
        # Espera 3 segundos antes del siguiente envío
        time.sleep(3)

if __name__ == "__main__":
    iniciar_sensor()