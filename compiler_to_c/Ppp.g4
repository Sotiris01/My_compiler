

grammar Ppp;

@parser::members {

exe   = open("exe.c", "w")
header = open("header.h", "w")

classDict = {}
define = {}

def start(self):
	print("Start...")
	self.add("#include <stdio.h>")
	self.add("#include \"header.h\"")
	self.add("")

	self.Hadd("#define true  1")
	self.Hadd("#define false 0")
	self.Hadd("")

def end(self):
	print("End...")
	self.add("")
	self.add("int main(){")
	self.add("")
	self.add("\tmain_t main_self;")
	self.add("")
	self.add("\tmain__main(&main_self);")
	self.add("")
	self.add("\treturn 0;")
	self.add("}")
	self.exe.close()
	self.header.close()


def add(self, line):
	self.exe.write(line+"\n")

def Hadd(self, line):
	self.header.write(line+"\n")

def TAB(self, str):
	for i in range(len(str)):
		if str[i] == '\n':
			str = str[:i+1]+'\t'+str[i+1:]
	return '\t'+ str
}

/*
 * Parser Rules
 */

startRule 
	: 	{self.start()}
	 	(fixedVar)* classBegan* mainClassBegan EOF
	 	{self.end()}
	 	//{for c in self.classDict:}
	 	//{	print(c)}
	 	//{	print(self.classDict[c])}
	 	//{	print("")}
	;

fixedVar
	:	'@' IDENTIFIER NUM
		{self.define[$IDENTIFIER.text] = $NUM.text}
	;

mainClassBegan 
	:	CLASS MAIN ':'
		{self.classDict["main"] = {}}
		{self.currentClass = "main"}
		mainClassBody	
	;

classBegan
	:	{self.inheritsList = []}
		CLASS IDENTIFIER inherits? ':'
		{self.classDict[$IDENTIFIER.text] = {}}
		{self.currentClass = $IDENTIFIER.text}
		//{print(self.currentClass)}
		//{print(self.inheritsList)}
		classBody
	;

inherits
	:	INHERITS IDENTIFIER 	{self.inheritsList.append($IDENTIFIER.text)} 
			(','IDENTIFIER 		{self.inheritsList.append($IDENTIFIER.text)})*
	;

mainClassBody 
	:	{self.classDict[self.currentClass]["declarations"] = {}}
		classDeclarations
		{self.Hadd("")}
		{self.Hadd("typedef struct main_s{")}
		{self.Hadd($classDeclarations.cds)}
		{self.Hadd("}main_t;")}
		{self.classDict[self.currentClass]["methods"] = {}}
		mainClassBlock
		
	;



classBody
	:	{self.classDict[self.currentClass]["declarations"] = {}}
		classDeclarations
		{self.Hadd("")}
		{self.Hadd("typedef struct "+self.currentClass+"_s{")}
		{self.Hadd($classDeclarations.cds)}
		{self.Hadd("}"+self.currentClass+"_t;")}
		{self.classDict[self.currentClass]["methods"] = {}}
		classBlock
		{for inherit in self.inheritsList:}
		{	for method, description in self.classDict[inherit]["methods"].items():}
		{		if description["type"] == "method":}
		{			if self.classDict[self.currentClass]["methods"][method]["inhered"]:}
		{				if description["return"] == "void":}
		{					m = "void "}
		{				elif description["return"] in ["int","bool"]:}
		{					m = "int "}
		{				else:}
		{					m = description["return"] +"_t* "}
		{				m += self.currentClass +"__"+ method +'('+ self.currentClass+"_t* self"}
		{				self.classDict[self.currentClass]["methods"][method] = {"parameters": []}}
		{				self.classDict[self.currentClass]["methods"][method]["declarations"] = {}}
		{				for param in self.classDict[inherit]["methods"][method]["parameters"]:}
		{					m += ", int "+ param}
		{					self.classDict[self.currentClass]["methods"][method]["parameters"].append(param)}
		{					self.classDict[self.currentClass]["methods"][method]["declarations"][param] = "int"}
		{				m += ") {\n"}
		{				self.classDict[self.currentClass]["methods"][method]["return"] = description["return"]}
		{				self.classDict[self.currentClass]["methods"][method]["type"] = "method"}
		{				self.classDict[self.currentClass]["methods"][method]["inhered"] = False}
		{				m += description["body"] +"}\n"}
		{				self.classDict[self.currentClass]["methods"][method]["body"] = description["body"]}
		{				self.add(m)}
		{self.add($classBlock.c)}
	;

