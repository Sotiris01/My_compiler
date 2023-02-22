import starletc


tests = ["test0","test1","test2","test3","test4","max","test5","big_test","test6", "test7"]




print ("\n -> start testing 'starlet_compiler' whith :")
for i in range(len(tests)): 
	print("		"+tests[i]+".stl")
print("-"*80+'\n')		

for i in range(len(tests)):
	print("|-- start testing '"+tests[i]+"'")
	print("|....."+'\n')
	starletc.main(["-i", tests[i]+".stl"]) 
	print ("\n|-- '"+tests[i]+"' is OK --\n")

print("-------------------------------------------")	

