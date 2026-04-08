import tkinter as tk
from tkinter import messagebox
from logic import formatiraj_novac


BG_COLOR = "#071426"
CARD_COLOR = "#0d2138"
CARD_BORDER = "#27496d"
TEXT_MAIN = "#f2d39b"
TEXT_SECONDARY = "#d9e6f2"
BUTTON_HOVER = "#16314f"
INPUT_BG = "#10263f"


class ATMGUI:
    def __init__(self, prozor, logic):
        self.prozor = prozor
        self.logic = logic

        self.prozor.title("ATM aplikacija")
        self.prozor.geometry("900x760")
        self.prozor.resizable(False, False)
        self.prozor.configure(bg=BG_COLOR)

        self.pin_entry = None
        self.entry_uplata = None
        self.entry_podizanje = None
        self.entry_stari_pin = None
        self.entry_novi_pin = None

        self.prikazi_login()

    def obrisi_prozor(self):
        for widget in self.prozor.winfo_children():
            widget.destroy()

    def hover_on(self, event):
        event.widget.config(bg=BUTTON_HOVER)

    def hover_off(self, event):
        event.widget.config(bg=CARD_COLOR)

    def bind_enter(self, komanda):
        self.prozor.unbind("<Return>")
        self.prozor.bind("<Return>", lambda event: komanda())

    def napravi_naslov(self, parent, tekst, velicina=20, boja=TEXT_MAIN, pady=(0, 10)):
        label = tk.Label(
            parent,
            text=tekst,
            font=("Arial", velicina, "bold"),
            bg=BG_COLOR,
            fg=boja
        )
        label.pack(pady=pady)
        return label

    def napravi_podnaslov(self, parent, tekst):
        label = tk.Label(
            parent,
            text=tekst,
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        )
        label.pack(pady=(0, 20))
        return label

    def napravi_unos(self, parent, show=None):
        entry = tk.Entry(
            parent,
            font=("Arial", 13),
            justify="center",
            bg=INPUT_BG,
            fg="white",
            insertbackground="white",
            relief="flat",
            width=25,
            show=show
        )
        entry.pack(pady=10, ipady=8)
        return entry

    def napravi_malo_dugme(self, parent, tekst, komanda):
        dugme = tk.Button(
            parent,
            text=tekst,
            font=("Arial", 11, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY,
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            height=2,
            command=komanda,
            cursor="hand2"
        )
        dugme.pack(side="left", padx=10)
        dugme.bind("<Enter>", self.hover_on)
        dugme.bind("<Leave>", self.hover_off)
        return dugme

    def napravi_akcija_karticu(self, parent, levi_naslov, komanda):
        okvir = tk.Frame(
            parent,
            bg=CARD_BORDER,
            bd=0,
            highlightthickness=1,
            highlightbackground=CARD_BORDER
        )
        okvir.pack(pady=6, fill="x")

        dugme = tk.Button(
            okvir,
            text=levi_naslov,
            font=("Arial", 16, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_MAIN,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            anchor="w",
            padx=40,
            pady=16,
            command=komanda,
            cursor="hand2"
        )
        dugme.pack(fill="both")

        dugme.bind("<Enter>", self.hover_on)
        dugme.bind("<Leave>", self.hover_off)

        return dugme

    def napravi_balance_karticu(self, parent, stanje):
        stanje_formatirano = formatiraj_novac(stanje)

        okvir = tk.Frame(
            parent,
            bg=CARD_BORDER,
            bd=0,
            highlightthickness=1,
            highlightbackground=CARD_BORDER
        )
        okvir.pack(pady=(10, 16), fill="x")

        unutra = tk.Frame(okvir, bg=CARD_COLOR)
        unutra.pack(fill="both")

        levo = tk.Frame(unutra, bg=CARD_COLOR)
        levo.pack(side="left", padx=20, pady=18)

        desno = tk.Frame(unutra, bg=CARD_COLOR)
        desno.pack(side="right", padx=20, pady=18)

        label1 = tk.Label(
            levo,
            text="Trenutno stanje",
            font=("Arial", 16, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_SECONDARY
        )
        label1.pack(anchor="w")

        label3 = tk.Label(
            desno,
            text=f"{stanje_formatirano} RSD",
            font=("Arial", 24, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_MAIN
        )
        label3.pack(anchor="e")

    def proveri_pin(self):
        unet_pin = self.pin_entry.get()

        if self.logic.proveri_pin(unet_pin):
            self.prikazi_meni()
        else:
            messagebox.showerror("Greška", "Pogrešan PIN.")

    def prikazi_login(self):
        self.obrisi_prozor()
        self.bind_enter(self.proveri_pin)

        glavni = tk.Frame(self.prozor, bg=BG_COLOR)
        glavni.pack(expand=True)

        self.napravi_naslov(glavni, "ATM aplikacija", 24, TEXT_MAIN, pady=(30, 10))
        self.napravi_podnaslov(glavni, "Unesite PIN za nastavak")

        self.pin_entry = self.napravi_unos(glavni, show="*")
        self.pin_entry.focus_set()

        dugme = tk.Button(
            glavni,
            text="Prijava",
            font=("Arial", 13, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_MAIN,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_MAIN,
            relief="flat",
            bd=0,
            width=22,
            height=2,
            command=self.proveri_pin,
            cursor="hand2"
        )
        dugme.pack(pady=20)

        dugme.bind("<Enter>", self.hover_on)
        dugme.bind("<Leave>", self.hover_off)

    def odjava(self):
        self.logic.odjava()
        self.prikazi_login()

    def prikazi_meni(self):
        self.obrisi_prozor()
        self.prozor.unbind("<Return>")

        stanje = self.logic.vrati_stanje()
        ime = self.logic.vrati_ime_korisnika()

        glavni = tk.Frame(self.prozor, bg=BG_COLOR, padx=30, pady=16)
        glavni.pack(fill="both", expand=True)

        self.napravi_naslov(glavni, "ATM aplikacija", 22, TEXT_MAIN, pady=(0, 8))
        self.napravi_podnaslov(glavni, f"Dobrodošli, {ime}. Izaberite jednu opciju")

        self.napravi_balance_karticu(glavni, stanje)

        self.napravi_akcija_karticu(glavni, "Podizanje novca", self.prikazi_podizanje)
        self.napravi_akcija_karticu(glavni, "Uplata novca", self.prikazi_uplatu)
        self.napravi_akcija_karticu(glavni, "Provera stanja", self.prikazi_stanje)
        self.napravi_akcija_karticu(glavni, "Istorija transakcija", self.prikazi_istoriju)
        self.napravi_akcija_karticu(glavni, "Promena PIN-a", self.prikazi_promenu_pina)

        donji = tk.Frame(glavni, bg=BG_COLOR)
        donji.pack(pady=14)

        self.napravi_malo_dugme(donji, "Odjava", self.odjava)
        self.napravi_malo_dugme(donji, "Izlaz", self.prozor.destroy)

    def prikazi_stanje(self):
        self.obrisi_prozor()
        self.prozor.unbind("<Return>")

        stanje = self.logic.vrati_stanje()

        glavni = tk.Frame(self.prozor, bg=BG_COLOR, padx=30, pady=30)
        glavni.pack(fill="both", expand=True)

        self.napravi_naslov(glavni, "Provera stanja", 22)
        self.napravi_podnaslov(glavni, "Pregled trenutnog stanja računa")

        self.napravi_balance_karticu(glavni, stanje)

        dole = tk.Frame(glavni, bg=BG_COLOR)
        dole.pack(pady=20)

        self.napravi_malo_dugme(dole, "Nazad", self.prikazi_meni)

    def prikazi_uplatu(self):
        self.obrisi_prozor()
        self.bind_enter(self.uplati_novac)

        glavni = tk.Frame(self.prozor, bg=BG_COLOR)
        glavni.pack(fill="both", expand=True)

        centar = tk.Frame(glavni, bg=BG_COLOR)
        centar.place(relx=0.5, rely=0.5, anchor="center")

        self.napravi_naslov(centar, "Uplata novca", 22)
        self.napravi_podnaslov(centar, "Unesite iznos koji želite da uplatite")

        self.entry_uplata = self.napravi_unos(centar)
        self.entry_uplata.focus_set()

        dugmad = tk.Frame(centar, bg=BG_COLOR)
        dugmad.pack(pady=20)

        self.napravi_malo_dugme(dugmad, "Uplati", self.uplati_novac)
        self.napravi_malo_dugme(dugmad, "Nazad", self.prikazi_meni)

    def uplati_novac(self):
        unos = self.entry_uplata.get()
        uspesno, poruka = self.logic.uplati_novac(unos)

        if uspesno:
            messagebox.showinfo("Uspeh", poruka)
            self.prikazi_meni()
        else:
            messagebox.showerror("Greška", poruka)

    def prikazi_podizanje(self):
        self.obrisi_prozor()
        self.bind_enter(self.podigni_novac)

        glavni = tk.Frame(self.prozor, bg=BG_COLOR)
        glavni.pack(fill="both", expand=True)

        centar = tk.Frame(glavni, bg=BG_COLOR)
        centar.place(relx=0.5, rely=0.5, anchor="center")

        self.napravi_naslov(centar, "Podizanje novca", 22)
        self.napravi_podnaslov(centar, "Unesite iznos koji želite da podignete")

        self.entry_podizanje = self.napravi_unos(centar)
        self.entry_podizanje.focus_set()

        dugmad = tk.Frame(centar, bg=BG_COLOR)
        dugmad.pack(pady=20)

        self.napravi_malo_dugme(dugmad, "Podigni", self.podigni_novac)
        self.napravi_malo_dugme(dugmad, "Nazad", self.prikazi_meni)

    def podigni_novac(self):
        unos = self.entry_podizanje.get()
        uspesno, poruka = self.logic.podigni_novac(unos)

        if uspesno:
            messagebox.showinfo("Uspeh", poruka)
            self.prikazi_meni()
        else:
            messagebox.showerror("Greška", poruka)

    def prikazi_istoriju(self):
        self.obrisi_prozor()
        self.prozor.unbind("<Return>")

        transakcije = self.logic.vrati_transakcije()

        glavni = tk.Frame(self.prozor, bg=BG_COLOR, padx=30, pady=30)
        glavni.pack(fill="both", expand=True)

        self.napravi_naslov(glavni, "Istorija transakcija", 22)
        self.napravi_podnaslov(glavni, "Pregled svih uplata i isplata")

        okvir = tk.Frame(
            glavni,
            bg=CARD_BORDER,
            highlightthickness=1,
            highlightbackground=CARD_BORDER
        )
        okvir.pack(fill="both", expand=True, pady=10)

        canvas = tk.Canvas(okvir, bg=CARD_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(okvir, orient="vertical", command=canvas.yview)
        unutra = tk.Frame(canvas, bg=CARD_COLOR)

        unutra.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=unutra, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if len(transakcije) == 0:
            label = tk.Label(
                unutra,
                text="Nema transakcija.",
                font=("Arial", 13),
                bg=CARD_COLOR,
                fg=TEXT_SECONDARY
            )
            label.pack(pady=30)
        else:
            for transakcija in reversed(transakcije):
                label = tk.Label(
                    unutra,
                    text=transakcija,
                    font=("Arial", 13),
                    bg=CARD_COLOR,
                    fg=TEXT_SECONDARY,
                    anchor="w"
                )
                label.pack(fill="x", padx=20, pady=8)

        dole = tk.Frame(glavni, bg=BG_COLOR)
        dole.pack(pady=20)

        self.napravi_malo_dugme(dole, "Nazad", self.prikazi_meni)

    def prikazi_promenu_pina(self):
        self.obrisi_prozor()
        self.bind_enter(self.promeni_pin)

        glavni = tk.Frame(self.prozor, bg=BG_COLOR, padx=30, pady=30)
        glavni.pack(fill="both", expand=True)

        self.napravi_naslov(glavni, "Promena PIN-a", 22)
        self.napravi_podnaslov(glavni, "Unesite trenutni i novi PIN")

        label_stari = tk.Label(
            glavni,
            text="Trenutni PIN",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        )
        label_stari.pack(pady=(10, 5))

        self.entry_stari_pin = self.napravi_unos(glavni, show="*")

        label_novi = tk.Label(
            glavni,
            text="Novi PIN",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_SECONDARY
        )
        label_novi.pack(pady=(10, 5))

        self.entry_novi_pin = self.napravi_unos(glavni, show="*")
        self.entry_stari_pin.focus_set()

        dugmad = tk.Frame(glavni, bg=BG_COLOR)
        dugmad.pack(pady=20)

        self.napravi_malo_dugme(dugmad, "Promeni PIN", self.promeni_pin)
        self.napravi_malo_dugme(dugmad, "Nazad", self.prikazi_meni)

    def promeni_pin(self):
        stari_pin = self.entry_stari_pin.get()
        novi_pin = self.entry_novi_pin.get()

        uspesno, poruka = self.logic.promeni_pin(stari_pin, novi_pin)

        if uspesno:
            messagebox.showinfo("Uspeh", poruka)
            self.prikazi_meni()
        else:
            messagebox.showerror("Greška", poruka)