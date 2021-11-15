import random
from dataclasses import dataclass
import copy

import sys
import numpy as np
import const
from tkinter import *


@dataclass
class Cesta:
    zoznam_miest: []
    dlzka_cesty: float = 0
    fitness: int = 0    # fitness cesty je pomer k prvej vygenerovanej & 1-pomer

    def __init__(self, zoznam, dlzka: float):
        self.zoznam_miest = zoznam
        self.dlzka_cesty = dlzka


polohy_miest = [[0 for i in range(2)] for j in range(const.POCET_MIEST)]
najkratsia_cesta: Cesta
zaciatocna_cesta: float = 0   # dlzka zaciatocnej cesty pre urcenie fitness funkcie
cislo_generacie: int = 0

tabu_list = []
rodicia = []
potomkovia = []


def vypocitaj_dlzku(stav):
    dlzka: int = 0
    # prejde vsetky mesta
    for mesto in range(const.POCET_MIEST-1):
        mesto1 = np.array(polohy_miest[stav[mesto]])
        mesto2 = np.array(polohy_miest[stav[mesto + 1]])
        dlzka += np.linalg.norm(mesto1 - mesto2)

    # print("index mimo cyklu", mesto+1, stav, polohy_miest[stav[mesto+1]], polohy_miest[stav[0]],'\n')
    # doratanie cesty z posledneho mesta do prveho
    mesto1 = np.array(polohy_miest[stav[mesto+1]])
    mesto2 = np.array(polohy_miest[stav[0]])
    dlzka += np.linalg.norm(mesto1 - mesto2)

    return dlzka


def vypocitaj_fitness(dlzka: float):
    fitness = dlzka/zaciatocna_cesta
    fitness = (1 - fitness)
    # cesta je dlhsia ako zaciatocna, najnizsi fitnes
    if fitness < 0:
        return 0.01

    return fitness + 0.1


def swap(rodic, pozicia_prve: int, pozicia_druhe: int):
    #potomok = copy.deepcopy(rodic)
    potomok = Cesta(np.array(rodic.zoznam_miest), rodic.dlzka_cesty)
    potomok.fitness = rodic.fitness
    #dlzka_cesty = rodic.dlzka_cesty
    #fitness = rodic.fitness
    #for mesto in rodic.zoznam_miest:
    #   zoznam_miest.append(mesto)

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
    zaciatocna_cesta = najkratsia_cesta.dlzka_cesty

    print("Zaciatocna dlzka: %.2f" % najkratsia_cesta.dlzka_cesty)


def prva_generacia(rodic):
    global cislo_generacie, potomkovia

    # kazde mesto vymeni s kazdym dalsim
    for mesto in range(const.POCET_MIEST):
        for permutacia in range(mesto, const.POCET_MIEST):
            if permutacia != mesto:
                nova_cesta = swap(rodic, permutacia, mesto)
                nova_cesta.dlzka_cesty = vypocitaj_dlzku(nova_cesta.zoznam_miest)
                nova_cesta.fitness = vypocitaj_fitness(nova_cesta.dlzka_cesty)
               # print("NOVA", nova_cesta)
                potomkovia.append(nova_cesta)

    cislo_generacie += 1


def je_tabu(stav):
    global tabu_list
    for tabu_stav in tabu_list:
        prorovanenie = tabu_stav.zoznam_miest == stav.zoznam_miest
        if prorovanenie.all():
           # print("TABU ", stav)
            return True
    return False


def skontroluj_najkratsiu():
    global tabu_list, najkratsia_cesta, potomkovia
    najlepsia: Cesta = Cesta(najkratsia_cesta.zoznam_miest, najkratsia_cesta.dlzka_cesty)
    druha_najelpsia: Cesta = Cesta([], const.MAX_INT)

    for potomok in potomkovia:
        if je_tabu(potomok) is False and najlepsia.dlzka_cesty < potomok.dlzka_cesty < druha_najelpsia.dlzka_cesty:
            druha_najelpsia = potomok

        if je_tabu(potomok) is False and potomok.dlzka_cesty < najlepsia.dlzka_cesty:
            #najkratsia_cesta.dlzka_cesty = potomok.dlzka_cesty
            #najkratsia_cesta.zoznam_miest = potomok.zoznam_miest
            #najkratsia_cesta.fitness = potomok.fitness
            najlepsia = potomok

    if najlepsia.dlzka_cesty != najkratsia_cesta.dlzka_cesty:
       # print("novy najkratsi ", najlepsia)
        najkratsia_cesta = najlepsia
        tabu_list.append(najlepsia)

    else:
        #print("RUHY novy najkratsi ", druha_najelpsia)
        najkratsia_cesta = druha_najelpsia
        tabu_list.append(druha_najelpsia)
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

   # print("VYSLA SOM Z CYKLU ", mesto)
    mesto += 1
    x = polohy_miest[stav[mesto]][0] * 2
    y = polohy_miest[stav[mesto]][1] * 2
    Label(canvas, text=stav[mesto], bg="green").place(x=x-5, y=y-5)

    b = np.array(polohy_miest[stav[0]])
    canvas.create_line(x, y, 2*b[0], 2*b[1], fill="blue")
    canvas.mainloop()


