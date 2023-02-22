#SOTIRIS MPALATSIAS      AM 3036       USERNAME cse53036
#SOTIRIA KASTANA 		 AM 2995	   USERNAME cse52995


import sys, getopt

# me orismata 2 lekseis epistrefei se pososto epi % to poso diaferoun (100% -> entelws diaforetika kai 0% -> entelws idia)
def levenshtein(seq1, seq2):  
	size_x = len(seq1) + 1
	size_y = len(seq2) + 1
	matrix = [[0 for x in range(size_y)] for y in range(size_x)]
	for x in range(size_x):
		matrix [x][0] = x
	for y in range(size_y):
		matrix [0][y] = y

	for x in range(1, size_x):
		for y in range(1, size_y):
			if seq1[x-1] == seq2[y-1]:
				matrix [x][y] = min(
					matrix[x-1][y] + 1,
					matrix[x-1][y-1],
					matrix[x][y-1] + 1
				)
			else:
					matrix [x][y] = min(
					matrix[x-1][y] + 1,
					matrix[x-1][y-1] + 1,
					matrix[x][y-1] + 1
				)
	return ((matrix[size_x - 1][size_y - 1])/len(seq2),seq2)

# me vash ena ID kai mia lista leksewn epistrefei mia leksi mesa apo tin lista me tin opoia moiazei to ID perissotero
# epistrefei false ean h omoiotita tou ID me ta onomata tis listas einai polu mikrh 
def devenshtein_distance(id,list):

	difference_rate_array = []

	if list == None:
		list = ["if","while","dowhile","loop","exit","forcase","incase","return","print","input"]

	for l in list:
		difference_rate_array.append(levenshtein(id,l))

	min_value = min(difference_rate_array)

	if(min_value[0] < 0.5):
		return min_value[1]
	else:
		return False    

# me orisma (1) mas epistrefei ton epomeno xarakthra pou diavazei apo to arxeio . stl
# me orisma (-1) mas epistrefei ton prohgoumeno xarakthra tou arxeiou
def my_read(i):
	global line 
	global next_char
	global preview_char
	if (i == 1):
		if(preview_char == False):
			next_char = input_file.read(1)#--read--
		else:
			preview_char = False
		if (next_char == "\n"):
			line += 1
	elif (i == -1):
		if(next_char == "\n"):
			preview_char = True
			line -= 1
		else:
			preview_char = True
	else:
		pass

def lex ():

	global token
	global tokenID
	global line 
	global next_char   
	

	my_read(1)#--read--
	if(next_char == ''):    
		token = next_char
		tokenID = "EOFtk"
		return True # Okay

	while (next_char.isspace()) :    #---> white characters
		my_read(1)#--read-- 
		if(next_char == ''):
			token = next_char
			tokenID = "EOFtk"
			return True # Okay

	if (next_char.isalpha()) :        #---> letter
		mybuffer = next_char
		my_read(1)#--read--
		while (next_char.isalpha() or next_char.isdigit()) :
			mybuffer += next_char
			my_read(1)#--read--
		my_read(-1)#--preview character--
		if mybuffer in reserved_words:
			token = mybuffer
			tokenID = mybuffer + "tk"
			return True # Okay         #---> desdesmevmeni leksi
		if(len(mybuffer) > 30):
			mybuffer = mybuffer[0:30]
		token = mybuffer
		tokenID = "IDtk"
		return True # Okay             #---> id

	elif (next_char.isdigit()) :     #---> number
		mybuffer = next_char
		my_read(1)#--read--
		while (next_char.isdigit()) :
			mybuffer += next_char
			my_read(1)#--read--
		my_read(-1)#--preview character--
		if (int(mybuffer) > 32767):
			print ("\nSyntax Error in line: "+str(line)+" \n-> Numbers must be between -32767 end 32757 !!!\n")
			sys.exit()#error
		token = mybuffer
		tokenID = "constanttk"
		return True # Okay

	elif (next_char == "+") :      #---> +
		token = next_char
		tokenID = "addtk"
		return True # Okay

	elif (next_char == "-") :      #---> -
		token = next_char
		tokenID = "addtk"
		return True # Okay

	elif (next_char == "<") :      #---> <
		mybuffer = next_char
		my_read(1)#--read--
		if(next_char == "="):      #---> <=
			mybuffer += next_char
		elif(next_char == ">"):    #---> <>
			mybuffer += next_char
		else:
			my_read(-1)#--preview character--
		token = mybuffer
		tokenID = "relationaltk"
		return True # Okay

	elif (next_char == ">") :      #---> >
		mybuffer = next_char
		my_read(1)#--read--
		if(next_char == "="):       #---> >=
			mybuffer += next_char 
		else:
			my_read(-1)#--preview character--
		token = mybuffer
		tokenID = "relationaltk"
		return True # Okay
 
	elif (next_char == "=") :      #---> =
		token = next_char
		tokenID = "relationaltk" 
		return True # Okay

	elif (next_char == "*") :      #--- > *
		mybuffer = next_char
		my_read(1)#--read--
		if(next_char == "/"):       #---> >=
			print ("\nSyntax Error in line: "+str(line)+" \n-> Closed comments whithout opening them !!!\n") 
			sys.exit()
		else:
			my_read(-1)#--preview character--
		token = mybuffer
		tokenID = "multk"
		return True # Okay
		
	elif (next_char == "/") :                #---> /
		my_read(1)#--read--
		if (next_char == "/"):               #---> //
			my_read(1)#--read--
			while (next_char != "\n") :
				if(next_char == ''):
					token = next_char
					tokenID = "EOFtk"
					return True # Okay
				if (next_char != "/") :
					my_read(1)#--read--
				else:
					my_read(1)#--read--
					if (next_char == "/" or mybuffer == "*"):
						print ("\nSyntax Error in line: "+str(line)+" \n-> We can't have comments in comments !!!\n")
						sys.exit()#error
			lex()

		elif(next_char == "*"):              #---> /*
			open_com_line = line
			my_read(1)#--read--
			next_char_0 = next_char
			my_read(1)#--read--
			while (not(next_char_0 == "*" and next_char == "/")) :
				if (next_char_0 == "/" and next_char  == "/") :
					print ("\nSyntax Error in line: "+str(line)+" \n-> We can't have comments in comments !!!\n")
					sys.exit()#error
				elif (next_char_0 == "/" and next_char  == "*") :
					print ("\nSyntax Error in line: "+str(line)+" \n-> We can't have comments in comments !!!\n")
					sys.exit()#error
				elif (next_char_0 == '' or next_char  == '') :
					print ("\nSyntax Error in line: "+str(line)+" \n-> Opened comments in line: "+str(open_com_line)+" without closing them !!!\n")
					sys.exit()#error
				next_char_0 = next_char
				my_read(1)#--read--
			lex()
		
		else:
			my_read(-1)#--preview character--
			token = '/'
			tokenID = "multk"
			return True # Okay

	elif (next_char == ",") :    #---> ,
		token = next_char
		tokenID = "commatk" 
		return True # Okay

	elif (next_char == ";") :     #---> ;
		token = next_char
		tokenID = "semicolontk"
		return True # Okay 
 
	elif (next_char == ":") :      #---> :
		mybuffer = next_char
		my_read(1)#--read--
		if(next_char == "="):      #---> :=
			mybuffer += next_char 
		else:
			my_read(-1)#--preview character--
			token = mybuffer
			tokenID = "colontk"
			return True # Okay
		token = mybuffer
		tokenID = "colonEqualtk"
		return True # Okay

	elif (next_char == "[") :     #---> [
		token = next_char
		tokenID = "openBracketstk"
		return True # Okay

	elif (next_char == "]") :     #---> ]
		token = next_char
		tokenID = "closeBracketstk"
		return True # Okay

	elif (next_char == "(") :     #---> (
		token = next_char
		tokenID = "openParenthesestk"
		return True # Okay

	elif (next_char == ")") :     #---> )
		token = next_char
		tokenID = "closeParenthesestk"
		return True # Okay
	else:
		print("\nSyntax Error in line: "+str(line)+
			" \n-> Starlet doesn't support symbol {" + next_char + "}\n")
		sys.exit()#error