classDeclarations returns[string cds]
	:							{$cds  = ""}
		((CD=classDeclaration	{$cds += '\t'+ $CD.cd +'\n'})+';')?
								{if self.currentClass not in ["main"]:}
								{	for inherit in self.inheritsList:}
								{		for declar, type in self.classDict[inherit]["declarations"].items():}
								{			if declar not in self.classDict[self.currentClass]["declarations"]:}
								{				self.classDict[self.currentClass]["declarations"][declar] = type}
								{				$cds += '\t'+ type +' '+ declar +";\n"}
	;

classDeclaration returns[string cd]
	:	(INT 			{$cd="int "}
						{type = "int"}
	|	BOOL 			{$cd="int "}
						{type = "int"}
	|	IDENTIFIER 		{$cd=$IDENTIFIER.text+"_t "}
						{type = $IDENTIFIER.text} )

		IDENTIFIER 		{$cd +=       $IDENTIFIER.text} 
						{self.classDict[self.currentClass]["declarations"][$IDENTIFIER.text]=type}
		(','IDENTIFIER 	{$cd += ',' + $IDENTIFIER.text}
						{self.classDict[self.currentClass]["declarations"][$IDENTIFIER.text]=type}
		)* ';'
						{$cd += ';'}
	;

mainClassBlock 
	:	(method 	{self.add($method.m)})*
		mainMethod	{self.add($mainMethod.m)}
	;

classBlock returns[string c=""]
	:	(initMethod	{self.add($initMethod.m)})+

		{for inherit in self.inheritsList:}
		{	for method, description in self.classDict[inherit]["methods"].items():}
		{			if description["type"] == "method":}
		{				self.classDict[self.currentClass]["methods"][method] = {"return": description["return"]}}
		{				self.classDict[self.currentClass]["methods"][method]["inhered"] = True}

		(method 	{$c += $method.m})*
	;

mainMethod returns[string m = "\n"]
	:	DEF	MAIN '(' SELF ')' ':' '-'
				{self.currentMethod = {"name": "main", "type": "void"}}
				{$m += "void main__main(main_t* self){\n"}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]] = {"return": self.currentMethod["type"]}}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["type"] = "main"}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"] = {}}
		body 	{$m += $body.b+"}"}
	;

initMethod returns[string m = "\n"]
	:	DEF	INIT
				{self.currentMethod = {"name": self.currentClass, "type": "void"}}
				//{self.currentMethod = {"name": "constructor", "type": "void"}}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]] = {"parameters": []}}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"] = {}}
		FP=formalParameters ':' IDENTIFIER
				{$m += "void "+self.currentClass+"__"+str($FP.n)+$FP.fp+"{\n"}
				{self.currentMethod["name"] = self.currentClass+"__"+str($FP.n)}
				//{self.currentMethod["name"] = "constructor__"+str($FP.n)}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]] = self.classDict[self.currentClass]["methods"].pop(self.currentClass)}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["return"] = self.currentMethod["type"]}
				{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["type"] = "constructor"}
		body 	{$m += $body.b+"}"}
	;

method returns[string m = "\n"]
	:	DEF	name=IDENTIFIER
						{self.currentMethod = {"name": $name.text, "type": ""}}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]] = {"parameters": []}}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"] = {}}
		FP=formalParameters ':' 
		('-'			{$m += "void "}
						{self.currentMethod["type"] = "void"}
		| INT 			{$m += "int "}
						{self.currentMethod["type"] = "int"}
		| BOOL 			{$m += "int "}
						{self.currentMethod["type"] = "bool"}
		| IDENTIFIER 	{$m += $IDENTIFIER.text+"_t* "}
						{self.currentMethod["type"] = $IDENTIFIER.text})
						{$m += self.currentClass+"__"+$name.text+"__"+str($FP.n)+$FP.fp+"{\n"}
						{self.currentMethod["name"] = self.currentMethod["name"]+"__"+str($FP.n)}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]] = self.classDict[self.currentClass]["methods"].pop($name.text)}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["return"] = self.currentMethod["type"]}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["type"] = "method"}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["inhered"] = False}
		body 			{$m += $body.b+"}\n"}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["body"] = $body.b}
	;

