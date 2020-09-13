from __future__ import print_function
import sys
import operator
import re
import argparse
import xml.etree.ElementTree as ET

def err(kod,text):
	print(text, file = sys.stderr)
	exit(kod)


input_file = None
vstup = None

typ = 0
hodnota = 1
# argumenty vstupu
if len(sys.argv) < 2:
	print("Error", file = sys.stderr)
	exit(10)

parser = argparse.ArgumentParser(description='Help me please!')
parser.add_argument("--source", help="source file with XML input code")
parser.add_argument("--input", help="file with input data to interpret")
args = parser.parse_args()

#Zistenie ktoré argumenty sú zadané
if args.source is None:
	if args.input is None:
		print("Error 3", file = sys.stderr)
		exit(10)
	if args.input is not None:
		try:
			vstup = sys.stdin.read()
			input_file = open(args.input,"r")
		except:
			print("Error 1", file = sys.stderr)
			exit(11)

if args.source is not None:
	if args.input is None:
		try:
			vstup = open(args.source,"r").read()
		except:
			print("Error .....", file = sys.stderr) 
			exit(11)
	if args.input is not None:
		try:
			vstup = open(args.source,"r").read()
			input_file = open(args.input,"r")
		except:
			print("Error 2", file = sys.stderr)
			exit(11)


vstup = ET.fromstring(vstup)
slovnik = {}
zoznam_instr = []

instrukce = ["MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", 
					"RETURN", "PUSHS", "POPS", "ADD", "SUB", "MUL", "IDIV", "LT", "GT", 
					"EQ", "ADD", "OR", "NOT", "INT2CHAR", "STRI2INT", "READ", "WRITE",
					"CONCAT", "STRLEN", "GETCHAR", "SETCHAR", "AND", "TYPE", "LABEL", "JUMP", 
					"JUMPIFEQ", "JUMPIFNEQ", "EXIT", "DPRINT", "BREAK"]

instr_nic = ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"];
instr_label = ["CALL", "LABEL", "JUMP"];
instr_symb = ["PUSHS", "WRITE", "DPRINT"];
instr_var = ["DEFVAR", "POPS"];
instr_var_sym = ["MOVE", "INT2CHAR", "STRLEN", "TYPE", "NOT"];
instr_var_type = ["READ"];
instr_var_2sym = ["ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR",
                      		"STRI2INT", "CONCAT", "GETCHAR", "SETCHAR"];
instr_label_2sym = ["JUMPIFEQ", "JUMPIFNEQ"];

var_regex = "^(GF|LF|TF)@([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$"
string_regex = "^([^\s#\\\\]|\\\\[0-9]{3})*$"
nil_regex = "^nil$"
bool_regex = "^(true|false)$"
int_regex = "^[+|-]?[0-9]+$"
type_regex = "^(string|int|bool|)$"
label_regex = "^([a-zA-Z]|[_!?*%$&-]\w)([a-zA-Z0-9]|[_!?*%$&-])*$"

#Kontrola obsahu argumentov podľa regexu
def Kontrola_reg(string):
	if string == None:
		err(32,"Prazdny retazec")
	if re.match(bool_regex, string):
		return "bool"
	if re.match(int_regex, string):
		return "int"
	if re.match(type_regex, string):
		return "type"
	if re.match(var_regex,string):
		return "var"
	if re.match(nil_regex,string):
		return "nil"
	if re.match(string_regex,string):
		return "string"
	if re.match(label_regex, string):
		return "label"