# prosthetei tis 4ades tou endiamesou kwdika stin global quad_List
def genquad(a, b, c, d):
	global quad_list
	quad_list.append([nextquad(), a, b, c, d])
	
def genquad_c(a):
	global quad_list_c
	quad_list_c.append([nextquad()-1, a])

def update_varlist_c(a):
	global varlist_c
	if a not in varlist_c:
		varlist_c.append(a)

# epistrefei ton arithmo tis epomenis tetradas tou endiamesou kwdika	
def nextquad():
	return len(quad_list)

# epistrefei kathe fora kai diaforetiko onoma typou T_i (opou i enas akeraios arithmos) 
def newTemp():
	global new_temp
	new_temp+=1
	tempVar = "T_"+str(new_temp)
	addEntityNewTempVar(tempVar)
	update_varlist_c(tempVar)
	return tempVar

# sygxwnevei tis listes A,B stin list kai tin epistrefei 
def merge(A, B):
	list = A + B
	return list

# epistrefei mia kenh lista
def emptylist():
	return []

# sta stoixeia tis global quad_list , ta opoia einai shmademena sto list, 
# topothetoume sti teleftaia thesi tis 4adas to label
def backpatch(list, label):
	global quad_list
	for l in list:
		for ql in quad_list:
			if ql[0] == l:
				ql[4] = label
				break
	backpatch_c(list, label)			

def backpatch_c(list, label):
	global quad_list_c
	for l in list:
		for ql in quad_list_c:
			if ql[0] == l:
				ql[1] += " L_"+str(label)+";"
				break
				
# epistrefei mia lista me to stoixeio a 
def makelist(a):
	return [a]

# kathe fora pou diagrafoume ena Scope kaloume tin genASM, 
# , h opoia diavazei tin lista me tis 4ades tou endiamesou kwdika, 
# , ksekinwntas kathe fora apo ekei pou teleiwse mexri kai tin
# teleftaia 4ada pou exei paraxthei mexri stigmhs .
# Dhladh kathe fora pou kaleitai metatrepei mia synartisi se teliko kwdika. 
def genASM(main):
	global asm_list
	par_count = 0		# voithikos metritis me ton opoio metrame to plithos parametrwn , kathe fora pou kaleitai mia synartisi
	L = 0				# voithitiki metavliti
	l = len(asm_list)-1 # to shmeio apo to opoio synexizoume tin anagnosi tou endiamesou kwdika 
	if main :			# an h main == True ksekinaei h metafrasi tis main kai topothetoume tin label "Lmain"
		asm_list.append({"label": "Lmain:", "commands": []})
		asm_list[-1]["commands"].append("add $sp,$sp,"+str(Scope_list[-1]["totalOffset"]))
		asm_list[-1]["commands"].append("move $s0,$sp")

	for quad in quad_list[l:]:
		commands = []
		if quad[1] == "begin_block":
			par_count = 0
			commands += (begin(quad))
		elif quad[1] == "end_block":
			par_count = 0
			commands += (end(quad))
		elif quad[1] == ":=":
			par_count = 0
			commands += (assignment(quad))
		elif quad[1] in ["=", "<", ">", "<=", ">=", "<>"] :
			par_count = 0
			commands += (branch(quad))
		elif quad[1] in ["-", "+", "*", "/"] :
			par_count = 0
			commands += (op(quad))
		elif quad[1] == "par":
			if par_count == 0:		# stin periptosi afti, einai i proti parametros kai ksekinaei mia klisi mias synartisis
				par_count += 1
				L = len(asm_list)   # shmeionoume tin sugkekrimenh grammi tou telikou kwdika gia na tin symplirosoume 
									# meta pou tha kseroume to onoma tis synartisis pou tha klhthei 
				commands += (first_par_0())
			comm,CVREF = (par(quad,par_count))	
			commands += comm
			if CVREF:		    # to perasma parametrou me "inadnout" katanalwnei 2 tetrades , 
				par_count += 2  # stin periptosi afti o metritis parametrwn par_count auksanetai kata 2 
			else:
				par_count += 1	# diaforetika kata 1 
		elif quad[1] == "jump":
			par_count = 0
			commands += (jump(quad))
		elif quad[1] == "call":
			par_count = 0
			commands += (call(quad))
			first_par_1(quad,L,commands)	# twra gnwrizoume tin synartisi pou tha klithei , synepws shmeiwnoume
											# to framelength aftis stin grammi telikou kwdika pou eixame apothikefsei nwritera
		elif quad[1] == "RETV":
			par_count = 0
			commands += (retv(quad))
		elif quad[1] == "halt":
			par_count = 0
			commands += (halt(quad))
		elif quad[1] == "in":
			par_count = 0
			commands += (input(quad))
		elif quad[1] == "out":
			par_count = 0
			commands += (output(quad))

		asm_list.append({"label": "L"+str(quad[0])+":", "commands": commands})

def begin(quad):
	commands = []
	commands.append("sw $ra,($sp)")
	return commands

def  end(quad):
	commands = []
	commands.append("lw $ra,($sp)")
	commands.append("jr $ra")
	return commands

def assignment(quad):
	commands = []
	commands += (loadvr(quad[2],1))
	commands += (storerv(1,quad[4]))
	return commands

def branch(quad):
	commands = []
	commands += (loadvr(quad[2],1))
	commands += (loadvr(quad[3],2))
	if quad[1] == "=":
		commands.append("beq $t1,$t2,L"+str(quad[4]))
	elif quad[1] == "<":
		commands.append("blt $t1,$t2,L"+str(quad[4]))
	elif quad[1] == ">":
		commands.append("bgt $t1,$t2,L"+str(quad[4]))
	elif quad[1] == "<=":
		commands.append("ble $t1,$t2,L"+str(quad[4]))
	elif quad[1] == ">=":
		commands.append("bge $t1,$t2,L"+str(quad[4]))
	elif quad[1] == "<>":
		commands.append("bne $t1,$t2,L"+str(quad[4]))
	return commands

def op(quad):
	commands = []
	commands += (loadvr(quad[2],1))
	commands += (loadvr(quad[3],2))
	if quad[1] == "+":
		commands.append("add $t1,$t1,$t2")
	elif quad[1] == "-":
		commands.append("sub $t1,$t1,$t2")
	elif quad[1] == "*":
		commands.append("mul $t1,$t1,$t2")
	elif quad[1] == "/":
		commands.append("div $t1,$t1,$t2")
	commands += (storerv(1,quad[4]))
	return commands

def first_par_0():
	return [""]

def first_par_1(quad,L,commands):
	global asm_list
	entity,nestingLevel = search_for(quad[2])
	asm_list[L]["commands"][0] = "addi $fp, $sp,"+str(entity["framelength"])

