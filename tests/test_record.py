
import pytest, os, shutil
import echeance
try:
    import record
except:
    pass


@pytest.fixture
def crazy():
    """Le contenu d'un fichier crazy.txt"""
    return "novoban01.xsb;12\nnovoban02.xsb;15\nsokoban02.xsb;18\nsokoban01.xsb;12\n"

@pytest.fixture()
def records():
    """Le contenu d'un fichier records.txt"""
    return "novoban01.xsb;12;crazy\nnovoban02.xsb;15;crazy\nnovoban03.xsb;100;happy\nsokoban01.xsb;12;happy\n"


# *********************************************************************************************************
# Tests de la fonction meilleur_score_joueur()
# *********************************************************************************************************

class TestMeilleurScoreJoueur(object):
    """Tests de la fonction :py:func:`record.meilleur_score_joueur`."""
    pytestmark = echeance.ECHEANCE8

    def test_meilleur_score_return(self, arborescence_records):
        """Teste le type de la valeur de retour"""
        assert (isinstance(record.meilleur_score_joueur("crazy", "novoban", 1), int))  # Un entier

    def test_meilleur_score_joueur_avec_record_existant(self, arborescence_records):
        """Teste le score de crazy_ini lu sur différents puzzles"""
        assert( record.meilleur_score_joueur("crazy", "novoban", 1) == 12 )
        assert( record.meilleur_score_joueur("crazy", "sokoban", 1) == 12 )
        assert( record.meilleur_score_joueur("crazy", "sokoban", 2) == 18 )

    def test_meilleur_score_joueur_avec_record_non_existant(self, arborescence_records):
        """Teste le score de crazy_ini lu sur différents puzzles n'existant pas"""
        assert(record.meilleur_score_joueur("crazy_ini", "encoreunban", 1) == None)
        assert(record.meilleur_score_joueur("vraiment_personne", "novoban", 1) == None)


# *********************************************************************************************************
# Tests de la fonction sauv_meilleur_score_joueur()
# *********************************************************************************************************

class TestSauvMeilleurScoreJoueur(object):
    """Tests de la fonction :py:func:`record.sauv_meilleur_score_joueur`"""
    pytestmark = echeance.ECHEANCE8
    # "novoban01.xsb;12\nnovoban02.xsb;15\nsokoban02.xsb;18\nsokoban01.xsb;12\n"

    def test_sauv_meilleur_score_joueur_sur_score_existant_avec_amelioration(self, arborescence_records):
        """Teste la modification d'un meilleur score sur un score existant lorsque
        le nouveau score est meilleur que le précédent"""
        rep = record.sauv_meilleur_score_joueur("crazy", "novoban", 1, 6)
        assert( rep == True )           # La modif est-elle effective ?
        content = open("sauvegardes/crazy.txt", "r").read()
        assert( content == "novoban01.xsb;6\nnovoban02.xsb;15\nsokoban02.xsb;18\nsokoban01.xsb;12\n" ) # la modif est-elle effective ?

        rep = record.sauv_meilleur_score_joueur("crazy", "sokoban", 1, 6)  # La modification du fichier a-t-elle été faite ?
        assert (rep == True)
        content = open("sauvegardes/crazy.txt", "r").read()
        assert ( content == "novoban01.xsb;6\nnovoban02.xsb;15\nsokoban02.xsb;18\nsokoban01.xsb;6\n")  # la modif est-elle effective ?


    def test_sauv_meilleur_score_joueur_ajout(self, arborescence_records):
        """Teste l'ajout d'un meilleur score"""
        rep = record.sauv_meilleur_score_joueur("crazy", "novoban", 5, 15)
        assert( rep == True )
        assert (open("sauvegardes/crazy.txt", "r").read() == "novoban01.xsb;12\nnovoban02.xsb;15\nsokoban02.xsb;18\nsokoban01.xsb;12\nnovoban05.xsb;15\n" )  # la modif est-elle effective ?

    def test_sauv_meilleur_score_joueur_sur_score_existant_sans_amelioration(self, arborescence_records, crazy):
        """Teste la modification sur un score existant lorsque
        le nouveau score n'est pas meilleur que le précédent"""
        rep = record.sauv_meilleur_score_joueur("crazy", "sokoban", 1, 15)
        assert( rep == False )
        assert (open("sauvegardes/crazy.txt", "r").read() == crazy )  # la modif est-elle effective ?


