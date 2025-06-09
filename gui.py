from pyswip import Prolog
import tkinter as tk
from tkinter import ttk

class KierunkiApp:
    def __init__(self, master):
        self.master = master
        master.title("Dopasowanie kierunków studiów")

        # Pola wyboru
        self.zainteresowania = [
            'programowanie', 'technologie', 'logiczne_myslenie', 'matematyka',
            'fizyka', 'eksperymentowanie', 'czytanie', 'pisanie', 'dyskusje',
            'medycyna', 'ekonomia', 'finanse', 'biotechnologia', 'psychologia',
            'sztuczna_inteligencja', 'robotyka', 'inżynieria', 'prawo',
            'sztuka', 'muzyka', 'języki_obce', 'socjologia', 'filozofia',
            'zarządzanie', 'marketing', 'geologia', 'architektura',
            'gry_komputerowe', 'badania', 'czlowiek', 'nauka', 'innowacje',
            'zwierzeta', 'budownictwo', 'kosmos', 'analiza'
        ]

        self.przedmioty = [
            'matematyka', 'fizyka', 'chemia', 'biologia', 'filozofia', 'historia',
            'geografia', 'informatyka', 'psychologia', 'ekonomia', 'prawo',
            'sztuka', 'języki_obce', 'zarządzanie', 'statystyka', 'logika',
            'elektronika', 'mechanika', 'anatomia', 'socjologia', 'angielski',
            'wos', 'polski'
        ]

        self.cechy = [
            'logiczne_myslenie', 'kreatywnosc', 'dokladnosc', 'ciekawosc',
            'krytyczne_myslenie', 'analiza_danych', 'analityczne_myslenie',
            'komunikatywnosc', 'cierpliwosc', 'odpowiedzialnosc', 'wytrwalosc',
            'zdolnosci_organizacyjne', 'umiejetnosc_pracy_w_zespole',
            'samodzielnosc', 'adaptacyjnosc', 'empatia', 'otwartosc_na_nowe',
            'systematycznosc', 'abstrakcyjne_myslenie', 'przestrzenne_myslenie',
            'obserwacja', 'odpornosc_na_stres', 'elokwencja', 'przedsiebiorczosc'
        ]

        self.style = [
            'praktyka', 'samodzielna_nauka', 'analiza_teoretyczna', 'projekty',
            'laboratoria', 'czytanie', 'rozmowy', 'praca_w_grupie', 'seminaria',
            'warsztaty', 'prezentacje', 'eksperymenty', 'programowanie',
            'rozwiązywanie_problemów', 'dyskusje_debaty', 'teoria',
            'case_studies', 'pamieciowa', 'symulacje', 'obliczenia', 'debata',
            'analiza'
        ]

        self.check_vars = {}
        self.create_checkboxes()

        self.button = tk.Button(master, text="Analizuj", command=self.analizuj)
        self.button.pack(pady=10)

        self.results = tk.Text(master, height=15, width=80)
        self.results.pack()

        self.prolog = Prolog()
        self.prolog.consult("rekomendacje.pl")

    def create_checkboxes(self):
        categories = [('Zainteresowania', self.zainteresowania),
                      ('Przedmioty', self.przedmioty),
                      ('Cechy', self.cechy),
                      ('Style', self.style)]
        for category_name, items in categories:
            frame = tk.LabelFrame(self.master, text=category_name)
            frame.pack(fill="x", padx=5, pady=5)
            columns = 8  # Zmieniamy na 8 kolumn
            for index, item in enumerate(items):
                var = tk.IntVar()
                cb = tk.Checkbutton(frame, text=item, variable=var)
                row = index // columns
                col = index % columns
                cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)
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
                        self.results.insert(tk.END, f"{kierunek}: {round(wynik*10,1)} punktów\n")
                    else:
                        self.results.insert(tk.END, "Błąd w strukturze danych.\n")
            else:
                self.results.insert(tk.END, "Błąd: Wynik w nieoczekiwanym formacie.\n")
        else:
            self.results.insert(tk.END, "Brak wyników z Prologa.\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x1000")
    app = KierunkiApp(root)
    root.mainloop()
