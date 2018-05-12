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
    """
    Extrait le record sur un puzzle donné

    :param collec: collection du puzzle à tester
    :param numero: numero du puzzle à tester
    :return: un dictionnaire [pseudo, record]
    """
    chemin = os.path.join("sauvegardes", "records.txt")
    if os.path.isfile(chemin):
        if collection.est_dans_collection(collec, numero):
            with open(chemin, 'r', encoding="UTF-8") as fd:
                for ligne in fd.readlines():
                    if outil.puzzle_xsb(collec, numero) in ligne:
                        liste = ligne.split(';')
                        record = [liste[2][:-1], int(liste[1])]
                        return record


def est_record_jeu(collec, numero, score):
    """
    Teste si les parametres sont un record ou pas

    :param collec: collection du puzzle
    :param numero:  numero du puzzle
    :param score: score du joueur
    :return: True si record ou False
    """
    record = record_jeu(collec, numero)
    if record is None:
        return True
    if score > record[1]:
        return False
    else:
        return True


def sauv_record_jeu(pseudo, collec, numero, score):
    """
    Sauvegarde le nouveau record dans le fichier de record.

    :param pseudo: Pseudo du joueur ayant réalisé le nouveau record
    :param collec: Collection du puzzle sur lequel il y a eu un nouveau record
    :param numero: Numero du puzzle sur lequel il y a un nouveau record
    :param score: Score du nouveau record
    :return: True si la sauvegarde a été effectué sinon False
    """
    ligne = outil.puzzle_xsb(collec, numero) + ';' + str(score) + ';' + pseudo + '\n'
    chemin = os.path.join("sauvegardes", "records.txt")
    if os.path.isfile(chemin):

        with open(chemin, 'r', encoding='UTF-8') as fr:
            contenu_record = fr.readlines()
        temp = ''.join(contenu_record)

        if outil.puzzle_xsb(collec, numero) not in temp:
            temp += ligne
            with open(chemin, 'w', encoding='UTF-8') as fwr:
                fwr.write(temp)
            return True

        else:
            temp = temp.split('\n')
            for i in range(len(temp)):
                if temp[i].split(';')[0] == outil.puzzle_xsb(collec, numero):
                    a, b, c = temp[i].split(';')
                    if int(b) < score:
                        return False
                    else:
                        b = ';' + str(score) + ';'
                        c = pseudo
                    tup = (a, b, c)
                    temp[i] = ''.join(tup)
            temp = '\n'.join(temp)
            with open(chemin, 'w', encoding='UTF-8') as fwmr:
                fwmr.write(temp)
                return True

    else:
        with open(chemin, 'w', encoding='UTF-8') as fw:
            fw.write(ligne)
        return True


def sauv_meilleur_score_joueur(pseudo, coll, numero, score):
    """
    Sauvegarde le score établi par le joueur sur le puzzle dont la collection et le numero sont donnés en paramètre
    dans son fichier de meilleur score.

    :param pseudo: Le pseudo du joueur
    :param coll: La collection sur laquelle il joue
    :param numero: Le numéro du puzzle auquel il joue
    :param score: Le score obtenu après avoir joué
    :return: True si le score a été sauvegardé en tant que nouveau meilleur score, False sinon
    """
    chemin = os.path.join("sauvegardes", pseudo + ".txt")
    puzz = outil.puzzle_xsb(coll, numero)
    scores = dict()
    retval = False

    if os.path.isfile(chemin):
        with open(chemin, 'r', encoding='UTF-8') as fd:
            for sc in fd.readlines():
                sc = sc[:-1]
                puzzle, valeur = sc.split(';')
                scores[puzzle] = int(valeur)

            if est_meilleur_score_joueur(pseudo, coll, numero, score):
                scores[puzz] = score
                retval = True

        with open(chemin, 'w', encoding='UTF-8') as fd:
            for puzzle in scores:
                fd.write('{};{}\n'.format(puzzle, scores[puzzle]))

    else:
        with open(chemin, 'w', encoding='UTF-8') as fd:
            fd.write("{};{}\n".format(puzz, score))
            retval = True

    return retval


def meilleur_score_joueur(pseudo, coll, numero):
    """
    Renvoie le meilleur score d’un joueur à un puzzle.

    :param pseudo: Le pseudo du joueur
    :param coll: La collection sur laquelle il joue
    :param numero: Le numéro du puzzle auquel il joue
    :return: Le meilleur score du joueur, None s'il n'existe pas.
    """
    chemin = os.path.join("sauvegardes", pseudo + ".txt")
    puzz = outil.puzzle_xsb(coll, numero)

    if os.path.isfile(chemin):
        with open(chemin, 'r', encoding='UTF-8') as fd:
            for sc in fd.readlines():
                sc = sc[:-1]
                puzzle, valeur = sc.split(';')
                if puzzle == puzz:
                    return int(valeur)
    return None


def est_meilleur_score_joueur(pseudo, coll, numero, score):
    """
    Détermine si le score d’un joueur sur le puzzle dont la collection et le numero sont donnés en paramètre est un
    nouveau record personnel (nouveau meilleur score). La réponse est renvoyée au format booléen.

    :param pseudo: Le pseudo du joueur
    :param coll: La collection sur laquelle il joue
    :param numero: Le numéro du puzzle auquel il joue
    :param score: Le score obtenu après avoir joué
    :return: Le score est-il le meilleur score du joueur ?
    """
    meilleur = meilleur_score_joueur(pseudo, coll, numero)

    if meilleur is not None:
        return score < meilleur
    return True


def get_stat_partie(pseudo, coll, numero, score):
    """
    Permet d'obtenir une score sous forme de 3 étoiles pour que le joueur mesure ses performances.

    :param pseudo: pseudo du joueur   -> En quoi c'est utile ? Je ne sais pas...
    :param coll: collection du puzzle
    :param numero: numero du puzzle
    :param score: score réalisé par le joueur
    :return: Un score sous forme d'etoile pleine ou non
    """
    if os.path.isfile(os.path.join("sauvegardes", "records.txt")):
        if record_jeu(coll, numero) is None:
            return "\u2605 " * 3
        else:
            _, record_puzzle = record_jeu(coll, numero)
            ecart = abs(record_puzzle - score) / record_puzzle
            if ecart < 0.1 or (record_puzzle - score) <= 1:
                return "\u2605 "*3
            elif ecart < 0.25 or (record_puzzle - score) <= 2:
                return "\u2605 " * 2 + "\u2606"
            elif ecart < 0.50 or (record_puzzle - score) <= 4:
                return "\u2605 " + "\u2606" * 2
            else:
                return "\u2606 " * 3
