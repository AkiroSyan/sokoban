#!/Volumes/Stockage/tim/venv/default/bin/python
# coding: UTF-8
"""
Script: sokoban/graphics
Auteur: tim
Date: 5/8/18
"""

# Fonctions
import pygame
import os
import sys
import copy

import pygame_text_input

import collection

SCREEN_X = 800
SCREEN_Y = 600

RES_X = 55
RES_Y = 55

CLOCK = None

SYMBOLS = {
    '#': "wall",
    '.': "store",
    '$': "object",
    '*': "object_store",
    '@': "mover_down",
    '+': "mover_down_store",
    ' ': "ground",
}

SETTINGS = dict()

SPRITES = dict()

ACTIONS = {
    pygame.K_UP: "haut",
    pygame.K_LEFT: "gauche",
    pygame.K_DOWN: "bas",
    pygame.K_RIGHT: "droite",
    pygame.K_u: "undo",
    pygame.K_ESCAPE: "exit",
    pygame.K_g: "gagne",
    pygame.K_r: "reset",
    pygame.K_s: "skin",
    pygame.K_h: "aide",
}

FONT = "monospace"


def cls(screen):
    """
    Permet d'effacer l'écran
    :param screen: écran à effacer
    :return: None
    """
    screen.blit(pygame.Surface(screen.get_size()), (0, 0))


def init_screen(x, y):
    """
    Initialise un écran avec pygame de largeur :x: et de hauteur :y:
    :param x: Largeur de l'écran
    :param y: Hauteur de l'écran
    :return: écran initialisé
    """
    global SCREEN_X, SCREEN_Y, CLOCK, FONT
    SCREEN_X = x
    SCREEN_Y = y

    pygame.init()

    fontfile = os.path.join("assets", "DejaVuSans.ttf")

    if os.path.isfile(fontfile):
        FONT = fontfile

    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Sokoban')

    CLOCK = pygame.time.Clock()

    cls(screen)

    return screen


def load_sprites(skin):
    """
    Charge les sprites ainsi que les paramètres qui leurs sont associés
    :param skin: Nom du skin à charger
    :return: None
    """
    global RES_X
    global RES_Y
    global SPRITES
    global SETTINGS

    basepath = os.path.join("assets", "skins", skin)
    file = os.path.join(basepath, skin + ".ini")
    if os.path.isfile(file):
        defkey = "Default"
        with open(file, "r", encoding="iso-8859-1") as fd:
            for line in fd.readlines():
                if line[0] not in [';', '\n']:
                    if line[0] == '[':
                        defkey = line[1:-2]
                        if defkey not in SETTINGS.keys():
                            SETTINGS[defkey] = dict()
                    if '=' in line:
                        key, value = line[:-1].split('=')
                        SETTINGS[defkey][key] = value

        RES_X = int(SETTINGS["tiles"].pop("real_width", 50))
        RES_Y = int(SETTINGS["tiles"].pop("real_height", 50))

        SPRITES = copy.deepcopy(SETTINGS["tiles"])


def load_image(name):
    """
    Charge une image.
    :param name: Image à charger
    :return: Iimage et rectangle de collision de l'image (tuple)
    """
    fullname = os.path.join("assets", "skins", SETTINGS["header"]["name"], SPRITES[name])
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as e:
        print("Cannot load image: {}\n{}".format(fullname, e))
        sys.exit(2)
    return image, image.get_rect()


def affiche_sprite(screen, symbole, x=0, y=0):
    """
    Affiche le sprite correspondant au symbole texte
    :param screen: Écran pygame sur lequel afficher
    :param symbole: Symbole ASCII correspondant au sprite qu'on veut afficher
    :param x: Offset en x (sera multiplié par la résolution d'une image)
    :param y: Ofset en y (sera multiplié par la résolution d'une image)
    :return: True si l'image a bien été affichée
    """
    to_load = SYMBOLS.get(symbole, False)
    if to_load:
        img, rect = load_image(to_load)
        rect.x = x*RES_X
        rect.y = y*RES_Y
        screen.blit(img, rect)
        return True
    return False


