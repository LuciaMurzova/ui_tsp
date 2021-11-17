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

    #def vypocitaj_dlzku(self) -> float:
    #    dlzka: float = 0
    #    # prejde vsetky mesta
    #    for mesto in range(const.POCET_MIEST - 1):
    #        mesto1 = np.array(polohy_miest[self.zoznam_miest[mesto]])
    #        mesto2 = np.array(polohy_miest[self.zoznam_miest[mesto + 1]])
    #        dlzka += np.linalg.norm(mesto1 - mesto2)

        # doratanie cesty z posledneho mesta do prveho
    #    mesto1 = np.array(polohy_miest[self.zoznam_miest[mesto + 1]])
    #    mesto2 = np.array(polohy_miest[self.zoznam_miest[0]])
    #    dlzka += np.linalg.norm(mesto1 - mesto2)
    #    self.dlzka_cesty = dlzka


polohy_miest = [[0 for i in range(2)] for j in range(const.POCET_MIEST)]    # nacitane/vygenerovane polohy
najkratsia_cesta: Cesta
cislo_generacie: int = 0

tabu_list = []
susedia = []            # novy susedia aktualne najkratesej cesty
najdene_hodnoty = []    # vybrane cesty z kazdej generacie - pre vykreslenie grafu hladania


def vypocitaj_dlzku(stav):
    dlzka: int = 0
    # prejde vsetky mesta
    for mesto in range(const.POCET_MIEST-1):
        mesto1 = np.array(polohy_miest[stav[mesto]])
        mesto2 = np.array(polohy_miest[stav[mesto + 1]])
        dlzka += np.linalg.norm(mesto1 - mesto2)

    # doratanie cesty z posledneho mesta do prveho
    mesto1 = np.array(polohy_miest[stav[mesto+1]])
    mesto2 = np.array(polohy_miest[stav[0]])
    dlzka += np.linalg.norm(mesto1 - mesto2)

    return dlzka


def swap(rodic, pozicia_prve: int, pozicia_druhe: int):
    potomok = Cesta(np.array(rodic.zoznam_miest), rodic.dlzka_cesty)
    pozicia_pom = potomok.zoznam_miest[pozicia_prve]
    potomok.zoznam_miest[pozicia_prve] = potomok.zoznam_miest[pozicia_druhe]
    potomok.zoznam_miest[pozicia_druhe] = pozicia_pom
    return potomok


def vygeneruj_mesta():
    global najkratsia_cesta, polohy_miest, zaciatocna_cesta
    zoznam_miest = []

    # vygeneruje nahodne polohy miest podla zadaneho poctu a velkosti mapy
    for mesto in range(const.POCET_MIEST):
        polohy_miest[mesto][0] = random.randint(1, const.VELKOST_PLOCHY)
        polohy_miest[mesto][1] = random.randint(1, const.VELKOST_PLOCHY)
        print(polohy_miest[mesto][0], polohy_miest[mesto][1])
        zoznam_miest.append(mesto)

    najkratsia_cesta = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta.dlzka_cesty = vypocitaj_dlzku(najkratsia_cesta.zoznam_miest)
    #najkratsia_cesta.vypocitaj_dlzku()
    zaciatocna_cesta = najkratsia_cesta.dlzka_cesty

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta.dlzka_cesty)


def nacitaj_mesta():
    global najkratsia_cesta, polohy_miest, zaciatocna_cesta
    zoznam_miest = []

    # vygeneruje nahodne polohy miest podla zadaneho poctu a velkosti mapy
    for mesto in range(const.POCET_MIEST):
    #    polohy_miest[mesto][0] = int(input())
    #    polohy_miest[mesto][1] = int(input())
    #    print(polohy_miest[mesto][0], polohy_miest[mesto][1])
        zoznam_miest.append(mesto)

    polohy_miest = np.loadtxt('vstup.txt', delimiter=' ', dtype=int)

    najkratsia_cesta = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta.dlzka_cesty = vypocitaj_dlzku(najkratsia_cesta.zoznam_miest)
    #najkratsia_cesta.vypocitaj_dlzku()
    zaciatocna_cesta = najkratsia_cesta.dlzka_cesty

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta.dlzka_cesty)


def novy_susedia(rodic):
    global cislo_generacie, susedia

    # kazde mesto vymeni s kazdym dalsim
    for mesto in range(const.POCET_MIEST):
        for permutacia in range(mesto+1, const.POCET_MIEST):
            nova_cesta = swap(rodic, permutacia, mesto)
            nova_cesta.dlzka_cesty = vypocitaj_dlzku(nova_cesta.zoznam_miest)
           # nova_cesta.vypocitaj_dlzku()
            susedia.append(nova_cesta)

    cislo_generacie += 1


