import tkinter as tk
import random

taille = 10
case = 30

fenetre = tk.Tk()
fenetre.title("Snake - Matrice")

canvas = tk.Canvas(fenetre, width=taille*case, height=taille*case)
canvas.pack()

# matrice
grille = [[0]*taille for i in range(taille)]

# serpent position
x = 5
y = 5
grille[x][y] = 1

# nourriture
fx = random.randint(0,taille-1)
fy = random.randint(0,taille-1)
grille[fx][fy] = 2

direction = "Right"


def dessiner():

    canvas.delete("all")

    for i in range(taille):
        for j in range(taille):

            if grille[i][j] == 1:
                couleur = "green"
            elif grille[i][j] == 2:
                couleur = "red"
            else:
                couleur = "white"

            canvas.create_rectangle(
                j*case, i*case,
                j*case+case, i*case+case,
                fill=couleur,
                outline="black"
            )


def bouger():

    global x,y,fx,fy

    grille[x][y] = 0

    if direction == "Right":
        y += 1
    elif direction == "Left":
        y -= 1
    elif direction == "Up":
        x -= 1
    elif direction == "Down":
        x += 1

    if x == fx and y == fy:
        print("Nourriture mangée")
        fx = random.randint(0,taille-1)
        fy = random.randint(0,taille-1)
        grille[fx][fy] = 2

    grille[x][y] = 1

    dessiner()

    fenetre.after(300,bouger)


def clavier(event):

    global direction

    if event.keysym == "Right":
        direction = "Right"
    elif event.keysym == "Left":
        direction = "Left"
    elif event.keysym == "Up":
        direction = "Up"
    elif event.keysym == "Down":
        direction = "Down"


fenetre.bind("<Key>",clavier)

dessiner()

bouger()

fenetre.mainloop()