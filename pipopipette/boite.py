# -*- coding: utf-8 -*-


class Boite:
    """
    Classe représentant une boîte de la planche de jeu.

    Une boîte est constituée d'un attribut couleur de type str
    et d'un attribut pleine de type bool.

    Cette classe vous est fournie, vous n'avez pas à la modifier.
    """
    DICT_COULEURS = {'': 'grey', 'bleu': 'blue', 'rouge': 'red'}

    def __init__(self):
        self.couleur = ''
        self.pleine = False

    def assigner_couleur(self, couleur):
        self.couleur = couleur
        self.pleine = True

    def couleur_formattee(self):
        """
        Nécessaire pour l'affichage en console, NE PAS MODIFIER.
        """
        if self.pleine:
            return self.couleur[0].upper()
        else:
            return ''

    def couleur_affichage(self):
        """
        Nécessaire pour le TP4, NE PAS MODIFIER.
        """
        return Boite.DICT_COULEURS[self.couleur]

    def __repr__(self):
        """
        Nécessaire pour les tests, NE PAS MODIFIER.
        """
        if self.pleine:
            return 'Boîte pleine de couleur {}'.format(self.couleur)
        else:
            return 'Boîte non pleine'
