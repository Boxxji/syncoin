import 'package:flutter/material.dart';

class ComputeStatsPage extends StatelessWidget {
  const ComputeStatsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Green Compute Power'), centerTitle: true, backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            color: Colors.green.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  const Icon(Icons.bolt, color: Colors.green, size: 48),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('100% Green Energy', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.green)),
                    Text('Monetize solar surplus & idle power', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          const Text('Decarbonized Metrics', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          _ImpactTile(icon: Icons.speed, color: Colors.blue, label: 'Compute Throughput', value: '35.2 TOPS'),
          _ImpactTile(icon: Icons.solar_power, color: Colors.amber, label: 'Clean Energy Share', value: '100% Solar / Battery'),
          _ImpactTile(icon: Icons.savings, color: Colors.green, label: 'Direct Host Earnings', value: '100% Direct Payout'),
        ],
      ),
    );
  }
}

class _ImpactTile extends StatelessWidget {
  final IconData icon; final Color color; final String label, value;
  const _ImpactTile({required this.icon, required this.color, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(icon, color: color)),
        title: Text(label),
        trailing: Text(value, style: TextStyle(fontWeight: FontWeight.bold, color: color)),
      ),
    );
  }
}
