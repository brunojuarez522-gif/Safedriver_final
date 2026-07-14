import 'package:flutter/material.dart';
import '../models/alerta.dart';
import '../services/api_service.dart';

class AlertasScreen extends StatefulWidget {
  const AlertasScreen({super.key});
  @override
  State<AlertasScreen> createState() => _AlertasScreenState();
}

class _AlertasScreenState extends State<AlertasScreen> {
  late Future<List<Alerta>> _future;
  String _filtro = 'TODOS';

  @override
  void initState() {
    super.initState();
    _refrescar();
  }

  void _refrescar() {
    setState(() {
      _future = ApiService().fetchAlertas();
    });
  }

  Color _color(String n) => n == 'CRITICO'
      ? Colors.red
      : n == 'ALERTA'
          ? Colors.orange
          : Colors.green;

  IconData _icon(String t) => t == 'FATIGA_EXTREMA_O_EMERGENCIA' || t == 'FATIGA_TEMPRANA'
      ? Icons.bedtime
      : t == 'EXCESO_VELOCIDAD'
          ? Icons.speed
          : Icons.warning_amber_rounded;

  // Actualizado para mostrar las nuevas métricas biométricas
  String _formatMetrics(Alerta a) {
    List<String> parts = [];
    if (a.valorBpm != null) parts.add('BPM: ${a.valorBpm}');
    if (a.parpadeosPorMinuto != null) parts.add('Parpadeos: ${a.parpadeosPorMinuto}');
    if (a.valorVelocidad != null) parts.add('Vel: ${a.valorVelocidad} km/h');
    return parts.isNotEmpty
        ? parts.join('  ·  ')
        : 'Telemetría no disponible';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        backgroundColor: const Color(0xFFE64A19),
        title: const Text('Historial de Alertas',
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.filter_list, color: Colors.white),
            onSelected: (val) => setState(() => _filtro = val),
            itemBuilder: (_) => ['TODOS', 'CRITICO', 'ALERTA']
                .map((f) => PopupMenuItem(value: f, child: Text(f)))
                .toList(),
          )
        ],
      ),
      body: Column(
        children: [
          if (_filtro != 'TODOS')
            Container(
              width: double.infinity,
              color: Colors.orange.shade100,
              padding: const EdgeInsets.all(8),
              child: Text(
                'Mostrando solo: $_filtro',
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepOrange),
              ),
            ),
          Expanded(
            child: RefreshIndicator(
              onRefresh: () async => _refrescar(),
              child: FutureBuilder<List<Alerta>>(
                future: _future,
                builder: (context, snap) {
                  if (snap.connectionState == ConnectionState.waiting) {
                    return const Center(
                        child: CircularProgressIndicator(color: Color(0xFFE64A19)));
                  }
                  if (snap.hasError) {
                    return Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error_outline, size: 48, color: Colors.grey),
                          const SizedBox(height: 16),
                          Text('Error de conexión', style: TextStyle(color: Colors.grey[700])),
                        ],
                      ),
                    );
                  }

                  final datos = snap.data ?? [];
                  final lista = _filtro == 'TODOS'
                      ? datos
                      : datos.where((a) => a.nivel == _filtro).toList();

                  if (lista.isEmpty) {
                    return const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.check_circle_outline, size: 64, color: Colors.green),
                          SizedBox(height: 16),
                          Text('No hay alertas registradas',
                              style: TextStyle(color: Colors.grey, fontSize: 16)),
                        ],
                      ),
                    );
                  }

                  return ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: lista.length,
                    itemBuilder: (_, i) {
                      final a = lista[i];
                      final color = _color(a.nivel);
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12)),
                        child: Container(
                          decoration: BoxDecoration(
                            border: Border(left: BorderSide(color: color, width: 5)),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: color.withOpacity(0.1),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Icon(_icon(a.tipo), color: color, size: 22),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Expanded(
                                            child: Text(
                                              a.tipo,
                                              style: TextStyle(
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 14,
                                                  color: color),
                                              overflow: TextOverflow.ellipsis,
                                            ),
                                          ),
                                          const SizedBox(width: 8),
                                          Container(
                                            padding: const EdgeInsets.symmetric(
                                                horizontal: 8, vertical: 4),
                                            decoration: BoxDecoration(
                                              color: color.withOpacity(0.1),
                                              borderRadius: BorderRadius.circular(6),
                                              border: Border.all(color: color),
                                            ),
                                            child: Text(
                                              a.nivel,
                                              style: TextStyle(
                                                  color: color,
                                                  fontSize: 10,
                                                  fontWeight: FontWeight.bold),
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        'Conductor #${a.conductorId}  ·  ${_formatMetrics(a)}',
                                        style: const TextStyle(color: Colors.grey, fontSize: 12),
                                      ),
                                      if (a.timestamp.length > 10)
                                        Text(
                                          a.timestamp.substring(0, 19),
                                          style: const TextStyle(color: Colors.grey, fontSize: 11),
                                        ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}