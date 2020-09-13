#include "code_gen.h"
#include "symtable.h"
#include <stdio.h>

int main()
{
	symbol string_prompt_symbol = {.immediate = true, .type = SYM_STRING, .string_val = "Zadej retezec a ja ti ho zopakuju:"};
	symbol int_prompt_symbol = {.immediate = true, .type = SYM_STRING, .string_val = "Zadej cele cislo a ja ti ho zopakuju:"};
	symbol float_prompt_symbol = {.immediate = true, .type = SYM_STRING, .string_val = "Zadej realne cislo a ja ti ho zopakuju:"};
	symbol tell_string_symbol = {.immediate = true, .type = SYM_STRING, .string_val = "Zadal jsi:"};
	symbol eol_symbol = {.immediate = true, .type = SYM_STRING, .string_val = "\n"};
	symbol retval_symbol = {.id = "$retval", .frame = SYM_TF, .immediate = false};
	//symbol test_string_symbol = {.id = "test_string", .immediate = false, .type = SYM_STRING, .string_val = "retezec"};

	// --------------PROGRAM------------------
	// Create a dstring to store program's code
	dstring program;
	gencontrol_redirect_output(&program); // redirect code generator's output to program

	gen_program_header();
	gen_builtin_functions();

	// Prompt user to enter a string, then print it back
	gen_write(&string_prompt_symbol);
	gen_call_prepare();
	gen_call("inputs");
	gen_write(&tell_string_symbol);
	gen_write(&retval_symbol);

	// Prompt user to enter an integer, then print it back
	gen_write(&int_prompt_symbol);
	gen_call_prepare();
	gen_call("inputi");
	gen_write(&tell_string_symbol);
	gen_write(&retval_symbol);
	gen_write(&eol_symbol);

	// Prompt user to enter a float, then print it back
	gen_write(&float_prompt_symbol);
	gen_call_prepare();
	gen_call("inputf");
	gen_write(&tell_string_symbol);
	gen_write(&retval_symbol);
	gen_write(&eol_symbol);

	/*
	gen_definition(&test_string_symbol);
	test_string_symbol.immediate = true;
	gen_assignment(&test_string_symbol);
	test_string_symbol.immediate = false;

	// Call length, ord, chr, substr
	gen_call_prepare();
	gen_call_arg("s", &test_string_symbol);
	gen_call("length");
	gen_write(&float_prompt_symbol);
	*/

	gen_program_exit(0);
	// -----------END OF PROGRAM--------------

	// Print program's source code
	printf("%s", program.data);

	dstring_free(&program);

	return 0;
}
