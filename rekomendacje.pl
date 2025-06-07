% Fakty: kierunki_studiow(Kierunek, ListaZainteresowan, ListaPrzedmiotow, ListaCech, ListaStylow).
kierunki_studiow('Informatyka', 
    ['programowanie', 'technologie', 'logiczne_myslenie'], 
    ['matematyka', 'fizyka'], 
    ['logiczne_myslenie', 'kreatywnosc'], 
    ['praktyka', 'samodzielna_nauka']).

kierunki_studiow('Matematyka', 
    ['matematyka', 'logiczne_myslenie'], 
    ['matematyka', 'fizyka'], 
    ['logiczne_myslenie', 'dokladnosc'], 
    ['samodzielna_nauka', 'analiza_teoretyczna']).

kierunki_studiow('Automatyka i Robotyka', 
    ['technologie', 'programowanie'], 
    ['fizyka', 'matematyka'], 
    ['kreatywnosc', 'logiczne_myslenie'], 
    ['praktyka', 'projekty']).

kierunki_studiow('Fizyka Techniczna', 
    ['fizyka', 'matematyka', 'eksperymentowanie'], 
    ['fizyka', 'matematyka'], 
    ['dokladnosc', 'logiczne_myslenie'], 
    ['samodzielna_nauka', 'laboratoria']).

kierunki_studiow('Filozofia', 
    ['czytanie', 'pisanie', 'dyskusje'], 
    ['filozofia', 'historia'], 
    ['ciekawosc', 'krytyczne_myslenie'], 
    ['czytanie', 'rozmowy']).

kierunki_studiow('Inżynieria Biomedyczna', 
    ['technologie', 'medycyna'], 
    ['biologia', 'chemia', 'matematyka'], 
    ['kreatywnosc', 'analiza_danych'], 
    ['praktyka', 'projekty']).

kierunki_studiow('Ekonomia', 
    ['ekonomia', 'finanse'], 
    ['matematyka', 'geografia'], 
    ['analityczne_myslenie', 'komunikatywnosc'], 
    ['projekty', 'samodzielna_nauka']).

% Wagi poszczególnych kategorii (możesz dowolnie zmieniać)
waga(zainteresowania, 3).
waga(przedmioty, 2).
waga(cechy, 2).
waga(style, 1).

% Pomocnicze: liczenie wspólnych elementów list
wspolne_elementy([], _, 0).
wspolne_elementy([X|Xs], Lista2, Liczba) :-
    member(X, Lista2),
    !,
    wspolne_elementy(Xs, Lista2, Liczba1),
    Liczba is Liczba1 + 1.
wspolne_elementy([_|Xs], Lista2, Liczba) :-
    wspolne_elementy(Xs, Lista2, Liczba).

% Dopasowanie = suma (wspólnych elementów * waga) dla każdej kategorii
dopasowanie(Kierunek, Zainteresowania, Przedmioty, Cechy, Style, Wynik) :-
    kierunki_studiow(Kierunek, ZInt, ZPrzedm, ZCechy, ZStyle),
    wspolne_elementy(Zainteresowania, ZInt, W1),
    wspolne_elementy(Przedmioty, ZPrzedm, W2),
    wspolne_elementy(Cechy, ZCechy, W3),
    wspolne_elementy(Style, ZStyle, W4),
    waga(zainteresowania, WagaZ),
    waga(przedmioty, WagaP),
    waga(cechy, WagaC),
    waga(style, WagaS),
    Wynik is W1 * WagaZ + W2 * WagaP + W3 * WagaC + W4 * WagaS.

% Obliczanie maksymalnego możliwego dopasowania (do przeskalowania)
maks_dopasowanie(Kierunek, MaxWynik) :-
    kierunki_studiow(Kierunek, ZInt, ZPrzedm, ZCechy, ZStyle),
    waga(zainteresowania, WagaZ),
    waga(przedmioty, WagaP),
    waga(cechy, WagaC),
    waga(style, WagaS),
    length(ZInt, L1),
    length(ZPrzedm, L2),
    length(ZCechy, L3),
    length(ZStyle, L4),
    MaxWynik is L1*WagaZ + L2*WagaP + L3*WagaC + L4*WagaS.

% Top5 kierunków z procentowym dopasowaniem
top5_dopasowania(Zainteresowania, Przedmioty, Cechy, Style, Top5) :-
    findall((Kierunek, Procent),
        (
            kierunki_studiow(Kierunek, _, _, _, _),
            dopasowanie(Kierunek, Zainteresowania, Przedmioty, Cechy, Style, Wynik),
            maks_dopasowanie(Kierunek, MaxWynik),
            (
                MaxWynik > 0
            ->
                Procent is (Wynik / MaxWynik) * 100
            ;
                Procent is 0
            )
        ),
        Wyniki),
    sort(2, @>=, Wyniki, Posortowane),
    take(5, Posortowane, Top5).

% take(N, Lista, Wynik)
take(0, _, []) :- !.
take(_, [], []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N1 is N - 1,
    take(N1, Xs, Ys).
