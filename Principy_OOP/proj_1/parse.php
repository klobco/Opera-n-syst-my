<?php
$instrukce = array("MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", 
					"RETURN", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", 
					"EQ", "ADD", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE",
					"CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "AND", "TYPE", "LABEL", "JUMP", 
					"JUMPIFEQ", "JUMPIFNEQ", "EXIT", "DPRINT", "BREAK");

$instr_nic = array("CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK");
$instr_label = array("CALL", "LABEL", "JUMP");
$instr_symb = array("PUSHS", "WRITE", "DPRINT");
$instr_var = array("DEFVAR", "POPS");
$instr_var_sym = array("MOVE", "INT2CHAR", "STRLEN", "TYPE", "NOT");
$instr_var_type = array("READ");
$instr_var_2sym = array("ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR",
                      		"STRI2INT", "CONCAT", "GETCHAR", "SETCHAR");
$instr_label_2sym = array("JUMPIFEQ", "JUMPIFNEQ");



$tmp  = array(
    "help::",  
);
$args = getopt("", $tmp);

if(array_key_exists("help",$args))
{
	$help="
Skript načíta zo stdin súbor ktorý skontroluje (syntaktická a lexikálna analýza) a vygeneruje xml formát na stdout.

Príklad: php7.3 parse.php [--help] <in.src >out.xml
";
	echo $help;
	exit(0);
}

function Test_instrukce($line){
	global $instrukce;
	global $err;
	$keyword = strtok($line, " ");
	$keyword = trim($keyword);
	$keyword = strtoupper($keyword);
	if (in_array($keyword, $instrukce) == false) {
		fwrite($err, "Zle keyword\n");
		exit(22);
	}
}

function Test_symb($type){
	global $err;
	$type = trim($type);
	if (preg_match('/^(string|int|bool|)$/i', $type)) {
		return "type";
	}
	if (preg_match('/^int@[+|-]?[0-9]+$/', $type)) {
		return "int";
	}
	elseif (preg_match('/^bool@(true|false)$/', $type)) {
		return "bool";
	}
	elseif (preg_match('/^nil@nil$/', $type)) {
		return "nil";
	}
	elseif (preg_match('/^string@([^\s#\\\\]|\\\\[0-9]{3})*$/', $type)) {
		return "string";
	}
	elseif (preg_match('/^(GF|LF|TF)@([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$/', $type)) {
		return "var";
	}
	else {
		fwrite($err, "Zlý symbol\n");
		exit(23);
	}
}

$vstup = fopen('php://stdin', "r");
$err = fopen('php://stderr', "w");

$ria = fgets($vstup);
$counter = 0;

if (preg_match('/#.*$/', $ria)) {
	$posi = strpos($ria, "#");
	$ria = substr($ria, 0, $posi);
}

$ria = preg_split('#\s+#', $ria);
$ria = array_filter($ria);
$ria = strtoupper(trim($ria[0]));
if ($ria != ".IPPCODE19") {
	fwrite($err, "Zly format suboru\n");
	exit(21);
}

$xml = xmlwriter_open_memory();
xmlwriter_set_indent($xml, 1);
xmlwriter_set_indent_string($xml, '  ');
xmlwriter_start_document($xml, '1.0', 'UTF-8');

xmlwriter_start_element($xml, 'program');
xmlwriter_start_attribute($xml, 'language');
xmlwriter_text($xml, 'IPPcode19');
xmlwriter_end_attribute($xml);


