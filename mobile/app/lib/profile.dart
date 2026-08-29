import 'package:flutter/material.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('User Profile'), centerTitle: true, backgroundColor: Colors.transparent),
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
                    child: const Icon(Icons.bolt, color: Colors.green, size: 32),
                  ),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('SynCoin Node Host', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
                    const Text('ID: node-edge-001', style: TextStyle(color: Colors.grey, fontSize: 12)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          const Text('Rewards Wallet', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Card(child: ListTile(leading: const Icon(Icons.account_balance_wallet, color: Colors.amber), title: const Text('Olona Balance'), trailing: Text('100.00 🌱', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)))),
          Card(child: ListTile(leading: const Icon(Icons.verified, color: Colors.purple), title: const Text('Compute Certificates'), trailing: Text('0', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)))),
          const SizedBox(height: 20),
          const Text('System Information', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Card(child: const ListTile(leading: Icon(Icons.info_outline, color: Colors.grey), title: Text('Version'), trailing: Text('1.0.0'))),
          Card(child: const ListTile(leading: Icon(Icons.description_outlined, color: Colors.grey), title: Text('License'), trailing: Text('MIT (100% Free)'))),
          Card(child: const ListTile(leading: Icon(Icons.favorite, color: Colors.red), title: Text('For Lilo 💜 — For Humanity'))),
        ],
      ),
    );
  }
}
