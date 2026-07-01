# SynCoin — Installation Guide

## Prerequisites
- Python 3.9+
- A smartphone (optional, for mobile app)
- Internet connection

## Quick Install (1 minute)

```bash
# Clone the project
git clone https://github.com/Boxxji/syncoin.git
cd syncoin

# Run the node
python3 syncoin_node.py
```

## Usage

### Start a P2P node
```bash
python3 -c "
import syncoin_node
n = syncoin_node.SynCoinNode('my-node', port=8766)
n.start()
print(f'Node started: {n.id}')
print(f'Olona: {n.olona}')
input('Press Enter to stop...')
"
```

### Contribute compute
```python
n.contribute(10)  # 10 cycles = 1 Olona
```

### Plant a tree
```python
n.plant_tree()  # 50 Olona
```

### Earn an NFT
```python
n.claim_nft('gold')  # bronze, silver, gold, platinum, diamond
```

### Connect to a peer
```python
n.connect('192.168.1.X', 8766)
```

## Mobile App (Flutter)

```bash
cd mobile
flutter pub get
flutter run
```

## iOS App (Swift)

Open the `ios/` folder in Xcode, select your iPhone, and click Run.

## API

The node exposes an HTTP API on the configured port (default: 8766):

| Action | Method | Body | Response |
|--------|--------|------|----------|
| Ping | POST | `{"action":"ping"}` | `{"status":"pong","node":"..."}` |
| Compute | POST | `{"action":"compute","cycles":10}` | `{"status":"ok","olona":1}` |
| Stats | POST | `{"action":"stats"}` | `{...stats...}` |
| Peers | POST | `{"action":"peers"}` | `{"peers":[...]}` |

## Docker

```bash
docker build -t syncoin .
docker run -p 8766:8766 syncoin
```

## License

AGPL v3 + Non-Commercial Clause. Free forever. For everyone.