def affiche_entrepot(screen, entrepot):
    """
    Affiche l'entrepôt passé en paramètres et redimensionne l'écran
    :param screen: Écran sur lequel afficher l'entrepôt
    :param entrepot: Tableau représentant l'entrepôt à afficher
    :return: None
    """
    cls(screen)

    global SCREEN_Y, SCREEN_X
    max_y = len(entrepot)
    max_x = 0

    for l in entrepot:
        max_x = max(len(l), max_x)

    largeur = max_x * RES_X
    hauteur = max_y * RES_Y

    screen = redimensionne_ecran(screen, largeur, hauteur)

    for y, ligne in enumerate(entrepot):
        for x, case in enumerate(ligne):
            affiche_sprite(screen, case, x, y)


def interprete_action(action):
    """
    Interprète l'action passée en paramètre selon le tableau de correspondance ACTIONS

    :param action: Caractère à interpréter
    :return: Action interprétée
    """
    return ACTIONS.get(action, None)


def cycle_through_skins():
    """
    Boucle parmi les skins présents et charge le prochain
    :return: None
    """
    basepath = os.path.join("assets", "skins")

    skins = [skin for skin in os.listdir(basepath) if not skin.startswith(".")]

    current_skin = SETTINGS["header"]["name"]

    next_idx = (skins.index(current_skin) + 1) % len(skins)

    next_skin = skins[next_idx]

    load_sprites(next_skin)


def saisie_pseudo(screen):
    """
    Demande la saisie du pseudo du joueur et effectue les vérifications nécessaires
    :param screen: Écran sur lequel afficher la demande de saisie
    :return: Pseudo du joueur
    """
    texte_pseudo = affiche_texte("Entrez votre pseudo")
    text_input = pygame_text_input.TextInput(FONT, font_size=50,
                                             text_color=(255, 255, 255), cursor_color=(255, 255, 255))

    curseur = affiche_texte(">", 50)

    retval = False

    while not retval:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(2)
        retval = text_input.update(events)

        cls(screen)

        screen.blit(curseur, (50, 300))

        screen.blit(text_input.get_surface(), (120, 300))
        screen.blit(texte_pseudo, centre_x(texte_pseudo, 100))

        pygame.display.flip()

        CLOCK.tick(25)

    if text_input.get_text() in ['', 'record']:
        pseudo = 'crazy'
    else:
        pseudo = text_input.get_text()

    return pseudo


def redimensionne_ecran(screen, x, y):
    global SCREEN_X, SCREEN_Y

    if SCREEN_X != x or SCREEN_Y != y:
        SCREEN_X = x
        SCREEN_Y = y
        screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

    return screen


def affiche_texte(texte, font_size=60, text_color=(255, 255, 255)):
    """
    Crée l'objet texte représentant le texte à afficher
    :param texte: Texte à afficher
    :param font_size: Taille de police
    :param text_color: Couleur du texte
    :return: Objet texte
    """
    font = pygame.font.Font(FONT, font_size)
    return font.render(texte, True, text_color)


def centre_x(texte, y):
    """
    Retourne les coordonnées nécessaires pour centrer le texte en x
    :param texte: Texte à centrer
    :param y: Position en Y
    :return: Coordonnées x, y du texte centré
    """
    return (SCREEN_X - texte.get_width()) // 2, y


def affiche_aide(screen):
    screen = redimensionne_ecran(screen, 800, 600)

    cls(screen)

    aides = {'<flèches>': "se déplacer",
             '<u>': "annuler l'action précédente",
             '<r>': "réinitialiser le puzzle",
             '<s>': "changer l'apparence du jeu (skin)",
             '<h>': "afficher l'aide",
             '<esc>': "retour au menu/jeu"}

    texte_entete = affiche_texte("Comment jouer ?", 72)

    screen.blit(texte_entete, centre_x(texte_entete, 20))

    for i, key_desc in enumerate(aides.items()):
        key, desc = key_desc
        y = 150 + i * 60
        screen.blit(affiche_texte(key, 30), (50, y))
        screen.blit(affiche_texte(':    ' + desc, 30), (250, y))

    pygame.display.flip()

    while True:
        CLOCK.tick(25)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)

                if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    return


