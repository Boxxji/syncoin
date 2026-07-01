class SynCoinNode {
  String _id;
  int _olona = 100;
  int _trees = 0;
  int _computeShared = 0;
  int _nfts = 0;
  bool _contributing = false;
  List<Map<String, dynamic>> _peers = [];

  SynCoinNode() : _id = _generateId();

  static String _generateId() {
    final now = DateTime.now().millisecondsSinceEpoch;
    return 'node-${now.toString().substring(now.toString().length - 8)}';
  }

  String get id => _id;
  int get olona => _olona;
  int get trees => _trees;
  int get compute => _computeShared;
  int get nfts => _nfts;
  int get peers => _peers.length;

  void startContributing(Function(Map) onUpdate) {
    _contributing = true;
    // Simulation de contribution (vrai P2P dans la version complète)
    Future.doWhile(() async {
      if (!_contributing) return false;
      await Future.delayed(Duration(seconds: 30));
      _computeShared += 10;
      _olona += 1;
      onUpdate(stats());
      return _contributing;
    });
  }

  void stopContributing() {
    _contributing = false;
  }

  void plantTree() {
    if (_olona >= 50) {
      _olona -= 50;
      _trees += 1;
    }
  }

  void claimNft(String tier) {
    _nfts += 1;
  }

  Map<String, dynamic> stats() {
    return {
      'olona': _olona,
      'trees': _trees,
      'compute': _computeShared,
      'nfts': _nfts,
      'peers': _peers.length,
    };
  }
}
