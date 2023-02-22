import sys
from antlr4 import *
from PppLexer import PppLexer
from PppParser import PppParser
from PppListener import PppListener
from PppMyListener import MyListener



def main(argv):
	input_stream = FileStream(argv[1])
	lexer = PppLexer(input_stream)
	stream = CommonTokenStream(lexer)
	parser = PppParser(stream)
	tree = parser.startRule()
	PppListeners = PppListener()
	MyListeners = MyListener()
	walker = ParseTreeWalker()
	walker.walk(PppListeners, tree)
	walker.walk(MyListeners, tree)

if __name__ == '__main__':
	main(sys.argv)
