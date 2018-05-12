#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
Auteur: girartim
Date: 19/03/2018
"""

import string
import os

BLOCS = {
    "mur": '#',
    "cible": '.',
    "caisse": '$',
    "caisse sur cible": '*',
    "gardien": '@',
    "gardien sur cible": '+',
    "vide": ' ',
}


# Fonctions
def init_entrepot():
    """
    Initialisation de l'entrepot.

    :return: Liste contenant l'entrepot
    """
    return [['#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', ' ', '$', ' ', '.', '#'],
            ['#', ' ', '$', '@', '$', ' ', '#'],
            ['#', '.', ' ', '$', ' ', '.', '#'],
            ['#', '#', '#', '#', '#', '#', '#']]


def init_joueur():
    """
    Créer le dictionnaire correspondant à un joueur

    :return: le dictionnaire joueur modélisant le joueur et sa partie
    """
    return {"pseudo": "crazy",  # le joueur s'appelle crazy
            "collection": "novoban",  # il joue actuellement avec la collection novoban
            "numero": 5,  # sur le puzzle novoban05.xsb
            "max": 8,  # il a déjà résolu tous les puzzles de novoban01.xsb à novoban07.xsb,
            # il peut jouer à novoban08.xsb mais ne l'a pas encore résolu
            "score": 0,  # il atteint pour l'instant un score de 0
            "historique": []  # il n'a pas encore d'éléments chargés dans l'historique
            }


def puzzle_xsb(collection, numero):
    """
    Permet d'avoir le nom du fichier puzzle à partir des paramètres entrés. Le numéro doit etre inférieur à 99.

    :param collection: Nom de la collection dans laquelle le puzzle est présent
    :param numero: Numéro du puzzle dans la collection
    :return: le nom du fichier .xbs
    """
    if numero > 99:
        return
    puzzle = str(collection) + "{:02}".format(numero) + ".xsb"
    return str(puzzle)


def chemin_puzzle(collection, numero):
    """
    Permet d'avoir le chemin d'acces au fichier puzzle dont les caractéristiques sont donnés en paramètre.

    :param collection: Nom de la collection dans laquelle le puzzle est présent
    :param numero: Numéro du puzzle dans la collection
    :return: Le chemin d'accès au fichier .xbs si le fichier existe ou None
    """
    if puzzle_xsb(collection, numero) is not None:
        chemin = os.path.join("collections", str(collection), puzzle_xsb(collection, numero))
        return chemin


def coords(entrepot):
    """
    Cherche les coordonées du joueur dans l'entrepot

    :param entrepot: Li liste contenant le puzzle
    :return: liste de coordonnées du joueur
    """
    x = 0
    y = 0
    for ligne in entrepot:
        if '@' in ligne:
            y = ''.join(ligne).find('@')
            break
        elif '+' in ligne:
            y = ''.join(ligne).find('+')
            break
        else:
            x += 1
    return [x, y]  # Programme principal


def coords_deplacees(c, direction):
    """
    Permet d'avoir les nouveaux coordonnées du gardien

    :param c: liste avec les coordonnées du gardien
    :param direction: direction du placement du gardien
    :return: liste avec les nouveaux coordonnées du gardien
    """
    if direction == 'haut':
        c[0] -= 1
    elif direction == 'bas':
        c[0] += 1
    elif direction == 'gauche':
        c[1] -= 1
    elif direction == 'droite':
        c[1] += 1
    return c


def parse_pXX(pXX):
    """
    Prends l'entrée de l'utilisateur et donne le numero du puzzle
    :param pXX: entrée de l'utilisateur sous cette forme
    :return: le numéro du puzzle
    """
    if pXX[0].upper() == 'P':
        if len(pXX) == 2:
            if pXX[1] in string.digits:
                return int(pXX[1:])
        if len(pXX) == 3:
            if pXX[1] in string.digits:
                if pXX[2] in string.digits:
                    return int(pXX[1:])
