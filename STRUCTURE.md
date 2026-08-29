SynCoin-OS/ (v1.0.0 — MIT License)
├── README.md                      # Présentation complète, documentation & guides
├── LICENSE                        # Licence MIT (100% Libre & Gratuit)
├── CODE_OF_CONDUCT.md             # Règles de la communauté & éthique verte
├── CONTRIBUTING.md                # Guide de contribution open source
├── requirements.txt               # Dépendances Python légères (websockets, nats-py, aiohttp)
├── docker-compose.yml             # Déploiement multi-services (Hub + NATS)
├── Dockerfile                     # Image Docker du Nœud SynCoin
│
├── 🧠 CORE NETWORK & DISPATCHING
│   ├── syncoin_node.py            # Nœud P2P & Hub WebSocket/NATS (Sun-Follower Priority)
│   ├── syncoin_gateway.py         # Gateway REST OpenAI-Compatible (:8767) & Remuneration Marketplace
│   ├── syncoin_energy_daemon.py   # Arbitre Solaire & Batteries Résidentielles (BESS)
│   └── syncoin_worker.py          # Client Worker Universel CLI multi-plateforme
│
├── 🖥️ APPLICATIONS DESKTOP (macOS & Windows PC)
│   └── desktop/
│       ├── desktop_app.py         # Application GUI Bureau complète (Tkinter dark theme)
│       └── package_desktop.py     # Script de build d'exécutable autonome (.app / .exe)
│
├── 📱 APPLICATION NATIVE iOS (iPhone & iPad)
│   └── ios/
│       ├── SynCoinApp.swift       # Application native SwiftUI avec monitoring en direct
│       ├── WasmEngine.swift       # Moteur WebAssembly Wasm3 pour calculs locaux
│       ├── SynCoin.xcodeproj/     # Projet Xcode complet
│       └── wasm3/                 # Interpréteur WebAssembly embarqué en C
│
├── 🤖 APPLICATION MOBILE ANDROID (Flutter / Dart)
│   └── mobile/
│       └── app/
│           ├── lib/
│           │   ├── main.dart      # Application Flutter pour Android avec terminal et jauges
│           │   ├── wallet.dart    # Gestionnaire de portefeuille Olona & gains
│           │   └── p2p.dart       # Client WebSocket mobile
│           └── pubspec.yaml
│
├── 📜 SMART CONTRACTS SOLANA (Rémunération & Écologie)
│   └── contracts/
│       ├── olona_token.rs         # Token de récompense Anchor/Rust
│       └── nft_mint.rs            # Certificats de contribution décarbonée
│
├── 🧪 SUITE DE TESTS AUTOMATISÉS
│   └── tests/
│       ├── test_node.py           # Tests unitaires du nœud historique
│       └── test_syncoin_e2e.py    # Test End-to-End validant le cycle complet (16/16 OK)
│
└── 📚 DOCUMENTATION & SPÉCIFICATIONS
    └── docs/
        ├── index.html             # Landing page interactive
        ├── architecture.md        # Architecture Neocloud et topologie mesh
        ├── economie.md            # Modèle économique de redistribution (90/10)
        └── whitepaper.md          # Livre blanc SynCoin

