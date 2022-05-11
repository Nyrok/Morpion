import random
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from win32api import GetSystemMetrics
import pygame

root = tk.Tk()
root.withdraw()
pygame.init()
font = pygame.font.Font(None, 32)


def main(recommencer: bool = False) -> None:
    """
    Fonction qui permet de créer la Grille
    :param recommencer: Savoir si on recommence la partie ou une nouvelle partie
    """
    pygame.display.set_caption("Morpion", "")
    global mode
    global ecran
    global jeu
    global tour
    global joueur_x
    global joueur_o
    global score

    ecran = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.RESIZABLE)
    ecran.fill((0, 0, 0))
    jeu = True
    grille = creer_grille()
    if not recommencer:
        joueur_x = simpledialog.askstring(title='Morpion', prompt='Quel est le pseudo du joueur X ?')
        mode = 'joueur' if messagebox.askyesno('Morpion', 'Voulez-vous jouer contre un joueur ?') else 'pc'
        if mode == 'joueur':
            joueur_o = simpledialog.askstring(title='Morpion', prompt='Quel est le pseudo du joueur O ?')
        else:
            joueur_o = 'Ordinateur'
        score = {joueur_x: 0, joueur_o: 0}
    tour = 'X' if random.randint(1, 2) == 1 else 'O'
    score_text = font.render('Score: ({}) {} - {} ({})'
                             .format(joueur_x, score[joueur_x], score[joueur_o], joueur_o), True, (255, 255, 255))
    score_text_Rect = score_text.get_rect()
    score_text_Rect.center = (GetSystemMetrics(0) // 2, GetSystemMetrics(1) // 2.5)
    ecran.blit(score_text, score_text_Rect)
    if tour == 'O' and mode == 'pc':
        jouer(tour, grille)
    while jeu:
        affiche_grille()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for rectangle in grille:
                    if type(rectangle) == pygame.Rect and rectangle.collidepoint(event.pos):
                        affiche_grille()
                        jouer(tour, grille, rectangle)
            elif event.type == pygame.QUIT:
                jeu = False
                pygame.quit()


def creer_grille() -> list:
    """
    Fonction qui permet de créer la Grille
    """
    cases = []
    taille_case = (GetSystemMetrics(0) - GetSystemMetrics(1)) / 10
    colonne = int(GetSystemMetrics(0) / 10)
    for x in range(0, colonne, int(taille_case)):
        ligne = 3
        for y in range(0, GetSystemMetrics(1), int(taille_case)):
            if ligne > 0:
                rect = pygame.Rect(x + (GetSystemMetrics(0) / 2.25), y + (GetSystemMetrics(1) / 8),
                                   taille_case, taille_case)
                pygame.draw.rect(ecran, (255, 255, 255), rect, 3)
                cases.append(rect)
                ligne = ligne - 1
    return cases


def affiche_grille() -> None:
    """
    Fonction qui permet d'afficher la Grille avec et sans numéros
    """
    pygame.display.flip()


def jouer(j: str, g: list, r: pygame.Rect = None) -> None:
    """
    Fonction qui permet à l'un des joueurs de jouer sur la Grille
    :param j: Joueur
    :param g: Grille
    :param r: Rectangle (facultatif)
    """
    global tour
    image_x = pygame.image.load("assets/x.png").convert_alpha()
    image_o = pygame.image.load("assets/o.png").convert_alpha()
    if not r:
        case = random.randrange(len(g))
        if type(g[case]) == pygame.Rect:
            image_x = pygame.transform.scale(image_x, (g[case].width, g[case].height))
            image_o = pygame.transform.scale(image_o, (g[case].width, g[case].height))
            ecran.blit(image_x, (g[case].topleft, g[case].bottomright)) if tour == 'X' else ecran.blit(
                image_o, (g[case].topleft, g[case].bottomright))
            g[case] = j
            tour = 'X' if j == 'O' else 'O'
        else:
            jouer(j, g)
            return
    else:
        case = g.index(r)
        image_x = pygame.transform.scale(image_x, (g[case].width, g[case].height))
        image_o = pygame.transform.scale(image_o, (g[case].width, g[case].height))
        ecran.blit(image_x, (g[case].topleft, g[case].bottomright)) if tour == 'X' \
            else ecran.blit(image_o, (g[case].topleft, g[case].bottomright))
        g[case] = j
        tour = 'X' if j == 'O' else 'O'
    affiche_grille()
    if victoire(g):
        score[joueur_x if j == 'X' else joueur_o] += 1
        messagebox.showinfo('Morpion',
                            'Le joueur {} qui était {} a gagné !\nScore: ({}) {} - {} ({})'
                            .format(j, joueur_x if j == 'X' else joueur_o, joueur_x, score[joueur_x],
                                    score[joueur_o], joueur_o))
        main(True) if messagebox.askyesno('Morpion', "Voulez-vous recommencer cette partie ?") else main() \
            if messagebox.askyesno('Morpion', "Voulez-vous commencer une nouvelle partie ?") else exit()
    elif egalite(g):
        messagebox.showinfo('Morpion', 'Vous avez fait égalité.\nScore: ({}) {} - {} ({})'
                            .format(joueur_x, score[joueur_x], score[joueur_o], joueur_o))
        main(True) if messagebox.askyesno('Morpion', "Voulez-vous recommencer cette partie ?") else main() \
            if messagebox.askyesno('Morpion', "Voulez-vous commencer une nouvelle partie ?") else exit()
    if mode == 'pc' and j == 'X':
        jouer('O', g)
    affiche_grille()


def egalite(g: list) -> bool:
    """
    Fonction qui vérifie si la situation d'égalité est présente dans la grille
    :param g: Grille
    :return: Valeur Booléenne
    """
    assert (type(g) == list)
    for c in g:
        if type(c) == pygame.Rect:
            return False
    return True


def victoire(g: list) -> bool:
    """
    Fonction qui vérifie si la situation de victoire est présente pour l'un des
    joueurs
    :param g: Grille
    :return: Valeur Booléenne
    """
    assert (type(g) == list)
    cases_alignes = [
        # COLONNES
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],

        # LIGNES
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],

        # DIAGONALES
        [0, 4, 8],
        [2, 4, 6],
    ]

    for alignement in cases_alignes:
        if (g[alignement[0]] == "X" and g[alignement[1]] == "X" and g[alignement[2]] == "X") ^ (
                g[alignement[0]] == "O" and g[alignement[1]] == "O" and g[alignement[2]] == "O"):
            return True
    return False


main()
