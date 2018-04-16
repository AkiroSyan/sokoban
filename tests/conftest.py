"""
Script de fixtures pour les tests unitaires contenant différents entrepots de Sokoban. Puisque nommé `conftest.py`,
automatiquement importé par pytest.
"""

import pytest, os, sys, io

@pytest.fixture
def novoban01():
    """L'entrepot de novoban01.xsb"""
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', ' ', ' ', '$', '@', '#'],
             ['#', ' ', '*', '.', ' ', '#'],
             ['#', '#', ' ', ' ', ' ', '#'],
             [' ', '#', '#', '#', '#', '#']]

@pytest.fixture
def novoban02():
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', ' ', ' ', '$', ' ', '#'],
             ['#', '#', '*', '#', '.', '#'],
             ['#', ' ', ' ', '@', ' ', '#'],
             ['#', ' ', ' ', ' ', ' ', '#'],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', '#', '#', '#', ' ', ' ']]

@pytest.fixture
def novoban03():
    return [['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', '@', '#', '#', '#'],
             ['#', ' ', '$', '$', ' ', '#'],
             ['#', '.', ' ', ' ', '.', '#'],
             ['#', '#', '#', '#', '#', '#']]

@pytest.fixture
def novoban06():
    return [[' ', ' ', '#', '#', '#', '#', ' ', ' '],
             ['#', '#', '#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', ' ', '.', '#', '#', '#'],
             ['#', '#', '#', ' ', '#', '@', '.', '#'],
             [' ', ' ', '#', ' ', '$', '$', ' ', '#'],
             [' ', ' ', '#', ' ', ' ', '$', ' ', '#'],
             [' ', ' ', '#', '.', ' ', '#', '#', '#'],
             [' ', ' ', '#', '#', '#', '#', ' ', ' ']]

