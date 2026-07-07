import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from bdd import recuperer_tweets
from entrainement import nettoyer, stopwords_francais

DOSSIER = os.path.dirname(os.path.abspath(__file__))

lignes = recuperer_tweets()
textes = [nettoyer(ligne[0]) for ligne in lignes]
labels_positifs = [ligne[1] for ligne in lignes]
labels_negatifs = [ligne[2] for ligne in lignes]

classes = []
for i in range(len(lignes)):
    if labels_positifs[i] == 1:
        classes.append("positif")
    elif labels_negatifs[i] == 1:
        classes.append("negatif")
    else:
        classes.append("neutre")

vectorizer = CountVectorizer(stop_words=stopwords_francais)
X = vectorizer.fit_transform(textes)

X_train, X_test, yp_train, yp_test, yn_train, yn_test = train_test_split(
    X, labels_positifs, labels_negatifs,
    test_size=0.25, random_state=42, stratify=classes
)

modele_positif = LogisticRegression(C=5.0)
modele_positif.fit(X_train, yp_train)
yp_pred = modele_positif.predict(X_test)

modele_negatif = LogisticRegression(C=5.0)
modele_negatif.fit(X_train, yn_train)
yn_pred = modele_negatif.predict(X_test)

mc_pos = confusion_matrix(yp_test, yp_pred)
mc_neg = confusion_matrix(yn_test, yn_pred)

styles = getSampleStyleSheet()
doc = SimpleDocTemplate(os.path.join(DOSSIER, "rapport", "rapport_evaluation.pdf"), pagesize=A4)
contenu = []

contenu.append(Paragraph("Rapport d'évaluation du modèle d'analyse de sentiments", styles["Title"]))
contenu.append(Spacer(1, 12))

contenu.append(Paragraph(
    "Ce rapport présente les performances du prototype développé pour SocialMetrics AI. "
    "Le système repose sur deux régressions logistiques entraînées sur les tweets annotés "
    "de la table tweets : un modèle prédit si un tweet est positif, l'autre s'il est négatif. "
    "Le jeu de données contient " + str(len(lignes)) + " tweets annotés. "
    "L'évaluation est faite sur 25 pour cent des données, mises de côté pendant l'entraînement.",
    styles["Normal"]))
contenu.append(Spacer(1, 20))

contenu.append(Paragraph("1. Matrice de confusion des prédictions positives", styles["Heading2"]))
contenu.append(Image(os.path.join(DOSSIER, "rapport", "matrice_positive.png"), width=10 * cm, height=7.5 * cm))
contenu.append(Paragraph(
    "Sur les " + str(len(yp_test)) + " tweets de test, le modèle positif classe correctement "
    + str(int(mc_pos[0][0])) + " tweets non positifs et " + str(int(mc_pos[1][1])) + " tweets positifs. "
    "Il ne produit aucune fausse alerte (" + str(int(mc_pos[0][1])) + " faux positif), "
    "mais il manque " + str(int(mc_pos[1][0])) + " tweets réellement positifs, "
    "qu'il classe à tort comme non positifs.",
    styles["Normal"]))
contenu.append(Spacer(1, 20))

contenu.append(Paragraph("2. Matrice de confusion des prédictions négatives", styles["Heading2"]))
contenu.append(Image(os.path.join(DOSSIER, "rapport", "matrice_negative.png"), width=10 * cm, height=7.5 * cm))
contenu.append(Paragraph(
    "Le modèle négatif classe correctement " + str(int(mc_neg[0][0])) + " tweets non négatifs et "
    + str(int(mc_neg[1][1])) + " tweets négatifs. "
    "Il produit " + str(int(mc_neg[0][1])) + " fausse alerte et manque "
    + str(int(mc_neg[1][0])) + " tweets réellement négatifs. "
    "Ce modèle est légèrement plus performant que le modèle positif.",
    styles["Normal"]))
contenu.append(Spacer(1, 20))

contenu.append(Paragraph("3. Précision, rappel et F1-score", styles["Heading2"]))

