from pyswip import Prolog
import tkinter as tk

class KierunkiApp:
    def __init__(self, root, master):
        self.root = root
        self.master = master
        self.root.title("Dopasowanie kierunków studiów")
        self.master.configure(bg="#e6f0ff")

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
            'laboratoria', 'czytanie', 'rozmowy', 'praca_w_zespole', 'seminaria',
            'warsztaty', 'prezentacje', 'eksperymenty', 'programowanie',
            'rozwiązywanie_problemów', 'dyskusje_debaty', 'teoria',
            'case_studies', 'pamięciowa', 'symulacje', 'obliczenia', 'debata',
            'analiza'
        ]

        self.check_vars = {}
        self.create_checkboxes()

        self.button = tk.Button(self.master, text="Analizuj", command=self.analizuj,
                                bg="#4a90e2", fg="white", font=("Arial", 12, "bold"),
                                relief="raised", bd=3, activebackground="#357ABD")
        self.button.pack(pady=8)

        # Ramka na wyniki z przewijaniem
        results_frame = tk.Frame(self.master, bg="#e6f0ff")
        results_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.results = tk.Text(results_frame, height=12, width=60, font=("Arial", 10),
                            bg="#f0f6ff", fg="#003366", bd=2, relief="sunken", wrap="word")
        self.results.pack(side="left", fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.results.config(yscrollcommand=scrollbar_y.set)


        self.prolog = Prolog()
        self.prolog.consult("rekomendacje.pl")

    def create_checkboxes(self):
        categories = [
            ('Zainteresowania', self.zainteresowania),
            ('Przedmioty', self.przedmioty),
            ('Cechy', self.cechy),
            ('Style', self.style)
        ]
        for category_name, items in categories:
            frame = tk.LabelFrame(self.master, text=category_name, bg="#e6f0ff", fg="#003366",
                                  font=("Arial", 11, "bold"))
            frame.pack(fill="x", padx=5, pady=3)
            columns = 6
            for index, item in enumerate(items):
                var = tk.IntVar()
                cb = tk.Checkbutton(frame, text=item, variable=var, bg="#e6f0ff", fg="#003366",
                                    activebackground="#cce0ff", activeforeground="#002244",
                                    font=("Arial", 9))
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
                        wynik_zaokraglony = round(wynik * 10, 2)
                        self.results.insert(tk.END, f"{kierunek}: {wynik_zaokraglony} punktów dopasowania\n")
                    else:
                        self.results.insert(tk.END, "Błąd w strukturze danych.\n")
            else:
                self.results.insert(tk.END, "Błąd: Wynik w nieoczekiwanym formacie.\n")
        else:
            self.results.insert(tk.END, "Brak wyników z Prologa.\n")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x750")

    canvas = tk.Canvas(root, bg="#e6f0ff")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    main_frame = tk.Frame(canvas, bg="#e6f0ff")
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    main_frame.bind("<Configure>", on_frame_configure)

    # Obsługa scrolla kółkiem myszy:
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    app = KierunkiApp(root, main_frame)

    root.mainloop()
