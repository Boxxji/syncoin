SynCoin-OS/
├── README.md          # Présentation du projet
├── LICENSE            # AGPL v3 + clause non-commerciale
├── CODE_OF_CONDUCT.md # Règles de la communauté
├── CONTRIBUTING.md    # Comment contribuer
│
├── syncoin_node.py    # Nœud Python (référence)
│
├── mobile/            # App mobile (Flutter)
│   ├── app/
│   │   ├── lib/
│   │   │   ├── main.dart
│   │   │   ├── node.dart        # Nœud SynCoin
│   │   │   ├── wallet.dart      # Portefeuille Olona/NFT
│   │   │   └── p2p.dart         # Communication P2P
│   │   └── pubspec.yaml
│   └── README.md
│
├── docs/              # Documentation
│   ├── whitepaper.md  # Livre blanc
│   ├── architecture.md
│   └── legal.md       # Conformité RGPD/MiCA
│
├── contracts/         # Smart contracts Solana
│   ├── olona_token.rs # Token Olona
│   └── nft_mint.rs    # Mint NFTs
│
├── tests/
│   ├── test_node.py
│   └── test_p2p.py
│
└── audit/             # Rapports d'audit
    └── plan-app-mobile.md