def vyber_najlepsich_ruletou():
    global potomkovia, rodicia
    rodicia = []

    # scita fitness hodnoty vsetkych potomkov, vygeneruje nahodne cislo z <0 - sucet fitnes>
    for novy_rodic in range(const.POCET_RODICOV):
        # v prvej generacii je v momentalnej implementacii const.POCET_MIEST/2 potomkov
        if cislo_generacie == 1 and const.POCET_RODICOV >= int(const.POCET_MIEST/2):
            for potomok in potomkovia:
                rodicia.append(potomok)
            print("je ich viac no a co")
            return

        print("VYBERAM R c. ", novy_rodic)
        sucet_fitness = sum([potomok.fitness for potomok in potomkovia])
        vyber = random.uniform(0, sucet_fitness)
        print(sucet_fitness, "VYBER", vyber)

        aktualny: float = 0
        for potomok in enumerate(potomkovia):
            #print(potomok, "F", potomok[1].fitness)
            aktualny += potomok[1].fitness
            if vyber <= aktualny:
                print("VYLOSOVANY ", potomok[1])
                rodicia.append(potomok[1])
                #print("PRED ", potomkovia)
                potomkovia = np.delete(potomkovia, potomok[0])
                #print("PO ", potomkovia)
                break


def maximum(pole):
    max = 0
    for cislo in pole:
        if cislo > max:
            max = cislo

    return max


def vyber_najlepsich_turnajom():
    global potomkovia, rodicia
    rodicia = []
    vylosovany = []

    # scita fitness hodnoty vsetkych potomkov, vygeneruje nahodne cislo z <0 - sucet fitnes>
    if len(potomkovia) > const.POCET_RODICOV:
        print("TU TU")
        for novy_rodic in range(const.POCET_RODICOV):
            while len(vylosovany) <= const.N_TICE:
                na_losovanie = random.randint(0, len(potomkovia) - 1)
                if najdi_v_poli(na_losovanie, vylosovany) is False:
                    vylosovany.append(na_losovanie)

            print("VYLOSOVANY ", vylosovany)
            max_fitness = 0

            # vybratie potomka s najlepsim fitness
            for na_losovanie in vylosovany:
                if potomkovia[na_losovanie].fitness > max_fitness:
                    max_fitness = potomkovia[na_losovanie].fitness
                    novy_najlepsi = potomkovia[na_losovanie]

            # postupne odstranenie potomkov od najvacsieho indexu
            #for vybrany in range(0, const.N_TICE):
            #    max = maximum(vylosovany)
            #    print("MAZEM", vylosovany, max)
            #    potomkovia = np.delete(potomkovia, max)
            #    vylosovany.remove(max)
            print("potomkovia pred ", potomkovia)
            print("VYLOSOVANY ", vylosovany )
            potomkovia = np.delete(potomkovia, vylosovany)
            vylosovany.clear()
            print("potomkovia po ", potomkovia)
            print("VYBRAL SOM ", novy_najlepsi, "Z ", )
            rodicia.append(novy_najlepsi)

        #if len(potomkovia) % 3 == 0:
        #    r1 = r2 = r3 = 0
        #    print("dlzka 3", len(potomkovia))
        #    while r1 == r2 or r2 == r3 or r3 == r1:
        #        r1 = random.randint(0, len(potomkovia) - 1)
        #        r2 = random.randint(0, len(potomkovia) - 1)
        #        r3 = random.randint(0, len(potomkovia) - 1)

        #else:
        #    r1 = r2 = 0
        #    print("dlzka ", len(potomkovia))
        #    while r1 == r2:
        #        r1 = random.randint(0, len(potomkovia) - 1)
        #        r2 = random.randint(0, len(potomkovia) - 1)

        #print("r1 ", r1, 'r2 ', r2)


def najdi_v_poli(hladane, pole):
    for cislo in pole:
        if hladane == cislo:
            return True

    return False


def prve_chybajuce(pole, rozsah):
    for cislo in range(rozsah):
        if najdi_v_poli(cislo, pole) is False:
            return cislo

    return -1


