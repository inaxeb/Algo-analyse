import mysql.connector

tweets = [
    ("J'adore ce nouveau téléphone, il est incroyable !", 1, 0),
    ("Superbe journée, je suis trop content !", 1, 0),
    ("Merci pour ce service client au top, très réactif.", 1, 0),
    ("Ce film était magnifique, je le recommande à tous.", 1, 0),
    ("Excellente nouvelle, notre équipe a gagné !", 1, 0),
    ("Je suis fier de ce qu'on a accompli ensemble, bravo.", 1, 0),
    ("Quel plaisir de retrouver mes amis ce weekend, c'était génial.", 1, 0),
    ("Bravo pour cette mise à jour, tout marche parfaitement.", 1, 0),
    ("Ce restaurant est une pépite, on s'est régalés, excellent.", 1, 0),
    ("La livraison est arrivée en avance, super expérience.", 1, 0),
    ("J'aime beaucoup cette chanson, elle me met de bonne humeur.", 1, 0),
    ("Très bonne conférence, j'ai appris plein de choses, merci.", 1, 0),
    ("Le concert était génial, une soirée inoubliable.", 1, 0),
    ("Enfin en vacances, le bonheur total !", 1, 0),
    ("Ce livre est passionnant, je le recommande vraiment.", 1, 0),
    ("Félicitations à toute l'équipe pour ce magnifique succès.", 1, 0),
    ("L'application est fluide et agréable, bravo aux développeurs.", 1, 0),
    ("Magnifique coucher de soleil ce soir, quel bonheur.", 1, 0),
    ("Trop heureux de mon nouveau travail, l'ambiance est top.", 1, 0),
    ("Un grand merci pour votre aide, vous êtes formidables.", 1, 0),
    ("Ce téléphone est excellent, je l'adore.", 1, 0),
    ("Journée parfaite, tout s'est super bien passé.", 1, 0),
    ("Le service était impeccable, merci beaucoup.", 1, 0),
    ("Film incroyable, j'ai adoré du début à la fin.", 1, 0),
    ("Très content de ma commande, qualité au top.", 1, 0),
    ("Quelle bonne surprise, ce restaurant est excellent.", 1, 0),
    ("Super concert hier soir, c'était magique.", 1, 0),
    ("J'adore cette application, elle est parfaite.", 1, 0),
    ("Merci pour cette super soirée, c'était génial.", 1, 0),
    ("Bravo, ce tutoriel est excellent et très clair.", 1, 0),
    ("Les vacances étaient parfaites, je suis ravi.", 1, 0),
    ("Ce livre est génial, une très belle découverte.", 1, 0),
    ("Équipe au top, victoire méritée, bravo !", 1, 0),
    ("Je recommande ce produit, il est parfait.", 1, 0),
    ("Magnifique spectacle, merci pour ce moment.", 1, 0),
    ("Très bon accueil, personnel adorable, parfait.", 1, 0),
    ("Cette chanson est superbe, je l'écoute en boucle.", 1, 0),
    ("Content du résultat, le travail est excellent.", 1, 0),
    ("Quel plaisir, la qualité est vraiment au rendez-vous.", 1, 0),
    ("Génial, la mise à jour apporte plein de bonnes choses.", 1, 0),
    ("Je déteste ce téléphone, il bug tout le temps.", 0, 1),
    ("Quelle journée horrible, tout va mal.", 0, 1),
    ("Service client catastrophique, personne ne répond.", 0, 1),
    ("Ce film était nul, j'ai perdu mon temps.", 0, 1),
    ("Très déçu par cette défaite, c'est rageant.", 0, 1),
    ("J'en ai marre de ces pannes à répétition, c'est nul.", 0, 1),
    ("Le pire restaurant de ma vie, à fuir absolument.", 0, 1),
    ("Cette mise à jour a tout cassé, c'est inadmissible.", 0, 1),
    ("Livraison en retard et colis abîmé, lamentable.", 0, 1),
    ("Je suis furieux, on m'a encore annulé mon rendez-vous.", 0, 1),
    ("Cette chanson est insupportable, quelle horreur.", 0, 1),
    ("Conférence ennuyeuse et nulle, je me suis endormi.", 0, 1),
    ("Le concert était une arnaque, son horrible.", 0, 1),
    ("Les vacances sont gâchées, il pleut tous les jours.", 0, 1),
    ("Ce livre est d'un ennui mortel, je l'ai abandonné.", 0, 1),
    ("Échec total du projet, tout est à refaire, c'est rageant.", 0, 1),
    ("L'application plante sans arrêt, c'est insupportable.", 0, 1),
    ("Quel temps affreux, ça me déprime.", 0, 1),
    ("Je hais les transports en commun, encore en grève.", 0, 1),
    ("Nul, décevant et hors de prix, à éviter.", 0, 1),
    ("Ce téléphone est nul, je regrette mon achat.", 0, 1),
    ("Journée catastrophique, rien ne marche.", 0, 1),
    ("Le service était lamentable, je suis très déçu.", 0, 1),
    ("Film ennuyeux et décevant, à éviter.", 0, 1),
    ("Commande jamais reçue, service catastrophique.", 0, 1),
    ("Ce restaurant était horrible, plats froids et service nul.", 0, 1),
    ("Concert décevant, le son était une horreur.", 0, 1),
    ("Cette application est nulle, elle plante sans arrêt.", 0, 1),
    ("Soirée gâchée, quelle horrible ambiance.", 0, 1),
    ("Ce tutoriel est nul, on ne comprend rien.", 0, 1),
    ("Vacances horribles, hôtel sale et personnel désagréable.", 0, 1),
    ("Livre décevant, l'histoire est nulle et ennuyeuse.", 0, 1),
    ("Défaite honteuse, l'équipe était lamentable.", 0, 1),
    ("Produit décevant, je déconseille fortement.", 0, 1),
    ("Spectacle raté, on s'est ennuyés du début à la fin.", 0, 1),
    ("Accueil désagréable, personnel odieux, à fuir.", 0, 1),
    ("Cette chanson est nulle, insupportable à écouter.", 0, 1),
    ("Déçu du résultat, le travail est bâclé.", 0, 1),
    ("Quelle arnaque, la qualité est déplorable.", 0, 1),
    ("Horrible, la mise à jour a tout détruit.", 0, 1),
    ("Le train part à 8h demain matin.", 0, 0),
    ("La réunion est prévue jeudi à 14h.", 0, 0),
    ("Il y a du monde dans le centre-ville aujourd'hui.", 0, 0),
    ("Le magasin ouvre à 9h et ferme à 19h.", 0, 0),
    ("J'ai acheté du pain en rentrant du travail.", 0, 0),
    ("Le nouveau modèle sort le mois prochain.", 0, 0),
    ("La météo annonce des nuages pour demain.", 0, 0),
    ("Je regarde la télé en mangeant.", 0, 0),
    ("Le bus numéro 12 passe par la gare.", 0, 0),
    ("La piscine est fermée le lundi.", 0, 0),
    ("Le colis doit arriver dans la semaine.", 0, 0),
    ("La vidéo dure une vingtaine de minutes.", 0, 0),
    ("Le match commence à 21h ce soir.", 0, 0),
    ("J'ai rendez-vous chez le dentiste mardi.", 0, 0),
    ("Le prix du billet est de quinze euros.", 0, 0),
    ("La boulangerie se trouve au coin de la rue.", 0, 0),
    ("Il reste trois places pour la séance de 20h.", 0, 0),
    ("Le document fait une dizaine de pages.", 0, 0),
    ("La mise à jour sera disponible la semaine prochaine.", 0, 0),
    ("Le musée est ouvert du mardi au dimanche.", 0, 0),
]

conn = mysql.connector.connect(host="localhost", user="root", password="")
curseur = conn.cursor()

curseur.execute("CREATE DATABASE IF NOT EXISTS socialmetrics")
curseur.execute("USE socialmetrics")

curseur.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive TINYINT NOT NULL,
    negative TINYINT NOT NULL
)
""")

curseur.execute("SELECT COUNT(*) FROM tweets")
nombre = curseur.fetchone()[0]

if nombre == 0:
    curseur.executemany(
        "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
        tweets,
    )
    conn.commit()
    print(len(tweets), "tweets inseres dans la table.")
else:
    print("La table contient deja", nombre, "tweets, aucune insertion.")

curseur.close()
conn.close()
print("Base de donnees prete.")