#Kontrola argumentov
def Kontrola_arg(ins):
	symb = False
	if ins.opcode in instr_nic:
		if (bool(ins.arg1) or bool(ins.arg2) or bool(ins.arg3)):
			exit(32)
	if ins.opcode in instr_label:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if arg1_key != "label":
			err(32,"must by label")
		if arg1_value == None:
			err(32,"Prazdny retazec")
		if re.match(label_regex,arg1_value):
			if "label" != arg1_key or arg1_key != "label" or bool(ins.arg3) or bool(ins.arg2):
				print("prikaz neprešiel : instr_label", file = sys.stderr)
				exit(32)

	if ins.opcode in instr_symb:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if arg1_key == "bool" or arg1_key == "int" or arg1_key == "string" or arg1_key == "var" or arg1_key == "nil":
			symb = True

		if Kontrola_reg(arg1_value) != arg1_key or symb == False or bool(ins.arg3) or bool(ins.arg2):
			print("prikaz neprešiel : instr_symb", file = sys.stderr)
			exit(32)

	if ins.opcode in instr_var:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if Kontrola_reg(arg1_value) != arg1_key or arg1_key != "var" or bool(ins.arg3) or bool(ins.arg2):
			print("prikaz neprešiel: instr_var", file = sys.stderr)
			exit(32)

	if ins.opcode in instr_var_sym:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
			arg2_key = ins.arg2[typ]
			arg2_value = ins.arg2[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if arg2_key == "string":
			if arg2_value == None:
				if Kontrola_reg(arg1_value) != arg1_key or arg1_key != "var" or bool(ins.arg3):
					print("prikaz neprešiel : instr_var_sym", file = sys.stderr)
					exit(32)
			elif re.match(string_regex,arg2_value):
				if Kontrola_reg(arg1_value) != arg1_key or arg1_key != "var" or bool(ins.arg3):
					print("prikaz neprešiel : instr_var_sym", file = sys.stderr)
					exit(32)
		else:
			if arg2_key == "bool" or arg2_key == "int" or arg2_key == "string" or arg2_key == "var" or arg2_key == "nil":
				symb = True
			if Kontrola_reg(arg2_value) != arg2_key or Kontrola_reg(arg1_value) != arg1_key or arg1_key != "var" or symb == False or bool(ins.arg3):
				print("prikaz neprešiel : instr_var_sym", file = sys.stderr)
				exit(32)

	if ins.opcode in instr_var_type:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
			arg2_key = ins.arg2[typ]
			arg2_value = ins.arg2[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if Kontrola_reg(arg2_value) != arg2_key or Kontrola_reg(arg1_value) != arg1_key or arg1_key != "var" or arg2_key != "type" or bool(ins.arg3):
			print("prikaz neprešiel : instr_var_type", file = sys.stderr)
			exit(32)

	if ins.opcode in instr_var_2sym:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
			arg2_key = ins.arg2[typ]
			arg2_value = ins.arg2[hodnota]
			arg3_key = ins.arg3[typ]
			arg3_value = ins.arg3[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if ((arg2_key == "bool" or arg2_key == "int" or arg2_key == "string" or arg2_key == "var" or arg2_key == "nil") and (arg3_key == "bool" or arg3_key == "int" or arg3_key == "string" or arg3_key == "var" or arg3_key == "nil")):
			symb = True

		if Kontrola_reg(arg2_value) != arg2_key or Kontrola_reg(arg1_value) != arg1_key or Kontrola_reg(arg3_value) != arg3_key or arg1_key != "var" or symb == False:
			print("prikaz neprešiel : instr_var_2sym", file = sys.stderr)
			exit(32)

	if ins.opcode in instr_label_2sym:
		try:
			arg1_key = ins.arg1[typ]
			arg1_value = ins.arg1[hodnota]
			arg2_key = ins.arg2[typ]
			arg2_value = ins.arg2[hodnota]
			arg3_key = ins.arg3[typ]
			arg3_value = ins.arg3[hodnota]
		except:
			err(32,"chyba argumentov XML")

		if arg1_key != "label":
			err(32,"must by label")

		if re.match(label_regex,arg1_value):
			if "label" != arg1_key or arg1_key != "label" or not bool(ins.arg3) or not bool(ins.arg2):
				print("prikaz neprešiel : instr_label", file = sys.stderr)
				exit(32)

		if ((arg2_key == "bool" or arg2_key == "int" or arg2_key == "string" or arg2_key == "var" or arg2_key == "nil") and (arg3_key == "bool" or arg3_key == "int" or arg3_key == "string" or arg3_key == "var" or arg3_key == "nil")):
			symb = True

		if Kontrola_reg(arg2_value) != arg2_key or Kontrola_reg(arg3_value) != arg3_key or symb == False:
			print("prikaz neprešiel : instr_label_2sym", file = sys.stderr)
			exit(32)

# Nadstavenie typu premennej
def Set_type_tmp(argument,typ2):
	if typ2 == "int":
		try:
			argument = int(argument)
			return argument
		except:
			print("Error arg", file = sys.stderr)
			exit(32)

	if typ2 == "bool":
		try:
			if argument=="false" or argument=="False" or argument==False:
				argument = bool(False)
			if argument=="true" or argument=="True" or argument==True:
				argument = bool(True)
			return argument

		except:
			print("Error arg", file = sys.stderr)
			exit(32)

	if typ2 == "string":
		try:
			argument = str(argument)
			return argument
		except:
			print("Error arg", file = sys.stderr)
			exit(32)

	if typ2 == "nil":
		try:
			argument = None
		except:
			print("Error arg", file = sys.stderr)
			exit(32)




OrderStack = []
GF={}

FramesStack=[]
DataStack=[]
Calls=[]
NilStack=[]

Labels={}

LF=None
TF=None
frames = {"GF":GF,"LF":LF,"TF":TF,"FramesStack":FramesStack,"DataStack":DataStack,"Labels":Labels,"Calls":Calls}


class instruct:
	"""objekt instrukce"""
	def __init__(self,opcode,order):
		self.opcode = opcode
		self.order = order
		self.arg1 = []
		self.arg2 = []
		self.arg3 = []



def LABEL(*args):
	instruction=args[0]

	if instruction.arg1[hodnota] not in frames["Labels"]:
		frames["Labels"].update({instruction.arg1[hodnota]:instruction.order})
	else:
		err(52,"Label already exist!")
	return instruction.order+1


zoznam_instr.append(instruct("nic",0))
index1 = 0

#Prvý priechod inštrkcí ktorý ich načíta do pola a urobí z nich objekty
for instruction in vstup:
	if instruction.attrib["opcode"].upper() not in instrukce:
		print("Error instruction not valid")
		exit(32)
	opcode = vstup[index1].attrib["opcode"].upper()
	order = int(vstup[index1].attrib["order"])
	if order in OrderStack:
		err(32,"Order already exists!")
	OrderStack.append(order)
	instr = instruct(opcode,order)
	for arg in instruction:
		#print(arg.tag)
		if arg.tag == "arg1":
			instr.arg1.append(arg.attrib["type"])
			instr.arg1.append(arg.text)
		elif arg.tag == "arg2":
			instr.arg2.append(arg.attrib["type"])
			instr.arg2.append(arg.text)
		elif arg.tag == "arg3":
			instr.arg3.append(arg.attrib["type"])
			instr.arg3.append(arg.text)
		else:
			exit(32)
	Kontrola_arg(instr)
	if instr.opcode == "LABEL":
		LABEL(instr)
	zoznam_instr.append(instr)
	index1 +=1

zoznam_instr = sorted(zoznam_instr, key=operator.attrgetter('order'))
max_order = len(zoznam_instr)-1
order = 1
tmp = 1
# test opcode 
while tmp <= max_order:
	if zoznam_instr[tmp].order != tmp:
		err(32,"Nesedia Opcode!")
	else:
		tmp = tmp+1

# zoznam všetkých inštrukcí
def DEFVAR(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
	    err(55,"Frame does not exist!")

	if arg1[1] in frames[arg1[0]]:
	    err(52,"Variable already declared!")

	frames[arg1[0]].update({arg1[1]:None})
	return instruction.order+1


def CREATEFRAME(*args):
	instruction=args[0]

	global TF
	frames["TF"]={}
	return instruction.order+1

def PUSHFRAME(*args):
	instruction=args[0]

	global TF
	global LF

	if TF == None:
		err(55,"Frames does not exist!")
	FramesStack.append(TF)
	try:
		if len(FramesStack) != 0:
			LF=FramesStack[-1]
		else:
			LF=None
	except:
		err(55,"Frame error!")
	TF=None
	return instruction.order+1

def POPFRAME(*args):
	instruction=args[0]

	global TF
	global LF

	if TF == None:
		err(55,"Frames does not exist!")

	if len(LF) == 0:
		err(55,"Local frame does not exist!")
	TF=FramesStack.pop()
	try:
		if len(FramesStack) != 0:
			LF=FramesStack[-1]
		else:
			LF=None
	except:
		err(55,"Frame error!")
	return instruction.order+1

def MOVE(*args):
	instruction=args[0]
	#Set_type(instruction)

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
	    err(55,"Frame does not exist!")

	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!") 
		frames[arg2[0]].update({arg2[1]:frames[arg1[0]][arg1[1]]})
		print("HALOOOOOOOOOOOOOOOOO:",arg1[1])
		if arg2[1] in NilStack:
			NilStack.append(arg1[1])
	else:
		if instruction.arg2[typ] == "nil":
			NilStack.append(arg1[1])
		new = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		frames[arg1[0]].update({arg1[1]:new})

	return instruction.order+1

def CALL(*args):
	instruction=args[0]

	Calls.append(instruction.order+1)

	if instruction.arg1[hodnota] not in frames["Labels"]:
		err(52,"Label does not exist!") 
	else:
		navrat = frames["Labels"][instruction.arg1[hodnota]]
		if navrat > 0 and navrat <= max_order:
			return navrat+1
		else:
			err(52,"Instruction does not exist!") 

def RETURN(*args):
	instruction=args[0]

	if len(Calls) == 0:
		err(56,"Calls are empty!")
	navrat = Calls.pop()
	if navrat > 0 and navrat <= max_order:
		return navrat + 1
	else:
		err(52,"Instruction does not exist") 


def PUSHS(*args):
	instruction=args[0]

	if instruction.arg1[typ] == "var":
		arg1=instruction.arg1[hodnota].split("@")
		if frames[arg1[0]] == None:
			err(55,"Frame does not exist!")
		if arg1[1] not in frames[arg1[0]]:
			err(54,"Variable does not exist!") # TODO navratovy kód
		DataStack.append(frames[arg1[0]][arg1[1]])
	else:
		new = Set_type_tmp(instruction.arg1[hodnota],instruction.arg1[typ])
		DataStack.append(new)
	return instruction.order+1

def POPS(*args):
	instruction=args[0]


	arg1=instruction.arg1[hodnota].split("@")
	if frames[arg1[0]] == None:
	    err(55,"Frame does not exist!")

	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!") 

	if len(DataStack) == 0:
		err(56,"Zasobnik je prazdny!")
	navrat = DataStack.pop()
	if navrat == None:
		NilStack.append(arg1[1])
	frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def ADD(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None and arg2[1] not in NilStack:
			err(56,"Variable is not set!")
		if type(frames[arg2[0]][arg2[1]]) == type(int(5)):
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Type must by int!")
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Type must be int!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg3[0]][arg3[1]]) == type(int(5)):
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Type must be int!")
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Type must be int!")

	if type(symb1) == type(symb2):
		navrat = symb1 + symb2
		frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def SUB(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg2[0]][arg2[1]]) == type(int(5)):
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Typ neni int!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg3[0]][arg3[1]]) == type(int(5)):
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Typ neni int!")

	if type(symb1) == type(symb2):
		navrat = symb1 - symb2
		frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def MUL(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg2[0]][arg2[1]]) == type(int(5)):
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Typ neni int!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg3[0]][arg3[1]]) == type(int(5)):
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Typ neni int!")

	if type(symb1) == type(symb2):
		navrat = symb1 * symb2
		frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def IDIV(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg2[0]][arg2[1]]) == type(int(5)):
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Typ neni int!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg3[0]][arg3[1]]) == type(int(5)):
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Typ neni int!")
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Typ neni int!")

	if symb2 == 0:
		err(57,"delenie nulou!")
	if type(symb1) == type(symb2):
		navrat = symb1 // symb2
		frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def LT(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if frames[arg2[0]][arg2[1]] != "nil":
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Type nil is not suported!")
	else:
		if instruction.arg2[typ] != "nil":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Type nil is not suported!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if frames[arg3[0]][arg3[1]] != "nil":
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Type nil is not suported!")
	else:
		if instruction.arg3[typ] != "nil":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Type nil is not suported!")

	if type(symb1) == type(symb2):
		if type(symb1) == (type(bool(True))):
			if int(symb1) < int(symb2):
				frames[arg1[0]].update({arg1[1]:bool(True)})
			else:
				frames[arg1[0]].update({arg1[1]:bool(False)})
		else:	
			navrat = symb1 < symb2
			frames[arg1[0]].update({arg1[1]:navrat})
	else:
		err(53,"Types does not match!")
	return instruction.order+1

def GT(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if frames[arg2[0]][arg2[1]] != "nil":
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Type nil is not suported!")
	else:
		if instruction.arg2[typ] != "nil":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Type nil is not suported!")

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		if frames[arg3[0]][arg3[1]] != "nil":
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			err(53,"Type nil is not suported!")
	else:
		if instruction.arg3[typ] != "nil":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Type nil is not suported!")

	if type(symb1) == type(symb2):
		if type(symb1) == (type(bool(True))):
			if int(symb1) > int(symb2):
				frames[arg1[0]].update({arg1[1]:bool(True)})
			else:
				frames[arg1[0]].update({arg1[1]:bool(False)})
		else:	
			navrat = symb1 > symb2
			frames[arg1[0]].update({arg1[1]:navrat})
	else:
		err(53,"Types does not match!")
	return instruction.order+1

def EQ(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None and arg2[1] not in NilStack:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
	else:
		symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None and arg3[1] not in NilStack:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
	else:
		symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])

	if type(symb1) == type(symb2):
		if type(symb1) == (type(bool(True))):
			if int(symb1) == int(symb2):
				frames[arg1[0]].update({arg1[1]:bool(True)})
			else:
				frames[arg1[0]].update({arg1[1]:bool(False)})
		else:	
			navrat = symb1 == symb2
			frames[arg1[0]].update({arg1[1]:navrat})
	else:
		err(53,"Types does not match!")
	return instruction.order+1


def AND(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(bool(True))):
			err(53,"Symbol must be bool!") 
	else:
		if instruction.arg2[typ] == "bool":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be bool!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(52,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(bool(True))):
			err(53,"Symbol must be bool!") 
	else:
		if instruction.arg3[typ] == "bool":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be bool!") 

	if type(symb1) == type(symb2):
		if symb1 and symb2:
			frames[arg1[0]].update({arg1[1]:bool(True)})
		else:
			frames[arg1[0]].update({arg1[1]:bool(False)})
	else:
		err(53,"Types does not match!")
	return instruction.order+1


def OR(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(bool(True))):
			err(53,"Symbol must be bool!") 
	else:
		if instruction.arg2[typ] == "bool":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be bool!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(bool(True))):
			err(53,"Symbol must be bool!") 
	else:
		if instruction.arg3[typ] == "bool":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be bool!") 

	if type(symb1) == type(symb2):
		if symb1 or symb2:
			frames[arg1[0]].update({arg1[1]:bool(True)})
		else:
			frames[arg1[0]].update({arg1[1]:bool(False)})
	else:
		err(53,"Types does not match!")
	return instruction.order+1

