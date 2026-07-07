# Algo-analyse

API d'analyse de sentiments pour SocialMetrics AI. Elle analyse des tweets en français et retourne un score de sentiment entre -1 (très négatif) et 1 (très positif).

## Fonctionnement

Deux régressions logistiques sont entraînées sur les tweets annotés de la base MySQL :

- un modèle prédit la probabilité qu'un tweet soit positif ;
- un modèle prédit la probabilité qu'un tweet soit négatif.

Le score renvoyé est : `probabilité positive - probabilité négative`, ce qui donne bien une valeur entre -1 et 1.

## Installation

### 1. Dépendances Python

```bash
pip3 install flask scikit-learn mysql-connector-python matplotlib joblib
```

### 2. MySQL

```bash
brew install mysql
brew services start mysql
```

### 3. Création de la base de données

```bash
python3 setup_bdd.py
```

Ce script crée la base `socialmetrics`, la table `tweets` et insère 100 tweets annotés.

Structure de la table `tweets` :

| Colonne  | Type | Description |
|----------|------|-------------|
| id       | INT (clé primaire, auto-incrément) | Identifiant unique |
| text     | TEXT | Contenu du tweet |
| positive | TINYINT | 1 si le tweet est positif, 0 sinon |
| negative | TINYINT | 1 si le tweet est négatif, 0 sinon |

### 4. Entraînement du modèle

```bash
python3 entrainement.py
```

Ce script entraîne les deux modèles, affiche les rapports de classification, sauvegarde les modèles dans `modele/` et les matrices de confusion dans `rapport/`.

### 5. Lancement de l'API

```bash
python3 app.py
```

L'API démarre sur `http://localhost:5000`.

## Utilisation de l'API

### POST /analyse

Envoie une liste de tweets, reçoit un score par tweet.

Requête :

```bash
curl -X POST http://localhost:5000/analyse \
  -H "Content-Type: application/json" \
  -d '["J'\''adore ce produit !", "Ce service est catastrophique."]'
```

Réponse :

```json
{
  "J'adore ce produit !": 0.75,
  "Ce service est catastrophique.": -0.68
}
```

### Gestion des erreurs

| Cas | Réponse |
|-----|---------|
| Corps non JSON | 400, `{"erreur": "Le corps de la requete doit etre du JSON."}` |
| JSON qui n'est pas une liste | 400, `{"erreur": "Le JSON doit etre une liste de tweets."}` |
| Liste vide | 400, `{"erreur": "La liste de tweets est vide."}` |
| Élément non texte dans la liste | 400, `{"erreur": "Chaque tweet doit etre une chaine de caracteres."}` |

## Réentraînement automatique

Le modèle est réentraîné chaque semaine avec les données les plus récentes de la table `tweets`.

Le script `reentrainement.sh` relance l'entraînement et garde une trace dans `reentrainement.log`.

Pour automatiser avec cron (tous les lundis à 3h du matin) :

```bash
crontab -e
```

Puis ajouter la ligne :

```
0 3 * * 1 /chemin/vers/Algo-analyse/reentrainement.sh
```

Pour ajouter de nouvelles données annotées avant le réentraînement :

```sql
INSERT INTO tweets (text, positive, negative) VALUES ("nouveau tweet", 1, 0);
```

## Fichiers du projet

| Fichier | Rôle |
|---------|------|
| `app.py` | API Flask avec l'endpoint POST /analyse |
| `bdd.py` | Connexion à MySQL et lecture des tweets |
| `setup_bdd.py` | Création de la base, de la table et insertion des données |
| `entrainement.py` | Entraînement, évaluation et sauvegarde des modèles |
| `reentrainement.sh` | Script de réentraînement pour le cron |
| `rapport/` | Matrices de confusion et rapport d'évaluation |

## Rapport d'évaluation

Le rapport complet (matrices de confusion, précision, rappel, F1-score, analyse et recommandations) se trouve dans `rapport/rapport_evaluation.pdf`.
