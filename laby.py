# Les bibliothèques utilisées.
import tkinter as Tk
from random import randint
from tkinter import font
import time

# Création d'une cellule.
class Cellule():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visitee = False
        self.murs = {'N': True, 'E': True, 'S': True, 'W': True}
        self.voisins = {'N': None, 'E': None, 'S': None, 'W': None}
# Création de la grille du labyrinthe.
class Grille():
    def __init__(self, l, c):
        self.l = l
        self.c = c
        self.cadrillage = []
        for i in range(self.l):
            grille_ligne = []
            for j in range(self.c):
                grille_ligne.append(Cellule(j, i))
            self.cadrillage.append(grille_ligne)
    # Accès à une cellule donnée.
    def cellule(self, x, y):
        if 0<=x<self.c and 0<=y<self.l:
            return self.cadrillage[y][x]
    
    def add_voisins(self):
        for i in range(self.l):
            for j in range(self.c):
                if j < self.c-1:
                    self.cellule(j, i).voisins['E'] = (j + 1, i)
                if j > 0:
                    self.cellule(j, i).voisins['W'] = (j - 1, i)
                if i < self.l-1:
                    self.cellule(j, i).voisins['S'] = (j, i + 1)
                if i > 0:
                    self.cellule(j, i).voisins['N'] = (j, i - 1)


    # Suppression des murs entre les cellules.
    def effaceMur(self, orientation, coord):
        if orientation == 'N':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 <= coord[1]-1:
                self.cellule(coord[0], coord[1]-1).murs['S'] = False
        if orientation == 'S':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.l > coord[1]+1:
                self.cellule(coord[0], coord[1]+1).murs['N'] = False
        if orientation == 'W':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if 0 <= coord[0]-1:
                self.cellule(coord[0]-1, coord[1]).murs['E'] = False
        if orientation == 'E':
            self.cellule(coord[0],coord[1]).murs[orientation] = False
            if self.c > coord[0]+1:
                self.cellule(coord[0]+1, coord[1]).murs['W'] = False
    # Affichage du labyrinthe.
    def __str__(self):
        """
        Génère une représentation textuelle du labyrinthe.
        """
        laby_lignes = []
        laby_l = ['+']
        for x in range(self.c):
            if self.cadrillage[0][x].murs['N']:
                laby_l.append('---+')
            else :
                laby_l.append('   +')
        laby_lignes.append(''.join(laby_l)) 
        for y in range(0,self.l):
            if self.cadrillage[y][0].murs['W'] :
                laby_l = ['|']
            else :
                laby_l = [' ']
            for x in range(self.c):
                if self.cadrillage[y][x].murs['E']:
                    laby_l.append('   |')
                else:
                    laby_l.append('    ')
            laby_lignes.append(''.join(laby_l))
            laby_l = ['+']
            for x in range(self.c):
                if self.cadrillage[y][x].murs['S']:
                    laby_l.append('---+')
                else:
                    laby_l.append('   +')
            laby_lignes.append(''.join(laby_l))
        #laby_lignes.append('\n')
        return '\n'.join(laby_lignes)

solution = []

#résolution du labyrinthe avec parcour dsf
def dsf(laby, start, end):
    pile = [start]
    path = []
    while pile:
        s = pile.pop()
        laby.cellule(s[0], s[1]).visitee = True
        is_voisin = False
        if s == end:
            path.append(s)
            return path
        for t in laby.cellule(s[0], s[1]).voisins:
            voisin = laby.cellule(s[0], s[1]).voisins[t]
            if voisin != None and laby.cellule(s[0], s[1]).murs[t] == False and laby.cellule(voisin[0], voisin[1]).visitee == False:
                is_voisin = True
                pile.append(voisin)
        
        while not is_voisin and path:
            s = path.pop()
            for t in laby.cellule(s[0], s[1]).voisins:
                voisin = laby.cellule(s[0], s[1]).voisins[t]
                if voisin != None and laby.cellule(s[0], s[1]).murs[t] == False and laby.cellule(voisin[0], voisin[1]).visitee == False:
                    is_voisin = True
                    pile.append(voisin)
        path.append(s)
    return "Erreur"

labyrinthe = Grille(20, 20)

# Génération du labyrinthe avec l'algorithme Sidewinder.
def exploration_sidewinder():
    global labyrinthe
    global solution
    if solution:
        dessiner_soluce(True)
    labyrinthe = Grille(20, 20)
    for i in range(labyrinthe.l):
        deb_parcour = 0
        for j in range(labyrinthe.c):
            destroy = randint(0, 1)
            if (destroy == 0 and j < labyrinthe.c-1) or (i == labyrinthe.l - 1 and j < labyrinthe.c-1):
                labyrinthe.effaceMur('E', (j, i))
            elif i < labyrinthe.l - 1:
                k = randint(deb_parcour, j)
                labyrinthe.effaceMur('S', (k, i))
                deb_parcour = j+1
    labyrinthe.add_voisins()
    solution = dsf(labyrinthe, (0,0), (labyrinthe.c-1,0))
    print(solution)
    return labyrinthe