//kontrola po riadkoch
while (($prikaz = fgets($vstup)) !== false) {



	$prikaz = trim($prikaz);
	$prikaz = preg_replace('/\s+/', ' ', $prikaz);

	if (empty($prikaz)) {
		continue;
	}

	if (preg_match('/#.*$/', $prikaz)) {
		$pos = strpos($prikaz, "#");
        $prikaz = substr($prikaz, 0, $pos);
        if (trim($prikaz) == '')
		{
 			continue;
		}
	}
	$counter++;
	Test_instrukce($prikaz);
	//echo $counter."\n";
	$prikaz2 = preg_split('#\s+#', $prikaz);
	$prikaz2 = array_filter($prikaz2);
	$prikaz2[0] = strtoupper($prikaz2[0]);

	// ak nemá argument
	if (count($prikaz2) == 1) {
		if (in_array($prikaz2[0], $instr_nic)) {

			xmlwriter_start_element($xml, 'instruction');
			xmlwriter_start_attribute($xml, 'order');
			xmlwriter_text($xml, $counter);
			xmlwriter_end_attribute($xml);
			xmlwriter_start_attribute($xml, 'opcode');
			xmlwriter_text($xml, $prikaz2[0]);
			xmlwriter_end_attribute($xml);

			xmlwriter_end_element($xml);
		}
		else
		{
			fwrite($err, "Zly operand\n");
			exit(23);
		}
	}
	//ak má 1 argument
	if (count($prikaz2) == 2) {
		if (in_array($prikaz2[0], $instr_var)) {
			if (preg_match('/^(GF|LF|TF)@([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$/', $prikaz2[1])) {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);

				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'var');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);
			}
			else {
				fwrite($err, "Zly operand\n");
				exit(23);
			}
		}
		elseif (in_array($prikaz2[0], $instr_symb)) {
			$type = Test_symb($prikaz2[1]);

			xmlwriter_start_element($xml, 'instruction');
			xmlwriter_start_attribute($xml, 'order');
			xmlwriter_text($xml, $counter);
			xmlwriter_end_attribute($xml);
			xmlwriter_start_attribute($xml, 'opcode');
			xmlwriter_text($xml, $prikaz2[0]);
			xmlwriter_end_attribute($xml);

			if ($type != "var") {
				$edit = end(explode('@',$prikaz2[1],2));
			}
			else
			{
				$edit = $prikaz2[1];
			}

			xmlwriter_start_element($xml, 'arg1');
			xmlwriter_start_attribute($xml, 'type');
			xmlwriter_text($xml, $type);
			xmlwriter_end_attribute($xml);
			xmlwriter_text($xml, $edit);

			xmlwriter_end_element($xml);
			xmlwriter_end_element($xml);
		}
		elseif (in_array($prikaz2[0], $instr_label)) {
			if (preg_match('/^([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$/', $prikaz2[1])) {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);


				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'label');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);
			}
			else {
				fwrite($err, "Zly operand\n");
				exit(23);
			}
		}
	}
	//ak má 2 argumenty
	if (count($prikaz2) == 3) {
		if (in_array($prikaz2[0], $instr_var_sym)) {
			if ((Test_symb($prikaz2[1]) == "var") && ($type=Test_symb($prikaz2[2]))) {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);

				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'var');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);
				xmlwriter_end_element($xml);

				if ($type != "var") {
					$edit = end(explode('@',$prikaz2[2],2));
				}
				else
				{
					$edit = $prikaz2[2];
				}
				xmlwriter_start_element($xml, 'arg2');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, $type);
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $edit);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);
			}
			else {
				fwrite($err, "Zly operand\n");
				exit(23);
			}
		}
		elseif (in_array($prikaz2[0], $instr_var_type)) {
			if ((Test_symb($prikaz2[1]) == "var") && ($type=Test_symb($prikaz2[2]))) {
				if ($type == "type") {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);

				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'var');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);
				xmlwriter_end_element($xml);

				xmlwriter_start_element($xml, 'arg2');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, "type");
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[2]);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);
				}
				else{
					fwrite($err, "Zly operand\n");
					exit(23);
				}
			}
			else{
				fwrite($err, "Zly operand\n");
				exit(23);
			}
		}
		else{
			fwrite($err, "Zly operand\n");
			exit(23);
		}
	}
	if (count($prikaz2) == 4) {
		if (in_array($prikaz2[0], $instr_var_2sym)) {
			if ((Test_symb($prikaz2[1]) == "var") && ($type=Test_symb($prikaz2[2])) && ($type2=Test_symb($prikaz2[3]))) {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);

				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'var');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);
				xmlwriter_end_element($xml);

				if ($type != "var") {
					$edit = end(explode('@',$prikaz2[2],2));
				}
				else
				{
					$edit = $prikaz2[2];
				}
				xmlwriter_start_element($xml, 'arg2');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, $type);
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $edit);
				xmlwriter_end_element($xml);

				if ($type2 != "var") {
					$edit2 = end(explode('@',$prikaz2[3],2));
				}
				else
				{
					$edit2 = $prikaz2[1];
				}
				xmlwriter_start_element($xml, 'arg3');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, $type2);
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $edit2);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);	
			}
			else{
				fwrite($err, "Zly operand\n");
				exit(23);
			}
		}
		elseif (in_array($prikaz2[0], $instr_label_2sym)) {
			if ((preg_match('/^([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$/', $prikaz2[1])) && ($type=Test_symb($prikaz2[2])) && ($type2=Test_symb($prikaz2[3]))) {
				xmlwriter_start_element($xml, 'instruction');
				xmlwriter_start_attribute($xml, 'order');
				xmlwriter_text($xml, $counter);
				xmlwriter_end_attribute($xml);
				xmlwriter_start_attribute($xml, 'opcode');
				xmlwriter_text($xml, $prikaz2[0]);
				xmlwriter_end_attribute($xml);

				xmlwriter_start_element($xml, 'arg1');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, 'label');
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $prikaz2[1]);
				xmlwriter_end_element($xml);

				if ($type != "var") {
					$edit = end(explode('@',$prikaz2[2],2));
				}
				else
				{
					$edit = $prikaz2[2];
				}
				xmlwriter_start_element($xml, 'arg2');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, $type);
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $edit);
				xmlwriter_end_element($xml);

				if ($type2 != "var") {
					$edit2 = end(explode('@',$prikaz2[3],2));
				}
				else
				{
					$edit2 = $prikaz2[1];
				}
				xmlwriter_start_element($xml, 'arg3');
				xmlwriter_start_attribute($xml, 'type');
				xmlwriter_text($xml, $type2);
				xmlwriter_end_attribute($xml);
				xmlwriter_text($xml, $edit2);

				xmlwriter_end_element($xml);
				xmlwriter_end_element($xml);
			}
			else{
				fwrite($err, "Zly operand\n");
				exit(23);
			}

		}
		else{
			fwrite($err, "Zly operand\n");
			exit(23);
		}
	}
}

xmlwriter_end_element($xml);
xmlwriter_end_document($xml);
echo xmlwriter_output_memory($xml);

//echo $prikaz2[0]."\n";
//echo fgets($vstup);
//fwrite($err, "Chyba vystupu");
//echo $instrukce[6];
?>