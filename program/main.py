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
najkratsia_cesta_lokalne: Cesta = Cesta([], 0)
najkratsia_cesta_globalne: Cesta = Cesta([], 0)
cislo_iteracie: int = 0

tabu_list = []
susedia = []                # novy susedia aktualne najkratesej cesty
najlepsie_lokalne = []      # lokalne najlepsie cesty z kazdej iteracie - pre vykreslenie grafu hladania
najlepsie_globalne = []     # globalne najelpsie cesty z kazdej iteracie - pre yvkreslenie grafu
iteracie = []               # ukladanie cisiel iteracii - pre vykreslenie grafu


def swap(rodic: Cesta, pozicia_prve: int, pozicia_druhe: int):
    potomok = Cesta(np.array(rodic.zoznam_miest), rodic.dlzka_cesty)
    pozicia_pom = potomok.zoznam_miest[pozicia_prve]
    potomok.zoznam_miest[pozicia_prve] = potomok.zoznam_miest[pozicia_druhe]
    potomok.zoznam_miest[pozicia_druhe] = pozicia_pom
    return potomok


def vygeneruj_mesta():
    global najkratsia_cesta_lokalne, najkratsia_cesta_globalne, polohy_miest
    zoznam_miest = []

    # vygeneruje nahodne polohy miest podla zadaneho poctu a velkosti mapy
    for mesto in range(const.POCET_MIEST):
        polohy_miest[mesto][0] = random.randint(0, const.SIRKA_PLOCHY)
        polohy_miest[mesto][1] = random.randint(0, const.VYSKA_PLOCHY)
        zoznam_miest.append(mesto)
        print(polohy_miest[mesto][0], polohy_miest[mesto][1])

    # prva cesta je zaroven aj najkratsia
    najkratsia_cesta_lokalne = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta_lokalne.vypocitaj_dlzku()
    najkratsia_cesta_globalne = najkratsia_cesta_lokalne

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta_lokalne.dlzka_cesty)


def nacitaj_mesta():
    global najkratsia_cesta_lokalne, najkratsia_cesta_globalne, polohy_miest
    zoznam_miest = []

    # vytvori zaciatocny zoznam miest 0 - const.POCET_MIEST-1
    for mesto in range(const.POCET_MIEST):
        zoznam_miest.append(mesto)

    # nacita polohy miest zo vstupneho suboru
    polohy_miest = np.loadtxt(const.VSTUPNY_SUBOR, delimiter=' ', dtype=int)

    # osetrenie prazdneho suboru, alebo suboru s menej mestami ako je potrebne
    if len(polohy_miest) < const.POCET_MIEST:
        print('V zadanom subore nie je potrebny pocet miest')
        exit()

    # prva cesta je zaroven aj najkratsia
    najkratsia_cesta_lokalne = Cesta(np.array(zoznam_miest), 0)
    najkratsia_cesta_lokalne.vypocitaj_dlzku()
    najkratsia_cesta_globalne = najkratsia_cesta_lokalne

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta_lokalne.dlzka_cesty)


def novy_susedia(akt_najlepsia: Cesta):
    global cislo_iteracie, susedia, iteracie

    # kazde mesto vymeni s kazdym dalsim
    for mesto in range(const.POCET_MIEST):
        for permutacia in range(mesto+1, const.POCET_MIEST):
            nova_permutacia = swap(akt_najlepsia, permutacia, mesto)    # vytvori novy objekt Cesta s vymeneymi mestami
            nova_permutacia.vypocitaj_dlzku()       # dopocitanie novej dlzky po vymene miest
            susedia.append(nova_permutacia)         # zaradi novu Cestu do zoznamu susedov aktualne najlepsej cesty

    cislo_iteracie += 1
    iteracie.append(cislo_iteracie)


def je_tabu(stav: []):
    global tabu_list
    # prejde cely tabu list, porovnava polohu kazdeho mesta v kontrolovanom stave s mestom v tabu stave
    for tabu_stav in tabu_list:
        porovanenie = tabu_stav.zoznam_miest == stav.zoznam_miest
        # zhoduju sa polohy vsetkych miest v zozname - stav je tabu
        if porovanenie.all():
            return True

    # nenaslo dany stav v zozname
    return False