# Création de la fenêtre.
root = Tk.Tk()
root.title("Générateur et solveur de labyrinthe")
root.geometry("600x600")
root.resizable(False, False)
# Changement du curseur de la fenêtre.
crosshair = "crosshair"
root.config(cursor=crosshair)
root.config(
    bg="#f0f0f0",
    padx=15,
    pady=15
)
# Le canevas de la fenêtre.
canvas = Tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()
canvas.configure(bg="#fffaf0")
# Personnalisation du canevas.
canvas.config(
    borderwidth=5,
    relief="ridge",
    highlightthickness=3,
    highlightbackground="#444444",
    highlightcolor="#ff6600"
)
# Le titre de la fenêtre.  
title_label = Tk.Label(root, text="Générateur et solveur de labyrinthe")
title_label.place(x=300, y=10, anchor="n")
# Personnalisation du titre.
title_label.config(
    fg="#333333",
    bg="#f0f0f0",
    padx=10,
    pady=5,
    borderwidth=2,
    relief="groove",
    font=("Helvetica", 16, "underline", "bold", "italic"),
    highlightthickness=2,
    highlightbackground="#666666",
    highlightcolor="#ff6600",
    )
# Animation du titre
def animation_titre():
    current_color = title_label.cget("fg")
    new_color = "#ff6600" if current_color == "#333333" else "#333333"
    title_label.config(fg=new_color)
    root.after(500, animation_titre)
animation_titre()
def close_window(event=None):
    root.destroy()
root.bind('<Alt-F4>', close_window)
# Création de la barre de menu.
menu_bar = Tk.Menu(root)
file_menu = Tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Quitter", command=close_window)
file_menu.add_command(label="Relancer le programme", command=lambda: root.destroy() or __import__('laby'))
file_menu.add_command(label="Générer un labyrinthe", command=lambda: dessiner_grillage())
menu_bar.add_cascade(label="Fichier", menu=file_menu)
root.config(menu=menu_bar)
# Le carré du labyrinthe.
carre_labyrinthe = canvas.create_rectangle(100, 100, 500, 500, fill="#ffffff", outline="#333333", width=3)
# Un bouton qui génène-ra le labyrinthe.
bouton = Tk.Button(root, text="Générer le labyrinthe", command=lambda: dessiner_grillage())
bouton.place(x=195, y=520, anchor="n")
bouton_soluce = Tk.Button(root, text="Résoudre le labyrinthe", command=lambda: dessiner_soluce())
bouton_soluce.place(x=400, y=520, anchor="n")
# Personnalisation des bouton.
bouton.config(
    fg="#000000",
    bg="#f0f0f0",
    padx=10,
    pady=5,
    borderwidth=2,
    relief="raised",
    font=("Helvetica", 12, "bold", "italic"),
    activebackground="#fffaf0",
    activeforeground="#000000",
    highlightthickness=2,
    highlightbackground="#444444",
    highlightcolor="#ff6600",
    takefocus=True
)
bouton_soluce.config(
    fg="#000000",
    bg="#f0f0f0",
    padx=10,
    pady=5,
    borderwidth=2,
    relief="raised",
    font=("Helvetica", 12, "bold", "italic"),
    activebackground="#fffaf0",
    activeforeground="#000000",
    highlightthickness=2,
    highlightbackground="#444444",
    highlightcolor="#ff6600",
    takefocus=True
)
# Le grillage du labyrinthe :
def dessiner_grillage():
    # fonction qui permet de tracer les murs du labyrinthe avec une marge de 99px et 
    # de longueur 20px en fonction du nombre de colonne et de lignes du labyrinthe
    global labyrinthe
    exploration_sidewinder()
    for i in range(0, labyrinthe.l * 20, 20):
        for j in range(0, labyrinthe.c * 20, 20):
            if labyrinthe.cellule(int(j/20), int(i/20)).murs['E']:
                canvas.create_line(j + 99 + 20, i + 99, j + 20 + 99, i + 20 + 99, fill="#000000")
            else:
                canvas.create_line(j + 20 + 99, i + 99, j + 20 + 99, i + 20 + 99, fill="#FFFFFF")
            if labyrinthe.cellule(int(j/20), int(i/20)).murs["S"]:
                canvas.create_line(j + 99, i + 20 + 99, j + 20 + 99, i + 20 + 99, fill="#000000")
            else:
                canvas.create_line(j + 99, i + 20 + 99, j + 20 + 99, i + 20 + 99, fill="#FFFFFF")
           
    canvas.create_line(99, 99, 99, 499, fill="#ffffff")
    canvas.create_line(99, 99, 499, 99, fill="#ffffff")
    canvas.create_line(99, 499, 499, 499, fill="#ffffff")
    canvas.create_line(499, 99, 499, 499, fill="#ffffff")

def dessiner_soluce(clean=False):
    global solution

    if clean:
        for pos in solution:
            canvas.create_rectangle(pos[0]*20+99+5, pos[1]*20+99+5,
                                    pos[0]*20+99+15, pos[1]*20+99+15,
                                    fill="#FFFFFF", outline="")
    else:
        for pos in solution:
            canvas.create_rectangle(pos[0]*20+99+5, pos[1]*20+99+5,
                                    pos[0]*20+99+15, pos[1]*20+99+15,
                                    fill="#5FFF81", outline="")
        

dessiner_grillage()
# Lancement de la boucle.
root.mainloop()

