class ForestPage extends StatelessWidget {
  const ForestPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Ma Forêt'), centerTitle: true, backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            color: Colors.green.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  const Icon(Icons.forest, color: Colors.green, size: 48),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('0 arbres', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.green)),
                    Text('Plante des arbres avec tes Olona', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          const Text('Impact environnemental', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          _ImpactTile(icon: Icons.cloud, color: Colors.blue, label: 'CO₂ absorbé', value: '0 kg/an'),
          _ImpactTile(icon: Icons.air, color: Colors.teal, label: 'Oxygène produit', value: '0 kg/an'),
          _ImpactTile(icon: Icons.ecology, color: Colors.green, label: 'Biodiversité', value: '0 espèces'),
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