def NOT(*args):
	instruction=args[0]
	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(bool(True))):
			err(53,"Symbol must be bool!") 
	else:
		if instruction.arg2[typ] == "bool":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be bool!") 

	if type(symb1) == type(bool(True)):
		if not symb1:
			frames[arg1[0]].update({arg1[1]:bool(True)})
		else:
			frames[arg1[0]].update({arg1[1]:bool(False)})
	else:
		err(53,"Types does not match!")
	return instruction.order+1


def INT2CHAR(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		if type(frames[arg2[0]][arg2[1]]) == type(int(5)):
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			err(53,"Type must by int!")
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Type must be int!")

	if type(symb1) == type(int(5)):
		try:
			navrat = chr(symb1)
			frames[arg1[0]].update({arg1[1]:navrat})
		except:
			err(58,"Pretypovanie zlyhalo!")
	return instruction.order+1


def STRI2INT(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg2[typ] == "string":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be string!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(int(5))):
			err(53,"Symbol must be int!") 
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be int!") 

	try:
		navrat = ord(symb1[symb2])
		frames[arg1[0]].update({arg1[1]:navrat})
	except:
		err(58,"Bad index")
	return instruction.order+1


def CONCAT(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg2[typ] == "string":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be string!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg3[typ] == "string":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be string!") 

	if symb1 == "None":
		symb1 = ""
	if symb2 == "None":
		symb2 = ""
	if type(symb1) == type(symb2):
		try:
			navrat = symb1 + symb2
			frames[arg1[0]].update({arg1[1]:navrat})
		except:
			err(58,"Concat corupted:)!")
	return instruction.order+1


def STRLEN(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg2[typ] == "string":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be string!") 

	navrat = len(symb1)
	frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1


def GETCHAR(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(52,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg2[typ] == "string":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be string!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(52,"Variable is not set!") 
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(int(5))):
			err(53,"Symbol must be int!")
	else:
		if instruction.arg3[typ] == "int":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be int!") 

	try:
		navrat = symb1[symb2]
		frames[arg1[0]].update({arg1[1]:navrat})
	except:
		err(58,"Bad index")
	return instruction.order+1


def SETCHAR(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]][arg2[1]] == None:
			err(56,"Variable is not set!")
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) != (type(int(5))):
			err(53,"Symbol must be int!") 
	else:
		if instruction.arg2[typ] == "int":
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])
		else:
			err(53,"Symbol must be int!") 

	if instruction.arg3[typ] == "var":
		arg3=instruction.arg3[hodnota].split("@")
		if frames[arg3[0]] == None:
			err(55,"Frame does not exist!")
		if arg3[1] not in frames[arg3[0]]:
			err(54,"Variable does not exist!")
		if frames[arg3[0]][arg3[1]] == None:
			err(56,"Variable is not set!")
		symb2 = frames[arg3[0]][arg3[1]]
		if type(symb2) != (type(str("ahoj"))):
			err(53,"Symbol must be string!") 
	else:
		if instruction.arg3[typ] == "string":
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])
		else:
			err(53,"Symbol must be string!") 

	if len(symb2) > 1:
		symb2 = symb2[0]
	try:
		navrat = frames[arg1[0]][arg1[1]]
		navrat = list(navrat)
		navrat[symb1] = symb2
		navrat = "".join(navrat) 
		frames[arg1[0]].update({arg1[1]:navrat})
	except:
		err(58,"Bad index")
	return instruction.order+1


