class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Profil'), centerTitle: true, backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 30,
                    backgroundColor: Colors.green.withOpacity(0.2),
                    child: const Icon(Icons.eco, color: Colors.green, size: 32),
                  ),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('SynCoin User', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                    const Text('ID: syncoin-001', style: TextStyle(color: Colors.grey, fontSize: 12)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          const Text('Portefeuille', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Card(child: ListTile(leading: const Icon(Icons.card_giftcard, color: Colors.amber), title: const Text('Olona'), trailing: Text('100', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)))),
          Card(child: ListTile(leading: const Icon(Icons.image, color: Colors.purple), title: const Text('NFTs'), trailing: Text('0', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)))),
          const SizedBox(height: 20),
          const Text('Informations', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Card(child: const ListTile(leading: Icon(Icons.info_outline, color: Colors.grey), title: Text('Version'), trailing: Text('0.1.0'))),
          Card(child: const ListTile(leading: Icon(Icons.description_outlined, color: Colors.grey), title: Text('Licence'), trailing: Text('AGPL v3'))),
          Card(child: const ListTile(leading: Icon(Icons.favorite, color: Colors.red), title: Text('Pour Lilo 💜'))),
        ],
      ),
    );
  }
}
