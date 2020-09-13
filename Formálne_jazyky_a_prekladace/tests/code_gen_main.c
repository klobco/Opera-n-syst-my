#include "code_gen.h"
#include "symtable.h"
#include <stdio.h>

int main()
{
	// Prepare test symbols
	symbol s1 = {.id = "global_var", .frame = SYM_GF, .immediate = false, .type = SYM_INT, .int_val = 25};
	symbol s2 = {.id = "func", .frame = SYM_GF, .immediate = false, .type = SYM_FUNC};

	// immediate symbols (won't be stored in a variable)
	symbol s3 = {.id = "temp_str", .frame = SYM_LF, .immediate = true, .type = SYM_STRING, .string_val = "first_param="};
	symbol s4 = {.id = NULL, .frame = SYM_LF, .immediate = true, .type = SYM_STRING, .string_val = "\n--> retezec se \\spec!&ln!m!\" znaky <--\n"};
	// variable
	symbol s5 = {.id = "int_var", .frame = SYM_LF, .immediate = false, .type = SYM_INT};

	// --------------PROGRAM------------------
	// 1) define global var (int, 25)
	// 2) define function with one parameter
	// 3) define local var "int_var" (int, 35)
	// 4) call function with "int_var" passed as argument

	// Create a dstring to store program's code
	dstring program;
	dstring_init(&program);
	gencontrol_redirect_output(&program); // redirect code generator's output to program

	gen_program_header();

	// Define global variable "global_var"
	gen_definition(&s1);

	// Define function "func"
	gen_function_start(s2.id);

	// Print "first_param=" <value of first param> EOL "--> retezec ..."
	gen_write(&s3);
	gen_write(&s5);
	gen_write(&s4);

	// End of function "func"
	gen_function_end(s2.id);

	// Define and init. local variable "int_var" to 25 (later used as argument to "func")
	gen_definition(&s5);
	symbol imm5 = {.immediate = true, .type = SYM_INT, .int_val = 35};
	gen_assignment(&s5, &imm5);

	// Call function with one argument
	gen_call_prepare();
	gen_call_arg(s5.id, &s5);
	gen_call(s2.id);

	gen_program_exit(0);
	// -----------END OF PROGRAM--------------

	// Print program's source code
	printf("%s", program.data);

	dstring_free(&program);

	return 0;
}
