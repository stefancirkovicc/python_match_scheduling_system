import json

FILE_NAME = "podaci.json"


def ucitaj_podatke():
    with open(FILE_NAME, "r", encoding="utf-8") as fajl:
        return json.load(fajl)


def sacuvaj_podatke(podaci):
    with open(FILE_NAME, "w", encoding="utf-8") as fajl:
        json.dump(podaci, fajl, indent=4, ensure_ascii=False)