# *********************************************************************************************************
# Tests de la fonction record_jeu()
# *********************************************************************************************************

class TestSauvRecord(object):
    """Tests de la fonction :py:func:`record.record_jeu`"""
    pytestmark = echeance.ECHEANCE8

    def test_record_jeu_return(self, arborescence_records):
        """Teste le type de la valeur de retour"""
        assert( isinstance(record.record_jeu("novoban", 2), list) ) # une liste ?
        assert( len(record.record_jeu("novoban", 2)) == 2 ) # de 2 éléments ?
        assert( isinstance(record.record_jeu("novoban", 2)[0], str) is True )  # le 1er = 1 chaine de caractère ?
        assert (isinstance(record.record_jeu("novoban", 2)[1], int) is True)  # le 2ème = un entier ?

    def test_record_jeu_sur_record_existant(self, arborescence_records):
        """Teste la lecture du record de deux records existants"""
        assert(record.record_jeu("novoban", 2) == ["crazy", 15])
        assert(record.record_jeu("sokoban", 1) == ["happy", 12])

    def test_record_jeu_sur_record_inexistant(self, arborescence_records):
        """Teste la lecture d'un record n'existant pas"""
        assert(record.record_jeu("sokoban", 18) == None)


# *********************************************************************************************************
# Tests de la fonction sauv_record_jeu()
# *********************************************************************************************************

class TestSauvRecordJeu(object):
    """Tests de la fonction :py:func:`record.sauv_record_jeu`"""
    pytestmark = echeance.ECHEANCE8

    def test_sauv_record_jeu_sur_record_existant_avec_amelioration(self, arborescence_records):
        """Teste la modification d'un record sur un record existant lorsque
        le nouveau score est meilleur que le précédent"""
        rep = record.sauv_record_jeu("incroyable", "novoban", 1, 6) # La modification du fichier a-t-elle été faite ?
        assert( rep == True )
        content = open("sauvegardes/records.txt", "r").read()
        assert( content == "novoban01.xsb;6;incroyable\nnovoban02.xsb;15;crazy\nnovoban03.xsb;100;happy\nsokoban01.xsb;12;happy\n" ) # la modif est-elle effective ?

        rep = record.sauv_record_jeu("incroyable", "sokoban", 1, 6)  # La modification du fichier a-t-elle été faite ?
        assert( rep == True )
        content =  open("sauvegardes/records.txt", "r").read()
        assert( content == "novoban01.xsb;6;incroyable\nnovoban02.xsb;15;crazy\nnovoban03.xsb;100;happy\nsokoban01.xsb;6;incroyable\n")  # la modif est-elle effective ?

    def test_sauv_record_jeu_avec_ajout(self, arborescence_records):
        """Teste l'jout d'un record (pour un jeu sans record antérieur)"""
        rep = record.sauv_record_jeu("incroyable", "novoban", 5, 15)
        assert( rep == True )
        content = open("sauvegardes/records.txt", "r").read()
        assert( content == "novoban01.xsb;12;crazy\nnovoban02.xsb;15;crazy\nnovoban03.xsb;100;happy\nsokoban01.xsb;12;happy\nnovoban05.xsb;15;incroyable\n" )  # la modif est-elle effective ?

    def test_sauv_record_jeu_sur_record_existant_avec_amelioration(self, arborescence_records, records):
        """Teste la modification d'un record sur un record existant lorsque
        le nouveau score n'est pas meilleur que le précédent"""
        rep = record.sauv_record_jeu("incroyable", "sokoban", 1, 15)
        assert( rep == False )
        content = open("sauvegardes/records.txt", "r").read()
        assert( content == "novoban01.xsb;12;crazy\nnovoban02.xsb;15;crazy\nnovoban03.xsb;100;happy\nsokoban01.xsb;12;happy\n" )  # la modif est-elle effective ?


# *********************************************************************************************************
# Tests de la fonction est_record()
# *********************************************************************************************************

