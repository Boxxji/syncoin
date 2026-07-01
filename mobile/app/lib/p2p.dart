import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'node.dart';
import 'wallet.dart';

class P2PNetwork {
  final SynCoinNode node;
  final Wallet wallet;
  Timer? _heartbeat;
  List<String> _peers = [];

  P2PNetwork({required this.node, required this.wallet});

  void start({int port = 8765}) {
    _heartbeat = Timer.periodic(Duration(seconds: 30), (_) => _broadcast());
    print('🌱 P2P started on port $port');
  }

  void stop() {
    _heartbeat?.cancel();
  }

  Future<void> _broadcast() async {
    for (final peer in _peers) {
      try {
        await http.post(
          Uri.parse('http://$peer/'),
          body: jsonEncode({'action': 'ping', 'node': node.id}),
          headers: {'Content-Type': 'application/json'},
        );
      } catch (_) {}
    }
  }

  Future<bool> connect(String host, int port) async {
    try {
      final url = 'http://$host:$port/';
      final resp = await http.post(
        Uri.parse(url),
        body: jsonEncode({'action': 'ping'}),
        headers: {'Content-Type': 'application/json'},
      );
      if (resp.statusCode == 200) {
        _peers.add('$host:$port');
        return true;
      }
    } catch (_) {}
    return false;
  }

  List<String> get peers => List.unmodifiable(_peers);
  int get peerCount => _peers.length;
}
