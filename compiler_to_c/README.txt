author --SOTIRIS MPALATISAS--

--- p++ is an simple object oriented program language
--- and this tool generates a program written in c from
    your object oriented program written in p++

-> in file Ppp.g4 you will find the grammar of the language written in
   antlr4

-> in file "examples" you will fine same examples written in p++ with the
   ending .ppp

-> the PppMyListener.py is generates the "tree.txt" with is the syntax tree
   of your program (in p++)

-> to execute run the follow

    > antlr4 -Dlanguage=Python3 -listener Ppp.g4

    now Parser/Lexer/Listeners are created

    > python PppExecute.py example.ppp

    now ther are two files, exe.c and header.h

    > gcc exe.c

    > ./a.out
