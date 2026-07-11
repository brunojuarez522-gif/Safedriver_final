extends Node2D

# --- RUTAS DE TU BACKEND ---
var url_login: String = "http://127.0.0.1:8000/token"
var url_alertas: String = "http://127.0.0.1:8000/alertas/"

# --- NODOS BASE ---
@onready var http_cliente = $ClienteHTTP
@onready var http_alertas = $HTTPAlertas
@onready var timer_alertas = $TimerAlertas
@onready var alarma_sonora = $AudioAlarma

var token_jwt: String = ""
var flota = {} # Diccionario para controlar los 3 camiones

func _ready() -> void:
	http_cliente.request_completed.connect(_al_recibir_login)
	http_alertas.request_completed.connect(_al_recibir_alertas)
	timer_alertas.timeout.connect(_consultar_alertas)

	construir_panel_flota()
	autenticar_backend()

# --- CONSTRUCTOR AUTOMÁTICO ---
func construir_panel_flota() -> void:
	# 1. Dibujar el Asfalto
	var fondo_asfalto = ColorRect.new()
	fondo_asfalto.color = Color(0.12, 0.12, 0.12)
	fondo_asfalto.size = Vector2(3000, 2000)
	add_child(fondo_asfalto)

	# 2. Panel superior de textos
	var canvas = CanvasLayer.new()
	add_child(canvas)

	var fondo_panel = ColorRect.new()
	fondo_panel.color = Color(0, 0, 0, 0.9)
	fondo_panel.set_anchors_preset(Control.PRESET_TOP_WIDE)
	fondo_panel.custom_minimum_size = Vector2(0, 140)
	canvas.add_child(fondo_panel)

	var hbox = HBoxContainer.new()
	hbox.set_anchors_preset(Control.PRESET_TOP_WIDE)
	hbox.custom_minimum_size = Vector2(0, 140)
	hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	hbox.add_theme_constant_override("separation", 100)
	fondo_panel.add_child(hbox)

	# 3. Cargar el icono por defecto de Godot
	var textura_por_defecto = preload("res://icon.svg")

	# 4. Crear los 3 Conductores
	for id in range(1, 4):
		var vbox = VBoxContainer.new()
		vbox.alignment = BoxContainer.ALIGNMENT_CENTER
		hbox.add_child(vbox)

		var lbl_titulo = _crear_texto("CONDUCTOR " + str(id), Color.CYAN, 22)
		var lbl_bpm = _crear_texto("BPM: --", Color.WHITE, 16)
		var lbl_parp = _crear_texto("Parpadeos: --", Color.WHITE, 16)
		var lbl_estado = _crear_texto("Estado: CARGANDO...", Color.YELLOW, 18)

		vbox.add_child(lbl_titulo)
		vbox.add_child(lbl_bpm)
		vbox.add_child(lbl_parp)
		vbox.add_child(lbl_estado)

		# Ajuste de altura para que los 3 carriles entren en la pantalla estándar
		var carril_y = 130 + (id * 125)

		# Dibujar línea separadora de carriles
		var linea = ColorRect.new()
		linea.color = Color(1, 1, 1, 0.3)
		linea.position = Vector2(0, carril_y - 62)
		linea.size = Vector2(3000, 4)
		add_child(linea)

		# Crear el Vehículo
		var sprite = Sprite2D.new()
		sprite.texture = textura_por_defecto
		sprite.scale = Vector2(0.5, 0.5) # Ligeramente más pequeños para mejor proporción
		sprite.position = Vector2(randf_range(-200, 500), carril_y)
		add_child(sprite)

		flota[id] = {
			"sprite": sprite,
			"ui_bpm": lbl_bpm,
			"ui_parp": lbl_parp,
			"ui_estado": lbl_estado,
			"velocidad_actual": 90.0,
			"estado": "NORMAL"
		}

