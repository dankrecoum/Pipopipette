# -*- coding: utf-8 -*-
import atexit
import winsound
from pipopipette.partie import PartiePipopipette
from tkinter import Tk, Canvas, messagebox, simpledialog, filedialog
from pipopipette.exceptions import ErreurPositionsCoup

winsound.PlaySound('mus_ghostbattle.wav', winsound.SND_LOOP | winsound.SND_ASYNC)


class CanvasPipopipette(Canvas):
    # Dans le TP, vous devrez ajouter un argument planche en entrée
    # à ce constructeur.

    def __init__(self, parent, planche, longueur_ligne=120):
        # Nombre de pixels par case, variable.
        self.planche = planche
        self.longueur_ligne = longueur_ligne
        self.largeur_ligne = self.longueur_ligne / 5
        self.dimension_boite = self.longueur_ligne + self.largeur_ligne

        # Dans le TP, ces champs devront être remplis à partir de l'attribut planche d'un objet Partie que vous ajouterez
        # au __init__(). Vous devrez aussi ajouter un attribut self.planche.
        #
        # Ici on crée des attributs n_boites_v, n_boites_h, lignes et boites, mais dans le TP
        # on lira directement ces attributs à partir de self.planche. Ces attributs sont donc
        # seulement pour les biens du labo, mais seront tous remplacés par self.planche dans le TP.

        # Appel du constructeur de la classe de base (Canvas).
        # Dans le TP, on remplace self.n_boites_v par self.planche.N_BOITES_V. Idem pour n_boites_h.
        super().__init__(parent,
                         width=self.planche.N_BOITES_V * self.dimension_boite + self.largeur_ligne - 1,
                         height=self.planche.N_BOITES_H * self.dimension_boite + self.largeur_ligne - 1)

    def dessiner_boites(self):
        # Ici, on itère sur le dictionnaire self.boites, sans se servir de la valeur de boite.
        # Dans le TP, on itèrera sur self.planche.boites.items() et boite sera un objet de
        # type Boite.
        for position, boite in self.planche.boites.items():
            ligne, col = position

            # On retrouve les points d'ancrage en x et en y de la boîte à partir de sa ligne et de sa colonne
            debut_boite_x = col * self.dimension_boite + self.largeur_ligne
            debut_boite_y = ligne * self.dimension_boite + self.largeur_ligne
            fin_boite_x = debut_boite_x + self.longueur_ligne
            fin_boite_y = debut_boite_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'grey'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre boite, c'est-à-dire utiliser 'fill=boite.couleur_affichage()'.
            self.create_rectangle(debut_boite_x, debut_boite_y, fin_boite_x, fin_boite_y, tags='boite',
                                  fill=boite.couleur_affichage())

    def dessiner_lignes(self):
        # Ici, on itère sur le dictionnaire self.lignes, sans se servir de la valeur de ligne.
        # Dans le TP, on itèrera sur self.planche.lignes.items() et ligne sera un objet de type
        # Ligne.
        for cle, ligne in self.planche.lignes.items():
            ligne_point, col_point, orientation = cle

            # On retrouve les points d'ancrage en x et en y de la ligne à partir de sa ligne, de sa colonne
            # et de son orientation
            if orientation == 'H':
                debut_ligne_x = col_point * self.dimension_boite + self.largeur_ligne
                debut_ligne_y = ligne_point * self.dimension_boite
                fin_ligne_x = debut_ligne_x + self.longueur_ligne
                fin_ligne_y = debut_ligne_y + self.largeur_ligne
            else:
                debut_ligne_x = col_point * self.dimension_boite
                debut_ligne_y = ligne_point * self.dimension_boite + self.largeur_ligne
                fin_ligne_x = debut_ligne_x + self.largeur_ligne
                fin_ligne_y = debut_ligne_y + self.longueur_ligne

            # Ici, on crée des rectangles de couleur 'white'. Dans votre TP, vous voudrez utiliser l'attribut
            # couleur de votre ligne, c'est-à-dire utiliser 'fill=ligne.couleur_affichage()'.
            self.create_rectangle(debut_ligne_x,
                                  debut_ligne_y,
                                  fin_ligne_x,
                                  fin_ligne_y,
                                  tags='ligne',
                                  fill=ligne.couleur_affichage(),
                                  width=1)

    def dessiner_points(self):
        # Cette fonction crée tous les points requis à partir des attributs self.n_boites_v et self.n_boites_h.
        # Dans le TP, on lira respectivement self.planche.N_BOITES_V et self.planche.N_BOITES_H
        for col in range(self.planche.N_BOITES_V + 1):
            for ligne in range(self.planche.N_BOITES_H + 1):
                origine_cercle_x = col * self.dimension_boite
                origine_cercle_y = ligne * self.dimension_boite
                fin_cercle_x = origine_cercle_x + self.largeur_ligne
                fin_cercle_y = origine_cercle_y + self.largeur_ligne

                self.create_oval(origine_cercle_x,
                                 origine_cercle_y,
                                 fin_cercle_x,
                                 fin_cercle_y,
                                 tags='point',
                                 fill='black')

    def obtenir_coup_joue(self, event):
        '''
        Méthode qui retrouve si un clic est fait sur une ligne, une boîte ou sur un point, et surtout pour retrouver
        laquelle.

        Dans votre TP, vous pourrez vous débarasser des sections de code concernant les clics sur un
        point et sur une boîte pour conserver seulement les sections sur les lignes et retourner None
        quand le clic est sur un point ou une boîte.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas

        Returns:
            None si le clic a été fait sur un point, (int, int, orientation) s'il
            a été fait sur une ligne et (int, int, 'Boite') si c'était une boîte
        '''

        col = int(event.x // self.dimension_boite)
        ligne = int(event.y // self.dimension_boite)

        x_relatif = event.x % self.dimension_boite
        y_relatif = event.y % self.dimension_boite

        coup = None

        if x_relatif < self.largeur_ligne:
            if y_relatif > self.largeur_ligne:
                # Clic sur une ligne verticale
                coup = (ligne, col, 'V')

        else:
            if y_relatif < self.largeur_ligne:
                # Clic sur une ligne horizontale
                coup = (ligne, col, 'H')

        return coup

    def actualiser(self):
        # On supprime les anciennes boîtes et on ajoute les nouvelles.
        self.delete('boite')
        self.dessiner_boites()

        # On supprime les anciennes lignes et on ajoute les nouvelles.
        self.delete('ligne')
        self.dessiner_lignes()

        # On dessine les points
        self.dessiner_points()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Figer la fenêtre
        self.resizable(0, 0)

        # Nom de la fenêtre et logo.
        self.iconbitmap('ul.ico')
        self.title('Pipopipette')

        # Dans le TP, vous voudrez ajouter un attribut self.partie,
        # avec comme valeur une nouvelle Partie

        self.introduction()
        self.partie = PartiePipopipette(self.charger_partie())
        self.initialiser_canvas()
        self.avec_ordi = messagebox.askyesno("Avec IA?", "Voulez-vous un joueur ordinateur comme joueur 2(Bleu) ?")

        # On lie un clic sur le Canvas à une méthode.
        self.canvas_planche.bind('<Button-1>', self.selectionner)

        # sauvegarde automatique lorsque fermeture brusque
        atexit.register(self.sauvegarde)

    def sauvegarde(self):
        if not self.partie.planche.est_pleine():
            save = messagebox.askyesno("Sauvegarde", "Voulez-vous sauvegarder la partie en cours ?")
            if save:
                name = simpledialog.askstring('Nom du fichier', 'Entrez le nom de la sauvegarde')
                self.partie.sauvegarder(f"{name}.txt")


    def charger_partie(self):
        self.withdraw()
        save = messagebox.askyesno("Charger?", "Voulez-vous charger une partie existante ?")
        self.deiconify()
        if save:
            fichier = filedialog.askopenfilename(title="Sélectionnez la sauvegarde",
                                                 filetypes=(("sauvegarde pipopipette", "*.txt"), ("All Files", "*.*")))
            return fichier

    def initialiser_canvas(self):
        # Création du canvas grille.
        # Dans le TP, vous voudrez passer self.partie.planche au constructeur
        # de Canvas
        self.canvas_planche = CanvasPipopipette(self, self.partie.planche)
        self.canvas_planche.actualiser()
        self.canvas_planche.grid()

    def selectionner(self, event):
        '''
        Méthode appelée lorsqu'un clic est fait sur votre fenêtre.

        Par défaut, comme notre fenêtre contient seulement notre Canvas, on va chercher
        le coup associé au clic à l'aide de self.canvas_planche.obtenir_coup_joue(event).

        Ici, pour vous montrer la gestion des exceptions et l'affichage de messages avec
        messagebox, on lance ici une exception ErreurClicPoint et on affiche une erreur si
        le clic a été fait sur un point (associé à un retour None de obtenir_coup_joue()).

        Dans votre TP, le retour de obtenir_coup_joue() sera à None si et seulement si le clic
        N'a PAS été effectué une ligne. Ainsi, si le coup est None, on ne fera rien, sinon on le jouera
        avec self.partie.jouer_coup(). Aussi, si le coup est sur une ligne déjà jouée, on attrapera
        l'exception lancée dans Planche.valider_coup() et on affichera un message d'erreur correspondant.
        Enfin, on s'assurera aussi de faire appel à l'actualisation du canvas et à la logique de
        fin de partie.

        Args:
            event (Event): L'objet Event relié au clic fait sur le canvas
        '''

        coup = self.canvas_planche.obtenir_coup_joue(event)

        if coup is not None:
            try:
                self.partie.planche.valider_coup(coup)
                self.partie.jouer_coup(coup)
                self.canvas_planche.actualiser()

                if self.avec_ordi:
                    self.jouer_ordi()  # appel du joueur ordi

                if self.partie.partie_terminee():
                    self.fin_de_partie()
                else:
                    self.canvas_planche.actualiser()

            except ErreurPositionsCoup as e:
                messagebox.showerror("Coup invalide", e)

    def fin_de_partie(self):
        self.boites_bleu, self.boites_rouge = self.partie.planche.bilan_boites()
        if self.partie.partie_nulle:
            messagebox.showinfo("Partie terminée", "La partie se termine sur un match nul")
        else:
            if self.boites_bleu > self.boites_rouge:
                self.gagnant_partie = self.partie.joueur_bleu.couleur
            else:
                self.gagnant_partie = self.partie.joueur_rouge.couleur
            messagebox.showinfo("Partie terminée!",
                                f"Il y {self.boites_bleu} boites bleues et {self.boites_rouge} boites rouges.\n Le "
                                f"gagnant de la partie est donc le joueur {self.gagnant_partie.upper()} ")

        new_game = messagebox.askyesno("Recommencez", "Voulez vous commencez une nouvelle partie ?")
        if new_game:
            self.nouvelle_partie()
        else:
            self.destroy()

    def jouer_ordi(self):
        if not self.partie.planche.maj_boites():
            coup_ordi = self.partie.joueur_bleu.choisir_coup(self.partie.planche)
            # time.sleep(1)
            self.partie.jouer_coup(coup_ordi)
            self.canvas_planche.actualiser()
            if not self.partie.planche.est_pleine():
                while self.partie.planche.maj_boites():
                    coup_ordi = self.partie.joueur_bleu.choisir_coup(self.partie.planche)
                    if coup_ordi is not None:
                        self.partie.jouer_coup(coup_ordi)
                        self.canvas_planche.actualiser()
                    else:
                        break

    def nouvelle_partie(self):
        self.partie = PartiePipopipette(self.charger_partie())
        self.canvas_planche.planche = self.partie.planche
        self.canvas_planche.actualiser()
        # self.charger_partie()
        self.avec_ordi = messagebox.askyesno("Avec IA?", "Voulez-vous un joueur ordinateur comme joueur 2(Bleu) ?")

    def introduction(self):
        self.withdraw()
        tuto = messagebox.askyesno("Pipopipette", "Bienvenue dans le palpitant jeu de pipopipette!\nVoulez-vous "
                                                  "suivre le tutoriel de présentation ?(cliquez sur No pour passer et "
                                                  "débuter la partie)")
        if tuto:
            messagebox.showinfo("Tutoriel d'introduction", "Le principe du jeu est simple:\nIl y a un joueur Humain("
                                                           "Vous bien sûr!) et un 2e joueur qui est Humain(Défiez un("
                                                           "e) pote!) ou Ordinateur(Voyez si vous pouvez le battre ^^ "
                                                           "!)")
            messagebox.showinfo("Tutoriel d'introduction", "Vous êtes le joueur rouge et vous devez battre le bleu en "
                                                           "replissant le plus de boîtes. C'est quoi remplir une "
                                                           "boîte?? Et bien vous devez jouer chacun à son tour une "
                                                           "ligne de la planche. Celui qui forme un petit carré "
                                                           "attribue sa couleur à celui-ci et joue à nouveau! Cool "
                                                           "n'est ce pas?")
            messagebox.showinfo("Tutoriel d'introduction", "Autre chose... Vous pouvez sauvegarder une partie en "
                                                           "cours à n'importe quel moment en fermant la fenêtre de "
                                                           "jeu. Vous pourrez la charger une autre fois :p.\n\nC'est "
                                                           "le fun non?\n\nEt bien c'était tout pour ce tutoriel and "
                                                           "LET THE GAME BEGIN !!")
        self.deiconify()
