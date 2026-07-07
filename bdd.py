import mysql.connector

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "socialmetrics",
}


def connexion():
    return mysql.connector.connect(**CONFIG)


def recuperer_tweets():
    conn = connexion()
    curseur = conn.cursor()
    curseur.execute("SELECT text, positive, negative FROM tweets")
    lignes = curseur.fetchall()
    curseur.close()
    conn.close()
    return lignes
