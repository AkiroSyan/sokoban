"""
==============================================================
Script test_outil.py (pour les fonctions de :py:mod:`outil`)
==============================================================
"""

import pytest, echeance
try:
    import outil
except:
    pass

# *********************************************************************************************************
# Tests de la fonction coords()
# *********************************************************************************************************
class TestCoords(object):
    """Tests de la fonction :py:func:`outil.coords`"""
    pytestmark = echeance.ECHEANCE3

    def test_coords_type_retour(self):
        """Teste si la fonction renvoie bien une liste de 2 éléments"""
        entrepot = [ ['$', '@', '#'] ]
        assert( isinstance(outil.coords(entrepot), list) is True )
        assert( len(outil.coords(entrepot)) == 2) # de 2 éléments

    def test_coords_sur_entrepot_fictif_avec_gardien_hors_cible(self):
        """Teste si les coordonnées du gardien @ sont bien repérées"""
        assert( outil.coords( [ ['#', ' ', '.'], ['$', '@', '#'] ] ) == [1, 1] )

    def test_coords_sur_entrepot_fictif_avec_gardien_sur_cible(self):
        """Teste si les coordonnées du gardien @ sont bien repérées lorsqu'il est sur une cible"""
        entrepot = [ ['#', ' ', '.'], ['$', '+', '#'] ]
        assert( outil.coords(entrepot) == [1, 1] ) # ayant les bonnes valeurs

    def test_coords_sur_plusieurs_entrepots(self, novoban01, novoban02, novoban03):
        """Teste sur plusieurs entrepôts de novoban"""
        assert (outil.coords(novoban01) == [2, 4] )
        assert( outil.coords(novoban02) == [5, 3] )
        assert( outil.coords(novoban03) == [3, 2] )


# *********************************************************************************************************
# Tests de la fonction parse_pXX()
# *********************************************************************************************************
class TestParsePXX(object):
    """Tests de la fonction :py:func:`outil.parse_pXX`"""
    pytestmark = echeance.ECHEANCE7

    def test_parse_pXX_return(self):
        """Teste le type de la valeur de retour"""
        assert (isinstance(outil.parse_pXX("p1"), int) is True)  # un entier ?

    def test_parse_pXX_saisie_valide(self):
        """Teste la valeur renvoyée lorsque la saisie est valide"""
        assert( outil.parse_pXX("p1") == 1)
        assert( outil.parse_pXX("p22") == 22 )
        assert( outil.parse_pXX("p10") == 10 )

    def test_parse_pXX_saisie_incorrecte(self):
        """Teste la valeur renvoyée lorsque la saisie est non valide"""
        assert( outil.parse_pXX("rien") is None )
        assert( outil.parse_pXX("prien") is None )


# *********************************************************************************************************
# Tests de la fonction puzzle_xsb()
# *********************************************************************************************************

class TestPuzzleXSB(object):
    """Tests de la fonction :py:func:`outil.puzzle_xsb`"""
    pytestmark = echeance.ECHEANCE2

    def test_puzzle_xsb_return(self):
        """Teste le type de la valeur renvoyée"""
        assert( isinstance(outil.puzzle_xsb("novoban", 1), str) is True) # la valeur renvoyée est une chaine de caractère

    def test_puzzle_xsb_numero_valide(self):
        """Teste si le nom du puzzle_xsb est correct sur plusieurs puzzles existants"""
        assert( outil.puzzle_xsb("novoban", 22) == "novoban22.xsb" )
        assert( outil.puzzle_xsb("novoban", 1) == "novoban01.xsb" )
        assert( outil.puzzle_xsb("sokoban", 36) == "sokoban36.xsb" )

    def test_puzzle_xsb_numero_non_valide(self):
        """Teste si la fonction puzzle_xsb lorsque le puzzle n'existe pas (car de numero > 99)"""
        assert (outil.puzzle_xsb("novoban", 103) is None)
        assert (outil.puzzle_xsb("novoban", 253) is None)


# *********************************************************************************************************
# Tests de la fonction chemin_puzzle()
# *********************************************************************************************************

