import requests
import time
import random

# ─── CONFIGURACIÓN ───────────────────────────────────────────────
API_URL_LOGIN       = "http://localhost:8000/token"
API_URL_ALERTA      = "http://localhost:8000/alertas/"
API_URL_CONDUCTORES = "http://localhost:8000/conductores/"
API_URL_VEHICULOS   = "http://localhost:8000/vehiculos/"

USUARIO    = "admin"
CONTRASENA = "safedriver123"

# IDs de la flota a simular
FLOTA_IDS = [1, 2, 3]

INTERVALO_NORMAL  = 3
INTERVALO_CRITICO = 1

UMBRAL_VELOCIDAD = 90.0

# ─── FUNCIONES DE SIMULACIÓN ─────────────────────────────────────

def obtener_token() -> str:
    print("🔐 Autenticando con el backend SafeDriver...")
    try:
        resp = requests.post(
            API_URL_LOGIN,
            data={"username": USUARIO, "password": CONTRASENA},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        else:
            print(f"❌ Error de login: {resp.status_code}")
            exit(1)
    except Exception as e:
        print(f"[CRÍTICO] Sin conexión: {e}")
        exit(1)

def inicializar_flota(token: str):
    print("⚙️ Verificando e inicializando base de datos para pruebas...")
    headers = {"Authorization": f"Bearer {token}"}
    
    for i in FLOTA_IDS:
        resp = requests.get(f"{API_URL_CONDUCTORES}{i}", headers=headers)
        if resp.status_code == 404:
            print(f"   ➜ Creando Conductor {i} y su Camión...")
            requests.post(API_URL_CONDUCTORES, json={
                "nombre": f"Conductor de Prueba {i}",
                "licencia": f"LIC-000{i}"
            }, headers=headers)
            requests.post(API_URL_VEHICULOS, json={
                "placa": f"TRK-90{i}",
                "modelo": "Volvo FH16 (Simulado)",
                "conductor_id": i
            }, headers=headers)
    print("✅ Base de datos lista.\n")

def leer_sensores_cabina() -> dict:
    # Simulando datos más realistas basados en los nuevos requerimientos biométricos
    estado_aleatorio = random.choice(["NORMAL", "FATIGA_TEMPRANA", "MICROSUEÑO", "ESTRES"])
    
    if estado_aleatorio == "NORMAL":
        frecuencia_parpadeo = round(random.uniform(12.0, 20.0), 1)
        valor_bpm = round(random.uniform(65.0, 85.0), 1)
        velocidad_kmh = round(random.uniform(60.0, 85.0), 1)
    elif estado_aleatorio == "FATIGA_TEMPRANA":
        frecuencia_parpadeo = round(random.uniform(26.0, 35.0), 1) # Parpadeo rápido por cansancio ocular
        valor_bpm = round(random.uniform(55.0, 59.0), 1)
        velocidad_kmh = round(random.uniform(70.0, 95.0), 1)
    elif estado_aleatorio == "MICROSUEÑO":
        frecuencia_parpadeo = round(random.uniform(0.0, 7.0), 1) # Ojos cerrados
        valor_bpm = round(random.uniform(45.0, 54.0), 1) # Relajación extrema
        velocidad_kmh = round(random.uniform(80.0, 100.0), 1)
    else: # ESTRES / PELIGRO
        frecuencia_parpadeo = round(random.uniform(15.0, 25.0), 1)
        valor_bpm = round(random.uniform(111.0, 130.0), 1)
        velocidad_kmh = round(random.uniform(91.0, 110.0), 1)

    return {
        "frecuencia_parpadeo": frecuencia_parpadeo,
        "valor_bpm": valor_bpm,
        "velocidad_kmh": velocidad_kmh,
        "nivel_fatiga": round(max(0.0, (12.0 - frecuencia_parpadeo) / 12.0), 2)
    }

def clasificar_alerta(sensores: dict) -> tuple[str, str]:
    bpm = sensores["valor_bpm"]
    parpadeos = sensores["frecuencia_parpadeo"]
    v = sensores["velocidad_kmh"]
    
    if bpm < 55 or bpm > 110 or parpadeos < 8:
        return "CRITICO", "FATIGA_EXTREMA_O_EMERGENCIA"
    elif bpm < 60 or parpadeos > 25:
        return "ALERTA", "FATIGA_TEMPRANA"
    elif v > UMBRAL_VELOCIDAD:
        return "ALERTA", "EXCESO_VELOCIDAD"
    else:
        return "NORMAL", "MONITOREO"

def enviar_alerta(token: str, sensores: dict, nivel: str, tipo: str, conductor_vehiculo_id: int) -> bool:
    payload = {
        "conductor_id": conductor_vehiculo_id,
        "vehiculo_id":  conductor_vehiculo_id,
        "nivel":        nivel,
        "tipo":         tipo,
        "valor_bpm":    sensores["valor_bpm"],
        "valor_velocidad": sensores["velocidad_kmh"],
        "parpadeos_por_minuto": sensores["frecuencia_parpadeo"]
    }
    try:
        resp = requests.post(API_URL_ALERTA, json=payload, headers={"Authorization": f"Bearer {token}"})
        return resp.status_code in (200, 201)
    except:
        return False

def iniciar_simulacion():
    print("=" * 55)
    print("   🚛 SafeDriver — Simulador IoT Multi-Vehículo 🚛")
    print("=" * 55)

    token = obtener_token()
    inicializar_flota(token)
    ciclo = 0

    while True:
        ciclo += 1
        id_actual = random.choice(FLOTA_IDS) 
        sensores = leer_sensores_cabina()
        nivel, tipo = clasificar_alerta(sensores)

        icono = {"NORMAL": "🟢", "ALERTA": "🟡", "CRITICO": "🔴"}[nivel]
        print(f"[Ciclo {ciclo:04d} | Chofer {id_actual}] {icono} {nivel:7s} | BPM={sensores['valor_bpm']} | Parpadeos={sensores['frecuencia_parpadeo']} | Vel={sensores['velocidad_kmh']:5.1f}")

        if nivel != "NORMAL":
            enviar_alerta(token, sensores, nivel, tipo, id_actual)

        time.sleep(INTERVALO_CRITICO if nivel == "CRITICO" else INTERVALO_NORMAL)

if __name__ == "__main__":
    iniciar_simulacion()