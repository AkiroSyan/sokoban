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


# Fonctions
def partie(joueur, entrepot):
    """
    Démarre une partie avec un joueur sur un entrepôt passés en paramètres
    :param joueur: Joueur avec lequel jouer
    :param entrepot: Entrepôt sur lequel jouer
    :return: None
    """
    while not puzzle.gagne(entrepot):
        terminal.affiche_entrepot_couleur(entrepot)
        action = terminal.saisie_action()
        intp = terminal.interprete_action(action)
        res = False

        if intp in ['gauche', 'droite', 'haut', 'bas']:
            res = puzzle.deplace(entrepot, intp)
        if intp == "exit":
            break

        print("score:", joueur['score'])

    terminal.affiche_entrepot_couleur(entrepot)


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
        if action == 'start':
            entrepot = collection.charge_puzzle(joueur["collection"], joueur["numero"])
            partie(joueur, entrepot)


if __name__ == '__main__':
    main()
