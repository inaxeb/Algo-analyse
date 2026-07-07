import os
import joblib
from flask import Flask, request, jsonify
from entrainement import nettoyer

DOSSIER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.json.ensure_ascii = False

vectorizer = joblib.load(os.path.join(DOSSIER, "modele", "vectorizer.joblib"))
modele_positif = joblib.load(os.path.join(DOSSIER, "modele", "modele_positif.joblib"))
modele_negatif = joblib.load(os.path.join(DOSSIER, "modele", "modele_negatif.joblib"))


@app.route("/analyse", methods=["POST"])
def analyse():
    donnees = request.get_json(silent=True)

    if donnees is None:
        return jsonify({"erreur": "Le corps de la requete doit etre du JSON."}), 400

    if not isinstance(donnees, list):
        return jsonify({"erreur": "Le JSON doit etre une liste de tweets."}), 400

    if len(donnees) == 0:
        return jsonify({"erreur": "La liste de tweets est vide."}), 400

    for tweet in donnees:
        if not isinstance(tweet, str):
            return jsonify({"erreur": "Chaque tweet doit etre une chaine de caracteres."}), 400

    tweets_propres = [nettoyer(tweet) for tweet in donnees]
    X = vectorizer.transform(tweets_propres)

    proba_positif = modele_positif.predict_proba(X)[:, 1]
    proba_negatif = modele_negatif.predict_proba(X)[:, 1]

    resultat = {}
    for i, tweet in enumerate(donnees):
        score = proba_positif[i] - proba_negatif[i]
        resultat[tweet] = round(float(score), 3)

    return jsonify(resultat)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
