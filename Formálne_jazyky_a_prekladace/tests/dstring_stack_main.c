#include "dstring_stack.h"
#include <stdio.h>

int main()
{
	dstring_stack st;
	dstring_stack_init(&st);

	printf(">Je zasobik prazdny?\n");
	printf("%d\n", dstring_stack_empty(&st));
	printf("\n");

	printf(">Pridan novy prvek\n\n");
	dstring_stack_push_new(&st);
	dstring_add(dstring_stack_top_data(&st), "retezec v prvni polozce zasobniku");

	printf(">Je zasobik prazdny?\n");
	printf("%d\n", dstring_stack_empty(&st));
	printf("\n");

	printf(">Obsah dstringu na vrchu zasobiku (prvni polozka):\n");
	printf("%s\n", dstring_stack_top_data(&st)->data);
	printf("\n");

	printf(">Pridan novy prvek\n\n");
	dstring_stack_push_new(&st);
	dstring_add(dstring_stack_top_data(&st), "retezec v druhe polozce zasobniku");

	printf(">Je zasobik prazdny?\n");
	printf("%d\n", dstring_stack_empty(&st));
	printf("\n");

	printf(">Obsah dstringu na vrchu zasobiku (druha polozka):\n");
	printf("%s\n", dstring_stack_top_data(&st)->data);
	printf("\n");

	printf(">Odstranen prvek z vrchu zasobiku\n\n");
	dstring_stack_pop(&st);

	printf(">Je zasobik prazdny?\n");
	printf("%d\n", dstring_stack_empty(&st));
	printf("\n");

	printf(">Obsah dstringu na vrchu zasobiku (prvni polozka):\n");
	printf("%s\n", dstring_stack_top_data(&st)->data);
	printf("\n");

	printf(">Odstranen prvek z vrchu zasobiku\n\n");
	dstring_stack_pop(&st);

	printf(">Je zasobik prazdny?\n");
	printf("%d\n", dstring_stack_empty(&st));
	printf("\n");

	return 0;
}
