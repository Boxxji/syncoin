import numpy as np
from sklearn.manifold import TSNE
import time
import logging

log = logging.getLogger('syncoin')

def process_coda_batch(samples, inject_nan_for_test=False):
    """
    Simule la réception de 'Codas' bioacoustiques (128D) 
    et calcule leur espace latent via t-SNE.
    """
    log.info(f"🐋 BioacousticWorker: Début du traitement de {samples} échantillons.")
    start_time = time.time()
    
    # Génération de embeddings synthétiques 128D (Simulation du signal pur)
    np.random.seed(int(time.time()))
    X = np.random.randn(samples, 128)
    
    if inject_nan_for_test:
        X[0, 0] = np.nan
        
    # Vérification S1-FAIL-FAST
    if np.isnan(X).any():
        log.error("🚨 [S1-FAIL-FAST] Matrice corrompue (NaN détecté). Arrêt critique du système.")
        # On ne capture PAS cette erreur avec un try..except. On crashe.
        raise ValueError("Matrice de Coda invalide : contient des NaN.")

    # Application de t-SNE (Proof of Compute)
    try:
        perplexity = min(30, max(1, samples - 1))
        # Utilisation de n_iter plus bas pour ne pas geler les petits noeuds P2P
        tsne = TSNE(n_components=2, perplexity=perplexity, n_iter=250, random_state=42)
        X_2d = tsne.fit_transform(X)
    except Exception as e:
        log.error(f"🚨 [S1-FAIL-FAST] Erreur mathématique t-SNE: {e}")
        raise e

    duration = time.time() - start_time
    log.info(f"✅ BioacousticWorker: Espace latent calculé en {duration:.2f}s.")
    return X_2d.tolist()