func _crear_texto(texto: String, color: Color, size: int) -> Label:
	var lbl = Label.new()
	lbl.text = texto
	lbl.add_theme_color_override("font_color", color)
	lbl.add_theme_color_override("font_outline_color", Color.BLACK)
	lbl.add_theme_constant_override("outline_size", 5)
	lbl.add_theme_font_size_override("font_size", size)
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return lbl

# --- LÓGICA DE MOVIMIENTO ---
func _process(delta: float) -> void:
	var ancho_pantalla = get_viewport_rect().size.x
	var requiere_alarma = false

	for id in flota.keys():
		var datos = flota[id]
		var sprite = datos["sprite"]
		var vel = datos["velocidad_actual"]

		sprite.position.x += vel * delta

		if sprite.position.x > ancho_pantalla + 150:
			sprite.position.x = -150

		if datos["estado"] == "CRITICO" or datos["estado"] == "ALERTA":
			requiere_alarma = true

	if requiere_alarma and not alarma_sonora.playing:
		alarma_sonora.play()
	elif not requiere_alarma and alarma_sonora.playing:
		alarma_sonora.stop()

# --- RED Y CONEXIÓN AL BACKEND ---
func autenticar_backend() -> void:
	var datos_login = "username=admin&password=safedriver123"
	var headers = PackedStringArray(["Content-Type: application/x-www-form-urlencoded"])
	http_cliente.request(url_login, headers, HTTPClient.METHOD_POST, datos_login)

func _al_recibir_login(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var respuesta = JSON.parse_string(body.get_string_from_utf8())
		token_jwt = respuesta.get("access_token", "")
		timer_alertas.start()
	else:
		print("❌ Falla de autenticación en backend.")

func _consultar_alertas() -> void:
	if token_jwt == "": return
	var headers = PackedStringArray(["Authorization: Bearer " + token_jwt])
	http_alertas.request(url_alertas, headers, HTTPClient.METHOD_GET)

func _al_recibir_alertas(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200: return
	var txt = body.get_string_from_utf8()
	if txt.is_empty(): return
	var alertas = JSON.parse_string(txt)
	if typeof(alertas) != TYPE_ARRAY: return

	var camiones_actualizados = {1: false, 2: false, 3: false}

	for alerta in alertas:
		var v_id = int(alerta.get("vehiculo_id", 0))
		
		if v_id in flota and not camiones_actualizados[v_id]:
			actualizar_estado_vehiculo(v_id, alerta)
			camiones_actualizados[v_id] = true
			
		if camiones_actualizados[1] and camiones_actualizados[2] and camiones_actualizados[3]:
			break

func actualizar_estado_vehiculo(id: int, alerta: Dictionary) -> void:
	var datos = flota[id]
	var nivel = alerta.get("nivel", "NORMAL")
	
	datos["estado"] = nivel
	datos["ui_bpm"].text = "BPM: " + str(alerta.get("valor_bpm", 0))
	datos["ui_parp"].text = "Parp/m: " + str(alerta.get("parpadeos_por_minuto", 0))

	match nivel:
		"CRITICO":
			datos["ui_estado"].text = "⚠️ CRÍTICO (MICROSUEÑO)"
			datos["ui_estado"].add_theme_color_override("font_color", Color.RED)
			datos["sprite"].modulate = Color.RED
			datos["velocidad_actual"] = 30.0 
		"ALERTA":
			datos["ui_estado"].text = "🔸 FATIGA TEMPRANA"
			datos["ui_estado"].add_theme_color_override("font_color", Color.ORANGE)
			datos["sprite"].modulate = Color.ORANGE
			datos["velocidad_actual"] = 55.0 
		_:
			datos["ui_estado"].text = "✅ ÓPTIMO"
			datos["ui_estado"].add_theme_color_override("font_color", Color.GREEN)
			datos["sprite"].modulate = Color.WHITE
			datos["velocidad_actual"] = 90.0
