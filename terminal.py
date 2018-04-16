#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
Auteur: girartim
Date: 19/03/2018
"""

import colorama
import outil
import collection

ACTIONS = {
    'Z': "haut",
    'Q': "gauche",
    'S': "bas",
    'D': "droite",
    'U': "undo",
    'E': "exit",
    'G': "gagne"
}

MENU = {
    'S': "start",
    'CN': "novoban",
    'CS': "sokoban",
    'PXX': "puzzle",
    'R': "reload",
    'E': "exit"
}


def affiche_entrepot(entrepot):
    """
    Affiche sur la console l'entrepôt passé en paramètre
    :param entrepot: entrepot à afficher
    :return: None
    """
    for ligne in entrepot:
        for case in ligne:
            print(case, end="")
        print()


def affiche_entrepot_couleur(entrepot):
    """
    Affiche en couleur sur la console l'entrepôt passé en paramètre
    :param entrepot: entrepot à afficher
    :return: None
    """
    couleurs = {
        outil.BLOCS['mur']: colorama.Fore.WHITE,  # mur
        outil.BLOCS['cible']: colorama.Fore.CYAN,  # cible
        outil.BLOCS['caisse']: colorama.Fore.GREEN,  # caisse
        outil.BLOCS['caisse sur cible']: colorama.Fore.YELLOW,  # caisse sur cible
        outil.BLOCS['gardien']: colorama.Fore.MAGENTA,  # gardien
        outil.BLOCS['gardien sur cible']: colorama.Fore.BLUE,  # gardien sur cible
        outil.BLOCS['vide']: colorama.Fore.RESET,
    }

    for ligne in entrepot:
        for case in ligne:
            print(couleurs[case], case, colorama.Fore.RESET, end="")
        print()


def saisie_action():
    """
    Demande à l'utilisateur la saisie d'une action
    :return: L'action choisie par l'utilisateur
    """
    saisie = "X"

    while not (saisie.upper() in ACTIONS.keys() and saisie != ""):
        print("\n❓Saisissez une action parmi :\n\
        1) [ZQSD] Déplacement - [U]ndo - [R]eset - [E]xit\n\
        2) (debug) [G]agne")

        saisie = input("> ")

    return saisie.upper()


def interprete_action(action):
    """
    Interprète l'action passée en paramètre selon le tableau de correspondance ACTIONS
    :param action: caractère à interpréter
    :return: action interprétée
    """
    return ACTIONS.get(action, None)


def saisie_pseudo():
    """
    Demmande le pseudo du joueur. Met le pseudo 'crazy' si rien n'est entré
    :return: Le pseudo
    """
    pseudo = -1
    while not (isinstance(pseudo, str) and pseudo != 'records'):
        pseudo = input("Pseudo : ")
    if pseudo == '':
        pseudo = 'crazy'
    return pseudo


def interprete_menu(saisie):
    if saisie[0] == 'P':
        return MENU['PXX']
    else:
        return MENU.get(saisie, None)


def saisie_menu(joueur):
    saisie = ''

    while not (saisie.upper() in MENU.keys() and saisie != ""):
        print("\n❓Choisir une option du menu parmi :\n\
            1) Lancer le puzzle {} (sS)\n\
            2) Changer de collection (cs pour sokoban)\n\
            3) Changer de puzzle au sein de novoban (pXX avec XX le numéro du puzzle de 1 au dernier niveau débloqué,"
              "valant actuellement {} (pP)\n\
            4) Recherger un puzzle sauvegardé (rR)\n\
            5) Quitter (eE)\n\ ".format(outil.puzzle_xsb(joueur["collection"], joueur["numero"]), joueur["max"]))
        saisie = input("> ")
        if saisie[0] == 'p' and collection.est_dans_collection(joueur["collection"], outil.parse_pXX(saisie)):
            if outil.parse_pXX(saisie) > joueur["max"] or outil.parse_pXX(saisie) < 1:
                saisie = ''
            else:
                return saisie.upper()

    return saisie.upper()


# Programme principal
def main():
    pass


if __name__ == '__main__':
    main()
