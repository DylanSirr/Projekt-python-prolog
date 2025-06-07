% --- Fakty ---
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

kierunki_studiow('Inżynieria Biomedyczna', 
    ['technologie', 'medycyna'], 
    ['biologia', 'chemia', 'matematyka'], 
    ['kreatywnosc', 'analiza_danych'], 
    ['praktyka', 'projekty']).

% --- Wagi ---
waga(zainteresowania, 3).
waga(przedmioty, 2).
waga(cechy, 2).
waga(style, 1).

% --- Pomocnicze ---
% Liczenie ile elementów z pierwszej listy występuje w drugiej
wspolne_elementy([], _, 0).
wspolne_elementy([X|Xs], Lista2, Liczba) :-
    member(X, Lista2),
    !,
    wspolne_elementy(Xs, Lista2, Liczba1),
    Liczba is Liczba1 + 1.
wspolne_elementy([_|Xs], Lista2, Liczba) :-
    wspolne_elementy(Xs, Lista2, Liczba).

% --- Dopasowanie kierunku ---
dopasowanie(Kierunek, Zainteresowania, Przedmioty, Cechy, Style, Wynik) :-
    kierunki_studiow(Kierunek, KInt, KPrzedm, KCechy, KStyle),
    wspolne_elementy(Zainteresowania, KInt, W1),
    wspolne_elementy(Przedmioty, KPrzedm, W2),
    wspolne_elementy(Cechy, KCechy, W3),
    wspolne_elementy(Style, KStyle, W4),
    waga(zainteresowania, WagaZ),
    waga(przedmioty, WagaP),
    waga(cechy, WagaC),
    waga(style, WagaS),
    Wynik is W1*WagaZ + W2*WagaP + W3*WagaC + W4*WagaS.

% --- Maksymalne możliwe dopasowanie dla kierunku ---
maks_dopasowanie(Kierunek, MaxWynik) :-
    kierunki_studiow(Kierunek, KInt, KPrzedm, KCechy, KStyle),
    waga(zainteresowania, WagaZ),
    waga(przedmioty, WagaP),
    waga(cechy, WagaC),
    waga(style, WagaS),
    length(KInt, L1),
    length(KPrzedm, L2),
    length(KCechy, L3),
    length(KStyle, L4),
    MaxWynik is L1*WagaZ + L2*WagaP + L3*WagaC + L4*WagaS.

% --- Porównanie do sortowania malejącego ---
compare_by_score(Delta, [_, P1], [_, P2]) :-
    (P1 > P2 -> Delta = '<' ; Delta = '>').

% --- Pobranie pierwszych N elementów listy ---
take(0, _, []) :- !.
take(_, [], []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N1 is N - 1,
    take(N1, Xs, Ys).

% --- Główna procedura zwracająca top 5 kierunków z procentami 0-100 ---
top5_dopasowania(Zainteresowania, Przedmioty, Cechy, Style, Top5) :-
    findall([Kierunek, Procent],
        (
            kierunki_studiow(Kierunek, _, _, _, _),
            dopasowanie(Kierunek, Zainteresowania, Przedmioty, Cechy, Style, Wynik),
            maks_dopasowanie(Kierunek, MaxWynik),
            MaxWynik > 0,
            Procent is (Wynik / MaxWynik) * 100
        ),
        Wyniki),
    predsort(compare_by_score, Wyniki, Posortowane),
    take(5, Posortowane, Top5).
