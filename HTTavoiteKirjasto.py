import time
import sys
import numpy

EROTIN = ";"
KATEGORIA1 = 4.5
KATEGORIA2 = 1.0
KATEGORIA3 = 0.3
KATEGORIA4 = 0.0
VIIKONPAIVAT = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
KUUKAUDET = 12
KATEGORIAT = 4

class DATA:
    Aika = None
    Sademaara = None

class PAIVA:
    Paivamaara = None
    Sademaara = None
    Kategoria = None
    KavijatMustikkamaa = None
    KavijatKauppatori = None
    KavijatHakaniemi = None

def kysyNimi(Kehote):
    Syote = input(Kehote)
    return Syote

def lueTiedosto(Nimi, Tiedot):
    Tiedot.clear()

    try:
        Tiedosto = open(Nimi, "r", encoding="UTF-8")
        Rivi = Tiedosto.readline()
        Rivi = Tiedosto.readline()
        while (len(Rivi) > 0):
            Rivi = Rivi.strip("\n")
            Sarakkeet = Rivi.split(EROTIN)
            Aika = time.strptime(Sarakkeet[0], "%Y.%m.%d %H:%M")
            Data = DATA()
            Data.Aika = Aika
            Data.Sademaara = Sarakkeet[2]
            Tiedot.append(Data)
            Rivi = Tiedosto.readline()
        Tiedosto.close()
    except OSError:
        print("Tiedoston '" + Nimi + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)

    print("Tiedosto '" + Nimi + "' luettu.")
    print("Tiedostosta lisättiin " + str(len(Tiedot)) + " datariviä listaan.")
    return Tiedot

def analysoiPaivat(Tiedot, Tulokset):
    Tulokset.clear()

    NykyinenPaiva = Tiedot[0].Aika
    Summa = 0.0
    for Alkio in Tiedot:
        if (NykyinenPaiva.tm_yday != Alkio.Aika.tm_yday):
            Paiva = PAIVA()
            Paiva.Paivamaara = time.strftime("%d.%m.%Y", NykyinenPaiva)
            Paiva.Sademaara = Summa
            Tulokset.append(Paiva)

            NykyinenPaiva = Alkio.Aika

            Summa = float(Alkio.Sademaara)
        else:
            Summa += float(Alkio.Sademaara)
    Paiva = PAIVA()
    Paiva.Paivamaara = time.strftime("%d.%m.%Y", NykyinenPaiva)
    Paiva.Sademaara = Summa
    Tulokset.append(Paiva)

    print("Päivittäiset summat laskettu " + str(len(Tulokset)) + " päivälle.")
    return Tulokset

def analysoiKategoriat(Tiedot, Tulokset):
    Tulokset.clear()
    Tulokset = [0, 0, 0, 0]

    for Alkio in Tiedot:
        if (Alkio.Sademaara >= KATEGORIA1):
            Tulokset[0] += 1
            Alkio.Kategoria = 1
        elif (Alkio.Sademaara >= KATEGORIA2):
            Tulokset[1] += 1
            Alkio.Kategoria = 2
        elif (Alkio.Sademaara >= KATEGORIA3):
            Tulokset[2] += 1
            Alkio.Kategoria = 3
        elif (Alkio.Sademaara >= KATEGORIA4):
            Tulokset[3] += 1
            Alkio.Kategoria = 4

    print("Päivät kategorisoitu " + str(len(Tulokset)) + " kategoriaan.")
    return Tulokset

def muotoileTuloste(PaivatLista, KategoriatLista, TulosteetLista):
    TulosteetLista.clear()

    Rivi = "Kategoria" + EROTIN + "Päivien lukumäärä:" + "\n"
    TulosteetLista.append(Rivi)
    for i in range(len(KategoriatLista)):
        Rivi = "Kategoria " + str(i + 1) + EROTIN + str(KategoriatLista[i]) + "\n"
        TulosteetLista.append(Rivi)
    
    Rivi = "\n" + "Kaikki päivittäiset sademäärät:" + "\n"
    TulosteetLista.append(Rivi)
    Rivi = "Pvm" + EROTIN + "mm" + "\n"
    TulosteetLista.append(Rivi)
    for Alkio in PaivatLista:
        Rivi = Alkio.Paivamaara + EROTIN + str(round(Alkio.Sademaara, 1)) + "\n"
        TulosteetLista.append(Rivi)

    return TulosteetLista

def kirjoitaTiedosto(Nimi, Lista):
    try:
        Tiedosto = open(Nimi, "w")
        for Rivi in Lista:
            Tiedosto.write(Rivi)
        Tiedosto.close()
    except OSError:
        print("Tiedoston '" + Nimi + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)
    print("Tiedosto '" + Nimi + "' kirjoitettu.")
    return None