class TestCheminPuzzle(object):
    """Tests de la fonction :py:func:`outil.chemin_puzzle`"""
    pytestmark = echeance.ECHEANCE2

    def test_chemin_puzzle_return(self):
        """Teste le type de la valeur renvoyée"""
        assert (isinstance(outil.chemin_puzzle("novoban", 1), str) is True)  # la valeur renvoyée est une chaine de caractère

    def test_chemin_puzzle_numero_valide(self):
        """Teste le chemin renvoyé sur plusieurs puzzles existants"""
        assert (outil.chemin_puzzle("novoban", 22) == "collections\\novoban\\novoban22.xsb"
                or outil.chemin_puzzle("novoban", 22) == "collections/novoban/novoban22.xsb")
        assert (outil.chemin_puzzle("novoban", 1) == "collections\\novoban\\novoban01.xsb"
                or outil.chemin_puzzle("novoban", 1) == "collections/novoban/novoban01.xsb")
        assert (outil.chemin_puzzle("sokoban", 36) == "collections\\sokoban\\sokoban36.xsb"
                or outil.chemin_puzzle("sokoban", 36) == "collections/sokoban/sokoban36.xsb")

    def test_chemin_puzzle_numero_non_valide(self):
        """Teste le chemin renvoyé lorsque le puzzle n'existe pas (car de numéro > 99)"""
        assert (outil.chemin_puzzle("novoban", 103) is None)
        assert (outil.chemin_puzzle("novoban", 342) is None)


# *********************************************************************************************************
# Tests de la fonction coords_deplacees()
# *********************************************************************************************************


class TestCoordsDeplacees(object):
    """Tests de la fonction :py:func:`outil.coords_deplacees`"""
    pytestmark = echeance.ECHEANCE3

    def test_coords_deplacees_return(self):
        """Teste le type de la valeur de retour"""
        assert( isinstance(outil.coords_deplacees([5, 3], "haut"), list) is True)  # renvoie une liste
        assert( len(outil.coords_deplacees([5, 3], "haut")) == 2)  # de 2 éléments
        assert( isinstance(outil.coords_deplacees([5, 3], "haut")[0], int) is True)  # entier
        assert (isinstance(outil.coords_deplacees([5, 3], "haut")[1], int) is True)  # entier

    def test_coords_deplacees_haut_dans_grille(self):
        """Teste des coordonnées déplacées vers le haut dans la grille"""
        assert( outil.coords_deplacees([5, 3], "haut") == [4, 3] )
        assert (outil.coords_deplacees([2, 6], "haut") == [1, 6] )

    def test_coords_deplacees_bas_valide(self):
        """Teste des coordonnées déplacées vers le bas dans la grille"""
        assert( outil.coords_deplacees([5, 3], "bas") == [6, 3] )
        assert (outil.coords_deplacees([2, 6], "bas") == [3, 6])

    def test_coords_deplacees_droite_valide(self):
        """Teste des coordonnées déplacées vers la droite dans la grille"""
        assert (outil.coords_deplacees([5, 3], "droite") == [5, 4])
        assert (outil.coords_deplacees([2, 6], "droite") == [2, 7])

    def test_coords_deplacees_gauche_valide(self):
        """Teste des coordonnées déplacées vers la gauche dans la grille"""
        assert (outil.coords_deplacees([5, 3], "gauche") == [5, 2])
        assert (outil.coords_deplacees([2, 6], "gauche") == [2, 5])

    def test_coords_deplacees_hors_entrepot(self):
        """Teste des coordonnées déplacées tombant hors de la grille"""
        assert (outil.coords_deplacees([0, 0], "haut") == [-1, 0])
        assert (outil.coords_deplacees([0, 0], "gauche") == [0, -1])


# *********************************************************************************************************
# Tests de la fonction init_entrepot() (seulement sur la 1ère écheance)
# *********************************************************************************************************

@pytest.mark.echeance1
def test_init_entrepot( ):
    """Teste si l'entrepôt est correctement renvoyé"""
    assert( outil.init_entrepot() == [  ['#', '#', '#', '#', '#', '#', '#'],
                                        ['#', '.', ' ', '$', ' ', '.', '#'],
                                        ['#', ' ', '$', '@', '$', ' ', '#'],
                                        ['#', '.', ' ', '$', ' ', '.', '#'],
                                        ['#', '#', '#', '#', '#', '#', '#']] )

# *********************************************************************************************************
# Tests de la fonction init_joueur() (seulement sur la 1ère écheance)
# *********************************************************************************************************

@pytest.mark.echeance1
def test_init_joueur( ):
    """Teste si le joueur est correctement renvoyé"""
    assert( outil.init_joueur() ==  {"pseudo" : "crazy",
              "collection" : "novoban",
              "numero" : 5,
              "max" : 8,
              "score" : 0,
              "historique" : []
             } )