def sparuj_rodicov(rodic1, rodic2):
    global potomkovia, rodicia
    vymeneny_index = []

    for novy_potomok in range(const.POCET_POTOMKOV):
        novy1 = []
        novy2 = []
        #prva_polka1 = []
        #prva_polka2 = []

        # -3 aby mala vyznam -> vymenia sa minimalne 2 mesta
        index_na_vymenu = random.randint(0, const.POCET_MIEST-3)
       # print(rodic1, rodic2, "na vymenu ", index_na_vymenu)

        # osetrenenie vytvorenia potomkov s vymenou na rovnakom indexe
        if najdi_v_poli(index_na_vymenu, vymeneny_index) is True:
            if const.POCET_POTOMKOV > const.POCET_MIEST - 3:    # osetrenie nekonecneho cyklu
              #  print("NIECO SA POKAZILO ")
                break
            while najdi_v_poli(index_na_vymenu, vymeneny_index) is True:
               # print("zhoduje sa ", index_na_vymenu)
                index_na_vymenu = random.randint(0, const.POCET_MIEST - 3)

        vymeneny_index.append(index_na_vymenu)

        prva_polka1 = rodic1.zoznam_miest[:vymeneny_index[novy_potomok]]
        druha_polka1 = rodic1.zoznam_miest[vymeneny_index[novy_potomok]:]

        prva_polka2 = rodic2.zoznam_miest[:vymeneny_index[novy_potomok]]
        druha_polka2 = np.array(rodic2.zoznam_miest[vymeneny_index[novy_potomok]:])

        for mesto in range(0, vymeneny_index[novy_potomok]):
            novy1.append(prva_polka1[mesto])
            novy2.append(prva_polka2[mesto])

        # doplnim prveho
        for nezmenene in range(0, const.POCET_MIEST - vymeneny_index[novy_potomok]):
            # print("doplnam zvysok pola")
            # osetrenie dvoch rovnakych miest v ceste
            #print('mam doplnit ', druha_polka2[nezmenene], novy1)
            if najdi_v_poli(druha_polka2[nezmenene], novy1) is False:
                #print('HLADAM ', druha_polka2[nezmenene], novy1)
                novy1.append(druha_polka2[nezmenene])
            else:
                chybajuce = prve_chybajuce(novy1, const.POCET_MIEST)
                if chybajuce >= 0:
                    novy1.append(chybajuce)
                else:
                    exit("doplnanie pola zlyhalo")
        novy1 = np.array(novy1)

        for nezmenene in range(0, const.POCET_MIEST - vymeneny_index[novy_potomok]):
            # print("doplnam zvysok pola")
            # osetrenie dvoch rovnakych miest v ceste
            #print('mam doplnit ', druha_polka2[nezmenene], novy1)
            if najdi_v_poli(druha_polka1[nezmenene], novy2) is False:
                #print('HLADAM ', druha_polka2[nezmenene], novy1)
                novy2.append(druha_polka1[nezmenene])
            else:
                chybajuce = prve_chybajuce(novy2, const.POCET_MIEST)
                if chybajuce >= 0:
                    novy2.append(chybajuce)
                else:
                    exit("doplnanie pola zlyhalo")
        novy2 = np.array(novy2)

        cesta = Cesta(novy1, vypocitaj_dlzku(novy1))
        cesta.fitness = vypocitaj_fitness(cesta.dlzka_cesty)
        potomkovia = np.append(potomkovia, cesta)

        cesta = Cesta(novy2, vypocitaj_dlzku(novy2))
        cesta.fitness = vypocitaj_fitness(cesta.dlzka_cesty)
        potomkovia = np.append(potomkovia, cesta)

      #  print("X ", vymeneny_index[novy_potomok], "POLKA ", prva_polka1, "druha", druha_polka2, novy1)

       # print("X ", vymeneny_index[novy_potomok], "POLKA ", prva_polka2, "druha", druha_polka1, novy2)

    while len(vymeneny_index) < const.POCET_POTOMKOV:
      #  print("NEMAM POTOMKOV")
        break


def nova_generacia():
    global rodicia, cislo_generacie, potomkovia
    cislo_generacie += 1
    # nahodne sparuje rodicov, pokial ich je nepar a jeden ostane tak mu prehodi mesta
    for rodic in range(int(const.POCET_RODICOV / 2)):
        if len(rodicia) < 2:
            break
        r1 = r2 = 0
        while r1 == r2:
            r1 = random.randint(0, len(rodicia)-1)
            r2 = random.randint(0, len(rodicia)-1)
      #  print(r1, r2, rodicia, len(rodicia))

       # print("r1, r2 ", r1, r2)
        rodic1 = rodicia[r1]
        rodic2 = rodicia[r2]

        sparuj_rodicov(rodic1, rodic2)

        # mesto s vacsim indexom sa musi mazat ako prve
        if r1 > r2:
            rodicia = np.delete(rodicia, r1)
            rodicia = np.delete(rodicia, r2)
        elif r1 < r2:
            rodicia = np.delete(rodicia, r2)
            rodicia = np.delete(rodicia, r1)

       # print("R1: ", rodic1, "R2: ", rodic2, "DLZKA ", rodicia, len(rodicia))


if __name__ == '__main__':

    if const.POCET_MIEST == 1:
        exit("Neexistuje cesta")
    elif const.POCET_MIEST == 2 or const.POCET_MIEST == 3:
        exit("Existuje iba 1 cesta")

   # vygeneruj_mesta()
    nacitaj_mesta()

    while cislo_generacie < const.POCET_GENERACII:
        prva_generacia(najkratsia_cesta)
        # kontrola vytvorenych potomkov, ci nie je nova najkratsia
        print("___", cislo_generacie, len(potomkovia), najkratsia_cesta)

        # prejde potomkov a vyberie najelpsieho - dalej bude generovat jeho susedov
        skontroluj_najkratsiu()
        potomkovia.clear()

    print("\nnajkratsia ", najkratsia_cesta)
    print('\ntabu ', tabu_list)
    print("Generacie ", cislo_generacie)

    nakresli_cestu(najkratsia_cesta.zoznam_miest)