class TestEstRecord(object):
    """Tests de la fonction :py:func:`record.est_record`"""
    pytestmark = echeance.ECHEANCE8

    def test_est_record_return(self, arborescence_records):
        """Teste le type de la valeur de retour"""
        assert(isinstance(record.est_record_jeu("novoban", 1, 2), bool)) # Est-ce une réponse booléenne ?

    def test_est_record_sur_record_existant(self, arborescence_records):
        """Teste si la fonction détecte un nouveau record, sur un record préalable dans records.txt"""
        assert (record.est_record_jeu("novoban", 1, 2) == True)  # La réponse est-elle correcte ?
        assert (record.est_record_jeu("novoban", 1, 150) == False)

    def test_est_record_sur_record_inexistant(self, arborescence_records):
        """Teste si la fonction détecte un nouveau record, sur un record n'existant pas dans records.txt"""
        assert (record.est_record_jeu("novoban", 57, 2) == True)  # La réponse est-elle correcte ?
        assert (record.est_record_jeu("novoban", 57, 150) == True)



# *********************************************************************************************************
# Tests de la fonction est_meilleur_score_joueur()
# *********************************************************************************************************

class TestEstMeilleurScore(object):
    """Tests de la fonction :py:func:`record.est_meilleur_score_joueur`"""
    pytestmark = echeance.ECHEANCE8

    def test_est_meilleur_score_return(self, arborescence_records):
        """Teste le type de la valeur de retour"""
        assert (isinstance(record.est_meilleur_score_joueur("crazy_ini", "novoban", 1, 2), bool))  # Est-ce une réponse booléenne ?

    def test_est_meilleur_score_joueur_sur_score_existant(self, arborescence_records):
        """Teste si la fonction détecte un nouveau meilleur score, sur un record préalable"""
        assert (record.est_meilleur_score_joueur("crazy", "novoban", 1, 2) == True)  # La réponse est-elle correcte ?
        assert (record.est_meilleur_score_joueur("crazy", "novoban", 1, 150) == False)
        assert (record.est_meilleur_score_joueur("crazy", "sokoban", 1, 2) == True)  # La réponse est-elle correcte ?

    def test_is_new_meilleur_score_joueur_sur_record_non_existant(self, arborescence_records):
        """Teste si la fonction détecte un nouveau meilleur score, sur un record n'existant pas au préalable"""
        assert (record.est_meilleur_score_joueur("crazy", "novoban", 57, 2) == True)  # La réponse est-elle correcte ?
        assert (record.est_meilleur_score_joueur("crazy", "novoban", 57, 150) == True)


# *********************************************************************************************************
# Tests de la fonction get_stat_partie()
# *********************************************************************************************************

class TestStatPartie(object):
    """Tests de la fonction :py:func:`record.get_stat_partie`"""

    def gest_stat_partie_return(self):
        """Teste de la valeur de retour"""
        assert( isinstance(record.get_stat_partie("crazy", "novoban", 2, 10), str) is True ) # renvoie une chaine de caractères

    def gest_stat_partie_sur_record_existant_record_faible(self, arborescence_records):
        """Teste les stats calculées sur des records de puzzles solvables en peu de coups"""
        assert( record.get_stat_partie("crazy", "novoban", 2, 12) == "★★★" ) # record battu
        assert (record.get_stat_partie("crazy", "novoban", 2, 16) == "★★★")  # dans les 10/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 18) == "★★☆")  # dans les 25/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 22) == "★☆☆")  # dans les 50/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 50) == "☆☆☆")  # au-delà

    def gest_stat_partie_sur_record_existant_record_eleve(self, arborescence_records):
        """Teste les stats calculées sur des records de puzzles solvables en beaucoup de coups"""
        assert( record.get_stat_partie("crazy", "novoban", 2, 20) == "★★★" ) # record battu
        assert (record.get_stat_partie("crazy", "novoban", 2, 109) == "★★★") # dans les 10/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 124) == "★★☆") # dans les 25/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 149) == "★☆☆") # dans les 50/100
        assert (record.get_stat_partie("crazy", "novoban", 2, 160) == "☆☆☆") # au delà

    def gest_stat_partie_sur_record_non_existant(self, arborescence_records):
        """Teste les stats calculées sur un record n'existant pas préalablement"""
        assert( record.get_stat_partie("crazy", "novoban", 5, 20) == "★★★" ) # record battu