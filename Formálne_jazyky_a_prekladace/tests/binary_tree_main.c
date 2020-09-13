#include "binary_tree.h"
#include "garbage.h"
#include "symtable.h"

void Print_tree(BTNodePtr TempTree)
{
  printf("Struktura binarniho stromu:\n");
  printf("\n");
  if (TempTree != NULL)
     Print_tree2(TempTree, "", 'X');
  else
     printf("strom je prazdny\n");
  printf("\n");
  printf("=================================================\n");
} 

void Print_tree2(BTNodePtr TempTree, char* sufix, char fromdir)
/* vykresli sktrukturu binarniho stromu */

{
     if (TempTree != NULL)
     {
	char* suf2 = (char*) malloc(strlen(sufix) + 4);
	strcpy(suf2, sufix);
        if (fromdir == 'L')
	{
	   suf2 = strcat(suf2, "  |");
	   printf("%s\n", suf2);
	}
	else
	   suf2 = strcat(suf2, "   ");
	Print_tree2(TempTree->RPtr, suf2, 'R');
        printf("%s  +-[%s]\n", sufix, TempTree->key);
	strcpy(suf2, sufix);
        if (fromdir == 'R')
	   suf2 = strcat(suf2, "  |");	
	else
	   suf2 = strcat(suf2, "   ");
	Print_tree2(TempTree->LPtr, suf2, 'L');
	if (fromdir == 'R') printf("%s\n", suf2);
	free(suf2);
    }
}

int main(){

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
	Print_tree(st.root);
	symtable_print(&st);
	printf("\n");

	// Free symtable
	printf(">Tabulka uvolena:\n");
	symtable_free(&st);

	symtable_print(&st);

	BTNodePtr TestTree;

	BTInit(&TestTree);

	char c[5]="ahoj";

	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"aaa");
	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"ahok");
	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"aokj");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"bokj");
	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"rca");
	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"por");
	BTInsertNode(&TestTree,c,NULL);
	//printf("%s\n",TestTree->key);
	strcpy(c,"a");
	BTInsertNode(&TestTree,c,NULL);

	strcpy(c,"125");
	BTInsertNode(&TestTree,c,NULL);

	strcpy(c,"a15");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"125");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"123");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"124");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"126");
	BTInsertNode(&TestTree,c,NULL);
	strcpy(c,"127");
	BTInsertNode(&TestTree,c,NULL);

	int a;
	a=5;
	BTInsertNode(&TestTree,"data",&a);

	BTNodePtr tmp = BTSearchNodeByKeyPtr(&TestTree,"data");
	printf("data:%d\n",*(int*)tmp->data);

	a=42;
	BTEditNodeByKey(&TestTree,"data",&a);
	tmp = BTSearchNodeByKeyPtr(&TestTree,"data");
	printf("data:%d\n",*(int*)tmp->data);

	Print_tree(TestTree);
	//printf("%s\n",TestTree->key);

	printf("Hledat1:%d\n",BTSearchNodeByKey(&TestTree,"rca"));
	printf("Hledat0:%d\n",BTSearchNodeByKey(&TestTree,"rcarrrr"));
	printf("Hledat0:%d\n",BTSearchNodeByKey(&TestTree,"rc"));
	printf("Hledat1:%d\n",BTSearchNodeByKey(&TestTree,"a"));
	printf("Hledat1:%d\n",BTSearchNodeByKey(&TestTree,"ahoj"));

	/*BTNodePtr tmp = BTSearchNodeByKeyPtr(&TestTree,"rca");
	printf("%s",tmp->key);
	tmp->key="cra";*/
	printf("Najviac vlavo:%s\n",BTFindMostLeft(&TestTree)->key);
	printf("Najviac vpravo:%s\n",BTFindMostRight(&TestTree)->key);

	BTDeleteNodeByKey(&TestTree,"a");

	

	BTDeleteNodeByKey(&TestTree,"bokj");
	BTDeleteNodeByKey(&TestTree,"ahoj");
	BTDeleteNodeByKey(&TestTree,"por");
	BTDeleteNodeByKey(&TestTree,"124");

	Print_tree(TestTree);

	BTDeleteTree(&TestTree);
	
	

	//printf("EditTest1:%d\n" ,BTEditNodeByKey(&TestTree,"a15","ccc"));
	//printf("EditTest0:%d\n" ,BTEditNodeByKey(&TestTree,"a14","ccc"));
	Print_tree(TestTree);

	GFreeAll();

	return 0;
}