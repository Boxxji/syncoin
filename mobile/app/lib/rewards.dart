import 'package:flutter/material.dart';

class RewardsPage extends StatelessWidget {
  const RewardsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Direct Rewards'), centerTitle: true, backgroundColor: Colors.transparent),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            color: Colors.amber.withOpacity(0.1),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  const Icon(Icons.account_balance_wallet, color: Colors.amber, size: 48),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('100.00 Olona', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.amber)),
                    Text('100% Direct Payout to Compute Host', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                  ]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          _ActionTile(icon: Icons.currency_exchange, color: Colors.green, title: 'Withdraw to Solana Wallet', subtitle: 'Instant SOL / USDC transfer', onTap: () {}),
          _ActionTile(icon: Icons.speed, color: Colors.blue, title: 'Redeem AI Compute Credits', subtitle: 'Free decentralized inference', onTap: () {}),
          _ActionTile(icon: Icons.verified, color: Colors.purple, title: 'Export Proof Certificate', subtitle: 'Cryptographic proof of compute', onTap: () {}),
          _ActionTile(icon: Icons.wifi, color: Colors.teal, title: 'Global P2P Mesh Access', subtitle: 'Zero-latency network routing', onTap: () {}),
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
