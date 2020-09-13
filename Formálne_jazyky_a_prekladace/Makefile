CC=gcc
CFLAGS=-Wall -Wextra -Werror -g -Itests/ -Isrc/
SRC_FILES=$(wildcard src/*.c)
TEST_FILES=$(wildcard tests/*.c)
SRC_OBJ_FILES=$(patsubst src/%.c, build/obj/src/%.o, $(SRC_FILES))
TESTS_OBJ_FILES=$(patsubst tests/%.c, build/obj/tests/%.o, $(TEST_FILES))

# ------------------------------
# Rules for building the project
# ------------------------------

all: create_build_dirs build_src build_tests

build_src: $(SRC_OBJ_FILES)

build_tests: $(TESTS_OBJ_FILES)

create_build_dirs:
	@mkdir -p build
	@mkdir -p build/obj
	@mkdir -p build/obj/src
	@mkdir -p build/obj/tests
	@mkdir -p build/output
	@mkdir -p build/interpret_output

# Compile src/*.c files into build/obj/src/*.o
build/obj/src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $^ -o $@

# Build each test (tests/*.c) into its own executable file in build/
build/obj/tests/%.o: tests/%.c $(SRC_OBJ_FILES) 
	$(CC) $(CFLAGS) -c $< -o $@
	$(CC) $(CFLAGS) $(SRC_OBJ_FILES) $@ -o $(patsubst tests/%.c, build/%, $<)

clean:
	rm -r build/

# -----------------------------
# Rules for testing the project
# -----------------------------

# Run tests for code generation
# NOTE: Expects interpret "ic18int" to be located in the main directory
test_code_gen: all
	@./build/code_gen_main > ./build/output/code_gen_main.out
	@echo "Vystup interpretu:"
	@./interpret/ic18int ./build/output/code_gen_main.out | tee ./build/interpret_output/code_gen_main.txt

test_builtin_code_gen: all
	@./build/builtin_code_gen_main > ./build/output/builtin_code_gen_main.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/builtin_code_gen_main.out | tee ./build/interpret_output/builtin_code_gen_main.txt

test_code_binary_tree: all
	@./build/binary_tree_main > ./build/output/binary_tree_main.out

test_code_parser: all
	@./build/parser_main > ./build/output/parser_main.out

test_symtable: all
	@./build/symtable_main | tee ./build/output/symtable_main.out

test_dstring_stack: all
	@./build/dstring_stack_main | tee ./build/output/dstring_stack_main.out

test_code_list: all
	@./build/list_main > ./build/output/list_main.out

test_expression: all
	@./build/expression_main > ./build/output/expression_main.out
	@echo "Vystup interpretu:"
	@data/interpret_expression_from_makefile

test_print: all
	@./build/parser_main <./data/print_program >./build/output/print_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/print_test.out | tee ./build/interpret_output/print_test.txt

test_imm_args: all
	@./build/parser_main <./data/imm_args_test >./build/output/imm_args_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/imm_args_test.out | tee ./build/interpret_output/imm_args_test.txt

test_substr: all
	@./build/parser_main <./data/substr_test >./build/output/substr_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/substr_test.out | tee ./build/interpret_output/substr_test.txt

test_conv_str: all
	@./build/parser_main <./data/conv_str_test >./build/output/conv_str_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/conv_str_test.out | tee ./build/interpret_output/conv_str_test.txt

test_cmp: all
	@./build/parser_main <./data/cmp_test >./build/output/cmp_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/cmp_test.out | tee ./build/interpret_output/cmp_test.txt

test_div_zero: all
	@./build/parser_main <./data/div_zero_test >./build/output/div_zero_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/div_zero_test.out | tee ./build/interpret_output/div_zero_test.txt

test_nil: all
	@./build/parser_main <./data/nil_test >./build/output/nil_test.out
	@echo "Vystup interpretu:"
	@stdbuf -oL ./interpret/ic18int ./build/output/nil_test.out | tee ./build/interpret_output/nil_test.txt

test_wis: all
	@. ./data/wis/examples.sh
