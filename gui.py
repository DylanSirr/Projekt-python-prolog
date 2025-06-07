from pyswip import Prolog
import tkinter as tk
from tkinter import ttk

class KierunkiApp:
    def __init__(self, master):
        self.master = master
        master.title("Dopasowanie kierunków studiów")

        # Pola wyboru
        self.zainteresowania = ['programowanie', 'technologie', 'logiczne_myslenie', 'matematyka',
                                 'fizyka', 'eksperymentowanie', 'czytanie', 'pisanie', 'dyskusje',
                                 'medycyna', 'ekonomia', 'finanse']
        self.przedmioty = ['matematyka', 'fizyka', 'chemia', 'biologia', 'filozofia', 'historia', 'geografia']
        self.cechy = ['logiczne_myslenie', 'kreatywnosc', 'dokladnosc', 'ciekawosc', 'krytyczne_myslenie',
                      'analiza_danych', 'analityczne_myslenie', 'komunikatywnosc']
        self.style = ['praktyka', 'samodzielna_nauka', 'analiza_teoretyczna', 'projekty',
                      'laboratoria', 'czytanie', 'rozmowy']

        self.check_vars = {}
        self.create_checkboxes()

        # Przycisk
        self.button = tk.Button(master, text="Analizuj", command=self.analizuj)
        self.button.pack(pady=10)

        # Wyniki
        self.results = tk.Text(master, height=10, width=50)
        self.results.pack()

        # Prolog
        self.prolog = Prolog()
        self.prolog.consult("rekomendacje.pl")

    def create_checkboxes(self):
        # Kategorie i checkboxy w siatce
        categories = [('Zainteresowania', self.zainteresowania),
                      ('Przedmioty', self.przedmioty),
                      ('Cechy', self.cechy),
                      ('Style', self.style)]
        for category_name, items in categories:
            frame = tk.LabelFrame(self.master, text=category_name)
            frame.pack(fill="x", padx=5, pady=5)
            columns = 4  # ile kolumn checkboxów w jednym wierszu?
            for index, item in enumerate(items):
                var = tk.IntVar()
                cb = tk.Checkbutton(frame, text=item, variable=var)
                row = index // columns
                col = index % columns
                cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)
                self.check_vars[item] = var

    def analizuj(self):
        # Zbieranie wybranych opcji
        zainteresowania = [item for item in self.zainteresowania if self.check_vars[item].get() == 1]
        przedmioty = [item for item in self.przedmioty if self.check_vars[item].get() == 1]
        cechy = [item for item in self.cechy if self.check_vars[item].get() == 1]
        style = [item for item in self.style if self.check_vars[item].get() == 1]

        # Zapytanie do Prologa
        query = f"top5_dopasowania({zainteresowania}, {przedmioty}, {cechy}, {style}, Top5)."
        results = list(self.prolog.query(query, maxresult=1))

        self.results.delete(1.0, tk.END)

        if results:
            top5 = results[0]['Top5']
            if isinstance(top5, list):
                if not top5:
                    top5 = []
                while len(top5) < 5:
                    top5.append(['Brak_danych', 0])
                self.results.insert(tk.END, "TOP 5 kierunków:\n\n")
                for entry in top5:
                    if isinstance(entry, list) and len(entry) == 2:
                        kierunek, wynik = entry
                        self.results.insert(tk.END, f"{kierunek}: {wynik*10}% dopasowania\n")
                    else:
                        self.results.insert(tk.END, "Błąd w strukturze danych.\n")
            else:
                self.results.insert(tk.END, "Błąd: Wynik w nieoczekiwanym formacie.\n")
        else:
            self.results.insert(tk.END, "Brak wyników z Prologa.\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x700")  # kwadratowe okno
    app = KierunkiApp(root)
    root.mainloop()
