#include "code_gen.h"
#include "symtable.h"
#include <stdio.h>

int main()
{
	// Prepare test symbols
	symbol s1 = {.id = "var1", .frame = SYM_LF, .immediate = false};
	symbol expr_result_sym = {.id = "$expr_result", .frame = SYM_GF, .immediate = false};
	symbol expr_result_type_sym = {.id = "$expr_result_type", .frame = SYM_GF, .immediate = false};

	// --------------PROGRAM------------------
	/*
		var1 = 10
		if var1 == 10 then
			print("var1 je rovno 10")
		else
			print("var1 neni rovno 10")
		end

		while var1 != 0 do
			var1 = var1 - 1
			print("var1 snizeno na ", var1)
		end
	*/

	// Create a dstring to store program's code
	dstring program;
	dstring_init(&program);
	gencontrol_redirect_output(&program); // redirect code generator's output to program

	gen_program_header();

	// Define and initialize variable "var1"
	gen_definition(&s1);
	symbol imm1 = {.immediate = true, .type = SYM_INT, .int_val = 10};
	gen_assignment(&s1, &imm1);

	gen_if("0");

	// TODO: expression analysis
	symbol imm2 = {.immediate = true, .type = SYM_INT, .int_val = 10};
	gen_assignment(&expr_result_sym, &imm2);
	symbol imm3 = {.immediate = true, .type = SYM_STRING, .string_val = "string@int"};
	gen_assignment(&expr_result_type_sym, &imm3);

	symbol imm_str1 = {.immediate = true, .type = SYM_STRING, .string_val = "var1 je rovno 10\n"};
	symbol imm_str2 = {.immediate = true, .type = SYM_STRING, .string_val = "var1 neni rovno 10\n"};

	gen_then("0");
		gen_write(&imm_str1);
	gen_else("0");
		gen_write(&imm_str2);
	gen_end_if("0");

	// TODO: while

	gen_program_exit(0);
	// -----------END OF PROGRAM--------------

	// Print program's source code
	printf("%s", program.data);

	dstring_free(&program);

	return 0;
}
