#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
Auteur: remy
Date: 14/03/2018
"""
import outil
import copy


# Fonctions
def gagne(entrepot):
    """
    Vérifie si le puzzle décrit par l”entrepot est résolu ou non (c’est à dire que toutes les caisses ont été placées
    sur des cibles) et renvoie la réponse sous forme booléenne.
    :param entrepot: l'entrepot correspondant à un puzzle
    :return: Le puzzle est-il terminé/résolu ?
    """
    for ligne in entrepot:
        for case in ligne:
            if case == '$':
                return False
    return True


def dimensions(entrepot):
    """
    Retourne une liste contenant la hauteur et la largeur de l'entrepôt

    :param entrepot: Entrepôt dont on cherche les dimensions
    :return: liste contenant respectivement la hauteur et la largeur de l'entrepôt
    """
    largeur = 0
    hauteur = 0
    for ligne in entrepot:
        hauteur += 1
        largeur = max(len(ligne), largeur)
    return [hauteur, largeur]


def incremente_score(joueur, inc):
    """
    Ajoute l'increment au score du joueur

    :param joueur: Nom du joueur
    :param inc: Valeur de lincrément
    :return: Rien
    """
    joueur["score"] += inc


def est_mur(entrepot, c):
    """
    Teste si la case de :entrepot: déterminée par ses coordonnées :c: est un mur

    :param entrepot: Entrepôt à tester
    :param c: Coordonnées de la case à tester
    :return: boolées si la case est un mur ou non, None si la case est en-dehors de l'entrepôt
    """
    return est_qqch(entrepot, c, outil.BLOCS['mur'])


def est_caisse(entrepot, c):
    """
    Teste si la case de :entrepot: déterminée par ses coordonnées :c: est une caisse

    :param entrepot: Entrepôt à tester
    :param c: Coordonnées de la case à tester
    :return: boolées si la case est une caisse ou non, None si la case est en-dehors de l'entrepôt
    """
    return est_qqch(entrepot, c, outil.BLOCS['caisse']) or est_qqch(entrepot, c, outil.BLOCS['caisse sur cible'])


def est_cible(entrepot, c):
    """
    Teste si la case de :entrepot: déterminée par ses coordonnées :c: est une cible

    :param entrepot: Entrepôt à tester
    :param c: Coordonnées de la case à tester
    :return: boolées si la case est une cible ou non, None si la case est en-dehors de l'entrepôt
    """
    return est_qqch(entrepot, c, outil.BLOCS['cible']) or est_qqch(entrepot, c,
                                                                   outil.BLOCS['gardien sur cible']) or est_qqch(
        entrepot, c, outil.BLOCS['caisse sur cible'])


def est_qqch(entrepot, c, qqch):
    """
    Teste si la case de :entrepot: déterminée par ses coordonnées :c: est la même que celle passée
    en paramètre avec :qqch:

    :param entrepot: Entrepôt à tester
    :param c: Coordonnées de la case à tester
    :param qqch: type de case à tester (attend une valeur de type : outil.BLOCS.['type à tester'])
    :return: boolées si la case est du bon type ou non, None si la case est en-dehors de l'entrepôt
    """
    assert qqch in outil.BLOCS.values()

    ligne, col = c
    max_ligne, max_col = dimensions(entrepot)

    if 0 <= ligne < max_ligne and 0 <= col < max_col:
        return entrepot[ligne][col] == qqch


def deplace(entrepot, direction):
    """
    Gère le déplacement de l'entrepôt.

    :param entrepot:
    :param direction:
    :return:
    """
    joueur = outil.coords(entrepot)
    next_c = outil.coords_deplacees(joueur[:], direction)
    beyond = outil.coords_deplacees(next_c[:], direction)

    x, y = joueur
    xn, yn = next_c
    xb, yb = beyond

    if est_caisse(entrepot, next_c):
        if not (est_mur(entrepot, beyond) or est_caisse(entrepot, beyond)):
            # On teste à chaque fois si on a affaire à une cible afin de remplacer par la bonne case
            entrepot[x][y] = outil.BLOCS['cible'] if est_cible(entrepot, joueur) else outil.BLOCS['vide']
            entrepot[xn][yn] = outil.BLOCS['gardien sur cible'] if est_cible(entrepot, next_c) \
                else outil.BLOCS['gardien']
            entrepot[xb][yb] = outil.BLOCS['caisse sur cible'] if est_cible(entrepot, beyond) \
                else outil.BLOCS['caisse']
            return True
    elif not est_mur(entrepot, next_c):
        entrepot[x][y] = outil.BLOCS['cible'] if est_cible(entrepot, joueur) else outil.BLOCS['vide']
        entrepot[xn][yn] = outil.BLOCS['gardien sur cible'] if est_cible(entrepot, next_c) \
            else outil.BLOCS['gardien']
        return True
    return False


def sauv_historique(joueur, entrepot):
    """
    Ajoute l'etat de l'entrepot à l'historique

    :param joueur: Nom du joueur (profil)
    :param entrepot: l'entrepot à ajouter à l'historique
    :return : Rien
    """
    joueur["historique"].append(copy.deepcopy(entrepot))


def undo(joueur):
    """
    Fait un retour arrière dans l'etat du puzzle en incrementant le score

    :param joueur: Nom du joueur
    :return: L'entrepot à l'état precedent
    """
    if len(joueur["historique"]) == 1:
        return copy.deepcopy(joueur["historique"][0])
    else:
        joueur["historique"].pop()
        incremente_score(joueur, 1)
        return copy.deepcopy(joueur["historique"][-1])


def reset(joueur):
    """
    Redemarre le puzzle

    :param joueur: Nom du joueur
    :return: Le puzzle à l'état initial
    """
    joueur["score"] = 0
    joueur["historique"] = copy.deepcopy(joueur["historique"][:1])
    return copy.deepcopy(joueur["historique"][0])


def version_gagnante(entrepot):
    for l, ligne in enumerate(entrepot):
        for c, case in enumerate(ligne):
            if case in [outil.BLOCS["cible"], outil.BLOCS["gardien sur cible"]]:
                entrepot[l][c] = outil.BLOCS["caisse sur cible"]
            if case == outil.BLOCS["caisse"]:
                entrepot[l][c] = outil.BLOCS["vide"]

    return entrepot
