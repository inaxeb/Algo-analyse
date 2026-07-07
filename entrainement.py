import os
import re
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from bdd import recuperer_tweets

DOSSIER = os.path.dirname(os.path.abspath(__file__))

stopwords_francais = [
    "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au",
    "aux", "avec", "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais",
    "ou", "donc", "ni", "car", "ne", "que", "qui", "quoi", "quand", "à", "son",
    "sa", "ses", "ils", "elles", "nous", "vous", "est", "sont", "cette", "cet",
    "aussi", "être", "avoir", "faire", "comme", "tout", "on", "lui", "je", "tu",
    "il", "elle", "suis", "es", "mon", "ma", "mes", "ton", "ta", "tes", "se",
]


def nettoyer(texte):
    texte = texte.lower()
    texte = re.sub(r"[^\w\s]", "", texte)
    return texte


def entrainer():
    lignes = recuperer_tweets()
    textes = [nettoyer(ligne[0]) for ligne in lignes]
    labels_positifs = [ligne[1] for ligne in lignes]
    labels_negatifs = [ligne[2] for ligne in lignes]

    vectorizer = CountVectorizer(stop_words=stopwords_francais)
    X = vectorizer.fit_transform(textes)

    # Classe globale de chaque tweet (positif, negatif ou neutre)
    # pour garder les memes proportions dans le train et le test.
    classes = []
    for i in range(len(lignes)):
        if labels_positifs[i] == 1:
            classes.append("positif")
        elif labels_negatifs[i] == 1:
            classes.append("negatif")
        else:
            classes.append("neutre")

    X_train, X_test, yp_train, yp_test, yn_train, yn_test = train_test_split(
        X, labels_positifs, labels_negatifs,
        test_size=0.25, random_state=42, stratify=classes
    )

    modele_positif = LogisticRegression(C=5.0)
    modele_positif.fit(X_train, yp_train)

    modele_negatif = LogisticRegression(C=5.0)
    modele_negatif.fit(X_train, yn_train)
    yp_pred = modele_positif.predict(X_test)
    yn_pred = modele_negatif.predict(X_test)

    # Une fois l'evaluation faite, on reentraine sur toutes les donnees
    # pour que le modele final soit le plus complet possible.
    modele_positif_final = LogisticRegression(C=5.0)
    modele_positif_final.fit(X, labels_positifs)

    modele_negatif_final = LogisticRegression(C=5.0)
    modele_negatif_final.fit(X, labels_negatifs)

    os.makedirs(os.path.join(DOSSIER, "modele"), exist_ok=True)
    joblib.dump(vectorizer, os.path.join(DOSSIER, "modele", "vectorizer.joblib"))
    joblib.dump(modele_positif_final, os.path.join(DOSSIER, "modele", "modele_positif.joblib"))
    joblib.dump(modele_negatif_final, os.path.join(DOSSIER, "modele", "modele_negatif.joblib"))

    os.makedirs(os.path.join(DOSSIER, "rapport"), exist_ok=True)

    print("Rapport de classification (positif) :")
    print(classification_report(yp_test, yp_pred, zero_division=0))
    print("Matrice de confusion (positif) :")
    print(confusion_matrix(yp_test, yp_pred))

    print("Rapport de classification (negatif) :")
    print(classification_report(yn_test, yn_pred, zero_division=0))
    print("Matrice de confusion (negatif) :")
    print(confusion_matrix(yn_test, yn_pred))

    figure = ConfusionMatrixDisplay(confusion_matrix(yp_test, yp_pred))
    figure.plot(cmap="Greens")
    plt.title("Matrice de confusion - predictions positives")
    plt.savefig(os.path.join(DOSSIER, "rapport", "matrice_positive.png"))
    plt.close()

    figure = ConfusionMatrixDisplay(confusion_matrix(yn_test, yn_pred))
    figure.plot(cmap="Reds")
    plt.title("Matrice de confusion - predictions negatives")
    plt.savefig(os.path.join(DOSSIER, "rapport", "matrice_negative.png"))
    plt.close()

    print("Modeles sauvegardes dans le dossier modele/")
    print("Matrices de confusion sauvegardees dans le dossier rapport/")


if __name__ == "__main__":
    entrainer()