def TYPE(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if instruction.arg2[typ] == "var":
		arg2=instruction.arg2[hodnota].split("@")
		if arg2[1] not in frames[arg2[0]]:
			err(54,"Variable does not exist!")
		if frames[arg2[0]] == None:
			err(55,"Frame does not exist!")
		if frames[arg2[0]][arg2[1]] == None and arg2[1] in NilStack:
			navrat = "nil"
		else:
			if frames[arg2[0]][arg2[1]] == None:
				navrat = ""
		symb1 = frames[arg2[0]][arg2[1]]
		if type(symb1) == (type(int(5))):
			navrat = "int"
		if type(symb1) == (type(bool(True))):
			navrat = "bool"
		if type(symb1) == (type(str("ahoj"))):
			navrat = "string"
	else:
		if instruction.arg2[typ] == "nil":
			navrat = "nil"
		if instruction.arg2[typ] == "string":
			navrat = "string"
		if instruction.arg2[typ] == "bool":
			navrat = "bool"
		if instruction.arg2[typ] == "int":
			navrat = "int"

	try:
		frames[arg1[0]].update({arg1[1]:navrat})
	except:
		err(58,"Bad type")
	return instruction.order+1

def JUMP(*args):
	instruction=args[0]

	if instruction.arg1[hodnota] not in frames["Labels"]:
		err(52,"Label does not exist!") 
	else:
		navrat = frames["Labels"][instruction.arg1[hodnota]]
		if navrat > 0 and navrat <= max_order:
			return navrat+1
		else:
			err(52,"Instruction does not exist!") 

def JUMPIFEQ(*args):
	instruction=args[0]

	if instruction.arg1[hodnota] not in frames["Labels"]:
		err(52,"Label does not exist!") 
	else:
		if instruction.arg2[typ] == "var":
			arg2=instruction.arg2[hodnota].split("@")
			if frames[arg2[0]] == None:
				err(55,"Frame does not exist!")
			if arg2[1] not in frames[arg2[0]]:
				err(52,"Variable does not exist!")
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])

		if instruction.arg3[typ] == "var":
			arg3=instruction.arg3[hodnota].split("@")
			if frames[arg3[0]] == None:
				err(55,"Frame does not exist!")
			if arg3[1] not in frames[arg3[0]]:
				err(52,"Variable does not exist!")
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])

		if type(symb1) == type(symb2):
			if symb1 == symb2:
				navrat = frames["Labels"][instruction.arg1[hodnota]]
				if navrat > 0 and navrat <= max_order:
					return navrat+1
				else:
					err(52,"Instruction does not exist!")
			else:
				return instruction.order+1
		else:
			err(53, "Types does not match!")

