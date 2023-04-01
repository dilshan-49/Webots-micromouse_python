# Webots-micromouse (R2023a)

W ramach projektu stworzono symulację działania robota typu micromouse, którego celem jest pokonanie labiryntu w jak najkrótszym czasie. 
Napisany kontroler dla robota został później wykorzystany przy projekcie robota typu maze-solver zbudowanego z Lego Mindstorms NXT 2.0, co miało na celu pokazanie możliwości efektywnego testowania i prototypowania oprogramowania z użyciem symulacji.

Zamodelowano labirynt 16x16 komórek z celem w postaci 4 komórek w centrum. Do pokonania laibryntu
wykorzystano robota e-puck dostępnego w bibliotece Webots.
Do znalezienia najkrótszej trasy w dziedzinie odległości wykorzystano algorytm zalewania wodą (floodfill).

Cały kod programu sterującego wirtualnym robotem jest zapisany w 2 językach: Python i C. 
W zależności od wybranego trybu sterowania wykonuje się jedna z 3 części kodu:
 sterowanie ręczne,
 eksploracja labiryntu,
 szybki przejazd.
Wybór trybu dokonuje się poprzez zmianę wartości zmiennej MODE na wartość 
odpowiednio: 1, 2 lub 3.

Sterowanie ręczne polega na krokowym poruszaniu się robotem z użyciem klawiatury 
za pomocą strzałek. Wykorzystywane jest do np. testowania dokładności skręcania robota, jego 
powtarzalności czy też do dobierania parametrów związanych z pracą czujników.

Eksploracja polega na autonomicznym przejściu robota przez labirynt w celu zmapowania 
wszystkich ścian. Przyjmując konwencje numeracji pól, 
gdzie pozycją startową jest komórka o numerze 0, robot przyjmuje za cel nieodwiedzoną pozycje 
o najniższym indeksie. Przeszukiwanie labiryntu kończy się po odwiedzeniu wszystkich
segmentów. Wyznaczana jest wtedy najkrótsza trasa w dziedzinie odległości do pola 
końcowego, które ma indeks 119, a wynik zapisywany jest do pliku tekstowego.

W szybkim przejeździe robot pobiera z pliku utworzonego po eksploracji labiryntu 
najkrótszą trasę i wykonuje zgodnie z nią przejazd.


