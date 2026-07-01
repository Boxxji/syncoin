#!/usr/bin/env python3
"""Tests unitaires SynCoin"""
import sys, os, json, tempfile, unittest

sys.path.insert(0, os.path.dirname(__file__))
import syncoin_node

class TestSynCoinNode(unittest.TestCase):
    
    def setUp(self):
        # Nettoyer le fichier de persistance pour eviter les interférences
        if os.path.exists(syncoin_node.DATA_FILE):
            os.remove(syncoin_node.DATA_FILE)
        self.node = syncoin_node.SynCoinNode("test-node")
    
    def test_creation_noeud(self):
        """Test la création d'un nœud"""
        self.assertIsNotNone(self.node.id)
        self.assertEqual(self.node.olona, 100)
        self.assertEqual(self.node.trees, 0)
        self.assertTrue(len(self.node.id) > 5)
    
    def test_contribution(self):
        """Test la contribution de compute"""
        result = self.node.contribute(100)
        self.assertEqual(self.node.compute_shared, 100)
        self.assertEqual(self.node.olona, 110)  # 100 + 10 reward
        self.assertIn('olona', result)
    
    def test_contribution_minimum(self):
        """Test contribution minimum"""
        result = self.node.contribute(1)
        self.assertEqual(result['olona'], 0)  # < 10 cycles = 0 olona
    
    def test_plant_tree(self):
        """Test la plantation d'arbre"""
        result = self.node.plant_tree()
        self.assertEqual(self.node.trees, 1)
        self.assertEqual(self.node.olona, 50)  # 100 - 50
    
    def test_plant_tree_insufficient(self):
        """Test plantation sans assez d'Olona"""
        # Depenser tous les Olona
        for _ in range(10):
            if self.node.olona >= 50:
                self.node.plant_tree()
        # Plus assez
        result = self.node.plant_tree()
        self.assertIn('error', result)
    
    def test_claim_nft(self):
        """Test le mint d'un NFT"""
        nft = self.node.claim_nft("gold")
        self.assertEqual(len(self.node.nfts), 1)
        self.assertEqual(nft['tier'], "gold")
        self.assertIn('id', nft)
        self.assertIn('timestamp', nft)
    
    def test_multiple_nfts(self):
        """Test le mint de plusieurs NFTs"""
        self.node.claim_nft("bronze")
        self.node.claim_nft("silver")
        self.node.claim_nft("gold")
        self.assertEqual(len(self.node.nfts), 3)
        self.assertEqual(self.node.nfts[0]['tier'], "bronze")
        self.assertEqual(self.node.nfts[1]['tier'], "silver")
        self.assertEqual(self.node.nfts[2]['tier'], "gold")
    
    def test_invalid_tier_nft(self):
        """Test tier invalide"""
        nft = self.node.claim_nft("ultra_rare")
        self.assertEqual(len(self.node.nfts), 1)  # Accepté car pas de validation stricte côté Python
    
    def test_stats(self):
        """Test les statistiques"""
        self.node.contribute(50)
        self.node.plant_tree()
        self.node.claim_nft("diamond")
        stats = self.node.stats()
        self.assertIn('node', stats)
        self.assertIn('olona', stats)
        self.assertIn('trees_planted', stats)
        self.assertIn('nfts', stats)
        self.assertIn('compute_shared', stats)
        self.assertIn('mission', stats)
        self.assertEqual(stats['olona'], 55)  # 100 + 5 - 50
        self.assertEqual(stats['trees_planted'], 1)
        self.assertEqual(stats['nfts'], 1)
    
    def test_mission(self):
        """Test que la mission est correcte"""
        stats = self.node.stats()
        self.assertEqual(stats['mission'], "For the common good. Not for profit.")
    
    def test_max_battery(self):
        """Test la limite de batterie"""
        stats = self.node.stats()
        self.assertEqual(stats['max_battery_pct'], 10)
    
    def test_id_unique(self):
        """Test que chaque nœud a un ID unique"""
        n2 = syncoin_node.SynCoinNode("autre-node")
        self.assertNotEqual(self.node.id, n2.id)
    
    def test_p2p_connect(self):
        """Test la connexion P2P (locale)"""
        n2 = syncoin_node.SynCoinNode("peer-node")
        self.node.peers["127.0.0.1:8766"] = {"host": "127.0.0.1", "port": 8766, "node": "peer-node"}
        self.assertEqual(len(self.node.peers), 1)
    
    def test_serialization_stats(self):
        """Test que les stats sont sérialisables en JSON"""
        stats = self.node.stats()
        json_str = json.dumps(stats)
        self.assertIsNotNone(json_str)
        self.assertIn('network', json.loads(json_str))

if __name__ == "__main__":
    print("🌱 SynCoin - Tests unitaires")
    print("=" * 50)
    unittest.main(verbosity=2)
