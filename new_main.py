import random
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np
import const
from tkinter import *


@dataclass
class Cesta:
    zoznam_miest: []
    dlzka_cesty: float = 0

    def __init__(self, zoznam, dlzka: float):
        self.zoznam_miest = zoznam
        self.dlzka_cesty = dlzka

    def vypocitaj_dlzku(self):
        dlzka: float = 0
        # prejde vsetky mesta
        for mesto in range(const.POCET_MIEST - 1):
            mesto1 = np.array(polohy_miest[self.zoznam_miest[mesto]])
            mesto2 = np.array(polohy_miest[self.zoznam_miest[mesto + 1]])
            dlzka += np.linalg.norm(mesto1 - mesto2)

        # doratanie cesty z posledneho mesta do prveho
        mesto1 = np.array(polohy_miest[self.zoznam_miest[const.POCET_MIEST - 1]])
        mesto2 = np.array(polohy_miest[self.zoznam_miest[0]])
        dlzka += np.linalg.norm(mesto1 - mesto2)
        self.dlzka_cesty = dlzka


polohy_miest = [[0 for i in range(2)] for j in range(const.POCET_MIEST)]    # nacitane/vygenerovane polohy
najkratsia_cesta: Cesta
cislo_iteracie: int = 0

tabu_list = []
susedia = []            # novy susedia aktualne najkratesej cesty
najdene_hodnoty = []    # vybrane cesty z kazdej iteracie - pre vykreslenie grafu hladania
iteracie = []          # ukladanie cisiel iteracii pre nasledne vykreslenie grafu


def swap(rodic, pozicia_prve: int, pozicia_druhe: int):
    potomok = Cesta(np.array(rodic.zoznam_miest), rodic.dlzka_cesty)
    pozicia_pom = potomok.zoznam_miest[pozicia_prve]
    potomok.zoznam_miest[pozicia_prve] = potomok.zoznam_miest[pozicia_druhe]
    potomok.zoznam_miest[pozicia_druhe] = pozicia_pom
    return potomok


def vygeneruj_mesta():
    global najkratsia_cesta, polohy_miest
    zoznam_miest = []

    # vygeneruje nahodne polohy miest podla zadaneho poctu a velkosti mapy
    for mesto in range(const.POCET_MIEST):
        polohy_miest[mesto][0] = random.randint(0, const.VELKOST_PLOCHY)
        polohy_miest[mesto][1] = random.randint(0, const.VELKOST_PLOCHY)
        print(polohy_miest[mesto][0], polohy_miest[mesto][1])
        zoznam_miest.append(mesto)

    najkratsia_cesta = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta.vypocitaj_dlzku()

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta.dlzka_cesty)


def nacitaj_mesta():
    global najkratsia_cesta, polohy_miest
    zoznam_miest = []

    # vytvori zaciatocny zoznam miest 0 - const.POCET_MIEST-1
    for mesto in range(const.POCET_MIEST):
    #    polohy_miest[mesto][0] = int(input())
    #    polohy_miest[mesto][1] = int(input())
        zoznam_miest.append(mesto)

    # nacita polohy miest zo vstupneho suboru
    polohy_miest = np.loadtxt(const.VSTUPNY_SUBOR, delimiter=' ', dtype=int)

    najkratsia_cesta = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta.vypocitaj_dlzku()

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta.dlzka_cesty)


def novy_susedia(rodic):
    global cislo_iteracie, susedia, iteracie

    # kazde mesto vymeni s kazdym dalsim
    for mesto in range(const.POCET_MIEST):
        for permutacia in range(mesto+1, const.POCET_MIEST):
            nova_cesta = swap(rodic, permutacia, mesto)
            nova_cesta.vypocitaj_dlzku()
            susedia.append(nova_cesta)

    cislo_iteracie += 1
    iteracie.append(cislo_iteracie)


def je_tabu(stav: []):
    global tabu_list
    for tabu_stav in tabu_list:
        prorovanenie = tabu_stav.zoznam_miest == stav.zoznam_miest
        if prorovanenie.all():
            return True
    return False


