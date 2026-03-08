matrice = [
[0,0,0],
[0,1,0],
[0,0,0]
]

def afficher():
    for ligne in matrice:
        print(ligne)

def trouver_joueur():
    for i in range(3):
        for j in range(3):
            if matrice[i][j] == 1:
                return i,j

while True:

    afficher()

    move = input("Direction (w,a,s,d): ")

    i,j = trouver_joueur()

    matrice[i][j] = 0

    if move == "w":
        i -= 1
    elif move == "s":
        i += 1
    elif move == "a":
        j -= 1
    elif move == "d":
        j += 1

    matrice[i][j] = 1