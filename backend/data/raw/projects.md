# Projets — Arsène Godonou

## Credit card fraud detection

Projet personnel de data science complet, suivant la méthodologie CRISP-DM,
sur un dataset réel fortement déséquilibré : 284 807 transactions, dont
seulement 0,17% de fraude.

- Analyse exploratoire et préparation des données, détection des biais et
  prévention des fuites de données (data leakage).
- Comparaison de plusieurs modèles supervisés selon des métriques adaptées
  aux jeux de données déséquilibrés (PR-AUC, F-beta), plutôt que
  l'accuracy classique qui serait trompeuse ici.
- Arbitrage métier documenté sur le choix du seuil de décision (compromis
  precision/recall), avec analyse d'interprétabilité (SHAP) des variables
  déterminantes.
- Résultat obtenu avec XGBoost : PR-AUC 0.825, Recall 78%, Precision 97%.
- Dépôt GitHub : github.com/Arsene666/credit-card-fraude-detection

## Assistant IA documentaire avec RAG

Projet personnel construisant un pipeline RAG (Retrieval-Augmented
Generation) de bout en bout.

- Ingestion de documents multi-format, chunking sémantique adaptatif,
  embeddings multilingues via Cohere, stockage vectoriel dans Qdrant.
- Recherche sémantique par similarité cosinus pour récupérer les passages
  pertinents.
- Simulation de mémoire conversationnelle multi-tours par réinjection de
  l'historique dans le contexte du LLM.
- Extension de l'agent avec recherche web temps réel via SerpApi pour les
  questions hors base documentaire.
- Interface conversationnelle Streamlit avec réponse en streaming.
- Dépôt GitHub : github.com/Arsene666/rag-assistant

## API de détection d'objets (Faster R-CNN)

Projet de formation personnel entraînant et servant un modèle de détection
d'objets.

- Entraînement d'un modèle Faster R-CNN (PyTorch) sur 1 340 images
  annotées, réparties sur 9 classes plus l'arrière-plan.
- Prétraitement et normalisation d'images hétérogènes (formats .jpeg,
  .png, tailles variables).
- Performance obtenue : mAP ≈ 0,64 (exécution CPU).
- Déploiement via une API REST FastAPI permettant l'upload d'image et le
  retour des objets détectés (bounding boxes + labels), conteneurisé avec
  Docker.
- Dépôt GitHub : github.com/Arsene666/object-detection

## AGRO-IA — système intelligent de suivi post-récolte

Projet technique de conception et prototypage visant à réduire les pertes
post-récolte.

- Développement du module embarqué (Arduino + capteurs environnementaux).
- Intégration des prédictions d'un modèle CNN de classification d'images.
- Fusion des données capteurs et des sorties du modèle pour estimer la
  durée de conservation restante des produits récoltés.
- Mise en place d'un système de recommandations pour améliorer la
  qualité et prolonger la durée de vie des récoltes.
- Prototype validé en environnement simulé.

## Ce portfolio lui-même

Ce site est lui-même un projet technique : un assistant IA basé sur un
pipeline RAG (FastAPI + Qdrant + LLM via OpenRouter) qui répond aux
questions des recruteurs uniquement à partir de mes vrais documents
(CV, bio, descriptions de projets) — jamais en inventant.
