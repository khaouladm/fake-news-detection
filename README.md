# Fake News Detection

## Description
Ce projet est une application de détection de fake news utilisant des modèles de machine learning, notamment BERT. L'application permet d'analyser des articles ou des URL en temps réel pour déterminer s'ils contiennent des informations fiables ou non. Elle est conçue pour être utilisée via une interface Streamlit.

## Fonctionnalités
- Analyse en temps réel des articles ou des URL.
- Prédictions basées sur un modèle BERT pré-entraîné.
- Interface utilisateur interactive avec Streamlit.
- Support multilingue (en cours d'intégration).

## Structure du projet
```
fake-news-detection/
│
├── app.py                     # Point d'entrée principal de l'application
├── config.py                  # Configuration globale (API keys, paramètres, etc.)
├── requirements.txt           # Dépendances Python
├── models/                    # Modèles pré-entraînés
│   ├── bert_model/            # Configuration du modèle BERT
│   └── fake_news_model.pkl    # Modèle de classification
├── tests/                     # Tests unitaires
├── translations/              # Fichiers de traduction pour le support multilingue
├── utils/                     # Fonctions utilitaires
│   ├── bert_predictor.py
│   ├── model_loader.py
│   ├── news_api.py
│   ├── preprocess.py
│   ├── real_time_analyzer.py
│   └── url_scraper.py
```

## Prérequis
- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)

## Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/khaouladm/fake-news-detection.git
   cd fake-news-detection
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. Lancez l'application Streamlit :
   ```bash
   streamlit run app.py
   ```
2. Ouvrez votre navigateur à l'adresse affichée (par défaut : `http://localhost:8501`).

## Tests
Pour exécuter les tests unitaires :
```bash
pytest tests/
```


## Licence
Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.

## Auteurs
- **Khaoula DM** - Créatrice et mainteneuse principale.