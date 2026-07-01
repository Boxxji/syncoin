import 'package:flutter/material.dart';
import 'rewards.dart';
import 'forest.dart';
import 'profile.dart';

void main() => runApp(const SynCoinApp());

class SynCoinApp extends StatelessWidget {
  const SynCoinApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SynCoin',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.dark(
          primary: Color(0xFF4CAF50),
          secondary: Color(0xFF81C784),
          surface: Color(0xFF1C1C1E),
        ),
        useMaterial3: true,
        fontFamily: 'SF Pro Display',
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  static const List<Widget> _pages = <Widget>[
    HomePage(),
    RewardsPage(),
    ForestPage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) => setState(() => _selectedIndex = index),
        backgroundColor: Theme.of(context).colorScheme.surface,
        indicatorColor: Color(0xFF4CAF50).withOpacity(0.2),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined, color: Colors.grey), selectedIcon: Icon(Icons.home, color: Color(0xFF4CAF50)), label: 'Accueil'),
          NavigationDestination(icon: Icon(Icons.card_giftcard_outlined, color: Colors.grey), selectedIcon: Icon(Icons.card_giftcard, color: Color(0xFF4CAF50)), label: 'Récompenses'),
          NavigationDestination(icon: Icon(Icons.forest_outlined, color: Colors.grey), selectedIcon: Icon(Icons.forest, color: Color(0xFF4CAF50)), label: 'Forêt'),
          NavigationDestination(icon: Icon(Icons.person_outline, color: Colors.grey), selectedIcon: Icon(Icons.person, color: Color(0xFF4CAF50)), label: 'Profil'),
        ],
      ),
    );
  }
}

// --- Pages ---

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('SynCoin', style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
        backgroundColor: Colors.transparent,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              const Spacer(flex: 2),
              Icon(Icons.eco, size: 80, color: Color(0xFF4CAF50)),
              const SizedBox(height: 16),
              Text('SynCoin', style: theme.textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text("Prête ton téléphone. Reçois des cadeaux.",
                   style: theme.textTheme.bodyLarge?.copyWith(color: Colors.grey)),
              const Spacer(flex: 2),
              _StatGrid(),
              const Spacer(flex: 2),
              SizedBox(
                width: double.infinity, height: 56,
                child: FilledButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Contribuer maintenant', style: TextStyle(fontSize: 16)),
                  style: FilledButton.styleFrom(
                    backgroundColor: Color(0xFF4CAF50),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.battery_5_bar, size: 16, color: Colors.grey),
                  const SizedBox(width: 4),
                  Text('Max 10% batterie', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                  const SizedBox(width: 24),
                  Icon(Icons.public, size: 16, color: Colors.grey),
                  const SizedBox(width: 4),
                  Text('For the common good', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
                ],
              ),
              const Spacer(flex: 1),
            ],
          ),
        ),
      ),
    );
  }
}

class _StatGrid extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        _StatCard(icon: Icons.card_giftcard, value: '100', label: 'Olona', color: Colors.amber),
        const SizedBox(width: 12),
        _StatCard(icon: Icons.forest, value: '0', label: 'Arbres', color: Colors.green),
        const SizedBox(width: 12),
        _StatCard(icon: Icons.bolt, value: '0', label: 'Compute', color: Colors.blue),
        const SizedBox(width: 12),
        _StatCard(icon: Icons.image, value: '0', label: 'NFTs', color: Colors.purple),
      ],
    );
  }
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  final Color color;

  const _StatCard({required this.icon, required this.value, required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 24),
            const SizedBox(height: 4),
            Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
