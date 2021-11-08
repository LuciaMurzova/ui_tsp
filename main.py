import random
import numpy as np
import const
from tkinter import *
#import tkinter as tk

mesta = [[0 for i in range(2)] for j in range(const.POCET_MIEST)]
zoznam = []          # pociatocne usporiadanie miest
zaciatocny_stav = 0  # vektor pre zaciatocne zoradenie 0 - pocet-1
zaciatocna_cesta = 0      # dlzka cesty pri zaciatocnom zoradeni
najkratsia_cesta = 0
najkratsia_cesta_stav = 0


def vygeneruj_mesta(canvas: Canvas):
    global zaciatocny_stav, zaciatocna_cesta
    # nahodne vygeneruje polohu miest, ich poradove cisla uklada do zoznamu
    for mesto in range(const.POCET_MIEST):
        mesta[mesto][0] = random.randint(1, const.VELKOST_PLOCHY)
        mesta[mesto][1] = random.randint(1, const.VELKOST_PLOCHY)
        canvas.create_oval(2*mesta[mesto][0]-5, 2*mesta[mesto][1]-5, 2*mesta[mesto][0]+5, 2*mesta[mesto][1]+5, fill="green")
        #print(mesta[mesto][0], mesta[mesto][1])
        zoznam.append(mesto)

    # vytvorenie vektora zaciatocneho stavu - cisla miest 0 - n-1
    zaciatocny_stav = np.array(zoznam)
    zaciatocna_cesta = vypocitaj_dlzku(zaciatocny_stav, canvas)
    # zaciatocna cesta je moomentalne najkratsia
    najkratsia_cesta = zaciatocna_cesta
    najkratsia_cesta_stav = zaciatocny_stav
    print("ZACIATOCNA DLZKA %.3f" % zaciatocna_cesta)


def vypocitaj_dlzku(stav, canvas: Canvas):
    dlzka = 0
    for mesto in range(const.POCET_MIEST - 1):
        a = np.array(mesta[mesto])
        b = np.array(mesta[mesto+1])
        dlzka += np.linalg.norm(a - b)
        canvas.create_line(2*a[0], 2*a[1], 2*b[0], 2*b[1], fill="blue")

    # pripocitanie cesty z posledneho do prveho mesta
    a = np.array(mesta[mesto+1])
    b = np.array(mesta[0])
    dlzka += np.linalg.norm(a - b)
    canvas.create_line(2*a[0], 2*a[1], 2*b[0], 2*b[1], fill="blue")
    return dlzka


def prva_generacia(zaciatocny_stav):
    


if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, width=2*const.VELKOST_PLOCHY, height=2*const.VELKOST_PLOCHY)
    canvas.configure(background="black")
    canvas.pack()
    vygeneruj_mesta(canvas)

    prva_generacia(zaciatocny_stav)

    root.mainloop()


