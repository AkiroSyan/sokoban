# coding: UTF-8
"""
Script: sokoban/collection
Auteur: girartim
Date: 19/03/2018
"""

import outil
import os
import pickle


# Fonctions

def dimensions(fichier):
    """
    Permet d'avoir les dimensions d'un puzzle passé en paramètre.
    :param fichier: chemin du fichier à analyser
    :return: Une liste avec la hauteur et la largeur
    """
    assert fichier is not None, "le fichier spécifié ne peux pas être None"

    if os.path.isfile(fichier):
        with open(fichier, 'r', encoding="UTF-8") as fd:
            largeur = 0
            hauteur = 0
            for ligne in fd.readlines():
                if ':' not in ligne:
                    hauteur += 1
                    largeur = max(len(ligne[:-1]), largeur)
        return [hauteur, largeur]


def est_dans_collection(collection, numero):
    """
    Teste si le puzzle dont le :numero: est fourni en paramètre fait partie de la collection
    dont le nom est donné dans le paramètre :collection:
    :param collection: Nom de la collection considérée
    :param numero: Numéro du puzzle recherché dans la collection
    :return: Booléen : le puzzle est-il dans la collection ?
    """
    puzzle = outil.puzzle_xsb(collection, numero)
    return os.path.isfile(f"collections/{collection}/{puzzle}")


def nbre_puzzle(collection):
    """
    Détermine le nombre de puzzles existant dans une :collection: dont le nom est fourni en paramètre.
    :param collection: Collection considérée
    :return: Nombre de puzzles dans la collection
    """

    collpath = f"collections/{collection}/"

    if os.path.isdir(collpath):
        return len(os.listdir(collpath))
    else:
        return 0


def debloque_niveau(joueur):
    """

    :param joueur:
    :return:
    """

    max_puzzle = nbre_puzzle(joueur["collection"])
    if joueur["max"] < max_puzzle:
        joueur["max"] += 1
        return True

    return False


def charge_puzzle(collection, numero):
    """
    Permet de creer une liste 2D correspondant à un puzzle donc la collection et le nom
    sont placés en paramètre.
    :param collection: Nom de la collection du puzzle à charger
    :param numero: Numéro du puzzle
    :return: Liste 2D contenant le puzzle. Non si le puzzle n'existe pas
    """
    chemin = outil.chemin_puzzle(collection, numero)
    puzzle = []

    if chemin is not None and os.path.isfile(chemin):
        with open(chemin, 'r', encoding="UTF-8") as fd:
            taille = dimensions(chemin)
            for ligne in fd.readlines():
                if ':' not in ligne:
                    puzzle.append(list("{:{largeur}}".format(ligne[:-1], largeur=taille[1])))
        return puzzle


def init_nouveau_joueur(pseudo):
    """
    Creation d'un nouveu profil de joueur
    :param pseudo: Nom du joueur
    :return: Dictionnaire avec les infos du joueur
    """
    return {"pseudo": pseudo,
            "collection": "novoban",
            "numero": 1,
            "max": 1,
            "score": 0,
            "historique": []
            }


def sauve_contexte(joueur):
    """
    Permet de faire une sauvegarde du profile du joueur
    :param joueur: Dictionnaire représentant le joueur
    :return: Si la sauvegarde à bien été effectué en booléen
    """
    pseudo = joueur["pseudo"]

    with open(f"sauvegardes/{pseudo}.save", "wb") as save:
        pickle.dump(joueur, save)
    with open(f"sauvegardes/{pseudo}.save", "rb") as test:
        return pickle.load(test, encoding="UTF-8") == joueur


def charge_contexte(pseudo):
    """
    Charge l'état de la partie sauvegarder pour le profil pseudo
    Ou créer un nouveau profil si le profil n'existe pas
    :param pseudo: nom du joueur
    :return: Dictionnaire contenant les infos du joueur
    """
    chemin = "sauvegardes/" + str(pseudo) + ".save"
    if os.path.isfile(chemin):
        with open(chemin, "rb") as save:
            return pickle.load(save, encoding="UTF-8")
    else:
        return init_nouveau_joueur(pseudo)
