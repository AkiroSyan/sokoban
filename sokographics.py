#!/Volumes/Stockage/tim/venv/default/bin/python
# coding: UTF-8
"""
Script: sokoban/sokographics
Auteur: tim
Date: 5/6/18
"""
import pygame
import sys

import collection
import puzzle
import terminal
import record
import graphics


# Programme principal
def partie(joueur, entrepot, screen):
    puzzle.sauv_historique(joueur, entrepot)
    pygame.display.set_caption(terminal.affiche_header(joueur))

    while not puzzle.gagne(entrepot):
        pygame.display.flip()
        graphics.CLOCK.tick(60)
        graphics.affiche_entrepot(screen, entrepot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(2)
            if event.type == pygame.KEYDOWN:
                intp = graphics.interprete_action(event.key)

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
                    graphics.affiche_entrepot(screen, entrepot)
                if intp == "skin":
                    graphics.cycle_through_skins()
                    graphics.affiche_entrepot(screen, entrepot)
                if intp == "exit":
                    return False
                collection.sauve_contexte(joueur)
            pygame.display.set_caption(terminal.affiche_header(joueur))

    pseudo = joueur["pseudo"]
    coll = joueur["collection"]
    numero = joueur["numero"]
    score = joueur["score"]

    nouveau_puzzle = False

    joueur["historique"] = list()
    if record.est_meilleur_score_joueur(pseudo, coll, numero, score):
        nouveau_puzzle = collection.debloque_niveau(joueur)
    record.sauv_meilleur_score_joueur(pseudo, coll, numero, score)
    record.sauv_record_jeu(pseudo, coll, numero, score)
    terminal.affiche_stat_partie(joueur)

    next = False

    texte_victoire = graphics.affiche_texte("Puzzle complété !", font_size=45)
    texte_debloque = graphics.affiche_texte("Nouveau puzzle débloqué", font_size=30)

    while not next:
        graphics.CLOCK.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(2)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    return True

        graphics.affiche_entrepot(screen, entrepot)
        screen.blit(texte_victoire, graphics.centre_x(texte_victoire, 20))
        if nouveau_puzzle:
            screen.blit(texte_debloque, graphics.centre_x(texte_debloque, 100))
        pygame.display.flip()



def main():
    screen = graphics.init_screen(800, 600)
    graphics.load_sprites("Yoshi")

    pseudo = graphics.saisie_pseudo(screen)

    joueur = collection.charge_contexte(pseudo)

    action = ''

    while not action == "exit":
        action = graphics.affiche_menu(screen, joueur)

        if action == 'start':

            joueur["historique"] = list()
            joueur["score"] = 0
            entrepot = collection.charge_puzzle(joueur["collection"], joueur["numero"])
            partie(joueur, entrepot, screen)

        if action == 'reload':
            if len(joueur["historique"]) > 0:
                entrepot = joueur["historique"][-1]
                partie(joueur, entrepot, screen)
            else:
                action = 'start'

if __name__ == '__main__':
    main()