def JUMPIFNEQ(*args):
	instruction=args[0]

	if instruction.arg1[hodnota] not in frames["Labels"]:
		err(52,"Label does not exist!") 
	else:
		if instruction.arg2[typ] == "var":
			arg2=instruction.arg2[hodnota].split("@")
			if frames[arg2[0]] == None:
				err(55,"Frame does not exist!")
			if arg2[1] not in frames[arg2[0]]:
				err(52,"Variable does not exist!")
			symb1 = frames[arg2[0]][arg2[1]]
		else:
			symb1 = Set_type_tmp(instruction.arg2[hodnota],instruction.arg2[typ])

		if instruction.arg3[typ] == "var":
			arg3=instruction.arg3[hodnota].split("@")
			if frames[arg3[0]] == None:
				err(55,"Frame does not exist!")
			if arg3[1] not in frames[arg3[0]]:
				err(52,"Variable does not exist!")
			symb2 = frames[arg3[0]][arg3[1]]
		else:
			symb2 = Set_type_tmp(instruction.arg3[hodnota],instruction.arg3[typ])

		if type(symb1) == type(symb2):
			if symb1 != symb2:
				navrat = frames["Labels"][instruction.arg1[hodnota]]
				if navrat > 0 and navrat <= max_order:
					return navrat+1
				else:
					err(52,"Instruction does not exist!")
			else:
				return instruction.order+1
		else:
			err(53, "Types does not match!")
			

