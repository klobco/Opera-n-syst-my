# IPK Dokumentácia k projektu 1 - varianta 1
## Autor: Martin Klobušický (xklobu03)

## Funkcie
Server dokáže spracovať 3 rôzne požiadavky a dokáže vracať dáta v podobe ``text/plain`` alebo ``application/json``.
Čo má vracať si vyberá na základe hlavičky ``Accept`` ak hlavička Accept obsahuje ``*/*`` zvolí sa ``text/plain``
### Hostname
Použil som jednoduchú funkciu ``gethostname()``.
### Cpu-name
V súbore ``/proc/cpuinfo`` hladám riadok model-name a ak ho nájdem vraciam to čo je za ním 
### Load
Tentokrát som použil súpor ``/proc/stat`` odkial si zoberiem aktuálne informácie 2x, v sekundovom intervale a pomocou výpočtu
vypočítam aktuálne vyťaženie procesoru.
### Load?refresh=
Robím preste to isté ako pri ``/load`` ale upravím hlavičku tak že jej pridám ďalší parameter ``Refresh:`` kde beriem hodnotu ktorá sa nachádza za ``=``.
## Chybové hlášky
### 404 Not Found
Vraciam v prípade že požiadavok ktorý uživateľ zadal môj program nepodporuje.
### 405 Method Not Allowed
V prípade že Požiadavok nepríde s metodou ``GET`` ale nejakou inou. Môj program podpruje iba ``GET``
### 406 Not Acceptable
Ak ``Accept`` neobsahuje žiadny z podporovaných formátov 
### 505 Version Not Supported
Ak Požiadavok prišiel so zlou(nepodporovanou) verziou protokolu HTTP môj program podporuje iba ``HTTP/1.1``