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
import record

ACTIONS = {
    'Z': "haut",
    'Q': "gauche",
    'S': "bas",
    'D': "droite",
    'U': "undo",
    'E': "exit",
    'G': "gagne",
    'R': "reset"
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
    """
    Interprete la saisie passé en paramètre selon le tableau MENU

    :param saisie: La saisie de l'utilisateur
    :return: Action à faire
    """
    if saisie[0] == 'P':
        return MENU['PXX']
    else:
        return MENU.get(saisie, None)


def saisie_menu(joueur):
    """
    Demande l'action que l'utilisateur veut entreprendre

    :param joueur: Profil du joueur
    :return: La saisie du joueur sur une forme défini
    """
    saisie = ''

    if joueur["collection"] == "sokoban":
        autre_coll = "novoban"
        autre_c = "cn"
    else:
        autre_coll = "sokoban"
        autre_c = "cs"

    while not (saisie.upper() in MENU.keys() and saisie != ""):
        saisie = input("\n❓Choisir une option du menu parmi :\n\
            1) Lancer le puzzle {} (sS)\n\
            2) Changer de collection ({} pour {})\n\
            3) Changer de puzzle au sein de novoban (pXX avec XX le numéro du puzzle de 1 au dernier niveau débloqué,"
                       "valant actuellement {} (pP)\n\
            4) Charger un puzzle sauvegardé (rR)\n\
            5) Quitter (eE)\n\
            >".format(outil.puzzle_xsb(joueur["collection"], joueur["numero"]), autre_c, autre_coll, joueur["max"]))
        if saisie[0].upper() == 'P' and collection.est_dans_collection(joueur["collection"], outil.parse_pXX(saisie)):
            if outil.parse_pXX(saisie) > joueur["max"] or outil.parse_pXX(saisie) < 1:
                saisie = ''
            else:
                return saisie.upper()

    return saisie.upper()


def affiche_stat_partie(joueur):
    """
    Permet d'afficher les stat de la partie du joueur et si il y record ou pas

    :param joueur: Dictionnaire contenant le profil du joueur
    :return: Rien
    """
    pseudo = joueur["pseudo"]
    coll = joueur["collection"]
    numero = joueur["numero"]
    score = joueur["score"]

    stat = record.get_stat_partie(pseudo, coll, numero, score)
    if record.est_record_jeu(coll, numero, score):
        print(stat, ">> Nouveau record ! <<")
    elif record.est_meilleur_score_joueur(pseudo, coll, numero, score):
        print(stat, ">> Nouveau record personnel ! <<")
    else:
        print(stat)


def affiche_header(joueur):
    """
    Affiche les infos sur le puzzle et les records au-dessus du puzzle

    :param joueur: Dictionnaire avec les infos du joueur
    :return: Le header
    """

    pseudo = joueur["pseudo"]
    coll = joueur["collection"]
    numero = joueur["numero"]
    score = joueur["score"]

    record_joueur = record.meilleur_score_joueur(pseudo, coll, numero)
    record_puzzle = record.record_jeu(coll, numero)
    puzzle = outil.puzzle_xsb(coll, numero)

    header = "{} | {} déplacements".format(puzzle, score)

    if record_joueur is not None :
        header += " | Record joueur : {}".format(record_joueur)
    if record_puzzle is not None:
        header += " - Record du puzzle : {} ({}) ".format(record_puzzle[1], record_puzzle[0])

    print(header)
    return header