def EXIT(*args):
	instruction=args[0]

	if instruction.arg1[typ] == "var":
		arg1=instruction.arg1[hodnota].split("@")

		if frames[arg1[0]] == None:
			err(55,"Frame does not exist!")

		if arg1[1] not in frames[arg1[0]]:
			err(54,"Variable does not exist!")
		if type(frames[arg1[0]][arg1[1]]) == type(int(5)):
			if frames[arg1[0]][arg1[1]] > 0 and frames[arg1[0]][arg1[1]] <= 49:
				exit(frames[arg1[0]][arg1[1]])
			else:
				err(57,"Not valid number!") 
		else:
			err(53,"Not valid type!")
	else:
		if instruction.arg1[typ] == "int":
			navrat = Set_type_tmp(instruction.arg1[hodnota],instruction.arg1[typ])
			if navrat > 0 and navrat <= 49:
				exit(navrat)
			else:
				err(57,"Not valid number!") 
		else:
			err(53,"Not valid type!")


def DPRINT(*args):
	instruction=args[0]

	if instruction.arg1[typ] == "var":
		arg1=instruction.arg1[hodnota].split("@")

		if frames[arg1[0]] == None:
			err(55,"Frame does not exist!")

		if arg1[1] not in frames[arg1[0]]:
			err(54,"Variable does not exist!")
		navrat = frames[arg1[0]][arg1[1]]
		print(navrat, file = sys.stderr)
	else:
		navrat = Set_type_tmp(instruction.arg1[hodnota],instruction.arg1[typ])
		print(navrat, file = sys.stderr)
	return instruction.order+1

