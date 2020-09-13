#/bin/bash

# IFJ18 - Priklady pro studenty pro dokresleni zadani

# -------------------------------------------
# -------------------------------------------
# POZNAMKA: SPOUSTI SE POMOCI "make test_wis"
# -------------------------------------------
# -------------------------------------------

COMPILER=./build/parser_main  # zde mùze byt vas prekladac IFJ18 (napr. ./ifj18)
INTERPRETER=./interpret/ic18int  # zde muze byt interpret IFJcode18 (./ic18int)

for i in ./data/wis/*.src; do

	IN=`echo $i | sed 's/\(.*\)\.src/\1.in/g'`
	OUT=`echo $i | sed 's/\(.*\)\.src/\1.out/g'`
	PRG=`echo $i | sed 's/\(.*\)\.src/\1.prg/g'`

	echo $COMPILER $i $IN $OUT $PRG
	$COMPILER < $i > $PRG   # nekontroluji se chyby pekladu (pro chybove testy nutno rozsirit)
	RETURNED_COMPILER=$?

	echo -n "DIFF: $INTERPRETER $i: "
	cat $IN | $INTERPRETER $PRG | diff - $OUT > /dev/null 2> /dev/null
	DIFFOK=$?
	if [ $DIFFOK -eq 0 ]; then
		echo "OK"
	else
		echo "DIFFERENCE to $OUT"
		cat $IN | $INTERPRETER $PRG | diff - $OUT
	fi
done;

rm ./data/wis/*.prg

exit 0