@pytest.fixture
def novoban10():
    return [[' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' '],
             [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' '],
             ['#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#'],
             ['#', ' ', ' ', '#', ' ', '$', ' ', ' ', ' ', '#'],
             ['#', ' ', ' ', ' ', '$', ' ', ' ', '#', ' ', '#'],
             ['#', ' ', '.', '.', ' ', '#', ' ', ' ', ' ', '#'],
             ['#', '#', '#', '@', ' ', '#', '#', '#', '#', '#'],
             [' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ', ' '],
             [' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' ']]


# ************************************************
# Les joueurs
# ************************************************

@pytest.fixture
def jcrazy():
    return { "pseudo" : "crazy",    "collection" : "novoban",
             "numero" : 5,          "max" : 8,
             "score" : 3,           "historique" : []     }

# ************************************************
# Les puzzles une fois résolus
# ************************************************
@pytest.fixture
def novoban01_gagne():
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', ' ', ' ', ' ', '@', '#'],
             ['#', ' ', '*', '*', ' ', '#'],
             ['#', '#', ' ', ' ', ' ', '#'],
             [' ', '#', '#', '#', '#', '#']]

@pytest.fixture
def novoban02_gagne():
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', ' ', ' ', ' ', ' ', '#'],
             ['#', '#', '*', '#', '*', '#'],
             ['#', ' ', ' ', '@', ' ', '#'],
             ['#', ' ', ' ', ' ', ' ', '#'],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', '#', '#', '#', ' ', ' ']]

@pytest.fixture
def novoban03_gagne():
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', '@', '#', '#', '#'],
             ['#', ' ', ' ', ' ', ' ', '#'],
             ['#', '*', ' ', ' ', '*', '#'],
             ['#', '#', '#', '#', '#', '#']]

@pytest.fixture
def novoban06_gagne():
    return [ [' ', ' ', '#', '#', '#', '#', ' ', ' '],
             ['#', '#', '#', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', ' ', ' ', '#', ' ', ' '],
             ['#', ' ', ' ', ' ', '*', '#', '#', '#'],
             ['#', '#', '#', ' ', '#', '@', '*', '#'],
             [' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
             [' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
             [' ', ' ', '#', '*', ' ', '#', '#', '#'],
             [' ', ' ', '#', '#', '#', '#', ' ', ' ']]

@pytest.fixture
def novoban10_gagne():
    return [ [' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' '],
             [' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' '],
             ['#', '#', '#', '#', '#', ' ', '#', ' ', '#', '#'],
             ['#', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'],
             ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
             ['#', ' ', '*', '*', ' ', '#', ' ', ' ', ' ', '#'],
             ['#', '#', '#', '@', ' ', '#', '#', '#', '#', '#'],
             [' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ', ' '],
             [' ', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' ']]


@pytest.fixture
def novoban01_mouv1():
    """L'entrepot de novoban01.xsb avec gardien sur cible"""
    return [ ['#', '#', '#', '#', ' ', ' '],
             ['#', ' ', ' ', '#', '#', '#'],
             ['#', ' ', ' ', '$', ' ', '#'],
             ['#', ' ', '*', '+', ' ', '#'],
             ['#', '#', ' ', ' ', ' ', '#'],
             [' ', '#', '#', '#', '#', '#']]


# *********************************************************************************************************
# Gestion des répertoires
# *********************************************************************************************************

REPERTOIRE_TESTS = os.path.dirname(os.path.realpath(__file__))
REPERTOIRE_CODES = os.path.dirname( REPERTOIRE_TESTS )

@pytest.fixture
def change_repertoire_courant():
    """Déplace le répertoire courant pour être celui des codes sources"""
    os.chdir(REPERTOIRE_CODES)
    yield change_repertoire_courant
    os.chdir(REPERTOIRE_TESTS) # replace la console dans le répertoire de tests après test

@pytest.fixture(scope="function")
def arborescence_records(request):
    """Prépare l'arborescence pour y créer deux fichiers crazy.txt et records.txt + sauvegarder un éventuel
    fichier de sauvegardes au nom de crazy"""

    os.chdir(REPERTOIRE_CODES)                          # Modifie le répertoire courant

    # Les fixtures importées des paramètres du module
    content_crazy = getattr(request.module, "crazy", "")
    if content_crazy:
        content_crazy = content_crazy()
    content_records = getattr(request.module, "records", "")
    if content_records:
        content_records = content_records()

    # Les fichiers existent-ils déjà des originaux ?
    avec_original_crazy, avec_original_records, avec_sauv = False, False, False
    if os.path.isfile("sauvegardes/crazy.txt"):
        with open("sauvegardes/crazy.txt", "r") as fd:
            avec_original_crazy = True
            content_crazy_ori = fd.read()
    if os.path.isfile("sauvegardes/records.txt"):
        with open("sauvegardes/records.txt", "r") as fd:
            avec_original_records = True
            content_records_ori = fd.read()
    if os.path.isfile("sauvegardes/crazy.save"):
        with open("sauvegardes/crazy.save", "rb") as fd:
            avec_sauv = True
            content_save_ori = fd.read()

    # Création des fichiers de tests
    open("sauvegardes/crazy.txt", "w").write(content_crazy)                               # Initialise le contenu de crazy.txt avec la fixture
    open("sauvegardes/records.txt", "w").write(content_records)  # Initialise le contenu de crazy.txt avec la fixture

    yield arborescence_records                   # lance le test

    if avec_original_crazy:
        open("sauvegardes/crazy.txt", "w").write(content_crazy_ori)     # restaure le contenu original de crazy.txt
    else:
        os.remove("sauvegardes/records.txt")                             # supprime le fichier s'il n'existait pas
    if avec_original_records:
        open("sauvegardes/records.txt", "w").write(content_records_ori)     # restaure le contenu original de crazy.txt
    else:
        os.remove("sauvegardes/crazy.txt")                             # supprime le fichier s'il n'existait pas
    if avec_sauv:
        open("sauvegardes/crazy.save", "wb").write(content_save_ori)
    os.chdir(REPERTOIRE_TESTS)                          # replace le répertoire courant dans celui des tests


# *********************************************************************************************************
# Fonction pour test
# *********************************************************************************************************

def meme_valeur(entrepot1, entrepot2):
    """Compare les deux entrepots fournis en paramètre pour vérifier si leur contenu (leurs cases) est identique ou non.
    Renvoie la réponse au format booléen.

    :param entrepot1:
    :param entrepot2:
    :return: False si une case est différente, True si les 2 entrepots sont indentiques
    :rtype: bool
    """

    for ligne in range(len(entrepot1)):
        for colonne in range(len(entrepot1[ligne])):
            if entrepot1[ligne][colonne] != entrepot2[ligne][colonne]:
                return False
    return True