def BREAK(*args):
	instruction=args[0]

	print("GF: ",GF, file = sys.stderr)
	print("LF: ",LF, file = sys.stderr)
	print("TF: ",TF, file = sys.stderr)
	print("DataStack: ",DataStack, file = sys.stderr)
	print("Labels:" ,Labels, file = sys.stderr)

	print("Instrukce:",instruction.order, file = sys.stderr)
	return instruction.order+1


def READ(*args):
	instruction=args[0]

	arg1=instruction.arg1[hodnota].split("@")

	if frames[arg1[0]] == None:
		err(55,"Frame does not exist!")
	if arg1[1] not in frames[arg1[0]]:
		err(54,"Variable does not exist!")

	if input_file is not None:
		navrat = input_file.readline()
		navrat = navrat.rstrip("\n")
	else:
		navrat = input()

	instr_type = instruction.arg2[hodnota]
	if instr_type == "int":
		navrat = Set_type_tmp(navrat,instr_type)
	elif instr_type == "string":
		navrat = Set_type_tmp(navrat,instr_type)
	elif instr_type == "bool":
		if navrat == True or navrat == "True" or navrat == "true":
			navrat = True
		else:
			navrat = False
	frames[arg1[0]].update({arg1[1]:navrat})
	return instruction.order+1

