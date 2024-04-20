import HTTavoiteKirjasto

def valikko():
    print("Valitse haluamasi toiminto:")
    print("1) Lue tiedosto")
    print("2) Analysoi")
    print("3) Kirjoita tiedosto")
    print("4) Analysoi viikonpäivittäiset sademäärät")
    print("5) Lue ja yhdistä Korkeasaari tiedosto")
    print("6) Kirjoita yhdistetty data tiedostoon")
    print("7) Analysoi viikoittaiset kävijämäärät")
    print("0) Lopeta")
    Syote = input("Anna valintasi: ")
    try:
        Valinta = int(Syote)
    except ValueError:
        Valinta = -1
    return Valinta

def paaohjelma():
    RiviTiedot = []
    AnalysoidutPaivat = []
    AnalysoidutKategoriat = []
    TulosteetLista = []
    YhdistettyLista = []
    Valinta = None

    while (Valinta != 0):
        Valinta = valikko()

        if (Valinta == 1):
            Nimi = HTTavoiteKirjasto.kysyNimi("Anna luettavan tiedoston nimi: ")
            RiviTiedot = HTTavoiteKirjasto.lueTiedosto(Nimi, RiviTiedot)
        elif (Valinta == 2):
            if (len(RiviTiedot) > 0):
                AnalysoidutPaivat = HTTavoiteKirjasto.analysoiPaivat(RiviTiedot, AnalysoidutPaivat)
                AnalysoidutKategoriat = HTTavoiteKirjasto.analysoiKategoriat(AnalysoidutPaivat, AnalysoidutKategoriat)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
        elif (Valinta == 3):
            if ((len(AnalysoidutPaivat) > 0) and (len(AnalysoidutKategoriat) > 0)):
                Nimi = HTTavoiteKirjasto.kysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                TulosteetLista = HTTavoiteKirjasto.muotoileTuloste(AnalysoidutPaivat, AnalysoidutKategoriat, TulosteetLista)
                HTTavoiteKirjasto.kirjoitaTiedosto(Nimi, TulosteetLista)
            else:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.")
        elif (Valinta == 4):
            if (len(RiviTiedot) > 0):
                TulosteetLista = HTTavoiteKirjasto.analysoiViikonpaivat(RiviTiedot, TulosteetLista)
                Nimi = HTTavoiteKirjasto.kysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                HTTavoiteKirjasto.kirjoitaTiedosto(Nimi, TulosteetLista)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
        elif (Valinta == 5):
            if (len(AnalysoidutPaivat) > 0):
                Nimi = HTTavoiteKirjasto.kysyNimi("Anna luettavan tiedoston nimi: ")
                YhdistettyLista = HTTavoiteKirjasto.yhdistaKavijat(Nimi, AnalysoidutPaivat, YhdistettyLista)
            else:
                print("Lue sademäärät ennen kävijämäärätietoja.")
        elif (Valinta == 6):
            if (len(YhdistettyLista) > 0):
                Nimi = HTTavoiteKirjasto.kysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                TulosteetLista = HTTavoiteKirjasto.muotoileYhdistettyTuloste(YhdistettyLista, TulosteetLista)
                HTTavoiteKirjasto.kirjoitaTiedosto(Nimi, TulosteetLista)
            else:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.")
        elif (Valinta == 7):
            if (len(YhdistettyLista) > 0):
                TulosteetLista = HTTavoiteKirjasto.analysoiKuukaudet(YhdistettyLista, TulosteetLista)
                Nimi = HTTavoiteKirjasto.kysyNimi("Anna kirjoitettavan tiedoston nimi: ")
                HTTavoiteKirjasto.kirjoitaTiedosto(Nimi, TulosteetLista)
            else:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.")
        elif (Valinta == 0):
            print("Lopetetaan.")
            RiviTiedot.clear()
            AnalysoidutPaivat.clear()
            AnalysoidutKategoriat.clear()
            TulosteetLista.clear()
            YhdistettyLista.clear()
        else:
            print("Tuntematon valinta, yritä uudestaan.")
        print()
    print("Kiitos ohjelman käytöstä.")
    return None

paaohjelma()
