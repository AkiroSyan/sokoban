# coding: UTF-8
"""
Script: sokoban/record
Auteur: girartim
Date: 19/03/2018
"""

import os
import outil
import collection


# Fonctions
def record_jeu(collec, numero):
    chemin = "sauvegardes/records.txt"
    if os.path.isfile(chemin):
        if collection.est_dans_collection(collec, numero):
            with open(chemin, 'r', encoding="UTF-8") as fd:
                for ligne in fd.readlines():
                    if outil.puzzle_xsb(collec, numero) in ligne:
                        liste = ligne.split(';')
                        record = [liste[2][:-1], int(liste[1])]
                        return record


def est_record_jeu(collec, numero, score):
    record = record_jeu(collec, numero)
    if score > record[1]:
        return False
    else:
        return True


def sauv_record_jeu(pseudo, collec, numero, score):
    ajout = outil.puzzle_xsb(collec, numero) + ';' + str(score) + pseudo
    if os.path.isfile("sauvegardes/records.txt"):
        with open("sauvegardes/records.txt", 'r', encoding='UTF-8') as fr:
            temp = fr.readlines()
        if outil.puzzle_xsb(collec, numero) not in temp:
            temp.append(ajout)
            return True
        else :
            i = temp.index(outil.puzzle_xsb(collec, numero))
            pass
    else:
        with open("sauvegardes/records.txt", 'w', encoding='UTF-8') as fw:
            fw.write(ajout)
            return True

# Programme principal
def main():
    pass


if __name__ == '__main__':
    main()