def najdi_lokalne_najlepsiu():
    global tabu_list, najkratsia_cesta_lokalne, susedia, najkratsia_cesta_globalne, najlepsie_globalne
    # najlepsiu nastavi na lokalne najlepsiu a druhu najlepsiu na max int
    najlepsia: Cesta = Cesta(najkratsia_cesta_lokalne.zoznam_miest, najkratsia_cesta_lokalne.dlzka_cesty)
    druha_najlepsia: Cesta = Cesta([], const.MAX_INT)

    # prechadza vsetky vygenerovane susedne vztahy a hlada lokalne najlepsieho suseda
    for sused in susedia:
        if je_tabu(sused) is False and najlepsia.dlzka_cesty < sused.dlzka_cesty < druha_najlepsia.dlzka_cesty:
            druha_najlepsia = sused

        elif je_tabu(sused) is False and sused.dlzka_cesty < najlepsia.dlzka_cesty:
            najlepsia = sused

    # existuje sused s kratsou cestou, ktory nie je tabu
    if najlepsia.dlzka_cesty < najkratsia_cesta_lokalne.dlzka_cesty:
        najkratsia_cesta_lokalne = najlepsia

        # ak je lokalne najlepsia cesta kratsia ako globalne najlepsia tak ju ulozi
        if najlepsia.dlzka_cesty < najkratsia_cesta_globalne.dlzka_cesty:
            najkratsia_cesta_globalne = najlepsia

    # neexistuje sused s kratsou cestou, ktory nie je tabu; vybera dlhsiu cestu preto aktualnu - kratsiu uklada do tabu
    else:
        tabu_list.append(najkratsia_cesta_lokalne)
        najkratsia_cesta_lokalne = druha_najlepsia

        # odstranenie prveho stavu z tabu pri prekroceni dlzky
        if len(tabu_list) >= const.VELKOST_TABU:
            tabu_list.pop(0)

    najlepsie_lokalne.append(najkratsia_cesta_lokalne.dlzka_cesty)
    najlepsie_globalne.append(najkratsia_cesta_globalne.dlzka_cesty)


def nakresli_cestu(stav_na_kreslenie: []):
    root = Tk()
    canvas = Canvas(root, width=2 * const.SIRKA_PLOCHY + 50, height=2 * const.VYSKA_PLOCHY + 50)
    canvas.configure(background="black")
    canvas.pack()

    for mesto in range(const.POCET_MIEST-1):
        # vykreslenie cisiel miest
        mesto_x = polohy_miest[stav_na_kreslenie[mesto]][0] * 2
        mesto_y = polohy_miest[stav_na_kreslenie[mesto]][1] * 2
        Label(canvas, text=stav_na_kreslenie[mesto], bg="firebrick").place(x=mesto_x, y=mesto_y)
        # vykreslenie ciar medzi aktualnym a nasledujucim mestom
        dalsie_mesto = np.array(polohy_miest[stav_na_kreslenie[mesto + 1]])
        canvas.create_line(mesto_x, mesto_y, 2*dalsie_mesto[0], 2*dalsie_mesto[1], fill="blue")

    # dokreslenie posledneho mesta
    mesto_x = polohy_miest[stav_na_kreslenie[const.POCET_MIEST - 1]][0] * 2
    mesto_y = polohy_miest[stav_na_kreslenie[const.POCET_MIEST - 1]][1] * 2
    Label(canvas, text=stav_na_kreslenie[const.POCET_MIEST - 1], bg="firebrick").place(x=mesto_x, y=mesto_y)
    # dokreslenie ciary medzi poslednym a prvym mestom
    dalsie_mesto = np.array(polohy_miest[stav_na_kreslenie[0]])
    canvas.create_line(mesto_x, mesto_y, 2*dalsie_mesto[0], 2*dalsie_mesto[1], fill="blue")
    canvas.mainloop()


if __name__ == '__main__':
    if const.POCET_MIEST <= 1:
        exit("Neexistuje cesta")
    elif const.POCET_MIEST == 2 or const.POCET_MIEST == 3:
        exit("Existuje iba 1 cesta")

    # NASTAVENIE PRE GENEROVANIE / NACITANIE MIEST
    vygeneruj_mesta()
    #nacitaj_mesta()

    while cislo_iteracie < const.POCET_ITERACII:
        novy_susedia(najkratsia_cesta_lokalne)
        # kontrola vytvorenych potomkov, ci nie je nova najkratsia
        print("___", cislo_iteracie, "pocet susedov: ", len(susedia), najkratsia_cesta_lokalne)

        # prejde potomkov a vyberie najelpsieho - dalej bude generovat jeho susedov
        najdi_lokalne_najlepsiu()
        susedia.clear()

    print("\n Globalne najkratsia ", najkratsia_cesta_globalne)
    print("Iteracie ", cislo_iteracie)

    # vytvorenie grafu
    plt.xlabel('Iteracie')
    plt.ylabel('Dlzka cesty')
    plt.plot(iteracie, najlepsie_lokalne, label='lokalne najlepsia')
    plt.plot(iteracie, najlepsie_globalne, label='globalne najlepsia')
    plt.legend()
    plt.show()

    # nakreslenie globalne najkratsej cesty
    nakresli_cestu(najkratsia_cesta_globalne.zoznam_miest)
