#include "expression.h"
#include "parser.h"
#include "symtable.h"
#include <stdio.h>

int main(int argc, char **argv)
{
	(void)argv;
	bool no_print = argc != 1;
		
	// Create a dstring to store program's code
	dstring program;
	dstring_init(&program);
	gencontrol_redirect_output(&program); // redirect code generator's output to program
	gen_program_header();
	gen_builtin_functions();

	if (!no_print)
		fprintf(stderr, "Zadej cely vyraz:\n"); // Prints to stderr so that stdout can be used to extract code

	// Add some symbols
	symbol s1 = {.id = "int_var", .frame = SYM_LF, .immediate = false, .type = SYM_INT, .int_val = 25};
	symbol s2 = {.id = "float_var", .frame = SYM_LF, .immediate = false, .type = SYM_FLOAT, .float_val = 3.3f};
	symbol s3 = {.id = "string_var", .frame = SYM_LF, .immediate = false, .type = SYM_STRING, .string_val = "testovaci_retezec"};
	symbol s4 = {.id = "nil_var", .frame = SYM_LF, .immediate = false, .type = SYM_NONE};
	symtable_add(&table_local, s1.id, &s1);
	symtable_add(&table_local, s2.id, &s2);
	symtable_add(&table_local, s3.id, &s3);
	symtable_add(&table_local, s4.id, &s4);

	gen_definition(&s1);
	gen_definition(&s2);
	gen_definition(&s3);
	gen_definition(&s4);

	s1.immediate = true;
	gen_assignment(&s1, &s1);
	s1.immediate = false;
	s2.immediate = true;
	gen_assignment(&s2, &s2);
	s2.immediate = false;
	s3.immediate = true;
	gen_assignment(&s3, &s3);
	s3.immediate = false;
	s4.immediate = true;
	gen_assignment(&s4, &s4);
	s4.immediate = false;

	// Expression analysis
	get_next_token();
	int expr_ret = expression_analysis(&table_local);

	if (!no_print)
		fprintf(stderr, "Navratovy kod precedencni analyzy: %d\n", expr_ret); // Prints to stderr so that stdout can be used to extract code

	// Print expression's result
	symbol expr_result_sym = {.id="$expr_result", .immediate=false, .frame=SYM_GF};
	gen_write(&expr_result_sym);
	//gen_debug_info();

	// Print program's source code
	if (!no_print)
		printf("%s", program.data);

	dstring_free(&program);

	return expr_ret;
}
