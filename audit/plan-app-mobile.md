# 📱 SynCoin Mobile App — Plan d'audit

## Concept
Une app iOS et Android qui utilise max 10% de la batterie du téléphone pour prêter du compute au réseau SynCoin. En échange : Olona (monnaie/cadeau) + NFTs.

## Récompenses
- **Olona** : Monnaie/cadeau du réseau. Échangeable contre data gratuit, MIDI, ou dons pour planter des arbres.
- **NFTs** : Offerts pour chaque palier de contribution. Preuve que tu as participé au bien commun.

## Tech Stack
- **Flutter** (Dart) — cross-platform iOS/Android
- **SynCoin Core** — Python, via embedded ou bridge
- **P2P** — WebSocket/Hydre pour la communication entre nœuds
- **Wallet** — Stockage local des Olona et NFTs

## Sécurité
- Sandboxé : max 10% CPU, max 10% batterie
- Zéro accès aux données personnelles
- Pas de tracking, pas de pub
- Open source, auditable par tous

## Audit requis
- [ ] Architecture app mobile
- [ ] Système de récompenses Olona
- [ ] NFTs — standard, mint, distribution
- [ ] Communication P2P sécurisée
- [ ] Licence et conformité
- [ ] Aucun lien avec l'Essaim ou le Roi
Nids: plan de forge echelonne - 10 comptes/jour sur le PC