def analysoiViikonpaivat(Tiedot, TulosteetLista):
    TulosteetLista.clear()
    ViikonpaivaLista = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    Viikonpaiva = 0

    for Alkio in Tiedot:
        Viikonpaiva = Alkio.Aika.tm_wday
        ViikonpaivaLista[Viikonpaiva] += float(Alkio.Sademaara)

    Rivi = "Viikonpäivä" + EROTIN + "Sadekertymä" + "\n"
    TulosteetLista.append(Rivi)
    for i in range(len(ViikonpaivaLista)):
        Rivi = VIIKONPAIVAT[i] + EROTIN + str(round(ViikonpaivaLista[i], 1)) + "\n"
        TulosteetLista.append(Rivi)

    ViikonpaivaLista.clear()
    return TulosteetLista

def yhdistaKavijat(Nimi, Paivat, Tulokset):
    Tulokset.clear()
    Kavijamaara = 0

    try:
        Tiedosto = open(Nimi, "r", encoding="UTF-8")
        Rivi = Tiedosto.readline()
        Rivi = Tiedosto.readline()
        for Alkio in Paivat:
            Rivi = Rivi.strip("\n")
            Sarakkeet = Rivi.split(EROTIN)
            Mustikkamaa = int(Sarakkeet[1])
            Kauppatori = int(Sarakkeet[2])
            Hakaniemi = int(Sarakkeet[3])
            Kavijamaara += Mustikkamaa + Kauppatori + Hakaniemi
            Alkio.KavijatMustikkamaa = Mustikkamaa
            Alkio.KavijatKauppatori = Kauppatori
            Alkio.KavijatHakaniemi = Hakaniemi
            Tulokset.append(Alkio)
            Rivi = Tiedosto.readline()
        Tiedosto.close()
    except OSError:
        print("Tiedoston '" + Nimi + "' käsittelyssä virhe, lopetetaan.")
        sys.exit(0)

    print("Tiedosto '" + Nimi + "' luettu.")
    print("Tiedot yhdistetty, kävijämäärä on yhteensä " + str(Kavijamaara) + ".")
    return Tulokset

def muotoileYhdistettyTuloste(Lista, TulosteetLista):
    TulosteetLista.clear()

    Rivi = "Pvm" + EROTIN + "Sademäärä" + EROTIN + "Mustikkamaa" + EROTIN + "Kauppatori" + EROTIN + "Hakaniemi" + "\n"
    TulosteetLista.append(Rivi)
    for Alkio in Lista:
        Mustikkamaa = str(Alkio.KavijatMustikkamaa)
        Kauppatori = str(Alkio.KavijatKauppatori)
        Hakaniemi = str(Alkio.KavijatHakaniemi)
        Rivi = Alkio.Paivamaara + EROTIN + str(round(Alkio.Sademaara, 1)) + EROTIN + Mustikkamaa + EROTIN + Kauppatori + EROTIN + Hakaniemi + "\n"
        TulosteetLista.append(Rivi)

    return TulosteetLista

def analysoiKuukaudet(Tiedot, TulosteetLista):
    TulosteetLista.clear()

    MatriisiKavijat = numpy.zeros((KUUKAUDET, KATEGORIAT), float)
    MatriisiPaivat = numpy.zeros((KUUKAUDET, KATEGORIAT), float)
    MatriisiTulos = numpy.zeros((KUUKAUDET, KATEGORIAT), float)
    
    for Alkio in Tiedot:
        AikaLeima = time.strptime(Alkio.Paivamaara, "%d.%m.%Y")
        KuukausiIndeksi = AikaLeima.tm_mon - 1
        KategoriaIndeksi = Alkio.Kategoria - 1
        MatriisiPaivat[KuukausiIndeksi][KategoriaIndeksi] += 1

        Kavijat = Alkio.KavijatMustikkamaa + Alkio.KavijatKauppatori + Alkio.KavijatHakaniemi
        for Sarake in range(KATEGORIAT):
            if (Sarake == KategoriaIndeksi):
                MatriisiKavijat[KuukausiIndeksi][Sarake] += Kavijat

    for Rivi in range(KUUKAUDET):
        for Sarake in range(KATEGORIAT):
            Kavijat = MatriisiKavijat[Rivi][Sarake]
            Paivat = MatriisiPaivat[Rivi][Sarake]
            if ((Kavijat != 0) and (Paivat != 0)):
                MatriisiTulos[Rivi][Sarake] = Kavijat / Paivat

    Rivi = "Kuukausi" 
    for Kategoria in range(KATEGORIAT):
        Rivi += EROTIN + "Kategoria " + str(Kategoria + 1)
    Rivi += "\n"
    TulosteetLista.append(Rivi)

    for x in range(KUUKAUDET):
        AikaLeima = time.strptime(str(x + 1), "%m")
        Aika = time.strftime("%b", AikaLeima)
        Rivi = Aika
        for y in range(KATEGORIAT):
            Rivi += EROTIN + str(round((MatriisiTulos[x][y]), 1))
        Rivi += "\n"
        TulosteetLista.append(Rivi)

    MatriisiKavijat = numpy.delete(MatriisiKavijat, numpy.s_[:], None)
    MatriisiPaivat = numpy.delete(MatriisiPaivat, numpy.s_[:], None)
    MatriisiTulos = numpy.delete(MatriisiTulos, numpy.s_[:], None)

    print("Kuukausikohtaiset sademäärät analysoitu.")
    return TulosteetLista