formalParameters returns[int n=0, string fp = ""]
	:	 '(' SELF 		{$fp += '('+self.currentClass+"_t* self"}
		(',' IDENTIFIER {$fp += ", int "+$IDENTIFIER.text}
						{$n += 1}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["parameters"].append($IDENTIFIER.text)}
						{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"][$IDENTIFIER.text] = "int"})* 
		 ')' 			{$fp += ')'}
	;

body returns[string b=""]
	:	(PASS';'{if self.currentMethod["type"] in ["int", "bool"]:}
				{	$b = "return 0;"}
	|	block 	{$b = $block.b}) ';'
	;

block returns[string b=""]
	:	(statement ';' {$b += self.TAB($statement.s)+'\n'})+ 
	;

statement returns[string s]
	:	localDeclaration	{$s = $localDeclaration.l}
	|	callConstructor 	{$s = $callConstructor.c}
	|	assignmentState		{$s = $assignmentState.a}
	|	ifState				{$s = $ifState.i}
	|	whileState 			{$s = $whileState.w}
	|	returnState			{$s = $returnState.r}
	|	printState			{$s = $printState.p}
	|	scanState			{$s = $scanState.s}
	|	callMethod			{$s = $callMethod.m+";;"}
	|	BREAK 				{$s = "break ;;"} //';;' What..?? why...???
	;


localDeclaration returns[string l]
	:	(INT 				{$l = "int "} 
							{type = "int"}
	| 	BOOL 				{$l = "int "}
							{type = "int"}
	| 	IDENTIFIER 			{$l = $IDENTIFIER.text+"_t "}
							{type = $IDENTIFIER.text})

		IDENTIFIER 			{$l += $IDENTIFIER.text}
		(assign expressions	{$l += ' '+ $assign.a +' '+ $expressions.e})? 
							{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"][$IDENTIFIER.text] = type}
		(','IDENTIFIER		{$l += ', ' + $IDENTIFIER.text}
		(assign expressions	{$l += ' '+ $assign.a +' '+ $expressions.e})? 	
							{self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"][$IDENTIFIER.text] = type}
					)* 
							{$l += ";"}
	;

callConstructor returns[string c]
	:	ID=identifier ASSIGN IDENTIFIER '(' {par=""}{n=0}(P=parameters{par = $P.p}{n=$P.n})? ')'
		{$c = $IDENTIFIER.text+"__"+str(n)+"(&"+$ID.i+par+');;'}
	;

assignmentState returns[string a]
	:	ID=identifier assign expressions
		{$a = $ID.i +' '+ $assign.a +' '+ $expressions.e +";;"}
	;

ifState returns[string i=""]
	:	IF C=conditions ':' block 
		{$i += "\nif ("+ $C.c +"){\n"}
		{$i += $block.b +'}'}
		(ELIF C=conditions ':' block
		{$i += "else if ("+ $C.c +"){\n"}
		{$i += $block.b +"}"})* 
		(ELSE ':' block
		{$i += "else {\n"+ $block.b +"}"})?
		{$i += "   "}
	;

whileState returns[string w=""]
	:	WHILE C=conditions ':' block 
		{$w += "\nwhile ("+ $C.c +"){\n"}
		{$w += $block.b +"\t}"}
	;


returnState returns[string r=""]
	:	RETURN expressions
		{if self.currentMethod["type"] in ["int","bool"]:}
		{	$r += "return "+ $expressions.e +';'}
		{else:}
		{	$r += "return &"+ $expressions.e +';'}
	;

printState returns[string p=""]
	:								{$p += "printf(\"%d\\n\", "}
		OUT '(' (I=identifier 		{$p += $I.i}
				|M=callMethod 		{$p += $M.m}
				|   NUM 			{$p += $NUM.text}) ')'
									{$p += ");\n"}
	;

scanState returns[string s=""]
	:	IN '('ID=IDENTIFIER')'
		{$s += "scanf(\"%d\", &"+ $ID.text +");\n"}
	;

conditions returns[string c=""]
	:	(NOT 		{$c += '!'})? 
		expressions	{$c += '('+ $expressions.e +')'}
	;

expressions returns[string e=""]
	:	'(' expressions ')' {$e += '('+ $expressions.e +')'}
	|	E1=expressions	operetor E2=expressions
							{$e += $E1.e +' '+ $operetor.o +' '+ $E2.e}
	|	expression 			{$e += $expression.e}
	;

operetor returns[string o=""]
	:	math_op 	{$o += $math_op.m}
	|	relat_op 	{$o += $relat_op.r}
	|	logical_op 	{$o += $logical_op.l}
//	|	identity_op
	;

expression returns[string e=""]
	:	callMethod		{$e += $callMethod.m}
	|	identifier		{$e += $identifier.i}
	|	NUM 			{$e += $NUM.text}
	|	BOOLEAN 		{$e += $BOOLEAN.text}
	;

callMethod  returns[string m=""]
	:	(SELF  		{activeClass = self.currentClass} 	// from this class or parent's
						{x = "self"}
	|	ID=identifier	{activeClass = $ID.type}  			// from another class
						{x = "&"+$ID.i})

	('.' IDENTIFIER '(' {par=""}{n=0}(P=parameters{par = $P.p}{n=$P.n})? ')'
						{x = activeClass+"__"+$IDENTIFIER.text+"__"+str(n)+'('+x+par+')'}
						{activeClass = self.classDict[activeClass]["methods"][$IDENTIFIER.text+"__"+str(n)]["return"]})+
						{$m = x}
	;

parameters returns[int n, string p=""]
	:	parameter 		{$p += ', '+$parameter.p}
						{$n = 1}
		(',' parameter 	{$p += ', '+$parameter.p}
						{$n += 1})*
	;

parameter returns[string p]
	:	IDENTIFIER 	{if $IDENTIFIER.text in self.define:}
					{	$p = self.define[$IDENTIFIER.text]}
					{else:}
					{	$p = $IDENTIFIER.text}
	|	NUM 		{$p = $NUM.text}
	|	BOOLEAN 	{$p = $BOOLEAN.text}
	;

identifier returns[string type, string i=""]
	:				{local = True}
		(SELF '.' 	{$i += "self->"}
					{local = False})? 
		IDENTIFIER 	{if $IDENTIFIER.text in self.define:}
					{	$i = self.define[$IDENTIFIER.text]}
					{else:}
					{	$i += $IDENTIFIER.text}
					{	if local:}
					{		$type = self.classDict[self.currentClass]["methods"][self.currentMethod["name"]]["declarations"][$IDENTIFIER.text]}
					{	else:}
					{		$type = self.classDict[self.currentClass]["declarations"][$IDENTIFIER.text]}
	;

math_op	returns[string m=""]
	:	ADD 	{$m += $ADD.text}
	| 	SUB 	{$m += $SUB.text}
	| 	MUL 	{$m += $MUL.text}
	| 	DIV 	{$m += $DIV.text}
	;

relat_op returns[string r=""]
	:	GT 		{$r += $GT.text}
	| 	LT 		{$r += $LT.text}
	| 	EQUAL 	{$r += $EQUAL.text}
	|	LE 		{$r += $LE.text}
	| 	GE 		{$r += $GE.text}
	| 	NOTEQUAL{$r += $NOTEQUAL.text}
	;

logical_op returns[string l=""]
	:	AND 	{$l += "&&"}
	|	OR 		{$l += "||"}
	;

assign returns[string a=""]
	:	ASSIGN 			{$a += $ASSIGN.text}
	|	ADD_ASSIGN 		{$a += $ADD_ASSIGN.text} 
	| 	SUB_ASSIGN 		{$a += $SUB_ASSIGN.text}
	|	MUL_ASSIGN 		{$a += $MUL_ASSIGN.text}
	| 	DIV_ASSIGN 		{$a += $DIV_ASSIGN.text}
	;

//identity_op	
//	:	IS | (IS NOT)
//	;



/*
 * Lexer Rules
 */

CLASS		:	'class';
DEF 		:	'def';
MAIN 		:	'main';
INHERITS	:	'inherits';
INT			:	'int';
BOOL 		:	'bool';
INIT		:	'__init__';
SELF		:	'self';
RETURN		:	'return';
PASS		:	'pass';
IF			:	'if';
ELIF		:	'elif';
ELSE		:	'else';
WHILE		:	'while';
BREAK		:	'break';
IN 			:	'in';
OUT 		:	'out';

BOOLEAN		:	TRUE | FALSE;

TRUE		:	'true';
FALSE		:	'false';

//UNDERSCORE	:	'_';

GT			:	'>';
LT			:	'<';
EQUAL		:	'==';
LE			:	'<=';
GE			:	'>=';
NOTEQUAL	:	'!=';

ASSIGN		:	'=';
ADD_ASSIGN  :	'+=';
SUB_ASSIGN  :	'-=';
MUL_ASSIGN	:	'*=';
DIV_ASSIGN	:	'/=';

LPAREN		:	'(';
RPAREN		:	')';
SEMI		:	';';
COLON		:	':';
COMMA		:	',';
DOT			:	'.';

ADD			:	'+';
SUB			:	'-';
MUL			:	'*';
DIV			:	'/';

AND 		:	'and';
OR			:	'or';


//IS 			: 'is';
NOT			: 'not';

AT 			: '@';

IDENTIFIER	:	(LETTER (LETTER | [0-9] | '_')*);

LETTER		:	[a-zA-Z];
NUM			:	'-'? [0-9]+;
WS			:	[ \t\r\n]	->	skip;

COMMENTS	:	('###' ~[\r\n]* | '#' .*? '#') -> skip;