def par(quad,i):
	commands = []
	CVREF = False
	entity,nestingLevel = search_for(quad[2])
	if quad[3] == "CV":													#-> par,x,CV,_
		commands += (par_0(quad,i))
	elif quad[3] == "RET": 												#-> par,x,RET,_
		commands += (par_5(quad,entity["offset"]))                                                      
	else :																#-> par,x,REF,_  || par,x,CVREF,_
		if quad[3] == "CVREF":		
			commands += (par_0(quad,i))	# stin proti 4ada pername tin timi
			i += 1						# kai afkanoume to i gia na perasoume												
			CVREF = True				# gia na perasoume tin anafora stin defteri
		if nestingLevel == Scope_list[-1]["nestingLevel"]:				#  -> idio vathos fwliasmatos
			if entity["type"] == "Var":									#    -> an einai metavliti
				commands += (par_1(quad,i,entity["offset"]))				
			elif entity["type"] == "par":								#    -> an einai parametros
				if entity["parMode"] == "in":
					commands += (par_1(quad,i,entity["offset"]))		#      -> an einai perasmenh me "in"
				elif entity["parMode"] == "inout":
					commands += (par_2(quad,i,entity["offset"]))		#      -> an einai perasmenh me "inout"
				elif entity["parMode"] == "inandout":
					commands += (par_1(quad,i,entity["offset"]))		#      -> an einai perasmenh me "inandout"
		else:															#  -> diaforetiko vathos fwliasmatos
			if entity["type"] == "Var":									#    -> an einai metavliti
				commands += (par_3(quad,i))
			elif entity["type"] == "par":								#    -> an einai parametros
				if entity["parMode"] == "in":							#      -> an einai perasmenh me "in"  
					commands += (par_3(quad,i))
				elif entity["parMode"] == "inout":						#      -> an einai perasmenh me "inout"
					commands += (par_4(quad,i))
				elif entity["parMode"] == "inandout":					#      -> an einai perasmenh me "inandout"
					commands += (par_3(quad,i))
	
	return commands,CVREF

def par_0(quad,i):
	commands = []
	commands += (loadvr(quad[2],0))
	commands.append("sw $t0,-"+str(12+4*(i-1))+"($fp)")
	return commands

def par_1(quad,i,offset):
	commands = []
	commands.append("addi $t0,$sp,-"+str(offset))
	commands.append("sw $t0,-"+str(12+4*(i-1))+"($fp)")
	return commands

def par_2(quad,i,offset):
	commands = []
	commands.append("lw $t0,-"+str(offset)+"($sp)")
	commands.append("sw $t0,-"+str(12+4*(i-1))+"($fp)")
	return commands

def par_3(quad,i):
	commands = []
	commands += (gnlvcode(quad[2]))
	commands.append("sw $t0,-"+str(12+4*(i-1))+"($fp)")
	return commands

def par_4(quad,i):
	commands = []
	commands += (gnlvcode(quad[2]))
	commands.append("lw $t0,($t0)")
	commands.append("sw $t0,-"+str(12+4*(i-1))+"($fp)")
	return commands

def par_5(quad,offset):
	commands = []
	commands.append("add $t0,$sp,-"+str(offset))
	commands.append("sw $t0,-8($fp)")			
	return commands

def jump(quad):
	commands = []
	commands.append("j "+"L"+str(quad[4]))
	return commands

def call(quad):
	commands = []
	entity,nestingLevel = search_for(quad[2])
	nestingLevel += 1
	if nestingLevel == Scope_list[-1]["nestingLevel"] :			# h klhtheisa kai i kalousa exoun idio vathos fwliasmatos
		commands += (call_0())
	else:														# h kleithisa kai i kalousa exoun diaforetiko vathos fwliasmatos			
		commands += (call_1())
	commands.append("addi $sp,$sp,"+str(entity["framelength"]))
	commands.append("jal L"+str(entity["startQuad"]))
	commands.append("addi $sp,$sp,-"+str(entity["framelength"]))
	return commands

def call_0():
	commands = []
	commands.append("lw $t0,-4($sp)")
	commands.append("sw $t0,-4($fp)")
	return commands

def call_1():
	commands = []
	commands.append("sw $sp,-4($fp)")
	return commands

def retv(quad):
	commands = []
	commands += (loadvr(quad[4],1))
	commands.append("lw $t0,-8($sp)")
	commands.append("sw $t1,($t0)")
	for entity in Scope_list[-1]["Entity"]:		  # gia oles tis parametrous me typou perasmatos "inandout" tis synartisis
		if entity["type"] != "par":				  # pairnoume tin timh pou einai stin 1h apo tis 2 tetrades kai
			break                                 # tin apothikevoume stin anafora pou einai apothikevmeni sti 2h tetrada
		else:
			if entity["parMode"] == "inandout":
				commands.append("lw $t1,-"+str(entity["offset"])+"($sp)")		# 1h tetrada ($sp + offset)
				commands.append("lw $t0,-"+str(entity["offset"]+4)+"($sp)")		# 2h tetrada ($sp + offset + 4)
				commands.append("sw $t1,($t0)")
	return commands

def halt(quad):
	commands = []
	commands.append("li $v0,10")
	commands.append("syscall")
	return commands

def input(quad):
	commands = []
	commands.append("li $v0,5")
	commands.append("syscall")
	return commands

def output(quad):
	commands = []
	commands.append("li $v0,1")
	commands += loadvr(quad[4],0)
	commands.append("move $a0, $t0")
	# commands.append("li $a0,"+str(quad[4]))
	commands.append("syscall")
	return commands

def gnlvcode(v):
	commands = []
	entity,nestingLevel = search_for(v)
	commands.append("lw $t0,-4($sp)")									# stoiva tou gonea
	for j in range(Scope_list[-1]["nestingLevel"]-(nestingLevel+1)):    # in range(twrino vathos fwliasmatos - vathos fwliasmatos progonou pou exei ti metavliti)
		commands.append("lw $t0,-4($t0)")								# stoiva kathe progonou 
	commands.append("addi $t0,$t0,-"+str(entity["offset"]))
	return commands

