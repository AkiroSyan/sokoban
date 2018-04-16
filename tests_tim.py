# coding: UTF-8
"""
Script: sokoban/tests_tim.py
Auteur: girartim
Date: 19/03/2018
"""

# Fonctions
import outil
import terminal
import pickle
import os
import puzzle
import collection


# Programme principal
def main():
    j = outil.init_joueur()
    print(terminal.saisie_menu(j))


if __name__ == '__main__':
    main()
