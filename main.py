import random
import time


def main(recommencer: bool = False) -> None:
    global mode
    global joueur_x
    global joueur_o
    if not recommencer:
        joueur = input('Voulez-vous jouer contre un Joueur ? (oui / non)')
        joueur_x = input('Quel est le pseudonyme du Joueur X ?')
        if joueur.lower() == 'oui':
            mode = "joueur"
            joueur_o = input('Quel est le pseudonyme du Joueur O ?')
        else:
            mode = "pc"
            joueur_o = 'Ordinateur'
    print(joueur_x, 'versus', joueur_o)
    time.sleep(2)
    grille = creer_grille()
    affiche_grille(grille)
    jouer("X" if random.randint(1, 2) == 1 else "O", grille)


def creer_grille() -> list:
    return [' ' for _ in range(9)]


def affiche_grille(g: list) -> None:
    assert (type(g) == list)

    print("\nNuméros de la Grille de Jeu")

    print("_____________\n| 1 | 2 | 3 |\n| 4 | 5 | 6 |\n| 7 | 8 | 9 |\n_____________")

    print("\nGrille du Jeu")

    print("_____________\n| {} | {} | {} |\n| {} | {} | {} |\n| {} | {} | {} |\n_____________".format(g[0], g[1], g[2],
                                                                                                      g[3], g[4], g[5],
                                                                                                      g[6], g[7], g[8]))


def jouer(j: str, g: list) -> None:
    assert (type(g) == list and type(j) == str and (j == "O" or j == "X"))
    print("Joueur:", j, 'Nom:', joueur_x if j == 'X' else joueur_o)
    case_joueur = random.randrange(len(g)) if mode == 'pc' and j == 'O' else int(
        input('Quelle case voulez-vous jouer ?')) - 1
    case_jeu = g[case_joueur].replace(' ', '')

    if not case_jeu:
        g[case_joueur] = j
        affiche_grille(g)
        if victoire(g):
            print('Le joueur {} qui était {} a gagné !'.format(j, joueur_x if j == 'X' else joueur_o))
            main(True) if input("Voulez-vous recommencer cette partie ?").lower() == "oui" else main() \
                if input("Voulez-vous commencer une nouvelle partie ?").lower() == "oui" else exit()
        elif egalite(g):
            print('Aucun joueur n\'a gagné.')
            main(True) if input("Voulez-vous recommencer cette partie ?").lower() == "oui" else main() \
                if input("Voulez-vous commencer une nouvelle partie ?").lower() == "oui" else exit()
        else:
            jouer('X' if j == 'O' else 'O', g)
    else:
        if mode == 'joueur':
            print("La case mentionnée est occupée, choississez-en une autre.")
        jouer(j, g)


def egalite(g: list) -> bool:
    """
    Fonction qui vérifie si la situation d'égalité est présente dans la grille
    :param g: Grille
    :return: Valeur Booléenne
    """

    assert (type(g) == list)
    e = True
    for c in g:
        if c == ' ':
            e = False
    return e


def victoire(g: list) -> bool:
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
