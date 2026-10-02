# Zadania rekrutacyjne: robotyka w Webots

[English version](README_EN.md)

Witaj w rekrutacji do sekcji robotycznej Studenckiego Koła Astronautycznego! Przygotowaliśmy trzy zadania programistyczne w symulatorze robotów **Webots**. **Wybierz jedno z nich**. Zadania są od siebie niezależne i każde ma własny opis, światy symulacji, szkielet programu oraz sędziego, który automatycznie mierzy wynik.

| Zadanie | Robot | Czego dotyczy |
|---|---|---|
| [1. Line follower](01_line_follower/README.md) | e-puck | jazda wzdłuż linii, regulator, dwa tory |
| [2. Pick and place](02_pick_and_place/README.md) | ramię UR5e + chwytak | sterowanie manipulatorem, kinematyka |
| [3. Labirynt](03_maze/README.md) | e-puck | czujniki odległości, odometria, dwa labirynty |

Każdy folder zadania zawiera opis w pliku `README.md` (po polsku) i `README_EN.md` (po angielsku) oraz te same opisy w formacie PDF.

## Od czego zacząć

1. Zainstaluj Webots R2025a i Python 3 (szczegóły poniżej).
2. Pobierz to repozytorium: `git clone <adres repozytorium>` albo *Code → Download ZIP*.
3. Wybierz zadanie i przeczytaj jego opis.
4. Otwórz w Webots świat z folderu `worlds` i zacznij pisać kod w folderze `controllers`.

Wszystkie zadania piszesz w Pythonie. Nie musisz wcześniej znać Webots: opis każdego zadania zawiera wszystko, czego potrzebujesz, żeby zacząć.

## Czym jest Webots

Webots to darmowy, otwartoźródłowy symulator robotów rozwijany przez firmę Cyberbotics. Pozwala zbudować wirtualny świat z robotami, czujnikami i obiektami, a potem sterować robotami programami (tzw. kontrolerami) napisanymi m.in. w Pythonie, C lub C++. Symulacja uwzględnia fizykę: tarcie, masy, zderzenia i szum czujników, więc program, który działa w Webots, zachowuje się podobnie jak na prawdziwym robocie.

## Instalacja

1. Pobierz **Webots R2025a** ze strony https://cyberbotics.com albo z https://github.com/cyberbotics/webots/releases i zainstaluj go jak zwykłą aplikację.
2. Zainstaluj **Python 3** (https://www.python.org). Na Windows zaznacz w instalatorze opcję „Add Python to PATH”.
3. Jeśli Webots nie znajdzie Pythona sam, wskaż go w *Tools → Preferences → General → Python command*.
4. Repozytorium trzymaj w zwykłym folderze, **nie** w folderze instalacji Webots ani w folderze synchronizowanym z OneDrive.
5. Przy pierwszym otwarciu świata Webots pobiera modele robotów z internetu, więc potrzebne jest połączenie z siecią.

Szczegółowa instrukcja, opis interfejsu i rozwiązania typowych problemów znajdują się na końcu opisu każdego zadania.

## Zasady

- Rozwiązujesz zadanie samodzielnie. Możesz korzystać z dokumentacji, internetu i narzędzi AI, ale na rozmowie poprosimy Cię o wyjaśnienie kodu.
- Nie modyfikuj plików sędziego ani światów. Przy ocenie uruchomimy Twój sterownik w oryginalnych światach.
- Oddajesz plik sterownika, krótkie nagranie ekranu i kilka zdań opisu (szczegóły w opisie zadania).

Powodzenia!
