from PppListener import PppListener

test = True;
# test = False;

tree = open("tree.txt", "w")

def EnterPrint(name, ctx):
	if test:
		tree.write("\n\t:> {:<20}BEGAN => ".format(name)
			+ctx.getText()[0:50] + (" {...}"if len(ctx.getText())>50 else ""))

def ExitPrint(name, ctx):
	if test:
		tree.write("\n  <: {:<20}EXIT".format(name))

# This class defines a complete listener for a parse tree produced by PppParser.
class MyListener(PppListener):

	# Enter a parse tree produced by PppParser#startRule.
	def enterStartRule(self, ctx):
		EnterPrint("startRule", ctx)

	# Exit a parse tree produced by PppParser#startRule.
	def exitStartRule(self, ctx):
		ExitPrint("startRule", ctx)


	# Enter a parse tree produced by PppParser#fixedVar.
	def enterFixedVar(self, ctx):
		EnterPrint("fixedVar", ctx)

	# Exit a parse tree produced by PppParser#fixedVar.
	def exitFixedVar(self, ctx):
		ExitPrint("fixedVar", ctx)


	# Enter a parse tree produced by PppParser#mainClassBegan.
	def enterMainClassBegan(self, ctx):
		EnterPrint("mainClassBegan", ctx)

	# Exit a parse tree produced by PppParser#mainClassBegan.
	def exitMainClassBegan(self, ctx):
		ExitPrint("mainClassBegan", ctx)


	# Enter a parse tree produced by PppParser#classBegan.
	def enterClassBegan(self, ctx):
		EnterPrint("classBegan", ctx)

	# Exit a parse tree produced by PppParser#classBegan.
	def exitClassBegan(self, ctx):
		ExitPrint("classBegan", ctx)


	# Enter a parse tree produced by PppParser#inherits.
	def enterInherits(self, ctx):
		EnterPrint("inherits", ctx)

	# Exit a parse tree produced by PppParser#inherits.
	def exitInherits(self, ctx):
		ExitPrint("inherits", ctx)


	# Enter a parse tree produced by PppParser#mainClassBody.
	def enterMainClassBody(self, ctx):
		EnterPrint("mainClassBody", ctx)

	# Exit a parse tree produced by PppParser#mainClassBody.
	def exitMainClassBody(self, ctx):
		ExitPrint("mainClassBody", ctx)


	# Enter a parse tree produced by PppParser#classBody.
	def enterClassBody(self, ctx):
		EnterPrint("classBody", ctx)

	# Exit a parse tree produced by PppParser#classBody.
	def exitClassBody(self, ctx):
		ExitPrint("classBody", ctx)


	# Enter a parse tree produced by PppParser#classDeclarations.
	def enterClassDeclarations(self, ctx):
		EnterPrint("classDeclarations", ctx)

	# Exit a parse tree produced by PppParser#classDeclarations.
	def exitClassDeclarations(self, ctx):
		ExitPrint("classDeclarations", ctx)


	# Enter a parse tree produced by PppParser#classDeclaration.
	def enterClassDeclaration(self, ctx):
		EnterPrint("classDeclaration", ctx)

	# Exit a parse tree produced by PppParser#classDeclaration.
	def exitClassDeclaration(self, ctx):
		ExitPrint("classDeclaration", ctx)


	# Enter a parse tree produced by PppParser#mainClassBlock.
	def enterMainClassBlock(self, ctx):
		EnterPrint("mainClassBlock", ctx)

	# Exit a parse tree produced by PppParser#mainClassBlock.
	def exitMainClassBlock(self, ctx):
		ExitPrint("mainClassBlock", ctx)


	# Enter a parse tree produced by PppParser#classBlock.
	def enterClassBlock(self, ctx):
		EnterPrint("classBlock", ctx)

	# Exit a parse tree produced by PppParser#classBlock.
	def exitClassBlock(self, ctx):
		ExitPrint("classBlock", ctx)


	# Enter a parse tree produced by PppParser#mainMethod.
	def enterMainMethod(self, ctx):
		EnterPrint("mainMethod", ctx)

	# Exit a parse tree produced by PppParser#mainMethod.
	def exitMainMethod(self, ctx):
		ExitPrint("mainMethod", ctx)


	# Enter a parse tree produced by PppParser#initMethod.
	def enterInitMethod(self, ctx):
		EnterPrint("initMethod", ctx)

	# Exit a parse tree produced by PppParser#initMethod.
	def exitInitMethod(self, ctx):
		ExitPrint("initMethod", ctx)


	# Enter a parse tree produced by PppParser#method.
	def enterMethod(self, ctx):
		EnterPrint("method", ctx)

	# Exit a parse tree produced by PppParser#method.
	def exitMethod(self, ctx):
		ExitPrint("method", ctx)


	# Enter a parse tree produced by PppParser#formalParameters.
	def enterFormalParameters(self, ctx):
		EnterPrint("formalParameters", ctx)

	# Exit a parse tree produced by PppParser#formalParameters.
	def exitFormalParameters(self, ctx):
		ExitPrint("formalParameters", ctx)


	# Enter a parse tree produced by PppParser#body.
	def enterBody(self, ctx):
		EnterPrint("body", ctx)

	# Exit a parse tree produced by PppParser#body.
	def exitBody(self, ctx):
		ExitPrint("body", ctx)


	# Enter a parse tree produced by PppParser#block.
	def enterBlock(self, ctx):
		EnterPrint("block", ctx)

	# Exit a parse tree produced by PppParser#block.
	def exitBlock(self, ctx):
		ExitPrint("block", ctx)


	# Enter a parse tree produced by PppParser#statement.
	def enterStatement(self, ctx):
		EnterPrint("statement", ctx)

	# Exit a parse tree produced by PppParser#statement.
	def exitStatement(self, ctx):
		ExitPrint("statement", ctx)


	# Enter a parse tree produced by PppParser#localDeclaration.
	def enterLocalDeclaration(self, ctx):
		EnterPrint("localDeclaration", ctx)

	# Exit a parse tree produced by PppParser#localDeclaration.
	def exitLocalDeclaration(self, ctx):
		ExitPrint("localDeclaration", ctx)

	# Enter a parse tree produced by PppParser#callConstructor.
	def enterCallConstructor(self, ctx):
		EnterPrint("CallConstructor", ctx)

	# Exit a parse tree produced by PppParser#callConstructor.
	def exitCallConstructor(self, ctx):
		ExitPrint("CallConstructor", ctx)


	# Enter a parse tree produced by PppParser#assignmentState.
	def enterAssignmentState(self, ctx):
		EnterPrint("assignmentState", ctx)

	# Exit a parse tree produced by PppParser#assignmentState.
	def exitAssignmentState(self, ctx):
		ExitPrint("assignmentState", ctx)


	# Enter a parse tree produced by PppParser#ifState.
	def enterIfState(self, ctx):
		EnterPrint("ifState", ctx)

	# Exit a parse tree produced by PppParser#ifState.
	def exitIfState(self, ctx):
		ExitPrint("ifState", ctx)


	# Enter a parse tree produced by PppParser#whileState.
	def enterWhileState(self, ctx):
		EnterPrint("whileState", ctx)

	# Exit a parse tree produced by PppParser#whileState.
	def exitWhileState(self, ctx):
		ExitPrint("whileState", ctx)


	# Enter a parse tree produced by PppParser#returnState.
	def enterReturnState(self, ctx):
		EnterPrint("returnState", ctx)

	# Exit a parse tree produced by PppParser#returnState.
	def exitReturnState(self, ctx):
		ExitPrint("returnState", ctx)


	# Enter a parse tree produced by PppParser#printState.
	def enterPrintState(self, ctx):
		EnterPrint("printState", ctx)

	# Exit a parse tree produced by PppParser#printState.
	def exitPrintState(self, ctx):
		ExitPrint("printState", ctx)


	# Enter a parse tree produced by PppParser#scanState.
	def enterScanState(self, ctx):
		EnterPrint("scanState", ctx)

	# Exit a parse tree produced by PppParser#scanState.
	def exitScanState(self, ctx):
		ExitPrint("scanState", ctx)

	# Enter a parse tree produced by PppParser#conditions.
	def enterConditions(self, ctx):
		EnterPrint("conditions", ctx)

	# Exit a parse tree produced by PppParser#conditions.
	def exitConditions(self, ctx):
		ExitPrint("conditions", ctx)


	# Enter a parse tree produced by PppParser#expressions.
	def enterExpressions(self, ctx):
		EnterPrint("expressions", ctx)

	# Exit a parse tree produced by PppParser#expressions.
	def exitExpressions(self, ctx):
		ExitPrint("expressions", ctx)

	# Enter a parse tree produced by PppParser#operetor.
	def enterOperetor(self, ctx):
		EnterPrint("Operetor", ctx)

	# Exit a parse tree produced by PppParser#operetor.
	def exitOperetor(self, ctx):
		ExitPrint("Operetor", ctx)


	# Enter a parse tree produced by PppParser#expression.
	def enterExpression(self, ctx):
		EnterPrint("expression", ctx)

	# Exit a parse tree produced by PppParser#expression.
	def exitExpression(self, ctx):
		ExitPrint("expression", ctx)


	# Enter a parse tree produced by PppParser#methodCall.
	def enterCallMethod(self, ctx):
		EnterPrint("CallMethod", ctx)

	# Exit a parse tree produced by PppParser#methodCall.
	def exitCallMethod(self, ctx):
		ExitPrint("CallMethod", ctx)


	# Enter a parse tree produced by PppParser#parameters.
	def enterParameters(self, ctx):
		EnterPrint("parameters", ctx)

	# Exit a parse tree produced by PppParser#parameters.
	def exitParameters(self, ctx):
		ExitPrint("parameters", ctx)


	# Enter a parse tree produced by PppParser#parameter.
	def enterParameter(self, ctx):
		EnterPrint("parameter", ctx)

	# Exit a parse tree produced by PppParser#parameter.
	def exitParameter(self, ctx):
		ExitPrint("parameter", ctx)


	# Enter a parse tree produced by PppParser#identifierPRO.
	def enterIdentifier(self, ctx):
		EnterPrint("identifier", ctx)

	# Exit a parse tree produced by PppParser#identifierPRO.
	def exitIdentifier(self, ctx):
		ExitPrint("identifier", ctx)


	# Enter a parse tree produced by PppParser#math_op.
	def enterMath_op(self, ctx):
		EnterPrint("math_op", ctx)

	# Exit a parse tree produced by PppParser#math_op.
	def exitMath_op(self, ctx):
		ExitPrint("math_op", ctx)


	# Enter a parse tree produced by PppParser#relat_op.
	def enterRelat_op(self, ctx):
		EnterPrint("relat_op", ctx)

	# Exit a parse tree produced by PppParser#relat_op.
	def exitRelat_op(self, ctx):
		ExitPrint("relat_op", ctx)


	# Enter a parse tree produced by PppParser#logical_op.
	def enterLogical_op(self, ctx):
		EnterPrint("logical_op", ctx)

	# Exit a parse tree produced by PppParser#logical_op.
	def exitLogical_op(self, ctx):
		ExitPrint("logical_op", ctx)

	 # Enter a parse tree produced by PppParser#assign.
	def enterAssign(self, ctx):
		EnterPrint("assign", ctx)

	# Exit a parse tree produced by PppParser#assign.
	def exitAssign(self, ctx):
		ExitPrint("assign", ctx)
		

