LL(1) Expression Parser

A simple LL(1) Expression Parser built using Python and Tkinter to understand compiler design concepts in a practical way.
The project can analyze arithmetic expressions, validate syntax, show step-by-step parsing, and generate a parse tree through an interactive GUI.

Features
LL(1) table-driven parser
Real-time syntax checking
Step-by-step parsing trace
Parse tree visualization
Interactive GUI with Tkinter
Supports +, *, parentheses, and numbers
Grammar Used
E → TX
X → +TX | ε
T → FY
Y → *FY | ε
F → i | (E)
How It Works

The parser preprocesses the input by removing spaces and converting numbers into i.
It then uses stack-based LL(1) parsingrules to validate the expression and display the parsing process.

How to Run

Clone the repository:
git clone <repo-link>
cd <folder-name>

Run the file:
python expression_parser.py
Example Inputs

Valid:
2+3
(2+3)*4
7*(1+5)

Invalid:
++3
(2+3
4**
How to Use
Enter an arithmetic expression
Click Parse
View the parsing steps and result
Click Show Tree to visualize the parse tree
Tech Used
Python
Tkinter
Purpose

This project was built for learning and experimenting with:
Compiler Design
LL(1) Parsing
Parse Trees
Stack-based parsing techniques
