class RewardsPage extends StatelessWidget {
  const RewardsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Récompenses'), centerTitle: true, backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            color: Colors.amber.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  const Icon(Icons.card_giftcard, color: Colors.amber, size: 48),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('100 Olona', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.amber)),
                    Text('Gagne des Olona en contribuant', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _ActionTile(icon: Icons.forest, color: Colors.green, title: 'Planter un arbre', subtitle: '50 Olona', onTap: () {}),
          _ActionTile(icon: Icons.image, color: Colors.purple, title: 'Mint un NFT', subtitle: '25 Olona', onTap: () {}),
          _ActionTile(icon: Icons.wifi, color: Colors.blue, title: 'Data gratuit', subtitle: '10 Olona/h', onTap: () {}),
          _ActionTile(icon: Icons.music_note, color: Colors.teal, title: 'MIDI cadeau', subtitle: '5 Olona', onTap: () {}),
        ],
      ),
    );
  }
}

class _ActionTile extends StatelessWidget {
  final IconData icon; final Color color; final String title, subtitle; final VoidCallback onTap;
  const _ActionTile({required this.icon, required this.color, required this.title, required this.subtitle, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(icon, color: color)),
        title: Text(title), subtitle: Text(subtitle, style: const TextStyle(color: Colors.grey)),
        trailing: const Icon(Icons.chevron_right, color: Colors.grey),
        onTap: onTap,
      ),
    );
  }
}
