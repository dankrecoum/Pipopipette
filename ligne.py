# -*- coding: utf-8 -*-


class Ligne:
    """
    Classe représentant une ligne.

    Une ligne est constituée d'un attribut booléen jouee.
    """
    COULEUR_JOUEE = 'black'
    COULEUR_NON_JOUEE = 'white'

    def __init__(self):
        self.jouee = False

    def couleur_affichage(self):
        """
        Nécessaire pour le TP4, NE PAS MODIFIER.
        """
        if self.jouee:
            return Ligne.COULEUR_JOUEE
        else:
            return Ligne.COULEUR_NON_JOUEE

    def __repr__(self):
        """
        Nécessaire pour les tests, NE PAS MODIFIER.
        """
        return 'Ligne {}jouée'.format('' if self.jouee else 'non ')
