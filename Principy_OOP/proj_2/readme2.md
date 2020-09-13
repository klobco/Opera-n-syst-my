# Implementační dokumentace k 2. úloze do IPP 2018/2019

### Jméno a příjmení: Martin Klobušický
### Login: xklobu03

# Interpret
Môj interpret robí 2 priechody. V prvom načíta a syntakticky skontroluje všetky inštrukcie na to slúži funkcia ``Kontrola_arg`` ktorá pomocou regexu skontroluje správnosť argumentov, ďalej sa vytvoria ``labels`` a skontroluje sa či neexistujú inštrukcie s rovnakým  ``order``. Potom sa inštrukcie zoradia podľa ``order`` a ak je všetko v poriadku tak sa inštrukcie začnú vykonávať až pokiaľ sa nenarazí na poslednú inštrukciu.
Interpret musí mať aspoň jeden z dvoch argumentov

* ``--source`` : Je to XML kód ktorý sa má vykonať. Ak nieje nadstavený implicitne sa berie zo ``stdin``
* ``--input`` : Súbor so vstupnými dátami pre funkciu ``READ`` ak nieje nadstavený a narazí sa na inštrukciu ``READ`` používateľ musí ručne vložiť hodnotu cez ``stdin``

Ak nieje zadaný ani jeden argument nastane chyba ``10``, Ak sa súbory nepodarí otvoriť nastane chyba ``11``.
Môj program funguje objektovo takže každá inštrukcia je objekt a to neskutočne uľahčilo prácu. Podľa príslušného ``opcode`` sa potom zavolá odpovedajúca funkcia pomocou ``globals()``. Časom sa však objavili menšie chyby v základnom návrhu ktoré som už nestihol správne vyriešiť hlavne prácu so ``string`` a na začiatku som zle pochopil ``nil`` čo časom viedlo k dosť neriešiteľným problémom.
# Test
## Súbory
Na začiatku si všetky cesty nadstavím do aktuálneho adresára a podľa toho aké argumenty sú zadané tak cesty upravujem Potom skontrolujem či všetky súbory existujú a cesty k nim sú v poriadku Pri prechádzaní súborov hľadám súbor s príponou ``src``, ak ho nájdem tak hľadám súbory s rovnakým menom a príponami ``rc``, ``out``, ``in``. Ak neexistujú tak ich vytvorím a pokračujem na kontroly.
## HTML
Na úplnom začiatku si vytvorím HTML hlavičku kde si nadstavím nejaký základný ``CSS`` štýl a vytvorím tabuľku do ktorej postupne pridávam Ktoré testy prešli a ktoré nie a ich návratový kód. Na konci vypíšem Koľko testov prešlo a koľko nie.
## Kontroly
### Parse-only
Kontroly parsu prebiehajú tak že si vytvorím dočasný súbor do ktorého vložím výstup z ``parse.php`` ktorého vstupom je súbor ``src`` kde sa nachádza ``IPPcode19``. Zistím si návratový kód, ak nieje ``0`` tak ho porovnám s kódom uloženým v ``rc`` súbore a ak sa zhodujú test vyhodnotím ako úspešný. Ak je návratový kód ``0`` pokračujem na porovnanie výstupu ``parse.php`` so súborom ``out`` kde je uložený XML kód ktorý by sa mal zhodovať s mojim. Ak sa zhodujú tak test vyhodnotím ako úspešný. Na konci zmažem všetky dočasné pomocné súbory.
### Int-only
Kontroly interpretu prebiehajú skoro rovnako ako kontroly parsu. Takže v skratke, do dočasného súboru vložím výstup z ``interpret.py`` kde argumentom ``source`` je súbor ``src`` a argumentom ``input`` je súbor ``in``. Znova zistím návratové kódy a podľa toho porovnávam pomocou ``diff`` súbor s výstupom interpretu a súbor ``out`` alebo porovnávam návratové kódy. Na konci opäť zmažem všetky dočasné pomocné súbory.
### Spoločné kontroly
Ak nieje zadaný ani jeden parameter z ``int-only`` alebo ``parse-only`` Tak testy fungujú tak že sa súbor ``src`` pošle do ``parsu`` a výstup z parsu sa pošle do ``interpretu`` a ten výstup sa potom porovnáva so súborom ``out``. Na konci opäť zmažem všetky dočasné pomocné súbory.