def affiche_menu(screen, joueur):
    """
    Affiche le menu principal et attend le choix d'un item par l'utilisateur
    :param screen: Écran sur lequel afficher le menu
    :param joueur: Dictionnaire représentant le joueur
    :return: Choix effectué par le joueur
    """
    screen = redimensionne_ecran(screen, 800, 600)

    first_puzzle = joueur["numero"]
    # Utile pour reset l'historique si l'utilisateur joue un puzzle différent de
    #  celui d'origine

    nb_puzzle = str(joueur["numero"])
    collec = joueur["collection"]

    text_menu = affiche_texte("Menu principal", 72)
    text_jouer = affiche_texte("Jouer le puzzle N°" + nb_puzzle, 45)
    text_hint = affiche_texte("<= / => pour sélectionner un autre puzzle", 20)
    text_collec = affiche_texte("Changer de collection (actuel : " + collec + ")", 30)
    text_rej = affiche_texte("Charger une partie sauvegardée", 30)
    text_howto = affiche_texte("Comment jouer ?", 30)
    text_quit = affiche_texte("Quitter", 30)

    text_unsaved = affiche_texte("> pas de sauvegarde <", 20)

    choix = ['start', collec, 'reload', 'howto', 'exit']
    action = 'start'

    curseur = affiche_texte(">", 60)
    cur_val = 0
    curseur_pos = 125

    affichage_sauv = 0

    while True:
        cls(screen)
        CLOCK.tick(25)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                        val = 1 if event.key == pygame.K_RIGHT else -1
                        next_puzz = joueur["numero"] + val
                        if collection.est_dans_collection(collec, next_puzz) and next_puzz <= joueur["max"]:
                            joueur["numero"] = next_puzz
                            text_jouer = affiche_texte("Jouer le puzzle N°" + str(next_puzz), 45)

                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        val = 1 if event.key == pygame.K_DOWN else -1
                        cur_val = (cur_val + val) % 5
                        curseur_pos = 125 + cur_val * 90
                        action = choix[cur_val]

                    if event.key == pygame.K_RETURN:
                        if action in ['start', 'exit']:
                            if joueur['numero'] != first_puzzle:
                                joueur['historique'] = list()
                            return action
                        if action in ['sokoban', 'novoban']:
                            choix[1] = collec  # on mémorise l'autre collection pour le changement
                            action = collec

                            collec = 'novoban' if action == 'sokoban' else 'sokoban'  # on effectue le changement

                            if collection.change_collection(joueur, collec):  # on vérifie qu'il effectif
                                text_collec = affiche_texte("Changer de collection (actuel : " + collec + ")", 30)
                                text_jouer = affiche_texte("Jouer le puzzle N°" + str(joueur["numero"]), 45)
                            else:
                                print("pas de changement")
                        if action == 'reload':
                            if len(joueur["historique"]) > 0:
                                return action
                            else:
                                affichage_sauv = 25
                        if action == 'howto':
                            affiche_aide(screen)
                            cls(screen)

        screen.blit(text_menu, centre_x(text_menu, 20))
        screen.blit(text_jouer, centre_x(text_jouer, 150))
        screen.blit(text_hint, centre_x(text_hint, 210))
        screen.blit(text_collec, (100, 240))
        screen.blit(text_rej, (100, 330))
        screen.blit(text_howto, (100, 420))
        screen.blit(text_quit, (100, 510))
        screen.blit(curseur, (40, curseur_pos))

        if affichage_sauv > 0:  # Timer pour laisser afficher le "pas de sauvegarde"
            screen.blit(text_unsaved, centre_x(text_unsaved, 380))
            affichage_sauv -= 1

        pygame.display.flip()
