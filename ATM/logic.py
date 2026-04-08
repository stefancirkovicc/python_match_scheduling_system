from database import ucitaj_podatke, sacuvaj_podatke


def formatiraj_novac(iznos):
    return f"{iznos:,}".replace(",", ".")


class ATMLogic:
    def __init__(self):
        self.trenutni_korisnik_index = None

    def proveri_pin(self, unet_pin):
        podaci = ucitaj_podatke()

        for i, korisnik in enumerate(podaci["users"]):
            if korisnik["pin"] == unet_pin:
                self.trenutni_korisnik_index = i
                return True

        return False

    def odjava(self):
        self.trenutni_korisnik_index = None

    def vrati_trenutnog_korisnika(self):
        podaci = ucitaj_podatke()

        if self.trenutni_korisnik_index is None:
            return None

        return podaci["users"][self.trenutni_korisnik_index]

    def vrati_ime_korisnika(self):
        korisnik = self.vrati_trenutnog_korisnika()

        if korisnik is None:
            return ""

        return korisnik["ime"]

    def vrati_stanje(self):
        korisnik = self.vrati_trenutnog_korisnika()

        if korisnik is None:
            return 0

        return korisnik["balance"]

    def vrati_transakcije(self):
        korisnik = self.vrati_trenutnog_korisnika()

        if korisnik is None:
            return []

        return korisnik["transactions"]

    def uplati_novac(self, unos):
        if not unos.isdigit():
            return False, "Morate uneti broj."

        iznos = int(unos)

        if iznos <= 0:
            return False, "Iznos mora biti veći od 0."

        podaci = ucitaj_podatke()

        if self.trenutni_korisnik_index is None:
            return False, "Nijedan korisnik nije prijavljen."

        korisnik = podaci["users"][self.trenutni_korisnik_index]
        korisnik["balance"] += iznos
        korisnik["transactions"].append(f"Uplata: {formatiraj_novac(iznos)} RSD")

        sacuvaj_podatke(podaci)

        return True, f"Uspešno ste uplatili {formatiraj_novac(iznos)} RSD."

    def podigni_novac(self, unos):
        if not unos.isdigit():
            return False, "Morate uneti broj."

        iznos = int(unos)

        if iznos <= 0:
            return False, "Iznos mora biti veći od 0."

        podaci = ucitaj_podatke()

        if self.trenutni_korisnik_index is None:
            return False, "Nijedan korisnik nije prijavljen."

        korisnik = podaci["users"][self.trenutni_korisnik_index]

        if iznos > korisnik["balance"]:
            return False, "Nemate dovoljno sredstava na računu."

        korisnik["balance"] -= iznos
        korisnik["transactions"].append(f"Isplata: {formatiraj_novac(iznos)} RSD")

        sacuvaj_podatke(podaci)

        return True, f"Uspešno ste podigli {formatiraj_novac(iznos)} RSD."

    def promeni_pin(self, stari_pin, novi_pin):
        podaci = ucitaj_podatke()

        if self.trenutni_korisnik_index is None:
            return False, "Nijedan korisnik nije prijavljen."

        korisnik = podaci["users"][self.trenutni_korisnik_index]

        if stari_pin != korisnik["pin"]:
            return False, "Trenutni PIN nije ispravan."

        if not novi_pin.isdigit():
            return False, "Novi PIN mora sadržati samo brojeve."

        if len(novi_pin) != 4:
            return False, "Novi PIN mora imati tačno 4 cifre."

        if novi_pin == korisnik["pin"]:
            return False, "Novi PIN ne sme biti isti kao stari."

        for i, drugi_korisnik in enumerate(podaci["users"]):
            if i != self.trenutni_korisnik_index and drugi_korisnik["pin"] == novi_pin:
                return False, "Taj PIN već koristi drugi korisnik."

        korisnik["pin"] = novi_pin
        sacuvaj_podatke(podaci)

        return True, "PIN je uspešno promenjen."