import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';
import 'dart:async';

void main() => runApp(const SynCoinApp());

class SynCoinApp extends StatelessWidget {
  const SynCoinApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SynCoin CLI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: Colors.black,
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00FF00),
          surface: Colors.black,
          background: Colors.black,
        ),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontFamily: 'Courier', color: Color(0xFF00FF00), fontSize: 14),
          bodyMedium: TextStyle(fontFamily: 'Courier', color: Color(0xFF00FF00), fontSize: 12),
        ),
      ),
      home: const GrokTerminalScreen(),
    );
  }
}

class GrokTerminalScreen extends StatefulWidget {
  const GrokTerminalScreen({super.key});

  @override
  State<GrokTerminalScreen> createState() => _GrokTerminalScreenState();
}

class _GrokTerminalScreenState extends State<GrokTerminalScreen> {
  final List<String> _logs = [
    "> SYNCOIN OS v0.2.0 INITIALIZED", 
    "> BIOACOUSTIC T-SNE PROTOCOL LOADED",
    "> SYSTEM STANDBY. AWAITING NODE CONNECTION..."
  ];
  WebSocketChannel? _channel;
  int _olona = 0;
  int _computeCycles = 0;
  bool _isConnected = false;
  bool _isComputing = false;
  Timer? _computeTimer;

  final ScrollController _scrollController = ScrollController();

  void _addLog(String message) {
    setState(() {
      _logs.add("> $message");
      if (_logs.length > 100) _logs.removeAt(0); // Keep last 100 logs
    });
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
      }
    });
  }

  void _connect() {
    try {
      // Dans le futur, l'IP sera decouverte via DNS P2P
      _channel = WebSocketChannel.connect(Uri.parse('ws://127.0.0.1:8766')); 
      _addLog("CONNECTING TO SYNCOIN NETWORK [ws://127.0.0.1:8766]");
      
      _channel!.stream.listen(
        (message) {
          final data = jsonDecode(message);
          if (data['status'] == 'ok' && data.containsKey('olona')) {
            setState(() {
              _olona += data['olona'] as int;
            });
            _addLog("COMPUTE ACCEPTED. REWARD: +${data['olona']} OLONA");
          } else if (data['status'] == 'pong') {
            setState(() => _isConnected = true);
            _addLog("CONNECTION ESTABLISHED. NODE_ID: ${data['node']}");
          } else {
             _addLog("RECV: $message");
          }
        },
        onDone: () {
          setState(() {
            _isConnected = false;
            _isComputing = false;
          });
          _computeTimer?.cancel();
          _addLog("CONNECTION CLOSED BY PEER.");
        },
        onError: (error) {
          setState(() {
            _isConnected = false;
            _isComputing = false;
          });
          _computeTimer?.cancel();
          _addLog("CONNECTION ERROR: $error");
        },
      );
      
      // Handshake initial
      _channel!.sink.add(jsonEncode({"action": "ping"}));
    } catch (e) {
      _addLog("FAILED TO CONNECT: $e");
    }
  }

  void _toggleCompute() {
    if (!_isConnected) {
      _addLog("ERROR: NOT CONNECTED TO NETWORK");
      return;
    }
    setState(() {
      _isComputing = !_isComputing;
    });

    if (_isComputing) {
      _addLog("INITIATING BIOACOUSTIC T-SNE COMPUTE BATCH...");
      _computeTimer = Timer.periodic(const Duration(seconds: 2), (timer) {
        final cycles = 15;
        _channel!.sink.add(jsonEncode({"action": "compute", "cycles": cycles}));
        setState(() => _computeCycles += cycles);
        _addLog("TX: COMPUTE_BATCH [CYCLES: $cycles] [DIM: 128D]");
      });
    } else {
      _computeTimer?.cancel();
      _addLog("COMPUTE SEQUENCE TERMINATED BY USER.");
    }
  }

  @override
  void dispose() {
    _channel?.sink.close();
    _computeTimer?.cancel();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Status Bar (Top)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: const BoxDecoration(
                border: Border(bottom: BorderSide(color: Color(0xFF00FF00), width: 1)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text("NET: ${_isConnected ? 'ONLINE' : 'OFFLINE'}", 
                      style: const TextStyle(color: Color(0xFF00FF00), fontWeight: FontWeight.bold, fontFamily: 'Courier', fontSize: 13)),
                  Text("OLONA: $_olona", 
                      style: const TextStyle(color: Color(0xFF00FF00), fontWeight: FontWeight.bold, fontFamily: 'Courier', fontSize: 13)),
                  Text("CYCLES: $_computeCycles", 
                      style: const TextStyle(color: Color(0xFF00FF00), fontWeight: FontWeight.bold, fontFamily: 'Courier', fontSize: 13)),
                ],
              ),
            ),
            
            // Terminal View (Middle)
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(12),
                child: ListView.builder(
                  controller: _scrollController,
                  itemCount: _logs.length,
                  itemBuilder: (context, index) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 6),
                      child: Text(_logs[index], style: const TextStyle(fontFamily: 'Courier', color: Color(0xFF00FF00), fontSize: 14)),
                    );
                  },
                ),
              ),
            ),

            // Controls (Bottom)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: Color(0xFF00FF00), width: 1.5),
                        backgroundColor: _isConnected ? Colors.black : const Color(0xFF002200),
                        shape: const ContinuousRectangleBorder(),
                        padding: const EdgeInsets.all(20)
                      ),
                      onPressed: _isConnected ? null : _connect,
                      child: const Text("1. CONNECT_NODE", style: TextStyle(color: Color(0xFF00FF00), fontFamily: 'Courier', fontWeight: FontWeight.bold)),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: OutlinedButton(
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: Color(0xFF00FF00), width: 1.5),
                        backgroundColor: _isComputing ? const Color(0xFF00FF00) : Colors.black,
                        shape: const ContinuousRectangleBorder(),
                        padding: const EdgeInsets.all(20)
                      ),
                      onPressed: _toggleCompute,
                      child: Text(_isComputing ? "HALT_COMPUTE" : "2. START_COMPUTE", 
                        style: TextStyle(
                          color: _isComputing ? Colors.black : const Color(0xFF00FF00), 
                          fontFamily: 'Courier', 
                          fontWeight: FontWeight.bold
                        )
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
