#include "list.h"

List newlist;
int MaxListLength = 100;

/*void print_elements_of_list(List TL)	{
 Vytiskne seznam. 
	List TempList=TL;	
	int CurrListLength = 0;
	printf("-----------------");
	while ((TempList.First!=NULL) && (CurrListLength<MaxListLength))	{
		printf("\n\t %d",TempList.First->token_tmp.type);
		if ((TempList.First==TL.Active) && (TL.Active!=NULL))
			printf("\t <= toto je aktivní prvek ");
		TempList.First=TempList.First->ptr;	
		CurrListLength++;
	}
	printf("\n-----------------\n");
}*/

int main()
{
	/*InitList(&newlist);
	print_elements_of_list(newlist);
	ListInsert(&newlist, "ahoj");
	print_elements_of_list(newlist);
	ListInsert(&newlist, "ja");
	ListInsert(&newlist, "som");
	ListInsert(&newlist, "hehehehe");
	ListInsert(&newlist, "hehehehe");
	printf("%d\n", ListLen(&newlist));
	print_elements_of_list(newlist);
	if (ListSearch(&newlist, "som") == true)
	{
		printf("Našiel som prvok SOM\n");
	}
	if (ListSearch(&newlist, "ahojjj") == true)
	{
		printf("Našiel som prvok ahojjj\n");
	}
	DisposeList(&newlist);
	print_elements_of_list(newlist);*/

	/*List newlist1;
	InitList(&newlist1);
	token tmp = {.type=TOKEN_EOL};
	ListPush(&newlist1,tmp);
	tmp.type=TOKEN_EOF;
	ListPush(&newlist1,tmp);
	tmp.type=TOKEN_KEYWORD;
	ListPush(&newlist1,tmp);
	tmp.type=TOKEN_INT;
	ListPush(&newlist1,tmp);
	tmp.type=TOKEN_FLOAT;
	ListInsertLast(&newlist1,tmp);
	print_elements_of_list(newlist1);
	tmp=ListPop(&newlist1);
	printf("%d\n",tmp.type);
	print_elements_of_list(newlist1);

	DisposeList(&newlist1);*/
	return 0;
}