def loadvr(v,r):
	commands = []
	entity,nestingLevel = search_for(v)
	if(entity == "digit"): 										#-> v einai arithmos, search_for return ["digit","100"] for example
		commands += (load_0(nestingLevel,r))
	elif entity["type"] == "Var" :								#-> v einai metavliti
		if entity["global"] == "True":							#  -> v einai katholiki metavliti
			commands += (load_1(entity["offset"],r))
		elif Scope_list[-1]["nestingLevel"] == nestingLevel : 	#  -> v einai topiki metavliti
			commands += (load_2(entity["offset"],r))
		else:													#  -> v den einai oute topiki oute katholiki metavliti
			commands += (load_4(v,r))	
	elif entity["type"] == "tempVar" :							#-> v einai prosorini metavliti
		commands += (load_2(entity["offset"],r))
	elif entity["type"] == "par":								#-> v einai parametros
		if entity["parMode"] == "in":							#  -> v einai perasmeni me "in"
			if Scope_list[-1]["nestingLevel"] == nestingLevel :	#    -> vathos fwliasmatos iso me to trexon
				commands += (load_2(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (load_4(v,r))
		elif entity["parMode"] == "inout":						#  -> v einai perasmeni me "inout"
			if Scope_list[-1]["nestingLevel"] == nestingLevel : #    -> vathos fwliasmatos iso me to trexon
				commands += (load_3(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (load_5(v,r))		
		elif entity["parMode"] == "inandout":					#  -> v einai perasmeni me "inandout"
			if Scope_list[-1]["nestingLevel"] == nestingLevel : #    -> vathos fwliasmatos iso me to trexon
				commands += (load_2(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (load_4(v,r))
	return commands

def load_0(v,r):
	commands = []
	commands.append("li $t"+str(r)+","+str(v))
	return commands

def load_1(offset,r):
	commands = []
	commands.append("lw $t"+str(r)+",-"+str(offset)+"($s0)")
	return commands

def load_2(offset,r):
	commands = []
	commands.append("lw $t"+str(r)+",-"+str(offset)+"($sp)")
	return commands

def load_3(offset,r):
	commands = []
	commands.append("lw $t0,-"+str(offset)+"($sp)")
	commands.append("lw $t"+str(r)+",($t0)")
	return commands

def load_4(v,r):
	commands = []
	commands += (gnlvcode(v))
	commands.append("lw $t"+str(r)+",($t0)")
	return commands

def load_5(v,r):
	commands = []
	commands += (gnlvcode(v))
	commands.append("lw $t0,($t0)")
	commands.append("lw $t"+str(r)+",($t0)")
	return commands

def storerv(r,v):
	commands = []
	entity,nestingLevel = search_for(v)
	if entity["type"] == "Var" :								#-> v einai metavliti
		if entity["global"] == "True":							#  -> v einai katholiki metavliti
			commands += (store_1(entity["offset"],r))
		elif Scope_list[-1]["nestingLevel"] == nestingLevel : 	#  -> v einai topiki metavliti
			commands += (store_2(entity["offset"],r))
		else:													#  -> v den einai oute topiki oute katholiki metavliti
			commands += (store_4(v,r))
	elif entity["type"] == "tempVar" :							#-> v einai prosorini metavliti
		commands += (store_2(entity["offset"],r))
	elif entity["type"] == "par":								#-> v einai parametros
		if entity["parMode"] == "in":							#  -> v einai perasmeni me "in"
			if Scope_list[-1]["nestingLevel"] == nestingLevel : #    -> vathos fwliasmatos iso me to trexon
				commands += (store_2(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (store_4(v,r))
		elif entity["parMode"] == "inout":						#  -> v einai perasmeni me "inout"
			if Scope_list[-1]["nestingLevel"] == nestingLevel : #    -> vathos fwliasmatos iso me to trexon
				commands += (store_3(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (store_5(v,r))		
		elif entity["parMode"] == "inandout":					#  -> v einai perasmeni me "inandout"
			if Scope_list[-1]["nestingLevel"] == nestingLevel : #    -> vathos fwliasmatos iso me to trexon
				commands += (store_2(entity["offset"],r))
			else:												#    -> vathos fwliasmatos mikrotero apo to trexon 
				commands += (store_4(v,r))
	return commands

def store_1(offset,r):
	commands = []
	commands.append("sw $t"+str(r)+",-"+str(offset)+"($s0)")
	return commands

def store_2(offset,r):
	commands = []
	commands.append("sw $t"+str(r)+",-"+str(offset)+"($sp)")
	return commands

def store_3(offset,r):
	commands = []
	commands.append("lw $t0,-"+str(offset)+"($sp)")
	commands.append("sw $t"+str(r)+",($t0)")
	return commands	

def store_4(v,r):
	commands = []
	commands += (gnlvcode(v))
	commands.append("sw $t"+str(r)+",($t0)")
	return commands

def store_5(v,r):
	commands = []
	commands += (gnlvcode(v))
	commands.append("lw $t0,($t0)")
	commands.append("sw $t"+str(r)+",($t0)")
	return commands	

# prosthiki neou Scope stin global Scope_List 	
def addScope():		
	global Scope_list
	level = len(Scope_list)
	Scope_list.append({"Entity": [], "nestingLevel": level, "totalOffset": 12}) 		# to totalOffset krataei to trexon offset olou tou Scope, 
																					# kai afksanetai kata 4 me kathe prosthiki neou entity

# emfanish ston termatiko tou Scope prin diagrafei
def printDelScope(Scope):
	for entity in Scope["Entity"]:
		print("= ",entity)
	print("="+"-"*79)
	print("= nesting Level :",Scope["nestingLevel"])
	print("="*80)

# diagrafi enos Scope
def delScope():
	global Scope_list
	printDelScope(Scope_list[-1])		# typwnoume ston termatiko to Scope
	if len(Scope_list)>1:		# sthn periptosi pou den vriskomaste sto Scope tis main ,
		Scope_list[-2]["Entity"][-1]["framelength"] = Scope_list[-1]["totalOffset"]    # , metaferoume to synoliko totalOffset ws framelength  
																					  # sto entity ths synartisis 
		genASM(False)		# dhmiourgia telikou kwdika , to False dhlwnei oti den eimaste stin main
	else:
		genASM(True)		# dhmiourgia telikou kwdika , to True dhlwnei oti eimaste stin main
	try:
		del Scope_list[-1]	# diagrafi tou Scope
	except IndexError:
		print("ERROR in 'delScope()'")
		sys.exit()#error

# prosthetoume sto Scope ena enity typou variable
def addEntityNewVar(name):
	global Scope_list
	entity = {"name": name, "type": "Var", "offset": Scope_list[-1]["totalOffset"]}
	if Scope_list[-1]["nestingLevel"] == 0:		# sthn periptosi afti vriskomaste sthn main
		entity.update({"global" : "True"}) 		# shmadevoume tin metavliti afti ws katholikh
	else:
		entity.update({"global" : "False"}) 	# shmadevoume tin metavliti afti ws mh katholikh
	Scope_list[-1]["totalOffset"] += 4			# afksanoume to totalOffset tou trexon Scope kata 4 gia to epomenh metavliti
	Scope_list[-1]["Entity"].append(entity)

# prosthetoume sto Scope ena enity typou temporary variable
def addEntityNewTempVar(name):
	global Scope_list
	entity = {"name": name, "type": "tempVar", "offset": Scope_list[-1]["totalOffset"]}
	Scope_list[-1]["totalOffset"] += 4		# afksanoume to totalOffset tou trexon Scope kata 4 gia to epomenh metavliti
	Scope_list[-1]["Entity"].append(entity)

# prosthetoume sto Scope ena enity typou function
def addEntityNewFunction(name):
	global Scope_list
	entity = {"name": name, "type": "function", "startQuad": None, "framelength": None, "Arguments": []}
	Scope_list[-1]["Entity"].append(entity)

# prosthetoume sto Scope ena enity typou parameter
def addEntityNewPar(name, parMode):
	global Scope_list
	entity = {"name": name, "type": "par", "offset": Scope_list[-1]["totalOffset"], "parMode": parMode}
	if parMode == "inandout":		# stin periptosi pou h paramteros einai "inandout" ,
		Scope_list[-1]["totalOffset"] += 8	# , desmevoume 2 theseis twn 4 bytes , mia gia na kratisoume tin timh kai mia gia tin anafora
	else:	
		Scope_list[-1]["totalOffset"] += 4	# alliws kratame kanonika mia thesh twn 4 bytes
	Scope_list[-1]["Entity"].append(entity)

# prosthetoume sto entity tis synartisis ena kainourio Argument 
def addArgument(parMode):
	global Scope_list
	Scope_list[-2]["Entity"][-1]["Arguments"].append(parMode)

# psaxnoume sto Scope ena entity me vash to onoma tou 
def search_for(name):
	global Scope_list
	list = []
	for scope in Scope_list[::-1]:
		for entity in scope["Entity"]:
			if entity["name"] == name:
				return [entity, scope["nestingLevel"]]		# ean vrethei, epistrefoume to entity kai to epipedo fwliasmatos sto opoio vrethike
			else:
				list.append(entity["name"])					# ean den vrethei to prosthetoume se mia prosorini lista 
	if name.isdigit() :		# sthn periptosi pou den vrethei kanena entity elegxoume ean prokeitai gia arithmo
		return ["digit", name]		# an nai epistrefoume ton kwdiko "digit" kai ton arithmo afto
	dd = devenshtein_distance(name, list)		# elegxoume ean to name pou psaxnoume moiazei leksografika me kapoio apo ta onomata pou xrhsimopoioume mesa sto programma
	if dd:print ("\nSyntax Error in line: "+str(line)+
				" \n-> item named '"+name+"' not found, did you mean : '"+dd+"'")
	else:
		print ("\nSyntax Error in line: "+str(line)+
				" \n-> item named '"+name+"' not found")	
	sys.exit()#error
	
# psaxnoume sto trexon Scope ean yparxei ena onoma 
# stin periptosi pou yparxei termatizei to programma, alliws epistrefoume True
def search_if_repeat(name):
	global Scope_list
	for entity in Scope_list[-1]["Entity"]:
			if entity["name"] == name:
				print ("\nSyntax Error in line: "+str(line)+
				" \n-> you can't use the same name twice ")
				sys.exit()
	return True

# me orismata to onoma mia synartisis kai mia lista me ton typo parametrwn me ta opoia kaloume aftin tin synartisi 
# elegxoume ean tairiazoune me ta antistoixa orismata
def CheckforPar(fname, callPar):
	entity,_ = search_for(fname)
	if entity["type"] != "function":
		return False
	Par = entity["Arguments"]
	if len(callPar) != len(Par):
		return False
	for i, cp in enumerate(callPar):
		if cp == "CV": callPar[i] = "in"
		elif cp == "REF": callPar[i] = "inout"
		elif cp == "CVREF": callPar[i] = "inandout"
	for cp, p in zip(callPar,Par):
		if cp != p:
			return False
	return True

def program():                             
	lex()
	if(tokenID == "programtk"):            
		lex()  								
		addScope()							#-> prosthiki tou prwtou Scope (main Scope)                                 
		if(tokenID == "IDtk"):                
			thisToken = token
			lex()   						                        
			block(thisToken)   				                   
			if(tokenID == "endprogramtk") :
				lex() 						
				delScope() 					#-> diagrafh kai tou teleftaiou Scope 
				if (tokenID == "EOFtk") :
					lex() ####
				else : 
					print ("\nSyntax Error in line: "+str(line)+
						" \n-> There is code after the declaration of program's end " )
			else :
				print ("\nSyntax Error in line: "+str(line)+
					" \n->  Expected 'endprogram'\n-> or Expected semicolon (';')")
				sys.exit()#error
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected the name of program ")
			sys.exit()#error
	else :
		print ("\nSyntax Error in line: "+str(line)+" \n->  Expected 'program'")
		sys.exit()#errors

def block(name):
	declarations()       											
	subprograms()													
	if Scope_list[-1]["nestingLevel"] > 0:							#-> an den vriskomaste stin main 
		Scope_list[-2]["Entity"][-1]["startQuad"] = nextquad()      #   phgainoume sto proteleftaio Scope kai prosthetoume to 
																	#   to startQuad sto entity ths synartisis   
	genquad("begin_block", name, "", "")							
	genquad_c("")
	
	statements()         											
	if(tokenID == "endprogramtk") :									#-> an meta ta statements exoume tin desmevmeni leksi 
																	#   "endprogram" shmainei lhksh tou programmatos 
		genquad("halt", "", "", "")									#-> paragwgh endiamesou kwdika("halt" mono sthn lhksh tou programmatos)
		genquad_c("")
	genquad("end_block", name, "", "")								
	genquad_c("{}")


def declarations():
	while (tokenID == "declaretk") :                		
		lex()                                        		
		varlist()                                    
		if(tokenID == "semicolontk") :              		
			lex()											
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected semicolon ")
			sys.exit()#error


def varlist():
	if(tokenID == "IDtk") :  
		search_if_repeat(token)  				# elegxos gia to an exei dilothei allh metavliti 'h synartisi
												# me to idio onoma sto idio Scope			
		addEntityNewVar(token)					# prosthiki neas metavlitis sto Scope
		update_varlist_c(token)		
		lex()  
		while(tokenID == "commatk") :                           
			lex()                                                
			if (tokenID == "IDtk") : 
				search_if_repeat(token)
				addEntityNewVar(token)
				update_varlist_c(token)
				lex()  
			else:                                                      
				print ("\nSyntax Error in line: "+str(line)+    
					" \n-> There isn't id after comma ")        
				sys.exit()#error                                 
	else:                                                        
		pass			                                         


def subprograms():                                                                  
	while(tokenID == "functiontk") :                    
		subprogram()                                    


def subprogram():				
	global returnList		# lista sthn opoia apothikevoume ola ta return tis synartisis kai sto telos tou programmatos tin kanoume backpatch
	if (tokenID == "functiontk") :                                                      
		lex()  
		returnList.append(emptylist())
		if(tokenID == "IDtk") :                    
			thisToken = token
			search_if_repeat(token)		# elegxos gia to an exei dilothei allh metavliti 'h synartisi
										# me to idio onoma sto idio Scope
			lex()  
			addEntityNewFunction(thisToken)		# prosthiki neas synartisis sto Scope
			addScope()			#prosthiki neou Scope (gia thn nea synartisi)    
			funcbody(thisToken)                     
			if(tokenID == "endfunctiontk") :       
				lex()
				if len(returnList[-1]) == 0:		# ean den exei prostethei kanena return sti sunartisi vgazoume mhnuma lathous
					print("ERROR there is not return in function'",Scope_list[-2]["Entity"][-1]["name"],"'")
					sys.exit()#error
				backpatch(returnList[-1], nextquad()-1)
				del returnList[-1]		# adeiazoume tin returnList gia na eina etoimh gia thn epomenh synartisi
				delScope()
			else :
				print ("\nSyntax Error in line: "+str(line)+
					" \n->  Expected 'endfunction' \n-> or Expected semicolon (';')")
				sys.exit()#error
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected the name of function  ")
			sys.exit()#error
	else :	
		sys.exit()#error  ######


def funcbody(name):
	formalpars()      
	block(name)           
	


def formalpars():       
	if(tokenID == "openParenthesestk") :                
		lex()                                           
		myline = line                                
		formalparlist()                                
		if(tokenID == "closeParenthesestk") :         
			lex()
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Parentheses not closing , which opened on line : "
				+str(myline))
			sys.exit()#error
	else :
		print ("\nSyntax Error in line: "+str(line)+
			" \n-> Expected open Parentheses")
		sys.exit()#error


def formalparlist():
	if(tokenID == "intk" or
	   tokenID == "inouttk" or
	   tokenID == "inandouttk") :

		formalparitem()							
		while(tokenID == "commatk") :			
			lex()								
			if(tokenID == "intk" or 			
			   tokenID == "inouttk" or 			
			   tokenID == "inandouttk") : 	
				formalparitem()					
			else :                             
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Expected one type of : 'in', 'inout', 'inandout' ")
				sys.exit()#Error               
	elif(tokenID == "IDtk"):                  
		print ("\nSyntax Error in line: "+str(line)+
			" \n-> must specify the type of variable 'in','inout','inandout'")
		sys.exit()#error
	elif(tokenID == "closeParenthesestk"):		
		pass									
	else:
		print ("\nSyntax Error in line: "+str(line)+
			" \n-> the arguments of functions are not correct for example 'in x'")	
		sys.exit()#error


def formalparitem():
	if(tokenID == "intk" or          
	   tokenID == "inouttk" or
	   tokenID == "inandouttk") :
		thisToken = token 
		lex()
		if(tokenID == "IDtk") :      
			addArgument(thisToken)		# prosthiki neou Argument sto antistoixo entity ths synartisis (h opoia vriskete sto goniko Scope)
			addEntityNewPar(token, thisToken)	# prosthiki neou entity me metavlith typoy parameter
			lex()
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected the name of variable ")
			sys.exit()#error
	else : 
		sys.exit()#error ######

def statements():
	statement()                        
	while (tokenID == "semicolontk") : 
		lex()                           
		statement()                    


def statement():
	if (tokenID == "IDtk") :
		assignment_stat()               #<statement>   ::= <assigment-stat> |
	elif (tokenID == "iftk") :          #
		if_stat()                       #                  <if-stat> |
	elif (tokenID == "whiletk") :       #
		while_stat()                    #                  <while-stat> |
	elif (tokenID == "dowhiletk") :     #
		do_while_stat()                 #                  <do-while-stat> |
	elif (tokenID == "looptk") :        #
		loop_stat()                     #                  <loop-stat> |
	elif (tokenID == "exittk") :        #
		exit_stat()                     #                  <exit-stat> |
	elif (tokenID == "forcasetk") :     #
		forcase_stat()                  #                  <forcase-stat> |
	elif (tokenID == "incasetk") :      #
		incase_stat()                   #                  <incase-stat> |
	elif (tokenID == "returntk") :      #
		return_stat()                   #                  <return-stat> |
	elif (tokenID == "printtk") :       #
		print_stat()                    #                  <print-stat> |
	elif (tokenID == "inputtk") :       #
		input_stat()                    #                  <input-stat> |
	else:                               #
		pass                        
	

def assignment_stat():
	if(tokenID == "IDtk") : ####                     
		thisLine = line                              
		thisToken = token 
		entity,_ = search_for(token)		# elegxos an to ID afto yparxei, an oxi to programma termatizei
		if entity["type"] == "function":		# elegxos an to ID einai synartisi , an nai to programma termatizei 
			print ("\nSyntax Error in line: "+str(line)+
					" \n-> this name defined as function")
			sys.exit()
		lex()                                        
		if (tokenID == "colonEqualtk") :             
			lex()                                    
			E_place = expression()                   
			genquad(":=", E_place, "", thisToken)

			genquad_c(str(thisToken)+"="+str(E_place)+";")
		else :
			trueToken = devenshtein_distance(thisToken,None)
			if(trueToken):
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> maybe in "+str(line)+" do you mean '"+trueToken+"' instead  '"+thisToken+"' ?")
			else:	
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Expected colonEqual symbol")
			sys.exit()#error
	else : 
		sys.exit()#error ####


def if_stat():
	if (tokenID == "iftk") : ####                        
		lex()                                           
		if (tokenID == "openParenthesestk") :         
			lex()                                       
			myline = line                                 
			Cond_place = condition()                     
			if (tokenID == "closeParenthesestk") :          
				lex()                                   
				if (tokenID == "thentk") :              
					lex()                                
					backpatch(Cond_place['true'], nextquad())
					statements()                         
					iflist = makelist(nextquad())
					genquad("jump","" ,"" ,"" )
					genquad_c("goto")
					backpatch(Cond_place['false'], nextquad())
					elsepart()                          
					backpatch(iflist, nextquad())
					if (tokenID == "endiftk") :          
						lex()
					else :
						print ("\nSyntax Error in line: "+str(line)+
							" \n->  Expected 'endif' \n-> or Expected semicolon (';')")
						sys.exit()#error
				else :
					print ("\nSyntax Error in line: "+str(line)+
						" \n-> Expected 'then' ")
					sys.exit()#error
			else :
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Parentheses not closing , which opened on line : "
					+str(myline))
				sys.exit()#error
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected open Parentheses")
			sys.exit()#error
	else :
		sys.exit()#error ####


def elsepart():
	if (tokenID == "elsetk") :     
		lex()                       
		statements()                
	else:                            
		pass  


def while_stat():
	if (tokenID == "whiletk") :                   
		lex()                                     
		firstquad = nextquad()
		if (tokenID == "openParenthesestk") :     
			lex()                                 
			myline = line                        
			Cond_place = condition()                          
			if (tokenID == "closeParenthesestk") :  
				lex()                             
				backpatch(Cond_place['true'], nextquad())
				statements()                      
				if (tokenID == "endwhiletk") :   
					lex()
					genquad("jump", "", "", firstquad)
					genquad_c("goto L_"+str(firstquad)+";")
					backpatch(Cond_place['false'], nextquad())
				else :
					print ("\nSyntax Error in line: "+str(line)+
						" \n-> Expected 'endwhile' \n-> or Expected semicolon (';')")
					sys.exit()#error
			else :
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Parentheses not closing , which opened on line : "+str(myline))
				sys.exit()#error
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected open Parentheses")
			sys.exit()#error 
	else :
		sys.exit()#error ####


def do_while_stat():
	if (tokenID == "dowhiletk") :                          #<do-while-stat>   ::= dowhile
		lex()                                              #
		firstquad = nextquad()
		statements()                                       #                      <satements>
		if(tokenID == "enddowhiletk") :                    #                      enddowhile
			lex()                                          #
			if (tokenID == "openParenthesestk"):           #                      (
				lex()                                      #
				myline = line                              #
				Cond_place = condition() 
				backpatch(Cond_place['true'], firstquad)
				backpatch(Cond_place['false'], nextquad())
				if(tokenID == "closeParenthesestk") :      #                      )
					lex()
				else:
					print ("\nSyntax Error in line: "+str(line)+
						" \n-> Parentheses not closing , which opened on line : "
						+str(myline))
					sys.exit()#error
			else :
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Expected open Parentheses")
				sys.exit()#error
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected 'enddowhile' \n-> or Expected semicolon (';')")
			sys.exit()#error
	else:
		sys.exit()#error ####


def loop_stat():
	global exitList
	if(tokenID == "looptk"):           
		lex()                        
		myline = line
		exitList.append(emptylist())		# prosthetoume mia kenh lista sthn opoia tha shmeiosoume oles tis tetrades me ta "jump" apo ta "exit-statements"
		statements()                  
		if(tokenID == "endlooptk"):   
			lex()
			if len(exitList[-1]) == 0:		# ean h lista pou prosthesame sthn arxh ths loop einai kenh tote den yparxei exit kai tupwnetai warning (loop-forever)
				print("Warning!  there is a loop-endloop statement without 'exit' in line: "+str(myline))
			backpatch(exitList[-1], nextquad())		#sthn teleftaia lista tis exitList exoun shmeiothei oles oi tetrades me ta "jump" twn "exit-statements"
			del exitList[-1]		#apo thn exitList afairoume tin lista pou prosthesame stin arxh tou loop 
		else :
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected 'endloop' \n-> or Expected semicolon (';')")
			sys.exit()#error
	else :
		sys.exit()#error ####


def exit_stat():
	global exitList
	if(tokenID == "exittk"):    
		lex()
		if len(exitList) == 0  :		# an h exitList einai adeia shmainei oti den vriskomaste mesa se "loop_statement" (h exitList gemizei mono stin arxh tou loop kai adeiazei sto telos tis loop)
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> there is exit out of loop")
			sys.exit()
		t = makelist(nextquad())
		genquad("jump", "", "", "")
		genquad_c("goto")
		exitList[-1] = merge(exitList[-1], t)		#shmadevoume thn "jump" gia na ginei backpatch sto telos tis loop
	else: 
		sys.exit()#error 


def forcase_stat():
	if(tokenID == "forcasetk"):          
		lex()  
		firstquad = nextquad()      # sth firstquad tha epistrefoume meta apo kathe ektelesh tou default                       
		exitlist = emptylist()		# h exitList tha ginei backpatch sto telos ths forcase 
		while(tokenID == "whentk"):                                  
			lex()                                                     
			if(tokenID == "openParenthesestk"):                     
				lex()                                               
				myline = line                                     
				Cond_place = condition()                            
				if(tokenID == "closeParenthesestk"):                 
					lex()                                           
					if(tokenID == "colontk"):                       
						lex()                                       
						backpatch(Cond_place['true'], nextquad())
						statements()                                
						t = makelist(nextquad())
						genquad("jump", "", "", "")
						genquad_c("goto")
						exitlist = merge(exitlist, t)
						backpatch(Cond_place['false'], nextquad())
					else:                                              
						print ("\nSyntax Error in line: "+str(line)+    
							" \n-> Expected colon ")                   
						sys.exit()#error                             
				else:                                                 
					print ("\nSyntax Error in line: "+str(line)+     
						" \n-> Parentheses not closing , which opened on line : "
						+str(myline))                                  
					sys.exit()#error                                   
			else:                                                      
				print ("\nSyntax Error in line: "+str(line)+           
					" \n-> Expected open Parentheses")                 
				sys.exit()#error                                       
		if(tokenID == "defaulttk"):                            
			lex()                                             
			if(tokenID == "colontk"):                               
				lex()                                           
				statements()                                       
				genquad("jump", "", "", firstquad)
				genquad_c("goto L_"+str(firstquad)+";")
				if(tokenID == "enddefaulttk"):                      
					lex() 
					backpatch(exitlist, nextquad())
				else:
					print ("\nSyntax Error in line: "+str(line)+
						" \n-> Expected 'enddefault' \n-> or Expected semicolon (';')")
					sys.exit()#error
			else:
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Expected colon ")
				sys.exit()#error
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected 'default' ")
			sys.exit()#error
		if(tokenID == "endforcasetk"):
			lex()
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n->  Expected 'endforcase' ")
			sys.exit()#error
	else:
		sys.exit()#error ####


def incase_stat():
	#p0
	t = newTemp()		# thn metavliti t tin arxikopoioume se 0 kai thn kanoume ena ena ektelestei kapoio apo ta "when"
	flagquad = nextquad()		#shmeionoume tin arxi tis incase wste na tin kanoume backpatch sto telos tis 
	genquad(":=", "0", "", t)		#arxikopoihsh t = 0
	genquad_c(str(t)+"=0;")
	if(tokenID == "incasetk"):                                      
		lex()                                                        
		while(tokenID == "whentk"):                               
			lex()                                                 
			if(tokenID == "openParenthesestk"):                   
				lex()                                               
				myline = line                                     
				Cond_place = condition()                                     
				if(tokenID == "closeParenthesestk"):              
					lex()                                         
					if(tokenID == "colontk"):                        
						lex()  
						#p1
						backpatch(Cond_place['true'], nextquad()) 
						genquad(":=", "1", "", t)     # an h condition epistrepsei True tote t = 1                           
						genquad_c(str(t)+"=1;")
						statements()  
						#p2                             
						backpatch(Cond_place['false'], nextquad())
					else:                                            
						print ("\nSyntax Error in line: "+str(line)+ 
							" \n-> Expected colon ")                 
						sys.exit()#error                             
				else:                                                
					print ("\nSyntax Error in line: "+str(line)+     
						" \n-> Parentheses not closing , which opened on line : "
						+str(myline))                                
					sys.exit()#error                                 
			else:                                                    
				print ("\nSyntax Error in line: "+str(line)+         
					" \n-> Expected open Parentheses")              
				sys.exit()#error                                     
		if(tokenID == "endincasetk"):                                           
			lex()
			genquad("=", "1", t, flagquad)		# an h t = 1 , shmainei oti estw kai mia apo tis statements eketelesthkan , ara metavainoume stin arxi tis incase 
			genquad_c("if (1=="+str(t)+") goto L_"+str(flagquad)+";")
			
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n->  Expected 'endincase' \n-> or Expected semicolon (';')")
			sys.exit()#error
	else:
		sys.exit()#error ####


def return_stat():
	if(tokenID == "returntk"): 
		lex()                   
		E_place = expression()           
		genquad("RETV", "", "", E_place)
		genquad_c("return "+str(E_place)+";")
		t = makelist(nextquad())		# meta apo kathe return vazoume kai mia jump pou tha mas steilei sto telos tis synartisis 
		genquad("jump", "", "", "")
		genquad_c("goto")
		# stin arxi kathe synartisis prosthetoume kai mia lista stin returnList stin opoia tha shmeiwsoume ola ta return
		if returnList:		# an h returnList den einai adeia shmainei oti eimaste mesa se synartisi ,
			returnList[-1] = merge(returnList[-1], t)		# , ara shmadevoume to return
		else:				# an h returnList einai adeia shmainei oti h return einai ektos synartisis kai vgazoume mhnyma lathos 
			print("ERROR in line: " +str(line)+ "\n"+"->there is return out of function")
			sys.exit() 
	else:
		sys.exit()#error  ####


def print_stat():
	if(tokenID == "printtk"):  
		lex()                
		E_place = expression()
		genquad("out", "", "", E_place)
		genquad_c("printf(\"%d\","+str(E_place)+");")
	else:
		sys.exit()#error ####


def input_stat():
	if(tokenID == "inputtk"):  
		lex()                  
		if(tokenID == "IDtk"): 
			genquad("in", "", "",token)
			genquad_c("scanf(\"%d\",&"+str(token)+");")
			lex()
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n->  Expected a name for input  variable ")
			sys.exit()#error
	else:
		sys.exit()#error ####


def actualpars():
	if(tokenID == "openParenthesestk"):           
		lex()                                  
		myline = line                             
		AL_place = actualparlist()		# h actualparlist mas epistrefei mia lista me oles tis parametrous                     
		if(tokenID == "closeParenthesestk"):     
			lex()
			w = newTemp()
			rList = [w]
			for al in AL_place:		# gia kathe mia parametro apo tin lista pou epistrefei h actualparlist 
				rList.append(al[2])		# apo kathe parametro kratame ton tropo perasmatos tis (dioti meta elegxoume an tairiazoun me ta orismata tis synartisi )
				genquad(al[0], al[1], al[2], al[3])
			genquad("par", w, "RET", "")
			return rList
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Parentheses not closing , which opened on line : "
				+str(myline))
			sys.exit()#error
	else:
		print ("\nSyntax Error in line: "+str(line)+
			" \n-> Expected open Parentheses")
		sys.exit()#error


def actualparlist():
	AL_place = []		# dhmiorgoume mia lista stin opoia tha valoume oles tis parametrous pou tha epistrepsoun apo  tin actualparitem() 
	if(tokenID == "intk" or
	  tokenID == "inouttk" or
	  tokenID == "inandouttk"):
		AL_place.append(actualparitem())              
		while(tokenID == "commatk"):  
			lex()                     
			if(tokenID == "intk" or    
			   tokenID == "inouttk" or
			   tokenID == "inandouttk"):               
				AL_place.append(actualparitem())          
			else:                          
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Expected one type of : 'in', 'inout', 'inandout'  ")
				sys.exit()#error        
		return AL_place
	else:                               
		return AL_place


def actualparitem():
	if(tokenID == "intk"):                 
		lex()                              
		E_place = expression()             
		return ["par", E_place, "CV", ""] 		# oi tetrades epistrefontai ws lista dioti ginontai genquad oles mazi parapanw 
	elif(tokenID == "inouttk" or           
	     tokenID == "inandouttk"):         
		thisTokenID = tokenID
		lex()                               
		if(tokenID == "IDtk"):             
			thisToken = token
			entity,_ = search_for(token)		# elegxoume gia to an yparxei h metavliti afti kai an oxi to programma termatizei
			if entity["type"] == "function" :		# elegxoume an h parametros einai synartisi kai an nai to programma termatizei
					print ("\nSyntax Error in line: "+str(line)+
					" \n-> this name defined as function")
					sys.exit()
			lex()
			if thisTokenID == "inouttk":
				return ["par", thisToken, "REF", ""]
			else:
				return ["par", thisToken, "CVREF", ""]
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n->  Expected the name of variable")
			sys.exit()#error
	else:
		sys.exit()#error ####


def condition():
	BT_place = boolterm()              
	#p1
	Cond_place = BT_place
	while(tokenID == "ortk"):
		lex()                
		#p2
		backpatch(Cond_place['false'], nextquad())
		BT_place = boolterm()         
		#p3
		Cond_place['false'] = BT_place['false']
		Cond_place['true'] = merge(Cond_place['true'], BT_place['true'])
	return Cond_place	

def boolterm():
	BF_place = boolfactor()
	#p1				             
	BT_place = BF_place
	while(tokenID == "andtk"):
		lex()     
		#p2  
		backpatch(BT_place['true'], nextquad())
		BF_place = boolfactor()
		#p3 
		BT_place['true'] = BF_place['true']
		BT_place['false'] = merge(BT_place['false'], BF_place['false'])
	return BT_place                


def boolfactor():
	BF_place = {'true': [], 'false': []}
	if(tokenID == "nottk"):                     
		lex()                                   
		if(tokenID == "openBracketstk"):        
			lex()                                
			myline = line                        
			Cond_place = condition()                          
			if(tokenID == "closeBracketstk"):    
				lex()    
				#p1                       
				BF_place['true'] = Cond_place['false']
				BF_place['false'] = Cond_place['true']
				return BF_place
			else:                             
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> Brackets  not closing , which opened on line : "
					+str(myline))               
				sys.exit()#error                  
		else:                                     
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected open Brackets ")  
			sys.exit()#error                      
	elif(tokenID == "openBracketstk"):            
		lex()                                     
		myline = line                             
		Cond_place = condition()                             
		if(tokenID == "closeBracketstk"):                 
			lex()
			#p1
			return Cond_place                               
		else:                                    
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Brackets  not closing , which opened on line : "
				+str(myline))                    
			sys.exit()#error                      
	else:                                         
		E1_place = expression()                            
		RO_place = relational_oper()                      
		E2_place = expression()   
		#p1                    
		BF_place['true'] = makelist(nextquad())
		genquad(RO_place, E1_place, E2_place, "")
		genquad_c("if ("+str(E1_place)+" "+str(RO_place)+" "+str(E2_place)+") goto")
		BF_place['false'] = makelist(nextquad())
		genquad("jump", "", "", "")
		genquad_c("goto")
		return BF_place


def expression():
	OS_place = optional_sign() 
	T1_place = term()#T1        
	while(tokenID == "addtk"):  
		thisToken = token      
		add_oper()             
		T2_place = term()#T2   
		#p1
		w = newTemp()
		genquad(thisToken, T1_place, T2_place, w)
		genquad_c(str(w)+"="+str(T1_place)+str(thisToken)+str(T2_place)+";")
		T1_place = w
	#p2	
	if OS_place == "-":
		genquad("*",T1_place, "-1", T1_place)
		genquad_c(str(T1_place)+"= -"+str(T2_place)+";")
	return T1_place 


def term():
	F1_place = factor()       
	while(tokenID == "multk"):    
		thisToken = token
		mul_oper()             
		F2_place = factor()      
		#p1
		w = newTemp()
		genquad(thisToken, F1_place, F2_place, w)
		genquad_c(str(w)+"="+str(F1_place)+str(thisToken)+str(F2_place)+";")
		
		F1_place = w
	#p2
	return F1_place	



def factor():
	if(tokenID == "constanttk"):                  
		thisToken = token
		lex()    
		return thisToken                          
	elif(tokenID == "openParenthesestk"):         
		lex()                                     
		myline = line                             
		E_place = expression()                    
		if(tokenID == "closeParenthesestk"):      
			lex()                                 
			return E_place
		else:                                     
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Parentheses  not closing, which opened on line : " 
				+ str(myline))                    
			sys.exit()#error                      
	elif(tokenID == "IDtk"):                      
		thisToken = token
		lex()                                     
		ID_place = idtail()		# h idtail() ektos apo tin prosorini metavliti epistrofis, epistrefei kai mia lista me tous typous twn parametrwn                     
		if ID_place == None:	#e ean h lista afth einai kenh, tote prokeitai gia metavliti kai oxi gia synartisi
			entity,_ = search_for(thisToken)		# elegxoume ean afth h metavliti yparxei kai an oxi to programma termatizei
			if entity["type"] == "function" :			# ean h metavliti afti einai orismenh san synartisi tote to programma termatizei
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> this name defined as function")
				sys.exit()
			return thisToken
		else:		# ena h lista afth den einai kenh , prokeitai gia synartisi
			entity,_ = search_for(thisToken)		# elegxoume ean to onoma tis synartisi yparxei , ean oxi to programma termatizei
			if entity["type"] != "function" :			# elegxoume ean einai orismenh san synartisi , ean oxi to programma termatizei
				print ("\nSyntax Error in line: "+str(line)+
					" \n-> this name defined as variable")
				sys.exit()
			if CheckforPar(thisToken, ID_place[1:]):		# elegxoume ean o arithmos kai o tropos peramsatos twn parametrwn tairiazei me ta orismata tis synartisis
				genquad("call", thisToken, "", "")	
			else:
				print ("\nSyntax Error in line: "+str(line)+	
				" \n-> in function '",thisToken,"' par doesent match.")
				sys.exit()#error
			return ID_place[0]
	else:
		if(tokenID == "multk" or
		   tokenID == "addtk" or
		   tokenID == "relationaltk"):
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Starlet doesn't support this combination of symbols . ")
		else:
			print ("\nSyntax Error in line: "+str(line)+
				" \n-> Expected constant or id or open Parentheses (for expression)")
		sys.exit()#error


def idtail():
	if(tokenID == "openParenthesestk"):
		return actualpars()                  
	else:                            
		return None


def relational_oper():
	if(tokenID == "relationaltk"):       #<relational-oper>   ::= = | <= | >= | < | > | <>
		thisToken = token
		lex()
		return thisToken
	else:
		print ("\nSyntax Error in line: "+str(line)+
			" \n-> Expected relational operator ")
		sys.exit()#error


def add_oper():
	if(tokenID == "addtk"):   #<add-oper>   ::= + | -
		thisToken = token
		lex()
		return thisToken
	else:
		sys.exit()#error ####


def mul_oper():
	if(tokenID == "multk"):   #<mul-oper>   ::= * | /
		thisToken = token
		lex()
		return thisToken
	else:
		sys.exit()#error ####


def optional_sign():
	if(tokenID == "addtk"):
		return add_oper()           #<optional-sign>   ::= <add-oper>
	else:                    #
		return "+"
	
def my_definitions() :

	global reserved_words 
	
	reserved_words	= ["program", "endprogram", "declare" , 
					"if" , "then" , "else" , "endif" ,"dowhile" , "enddowhile" ,"while", 
					"endwhile" , "loop", "endloop" , 
					"exit" , "forcase" , "endforcase" , "incase" , 
					"endincase" , "when" , "endwhen" , "default" , 
					"enddefault" , "function" , "endfunction" , 
					"return" , "in" , "inout" , "inandout" , "and" , 
					"or", "not" , "input" , "print"]



def main(argv):
	
	
	global input_file
	ifile = ''
	global token
	token = ''
	global tokenID
	tokenID = ''
	global line 
	line = 1
	global next_char
	next_char = ' '
	global preview_char
	preview_char = False
	global new_temp
	new_temp = 0
	global quad_list
	quad_list = []
	global exitList
	exitList = []
	global returnList
	returnList = []
	global Scope_list
	Scope_list = []
	
	global quad_list_c
	quad_list_c = []
	global varlist_c
	varlist_c = []

	global asm_list
	asm_list = [{"label": "L:", "commands" :  ["j Lmain"]}]


	try:
		opts, args = getopt.getopt(argv,"hi:")
	except getopt.GetoptError:
		print ("starletc.py -i <input_file>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print ('starlet_compiler.py -i <input_file>')
			sys.exit()
		elif opt in ("-i"):
			ifile = arg

	if ifile == '':
		print ("Option {-i} is required")
		sys.exit()
	elif ifile[-4:] != '.stl':
		print (ifile + ": invalid file typ")
		print ("INFILE should have a '.stl' extension")
		sys.exit()

	input_file = open(ifile,'r')

	my_definitions()

	program()

	with open(ifile[:-4]+'.int', 'w') as f:
		for l in quad_list:
			p = str(l[0])+": "+str(l[1])+" "+str(l[2])+" "+str(l[3])+" "+str(l[4])+"\n"
			f.write(p)	

	with open(ifile[:-4]+'.c', 'w') as f:
		f.write("#include <stdio.h> \n")
		f.write("void main() \n{\n")
		f.write("int ")
		for a in varlist_c[0:-1]:
			f.write(str(a)+",")
		f.write(str(varlist_c[-1])+"; \n")
		for qlc, ql in zip(quad_list_c, quad_list):
			p = "L_"+str(qlc[0])+": "+str(qlc[1])+" //("+str(ql[1])+", "+str(ql[2])+", "+str(ql[3])+", "+str(ql[4])+")"+"\n"
			f.write(p)
		f.write("}")	

	with open(ifile[:-4]+'.asm', 'w') as f:
		for l in asm_list:
			f.write(str(l["label"])+"\n")
			for c in l["commands"] :
				f.write("\t"+str(c)+"\n")

	input_file.close()

if __name__ == "__main__":
	main(sys.argv[1:])