def je_tabu(stav):
    global tabu_list
    for tabu_stav in tabu_list:
        prorovanenie = tabu_stav.zoznam_miest == stav.zoznam_miest
        if prorovanenie.all():
            return True
    return False


def skontroluj_najkratsiu():
    global tabu_list, najkratsia_cesta, susedia
    najlepsia: Cesta = Cesta(najkratsia_cesta.zoznam_miest, najkratsia_cesta.dlzka_cesty)
    druha_najelpsia: Cesta = Cesta([], const.MAX_INT)

    for potomok in susedia:
        if je_tabu(potomok) is False and najlepsia.dlzka_cesty < potomok.dlzka_cesty < druha_najelpsia.dlzka_cesty:
            druha_najelpsia = potomok

        if je_tabu(potomok) is False and potomok.dlzka_cesty < najlepsia.dlzka_cesty:
            #najkratsia_cesta.dlzka_cesty = potomok.dlzka_cesty
            #najkratsia_cesta.zoznam_miest = potomok.zoznam_miest
            #najkratsia_cesta.fitness = potomok.fitness
            najlepsia = potomok

    if najlepsia.dlzka_cesty != najkratsia_cesta.dlzka_cesty:
        najkratsia_cesta = najlepsia
        tabu_list.append(najlepsia)
        najdene_hodnoty.append(najlepsia.dlzka_cesty)
    else:
        najkratsia_cesta = druha_najelpsia
        tabu_list.append(druha_najelpsia)
        najdene_hodnoty.append(druha_najelpsia.dlzka_cesty)
    if len(tabu_list) >= const.VELKOST_TABU:
        tabu_list.pop(0)


def nakresli_cestu(stav):
    root = Tk()
    canvas = Canvas(root, width=2 * const.VELKOST_PLOCHY + 20, height=2 * const.VELKOST_PLOCHY + 20)
    canvas.configure(background="black")
    canvas.pack()

    for mesto in range(const.POCET_MIEST-1):
        x = polohy_miest[stav[mesto]][0] * 2
        y = polohy_miest[stav[mesto]][1] * 2
        Label(canvas, text=stav[mesto], bg="green").place(x=x-5, y=y-5)

        b = np.array(polohy_miest[stav[mesto + 1]])
        canvas.create_line(x, y, 2*b[0], 2*b[1], fill="blue")

    mesto += 1
    x = polohy_miest[stav[mesto]][0] * 2
    y = polohy_miest[stav[mesto]][1] * 2
    Label(canvas, text=stav[mesto], bg="green").place(x=x-5, y=y-5)

    b = np.array(polohy_miest[stav[0]])
    canvas.create_line(x, y, 2*b[0], 2*b[1], fill="blue")
    canvas.mainloop()


def maximum(pole):
    max = 0
    for cislo in pole:
        if cislo > max:
            max = cislo

    return max


def najdi_v_poli(hladane, pole):
    for cislo in pole:
        if hladane == cislo:
            return True

    return False


if __name__ == '__main__':

    if const.POCET_MIEST == 1:
        exit("Neexistuje cesta")
    elif const.POCET_MIEST == 2 or const.POCET_MIEST == 3:
        exit("Existuje iba 1 cesta")

    #vygeneruj_mesta()
    nacitaj_mesta()

    while cislo_generacie < const.POCET_GENERACII:
        novy_susedia(najkratsia_cesta)
        # kontrola vytvorenych potomkov, ci nie je nova najkratsia
        print("___", cislo_generacie, len(susedia), najkratsia_cesta)

        # prejde potomkov a vyberie najelpsieho - dalej bude generovat jeho susedov
        skontroluj_najkratsiu()
        susedia.clear()

    print("\nnajkratsia ", najkratsia_cesta)
    print('\ntabu ', tabu_list)
    print("Generacie ", cislo_generacie)

    for stav in tabu_list:
        if stav.dlzka_cesty < najkratsia_cesta.dlzka_cesty:
            najkratsia_cesta.dlzka_cesty = stav.dlzka_cesty

    print("\nnajkratsia ", najkratsia_cesta)
    print('\ntabu ', tabu_list)
    print("Generacie ", cislo_generacie)

    x = []

    for g in range(cislo_generacie):
        x.append(g)

    plt.xlabel('Generacie')
    plt.ylabel('Dlzka cesty')
    plt.plot(x, najdene_hodnoty)
    plt.show()

    nakresli_cestu(najkratsia_cesta.zoznam_miest)