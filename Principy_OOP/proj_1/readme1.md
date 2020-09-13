# Dokumentace projektu IPP-1.část
### Autor: Martin Klobušický (xklobu03)

## Kontrola prvního řádku
Úplně na začátku kontroluji jestli je na prvním řádku ``.IPPcode19`` bez ohledu na velikost písmen. Jestli není na úplně  prvním řádku tak program skončí chybou ``21``. Jestli je vše v pořádku začne skript po řádcích kontrolovat instrukce a operandy.

## Komentáře
Komentáře fungují tak že když načtu řádek a obsahuje znak ``#`` tak všechno za ním, včetně něj odstaním a dále pokračuji na kontrolu instrukcí.

## Kontrola Instrukcí
Pro Kontrolu Instrukcí jsem si napsal funkci ``Test_instrukce`` která dostane jako argument první slovo na řádku a přetypuje si ho na velká písmena, pak ho porovnává s polem instrukcí kde jsou sepsané všechny instrukce které jazyk podporuje. Pokud se instrukce v poli nenachází, pak nastane chyba ``22``
Když je instrukce v pořádku skript začne kontrolovat operandy instrukce.
### Operandy
Instrukce jsem si rozdělil taky do několika polí podle toho kolik a jaké operandy můžou obsahovat. Když je instrukce v pořádku pak hledám v kterém poli se nachází a tak zjistím kolik a jaké operandy by měla mít. Když to zjistím tak na každém operandu zavolám funkci ``Test_symb`` která zjistí typ operandu (int,string,bool...) a porovná ho s očekávaným typem, když se shodují pak se začne generovat XML. Když se neshodují tak se vrátí chyba ``23``

## Generování XML
Pro generování XML jsem použil ``xmlwriter``. Generování provádím hned po tom jak zkontroluji instrukce a operandy. Pro určení pořadí instrukce používám proměnnou která se po načtení každého řádku inkrementuje. Neinkrementuje se jen v případe že se jedná o prázdný řádek neboj o řádek pouze s komentářem.