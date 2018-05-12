#! /usr/bin/env python3
# coding: UTF-8
"""
Script: outil.py
Auteur: remy
Date: 14/03/2018
"""
import collection
import outil
import puzzle
import terminal
import record
import os
import copy

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


def set_title(msg):
    # Tell the terminal to change the current title.
    if os.name == "posix" and os.getenv("TERM") in ["xterm", "xterm-256color"]:
        print("\x1B]0;%s\x07" % msg)

# Fonctions
def partie(joueur, entrepot):
    """

    :param joueur:
    :param entrepot:
    :return:
    """

    puzzle.sauv_historique(joueur, entrepot)  # On sauvegarde pour avoir l'état initial dans l'historique

    while not puzzle.gagne(entrepot):
        clear_screen()

        set_title(terminal.affiche_header(joueur))
        terminal.affiche_entrepot_couleur(entrepot)

        action = terminal.saisie_action()
        intp = terminal.interprete_action(action)  # Action interprétée

        if intp == 'gagne':
            entrepot = puzzle.version_gagnante(entrepot)

        if intp in ["gauche", "droite", "haut", "bas"]:
            res = puzzle.deplace(entrepot, intp)
            if res:
                puzzle.incremente_score(joueur, 1)
                puzzle.sauv_historique(joueur, entrepot)
        if intp == "undo":
            entrepot = puzzle.undo(joueur)
        if intp == "reset":
            entrepot = puzzle.reset(joueur)
        if intp == "exit":
            return

        collection.sauve_contexte(joueur)

    pseudo = joueur["pseudo"]
    coll = joueur["collection"]
    numero = joueur["numero"]
    score = joueur["score"]

    joueur["historique"] = list()
    if record.est_meilleur_score_joueur(pseudo, coll, numero, score):
        res = collection.debloque_niveau(joueur)
        if not res:
            print("Niveau maximum atteint dans la collection {}".format(coll))
        else:
            print("Nouveau puzztimle débloqué !")
    record.sauv_meilleur_score_joueur(pseudo, coll, numero, score)
    record.sauv_record_jeu(pseudo, coll, numero, score)
    terminal.affiche_stat_partie(joueur)


# Programme principal
def main():
    pseudo = terminal.saisie_pseudo()
    joueur = collection.charge_contexte(pseudo)

    action = ""

    while not action == "exit":
        saisie = terminal.saisie_menu(joueur)
        action = terminal.interprete_menu(saisie)

        if action == 'puzzle':
            nb = outil.parse_pXX(saisie)
            joueur["numero"] = nb
            joueur["historique"] = list()

        if action in ['sokoban', 'novoban']:
            collection.change_collection(joueur, action)

        if action == 'start':
            joueur["historique"] = list()
            joueur["score"] = 0
            entrepot = collection.charge_puzzle(joueur["collection"], joueur["numero"])
            partie(joueur, entrepot)

        if action == 'reload':
            if len(joueur["historique"]) > 0:
                print("on peut jouer tmtc")
                entrepot = joueur["historique"][-1]
                partie(joueur, entrepot)
            else:
                print("Pas de partie sauvegardée")


if __name__ == '__main__':
    main()
