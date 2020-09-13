#include "symtable.h"
#include "binary_tree.h"
#include "garbage.h"
#include <stdio.h>

int main()
{
	symtable st;
	symtable_init(&st);

	// Prepare symbols
	symbol s1 = {.id = "int_var", .frame = SYM_LF, .immediate = false, .type = SYM_INT, .int_val = 33};
	symbol s2 = {.id = "int_var2", .frame = SYM_LF, .immediate = false, .type = SYM_INT, .int_val = 66};
	symbol s3 = {.id = "float_var", .frame = SYM_LF, .immediate = false, .type = SYM_FLOAT, .float_val = 3.141592};
	symbol s4 = {.id = "func", .frame = SYM_LF, .immediate = false, .type = SYM_FUNC};
	symbol s5 = {.id = "func2", .frame = SYM_LF, .immediate = false, .type = SYM_FUNC};

	// Add symbols into symtable
	symtable_add(&st, s1.id, &s1);
	symtable_add(&st, s2.id, &s2);
	symtable_add(&st, s3.id, &s3);
	symtable_add(&st, s4.id, &s4);
	symtable_add(&st, s5.id, &s5);

	printf(">POZNAMKA: symbol_count bude mit nejspis spatnou hodnotu, neni to chybou v binary_tree,"
		" ale tim, ze symbol_count se inkrementuje i pokud polozka jiz existuje.\n");
	printf("\n");

	printf(">Pridano 5 rozdilnych symbolu, symbol_count by mel byt roven 5:\n");
	printf("symbol_count=%d\n", st.symbol_count);
	symtable_print(&st);
	printf("\n");

	// Add symbols into symtable AGAIN
	symtable_add(&st, s1.id, &s1);
	symtable_add(&st, s2.id, &s2);
	symtable_add(&st, s3.id, &s3);
	symtable_add(&st, s4.id, &s4);
	symtable_add(&st, s5.id, &s5);

	printf(">Vsech 5 symbolu pridano znova, nemela by nastat zadna zmena:\n");
	printf("symbol_count=%d\n", st.symbol_count);
	symtable_print(&st);
	printf("\n");

	// Find existing symbol
	printf(">Hledani symbolu \"int_var2\" (hodnota by mela byt 66):\n");
	symbol *f1 = symtable_find(&st, s2.id);
	if (f1)
		printf("nalezen, int_val:%d\n", f1->int_val);
	else
		printf("nenalezen - CHYBA\n");
	printf("\n");

	// Find non-existant symbol
	printf(">Hledani symbolu \"non_existant_var\" (neexistuje):\n");
	symbol *f2 = symtable_find(&st, "non_existant_var");
	if (f2)
		printf("nalezen - CHYBA\n");
	else
		printf("nenalezen\n");
	printf("\n");

	// Remove few symbols
	printf(">Odstraneni symbolu \"func\" a \"int_var\":\n");
	symtable_remove(&st, "func");
	symtable_remove(&st, "int_var");
	symtable_print(&st);
	printf("\n");

	// Free symtable
	printf(">Tabulka uvolena:\n");
	symtable_free(&st);

	symtable_print(&st);

	GFreeAll();

	return 0;
}
