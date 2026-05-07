LL(1) Expression Parser
A simple and interactive LL(1) Expression Parser built using Python and Tkinter.
This project helps visualize how parsing works in compiler design by showing step-by-step parsing execution, syntax validation, and parse tree generation.

Features


LL(1) Table-Driven Parsing


Real-time syntax validation


Step-by-step parser execution trace


Parse tree visualization


Interactive GUI using Tkinter


Supports arithmetic expressions with:


Addition (+)


Multiplication (*)


Parentheses (())


Integers / identifiers





Tech Stack


Python


Tkinter (GUI)



How It Works
The parser uses an LL(1) parsing table based on the grammar rules of arithmetic expressions.
Grammar Used
E → TXX → +TX | εT → FYY → *FY | εF → i | (E)
The input expression is first preprocessed:


Spaces are removed


Numbers are converted into i


The parser then validates the expression using stack-based LL(1) parsing



Installation & Run
1. Clone the Repository
git clone <your-repo-link>cd <repo-folder>
2. Run the Program
python expression_parser.py

How to Use


Enter an arithmetic expression in the input box


Example:
(2+3)*4


Click Parse


View:


Parsing steps


Stack operations


Input processing


Final result




Click Show Tree to visualize the parse tree



Example Inputs
Valid:
2+3(1+2)*57*(3+4)
Invalid:
++3(2+35**

Learning Purpose
This project was created to better understand:


Compiler Design


LL(1) Parsing


Context-Free Grammars


Parse Trees

Stack-based Parsing Techniques



Future Improvements


Better parse tree visualization


More grammar support


Error recovery handling


Tokenizer/Lexer integration


Dark/light theme support



Author
Made with Python for learning and experimenting with parsing concepts.