def skontroluj_najkratsiu():
    global tabu_list, najkratsia_cesta, susedia
    najlepsia: Cesta = Cesta(najkratsia_cesta.zoznam_miest, najkratsia_cesta.dlzka_cesty)
    druha_najlepsia: Cesta = Cesta([], const.MAX_INT)

    for potomok in susedia:
        if je_tabu(potomok) is False and najlepsia.dlzka_cesty < potomok.dlzka_cesty < druha_najlepsia.dlzka_cesty:
            druha_najlepsia = potomok

        if je_tabu(potomok) is False and potomok.dlzka_cesty < najlepsia.dlzka_cesty:
            najlepsia = potomok

    if najlepsia.dlzka_cesty != najkratsia_cesta.dlzka_cesty:
        najkratsia_cesta = najlepsia
        tabu_list.append(najlepsia)
        najdene_hodnoty.append(najlepsia.dlzka_cesty)
    else:
        najkratsia_cesta = druha_najlepsia
        tabu_list.append(druha_najlepsia)
        najdene_hodnoty.append(druha_najlepsia.dlzka_cesty)
    if len(tabu_list) >= const.VELKOST_TABU:
        tabu_list.pop(0)


def nakresli_cestu(stav_na_kreslenie: []):
    root = Tk()
    canvas = Canvas(root, width=2 * const.VELKOST_PLOCHY + 20, height=2 * const.VELKOST_PLOCHY + 20)
    canvas.configure(background="black")
    canvas.pack()

    for mesto in range(const.POCET_MIEST-1):
        mesto_x = polohy_miest[stav_na_kreslenie[mesto]][0] * 2
        mesto_y = polohy_miest[stav_na_kreslenie[mesto]][1] * 2
        Label(canvas, text=stav_na_kreslenie[mesto], bg="green").place(x=mesto_x - 5, y=mesto_y - 5)

        dalsie_mesto = np.array(polohy_miest[stav_na_kreslenie[mesto + 1]])
        canvas.create_line(mesto_x, mesto_y, 2*dalsie_mesto[0], 2*dalsie_mesto[1], fill="blue")

    mesto_x = polohy_miest[stav_na_kreslenie[const.POCET_MIEST - 1]][0] * 2
    mesto_y = polohy_miest[stav_na_kreslenie[const.POCET_MIEST - 1]][1] * 2
    Label(canvas, text=stav_na_kreslenie[const.POCET_MIEST - 1], bg="green").place(x=mesto_x - 5, y=mesto_y - 5)

    dalsie_mesto = np.array(polohy_miest[stav_na_kreslenie[0]])
    canvas.create_line(mesto_x, mesto_y, 2*dalsie_mesto[0], 2*dalsie_mesto[1], fill="blue")
    canvas.mainloop()


if __name__ == '__main__':
    if const.POCET_MIEST <= 1:
        exit("Neexistuje cesta")
    elif const.POCET_MIEST == 2 or const.POCET_MIEST == 3:
        exit("Existuje iba 1 cesta")

    #vygeneruj_mesta()
    nacitaj_mesta()

    while cislo_iteracie < const.POCET_ITERACII:
        novy_susedia(najkratsia_cesta)
        # kontrola vytvorenych potomkov, ci nie je nova najkratsia
        print("___", cislo_iteracie, len(susedia), najkratsia_cesta)

        # prejde potomkov a vyberie najelpsieho - dalej bude generovat jeho susedov
        skontroluj_najkratsiu()
        susedia.clear()

    for stav in tabu_list:
        if stav.dlzka_cesty < najkratsia_cesta.dlzka_cesty:
            najkratsia_cesta.dlzka_cesty = stav.dlzka_cesty

    print("\nnajkratsia ", najkratsia_cesta)
    print('\ntabu ', tabu_list)
    print("Iteracie ", cislo_iteracie)

    plt.xlabel('Iteracie')
    plt.ylabel('Dlzka cesty')
    plt.plot(iteracie, najdene_hodnoty)
    plt.show()

    nakresli_cestu(najkratsia_cesta.zoznam_miest)
