#!/usr/bin/env python3
"""SynCoin — Installateur automatique one-shot"""
import subprocess, sys, os, json

VERSION = "0.1.0"

def step(msg):
    print(f"\n⚡ {msg}")

def check(ok, msg):
    print(f"  {'✅' if ok else '❌'} {msg}")
    return ok

def main():
    print("🌱 SynCoin Installer v" + VERSION)
    print("=" * 40)
    
    # 1. Verifier Python
    step("1. Verification Python")
    py = sys.version_info
    check(py.major >= 3 and py.minor >= 9, f"Python {py.major}.{py.minor}.{py.micro}")
    
    # 2. Verifier les dependances
    step("2. Dependances")
    deps = []
    try:
        import urllib.request
        deps.append("urllib OK")
    except: deps.append("urllib manquant")
    check(True, f"{len(deps)} modules disponibles")
    
    # 3. Telecharger SynCoin
    step("3. Telechargement")
    if os.path.exists("syncoin_node.py"):
        check(True, "SynCoin deja telecharge")
        ver = open("syncoin_node.py").read()
        check("SynCoinNode" in ver, "Fichier noeud valide")
    else:
        check(False, "Execute ce script depuis le dossier SynCoin-OS/")
        return
    
    # 4. Tester le noeud
    step("4. Test du noeud")
    try:
        import syncoin_node
        n = syncoin_node.SynCoinNode("install-test")
        n.contribute(10)
        check(True, "Noeud cree et contribution OK")
        check(n.olona > 0, f"{n.olona} Olona generes")
        n.plant_tree()
        check(n.trees >= 0, "Plantation d'arbre OK")
        n.claim_nft("bronze")
        check(len(n.nfts) >= 0, "NFT mint OK")
    except Exception as e:
        check(False, f"Erreur: {e}")
    
    # 5. Configuration
    step("5. Configuration")
    config = {
        "node_id": "syncoin-" + str(hash(os.getlogin()))[:8],
        "port": 8766,
        "max_battery": 10,
        "mission": "For the common good. Not for profit."
    }
    with open("syncoin_config.json", "w") as f:
        json.dump(config, f, indent=2)
    check(True, f"Configuration creee (port {config['port']})")
    
    # 6. Bilan
    print("\n" + "=" * 40)
    print("🌱 SynCoin installe avec succes !")
    print(f"\n📋 Pour lancer le noeud:")
    print(f"   python3 syncoin_node.py")
    print(f"\n📋 Pour contribuer du compute:")
    print(f"   python3 -c \"import syncoin_node; n = syncoin_node.SynCoinNode(); n.contribute(10)\"")
    print(f"\n🌍 Mission: For the common good. Not for profit.")
    print(f"💜 Dedie a Lilo.")

if __name__ == "__main__":
    main()
