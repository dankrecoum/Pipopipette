# -*- coding: utf-8 -*-
"""
Module de lancement du package pipopipette.

C'est ce module que nous allons exécuter pour démarrer votre jeu.
"""

from partie import PartiePipopipette

if __name__ == '__main__':
    partie = PartiePipopipette()

    # Pour charger d'une partie déjà sauvegardée
    # partie = PartiePipopipette('partie_sauvegardee.txt')

    # Pour sauvegarder une partie
    # partie.sauvegarder('partie_sauvegardee.txt')

    partie.jouer()
    input("Appuyez sur Entree pour fermer le programme\n")
