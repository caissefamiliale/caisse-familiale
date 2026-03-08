import random

taille = 6

# créer la matrice
grille = [[0]*taille for i in range(taille)]

# position serpent
x = 3
y = 3
grille[x][y] = 1

# nourriture
fx = random.randint(0,taille-1)
fy = random.randint(0,taille-1)
grille[fx][fy] = 2


def afficher():
    for ligne in grille:
        print(ligne)
    print()


while True:

    afficher()

    direction = input("z=haut s=bas q=gauche d=droite : ")

    grille[x][y] = 0

    if direction == "z":
        x -= 1
    elif direction == "s":
        x += 1
    elif direction == "q":
        y -= 1
    elif direction == "d":
        y += 1

    if grille[x][y] == 2:
        print("🍎 nourriture mangée")

    grille[x][y] = 1