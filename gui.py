from pyswip import Prolog
import tkinter as tk
from tkinter import ttk

class KierunkiApp:
    def __init__(self, master):
        self.master = master
        master.title("Dopasowanie kierunków studiów")

        # Styl okna i widgetów - niebieska stylistyka
        master.configure(bg="#e6f0ff")

        self.zainteresowania = [
            'programowanie', 'technologie', 'logiczne_myslenie', 'matematyka',
            'fizyka', 'eksperymentowanie', 'czytanie', 'pisanie', 'dyskusje',
            'medycyna', 'ekonomia', 'finanse', 'biotechnologia', 'psychologia',
            'sztuczna_inteligencja', 'robotyka', 'inżynieria', 'prawo',
            'sztuka', 'muzyka', 'języki_obce', 'socjologia', 'filozofia',
            'zarządzanie', 'marketing', 'geologia', 'architektura',
            'gry_komputerowe', 'badania', 'człowiek', 'nauka', 'innowacje',
            'zwierzęta', 'budownictwo', 'kosmos', 'analiza'
        ]

        self.przedmioty = [
            'matematyka', 'fizyka', 'chemia', 'biologia', 'filozofia', 'historia',
            'geografia', 'informatyka', 'psychologia', 'ekonomia', 'prawo',
            'sztuka', 'języki_obce', 'zarządzanie', 'statystyka', 'logika',
            'elektronika', 'mechanika', 'anatomia', 'socjologia', 'angielski',
            'wos', 'polski'
        ]

        self.cechy = [
            'logiczne_myslenie', 'kreatywność', 'dokładność', 'ciekawość',
            'krytyczne_myslenie', 'analiza_danych', 'analityczne_myslenie',
            'komunikatywność', 'cierpliwość', 'odpowiedzialność', 'wytrwałość',
            'zdolności_organizacyjne', 'umiejętność_pracy_w_zespole',
            'samodzielność', 'adaptacyjność', 'empatia', 'otwartość_na_nowe',
            'systematyczność', 'abstrakcyjne_myslenie', 'przestrzenne_myslenie',
            'obserwacja', 'odporność_na_stres', 'elokwencja', 'przedsiębiorczość'
        ]

        self.style = [
            'praktyka', 'samodzielna_nauka', 'analiza_teoretyczna', 'projekty',
            'laboratoria', 'czytanie', 'rozmowy', 'praca_w_grupie', 'seminaria',
            'warsztaty', 'prezentacje', 'eksperymenty', 'programowanie',
            'rozwiązywanie_problemów', 'dyskusje_debaty', 'teoria',
            'case_studies', 'pamięciowa', 'symulacje', 'obliczenia', 'debata',
            'analiza'
        ]

        self.check_vars = {}
        self.create_checkboxes()

        self.button = tk.Button(master, text="Analizuj", command=self.analizuj,
                                bg="#4a90e2", fg="white", font=("Helvetica", 12, "bold"),
                                relief="raised", bd=3, activebackground="#357ABD")
        self.button.pack(pady=8)

        # Pole tekstowe z mniejszą czcionką i niebieskim tłem
        self.results = tk.Text(master, height=12, width=60, font=("Helvetica", 10), bg="#f0f6ff", fg="#003366", bd=2, relief="sunken")
        self.results.pack(padx=10, pady=5)

        self.prolog = Prolog()
        self.prolog.consult("rekomendacje.pl")

    def create_checkboxes(self):
        categories = [('Zainteresowania', self.zainteresowania),
                      ('Przedmioty', self.przedmioty),
                      ('Cechy', self.cechy),
                      ('Style', self.style)]
        for category_name, items in categories:
            frame = tk.LabelFrame(self.master, text=category_name, bg="#e6f0ff", fg="#003366",
                                  font=("Helvetica", 11, "bold"))
            frame.pack(fill="x", padx=5, pady=3)
            columns = 6
            for index, item in enumerate(items):
                var = tk.IntVar()
                cb = tk.Checkbutton(frame, text=item, variable=var, bg="#e6f0ff", fg="#003366",
                                    activebackground="#cce0ff", activeforeground="#002244",
                                    font=("Helvetica", 9))
                row = index // columns
                col = index % columns
                cb.grid(row=row, column=col, sticky='w', padx=6, pady=3)
                self.check_vars[item] = var

    def analizuj(self):
        zainteresowania = [item for item in self.zainteresowania if self.check_vars[item].get() == 1]
        przedmioty = [item for item in self.przedmioty if self.check_vars[item].get() == 1]
        cechy = [item for item in self.cechy if self.check_vars[item].get() == 1]
        style = [item for item in self.style if self.check_vars[item].get() == 1]

        query = f"top5_dopasowania({zainteresowania}, {przedmioty}, {cechy}, {style}, Top5)."
        results = list(self.prolog.query(query, maxresult=1))

        self.results.delete(1.0, tk.END)

        if results:
            top5 = results[0]['Top5']
            if isinstance(top5, list):
                while len(top5) < 5:
                    top5.append(['Brak_danych', 0])
                self.results.insert(tk.END, "TOP 5 kierunków:\n\n")
                for entry in top5:
                    if isinstance(entry, list) and len(entry) == 2:
                        kierunek, wynik = entry
                        wynik_zaokraglony = round(wynik, 2)
                        self.results.insert(tk.END, f"{kierunek}: {wynik_zaokraglony} punktów dopasowania\n")
                    else:
                        self.results.insert(tk.END, "Błąd w strukturze danych.\n")
            else:
                self.results.insert(tk.END, "Błąd: Wynik w nieoczekiwanym formacie.\n")
        else:
            self.results.insert(tk.END, "Brak wyników z Prologa.\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x1000")
    app = KierunkiApp(root)
    root.mainloop()
