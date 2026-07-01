#!/usr/bin/env bash
# SynCoin - Deploiement des smart contracts Solana
# Prérequis: Solana CLI, Anchor CLI

set -e

echo "🌱 SynCoin - Déploiement Smart Contracts"
echo "=========================================="

# 1. Vérifier les prérequis
echo ""
echo "📋 Vérification des prérequis..."

check_command() {
    if command -v $1 &> /dev/null; then
        echo "  ✅ $1 installé"
    else
        echo "  ❌ $1 manquant"
        return 1
    fi
}

check_command solana
check_command anchor

# 2. Configurer le réseau
echo ""
echo "🔧 Configuration du réseau..."
solana config set --url devnet 2>/dev/null || true
echo "  Réseau: $(solana config get | grep 'RPC URL' | awk '{print $3}')"

# 3. Build des contrats
echo ""
echo "📦 Build des smart contracts..."
cd contracts

# Olona Token
echo "  Token Olona..."
if [ -f olona_token.rs ]; then
    echo "    ✅ Source présente"
    # TODO: Compilation Anchor
fi

# NFT Mint
echo "  NFT Mint..."
if [ -f nft_mint.rs ]; then
    echo "    ✅ Source présente"
    # TODO: Compilation Anchor
fi

cd ..

# 4. Déploiement (à faire plus tard)
echo ""
echo "🚀 Déploiement (quand le projet sera public)"
echo "  anchor deploy"
echo ""
echo "✅ Préparation terminée"
echo "🌱 Pour Lilo. Pour le monde. Pour nous."
