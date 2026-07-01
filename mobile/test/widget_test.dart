import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:syncoin/main.dart';

void main() {
  testWidgets('SynCoin app displays home page', (tester) async {
    await tester.pumpWidget(const SynCoinApp());

    // Vérifie que le titre est présent
    expect(find.text('SynCoin'), findsWidgets);

    // Vérifie que les stats cards sont présentes
    expect(find.text('Olona'), findsOneWidget);
    expect(find.text('Arbres'), findsOneWidget);
    expect(find.text('Compute'), findsOneWidget);
    expect(find.text('NFTs'), findsOneWidget);

    // Vérifie que la navigation est présente
    expect(find.byType(NavigationBar), findsOneWidget);
  });

  testWidgets('Navigation between tabs works', (tester) async {
    await tester.pumpWidget(const SynCoinApp());

    // Accueil par défaut
    expect(find.text('Contribuer maintenant'), findsOneWidget);

    // Navigue vers Récompenses
    await tester.tap(find.text('Récompenses'));
    await tester.pumpAndSettle();
    expect(find.text('Planter un arbre'), findsOneWidget);

    // Navigue vers Forêt
    await tester.tap(find.text('Forêt'));
    await tester.pumpAndSettle();
    expect(find.text('Impact environnemental'), findsOneWidget);

    // Navigue vers Profil
    await tester.tap(find.text('Profil'));
    await tester.pumpAndSettle();
    expect(find.text('SynCoin User'), findsOneWidget);
  });

  testWidgets('Contribute button exists', (tester) async {
    await tester.pumpWidget(const SynCoinApp());
    expect(find.text('Contribuer maintenant'), findsOneWidget);
  });
}