def WRITE(*args):
	instruction=args[0]


	if instruction.arg1[typ] == "nil":
		print("",end='')
		return instruction.order+1

	if instruction.arg1[typ] == "var":
		arg1=instruction.arg1[hodnota].split("@")
		if frames[arg1[0]] == None:
			err(55,"Frame does not exist!")
		if arg1[1] not in frames[arg1[0]]:
			err(54,"Variable does not exist!") # TODO navratovy kód
		if frames[arg1[0]][arg1[1]] == None and arg1[1] in NilStack:
			print("",end='')
		if type(frames[arg1[0]][arg1[1]]) is bool:
			if frames[arg1[0]][arg1[1]] == True:
				print("true",end='')
			if frames[arg1[0]][arg1[1]] == False:
				print("false",end='')
		else:
			print(frames[arg1[0]][arg1[1]],end='')
	else:
		if type(instruction.arg1[hodnota]) is bool:
			if instruction.arg1[hodnota] == True:
				print("true",end='')
			if instruction.arg1[hodnota] == False:
				print("false",end='')
		else:
			print(instruction.arg1[hodnota],end='')
	return instruction.order+1


while order <= max_order:
	if zoznam_instr[order].opcode == "LABEL":
		order = order+1
		continue
	order = globals()[zoznam_instr[order].opcode](zoznam_instr[order])