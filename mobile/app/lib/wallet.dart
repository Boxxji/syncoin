class Wallet {
  String _address;
  int _olona = 0;
  List<Nft> _nfts = [];
  List<Transaction> _history = [];

  Wallet() : _address = _generateAddress();

  static String _generateAddress() {
    final now = DateTime.now().millisecondsSinceEpoch;
    return '0x${now.toRadixString(16)}${(now % 10000).toRadixString(16)}';
  }

  String get address => _address;
  int get olona => _olona;
  List<Nft> get nfts => List.unmodifiable(_nfts);
  List<Transaction> get history => List.unmodifiable(_history);

  void addOlona(int amount, {String reason = 'Contribution'}) {
    _olona += amount;
    _history.add(Transaction(
      type: TransactionType.reward,
      amount: amount,
      description: reason,
    ));
  }

  bool spendOlona(int amount, {String reason = 'Arbre planté'}) {
    if (_olona < amount) return false;
    _olona -= amount;
    _history.add(Transaction(
      type: TransactionType.spend,
      amount: -amount,
      description: reason,
    ));
    return true;
  }

  Nft claimNft(String tier) {
    final nft = Nft(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      tier: tier,
      timestamp: DateTime.now(),
    );
    _nfts.add(nft);
    _history.add(Transaction(
      type: TransactionType.nft,
      amount: 0,
      description: 'NFT ${tier.toUpperCase()}',
    ));
    return nft;
  }
}

class Nft {
  final String id;
  final String tier;
  final DateTime timestamp;

  Nft({required this.id, required this.tier, required this.timestamp});
}

enum TransactionType { reward, spend, nft }

class Transaction {
  final TransactionType type;
  final int amount;
  final String description;
  final DateTime timestamp;

  Transaction({
    required this.type,
    required this.amount,
    required this.description,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}