donnees_tableau = [
    ["Modèle", "Accuracy", "Précision", "Rappel", "F1-score"],
    ["Positif",
     str(round(accuracy_score(yp_test, yp_pred), 2)),
     str(round(precision_score(yp_test, yp_pred), 2)),
     str(round(recall_score(yp_test, yp_pred), 2)),
     str(round(f1_score(yp_test, yp_pred), 2))],
    ["Négatif",
     str(round(accuracy_score(yn_test, yn_pred), 2)),
     str(round(precision_score(yn_test, yn_pred), 2)),
     str(round(recall_score(yn_test, yn_pred), 2)),
     str(round(f1_score(yn_test, yn_pred), 2))],
]

tableau = Table(donnees_tableau, colWidths=[3 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm])
tableau.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
]))
contenu.append(tableau)
contenu.append(Spacer(1, 12))

contenu.append(Paragraph(
    "La précision de 1.00 signifie que lorsqu'un modèle signale un sentiment, il ne se trompe presque jamais. "
    "En revanche, le rappel plus faible (0.50 pour le positif, 0.70 pour le négatif) montre que les modèles "
    "laissent passer une partie des tweets qu'ils devraient détecter. Les modèles sont donc prudents : "
    "ils préfèrent ne rien signaler plutôt que de se tromper.",
    styles["Normal"]))
contenu.append(Spacer(1, 20))

contenu.append(Paragraph("4. Analyse des performances et biais observés", styles["Heading2"]))
contenu.append(Paragraph(
    "Forces : l'API répond correctement sur des exemples clairs. Un tweet très positif obtient un score "
    "proche de 1, un tweet très négatif un score proche de -1 et un tweet neutre un score proche de 0. "
    "Aucune fausse alerte n'est produite sur le jeu de test.",
    styles["Normal"]))
contenu.append(Spacer(1, 8))
contenu.append(Paragraph(
    "Faiblesses : le jeu de données est très petit (une centaine de tweets), donc le vocabulaire connu du "
    "modèle est limité. Un tweet exprimé avec des mots absents du jeu d'entraînement obtient un score proche "
    "de 0 même s'il est très marqué. Le rappel reste faible, une partie des sentiments n'est pas détectée.",
    styles["Normal"]))
contenu.append(Spacer(1, 8))
contenu.append(Paragraph(
    "Biais observés : le modèle s'appuie sur des mots isolés (sac de mots). Il ne comprend ni la négation "
    "(« pas génial » contient le mot génial et peut être vu comme positif), ni l'ironie, ni le contexte. "
    "Les tweets annotés sont synthétiques et bien écrits, alors que les vrais tweets contiennent des fautes, "
    "des abréviations et des emojis que le modèle ne connaît pas.",
    styles["Normal"]))
contenu.append(Spacer(1, 20))

contenu.append(Paragraph("5. Recommandations", styles["Heading2"]))
contenu.append(Paragraph(
    "1. Agrandir fortement le jeu de données avec de vrais tweets annotés par l'équipe de modération, "
    "en visant plusieurs milliers d'exemples.",
    styles["Normal"]))
contenu.append(Paragraph(
    "2. Passer du comptage de mots à une pondération TF-IDF et ajouter des bigrammes pour capturer "
    "des expressions comme « pas génial ».",
    styles["Normal"]))
contenu.append(Paragraph(
    "3. Gérer les emojis et les fautes d'orthographe courantes dans le nettoyage des textes.",
    styles["Normal"]))
contenu.append(Paragraph(
    "4. Suivre les performances après chaque réentraînement hebdomadaire pour vérifier que le modèle "
    "s'améliore avec les nouvelles données.",
    styles["Normal"]))
contenu.append(Paragraph(
    "5. À plus long terme, tester un modèle de langue pré-entraîné en français, plus robuste que le sac de mots.",
    styles["Normal"]))

doc.build(contenu)
print("Rapport genere : rapport/rapport_evaluation.pdf")
