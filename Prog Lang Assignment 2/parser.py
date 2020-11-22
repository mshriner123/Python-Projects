import re
import sys

#Programming Languages Assignment 2
#parser.py is a recursive descent parser for a given grammar. It uses one lookahead.
#The descriptions of the test files that I provided are in Test File Descriptions.txt.
#author: Michael Shriner
#date: October 25, 2020

def lex():

    global next_token #the next token in the parser
    global whole_file_str #the file as a string
    variable_token = "VARIABLE" #constant variable 
    constant_token = "CONSTANT" #constant variable
    progname_token = "PROGNAME" #constant variable
    
    terminal_regex = "^\s*(program|procedure|begin|call|;|end|:=|read|\(|,|\)|write|if|then|else|while|do|\+|\-|\*|%|/|<>|<=|>=|<|>|=|\$)(.*)"
    #terminal_regex: matches terminals after optional whitespace at the beginning of whole_file_str
    #group 1: any of the terminals listed in the first set of parenthesis
    #group 2: the remainder of whole_file_str after the matched terminal in group 1
    
    p = re.compile(terminal_regex, re.DOTALL) #re.DOTALL allows the . to match against any character INCLUDING \n
    m = p.match(whole_file_str)

    if m:
        next_token = m.group(1) #next token is the terminal that was matched in group 1
        whole_file_str = m.group(2) #changes whole_file_str to everything after the match in group 1
        
    else: #didn't match with terminal_regex
        #use regex that matches a constant
        constant_regex = "^\s*([0-9]+)(.*)"
        #constant_regex = 0 or more whitespace at the start of whole_file_str followed by one or more digits and 0 or more characters
        #group 1: one or more digits
        #group 2: the remainder of whole_file_str after the match in group 1
        
        p1 = re.compile(constant_regex, re.DOTALL)
        m1 = p1.match(whole_file_str)
        
        if m1:
            next_token = constant_token #next token is a constant
            whole_file_str = m1.group(2)#changes whole_file_str to everything after the match in group 1

        else: #didn't match with terminal_regex or constant_regex
            #use regex that matches a progname
            progname_regex = "^\s*([A-Z][0-9a-zA-Z]*)(.*)"
            #progname_regex = 0 or more whitespace at the start of whole_file_str followed by a capital letter followed by 0 or more letters or digits where letters can be
            #lowercase or uppercase followed by 0 or more characters
            #group 1: a capital letter followed by 0 or more letters or digits where letters can be lowercase or uppercase
            #group 2: the remainder of whole_file_str after the match in group 1

            p2 = re.compile(progname_regex, re.DOTALL)
            m2 = p2.match(whole_file_str)
        
            if m2:
                next_token = progname_token #next token is the progname that was matched in group 1
                whole_file_str = m2.group(2)#changes whole_file_str to everything after the match in group 1
            
            else:#didn't match with terminal_regex, constant_regex, or progname_regex
                #use regex that matches a variable
                var_regex = "^\s*([a-zA-Z][0-9a-zA-Z]*)(.*)"
                #var_regex: 0 or more whitespace at the start of whole_file_str followed by a capital or lowercase letter followed by 0 or more letters or digits where
                #letters can be upper or lowercase followed by 0 or more characters
                #group 1: a capital or lowercase letter followed by 0 or more letters or digits where letters can be upper or lowercase
                #group 2: the remainder of whole_file_str after the match in group 1

                p3 = re.compile(var_regex, re.DOTALL)
                m3 = p3.match(whole_file_str)
        
                if m3:
                    next_token = variable_token #next token is the variable that was matched in group 1
                    whole_file_str = m3.group(2)#changes whole_file_str to everything after the match in group 1

                else: #didn't match any of the regexes 
                    next_token = "Invalid token"


#<program> ::= program <progname> { <procedure_definition> } <compound stmt>                   
def program():

    if next_token == 'program':
        lex()
        
        if next_token == 'PROGNAME':
            lex()
        
            while next_token == 'procedure': #because <procedure definition> ::= procedure <procedure name> <compound stmt> and we can have 0 or more <procedure_definition> after <progname>
                procedure_definition()
              
            compound_stmt()
            
        else:
            error('PROGNAME')
    else:
        error('program')


#<procedure definition> ::= procedure <procedure name> <compound stmt>
def procedure_definition():

    if next_token == 'procedure':
        lex()
        procedure_name()
        compound_stmt()
    else:
       error('procedure')


# <stmt> ::= <simple stmt> | <structured stmt>
def stmt():

    if next_token == 'VARIABLE' or next_token == 'PROGNAME' or next_token == 'read' or next_token == 'write' or next_token == 'call':
        simple_stmt() # <simple stmt> starts with a variable, read, write, or call
        #I also checked for PROGNAME because lex() may match a progname when the token is a variable
        #note that any progname can be a variable but the reverse is not true (see grammar definitions)
        
    elif next_token == 'begin' or next_token == 'if' or next_token == 'while':
        structured_stmt() # <structured stmt> starts with begin, if, or while
            
    else:
        error('VARIABLE, read, write, begin, if, or while')
    
    
#<compound stmt> ::= begin <stmt> {; <stmt>} end
def compound_stmt():

    if next_token == 'begin':
        lex()
        stmt()

        while next_token == ';':
            lex()
            stmt()

        if next_token == 'end':
            lex()
        
        else:
            error('end')
    else:
        error('begin')


#prints the error as next_token and prints what the parser expected as the parameter expected_token
#then, it exits the program
def error(expected_token):

    print("Error:", next_token, "Expected:", expected_token)
    sys.exit()
    

#<simple stmt> ::= <assignment stmt> | <read stmt> | <write stmt> | <procedure call>
def simple_stmt():

    if next_token == 'read': #<read stmt> ::= read ( <variable> { , <variable> } )
        read_stmt()
        
    elif next_token == 'write': #<write stmt> ::= write ( <expression> { , <expression> } )
        write_stmt()

    elif next_token == 'VARIABLE' or next_token == 'PROGNAME': #<assignment stmt> ::= <variable> := <expression>
        assignment_stmt()

    elif next_token == 'call': #<procedure call> ::= call <procedure name> ( ) 
        procedure_call()
        
    else:
        error('read, write, VARIABLE, or call')


#<procedure name> ::= <variable>
def procedure_name():

    if next_token == 'VARIABLE' or next_token == 'PROGNAME':
        lex()
    else:
        error('VARIABLE')
    

#<procedure call> ::= call <procedure name> ( )
def procedure_call():

    if next_token == 'call':
        lex()
        procedure_name()

        if next_token == '(':
            lex()

            if next_token == ')':
                lex()

            else:
                error(')')
        else:
            error('(')
    else:
        error('call')


#<assignment stmt> ::= <variable> := <expression>
def assignment_stmt():

    if next_token == 'VARIABLE' or next_token == 'PROGNAME':
        lex()
        
        if next_token == ':=':
            lex()
            expression()
            
        else:
            error(':=')  
    else:
        error('VARIABLE')


# <read stmt> ::= read ( <variable> { , <variable> } )
def read_stmt():

    if next_token == 'read':
        lex()

        if next_token == '(':
            lex()

            if next_token == 'VARIABLE' or next_token == 'PROGNAME':
                lex()

                while next_token == ',':# 0 or more , <variable>
                    lex()
                    if next_token == 'VARIABLE' or next_token == 'PROGNAME':
                        lex()
                    else:
                        error('VARIABLE') #expects a variable after , 
                        
                if next_token == ')':
                    lex()
                    
                else:
                    error(')')
            else:
                error('VARIABLE')
        else:
            error('(')
    else:
        error('read')

#<write stmt> ::= write ( <expression> { , <expression> } )
def write_stmt():

    if next_token == 'write':
        lex()

        if next_token == '(':
            lex()
            expression()

            while next_token == ',': #0 or more , <expression>
                lex()
                expression()

            if next_token == ')':
                lex()
            else:
                error(')')
        else:
            error('(')
    else:
        error('write')
    

#<structured stmt> ::=	<compound stmt> | <if stmt> | <while stmt>
def structured_stmt():

    if next_token == 'begin': # <compound stmt> ::= begin <stmt> {; <stmt>} end
        compound_stmt()
        
    elif next_token == 'if': #<if stmt> ::= if <expression> then <stmt> | if <expression> then <stmt> else <stmt>
        if_stmt()

    elif next_token == 'while': #<while stmt> ::= while <expression> do <stmt>
        while_stmt()

    else:
        error('begin, if, or while')


#<sign> ::= + | -
def sign():

    if next_token == '+' or next_token == '-':
        lex()
    else:
        error('+ or -')

        
#<adding_operator> ::= + | -
def adding_operator():
    
    if next_token == '+' or next_token == '-':
        lex()
    else:
        error('+ or -')


#<simple expr> ::= [ <sign> ] <term> { <adding_operator> <term> }
def simple_expr():

    if next_token == '+' or next_token == '-': #can have 0 or 1 + or -
        sign()
    
    term()

    while next_token == '+' or next_token == '-': #can have 0 or more <adding_operator> <term>
        adding_operator()
        term()
       
# <term> ::= <factor> { <multiplying_operator> <factor> }
def term():
    
    factor()

    #can have 0 or more <multiplying_operator> <factor>
    while next_token == '*' or next_token == '%' or next_token == '/': #<multiplying_operator> ::= * | % | /
        lex()
        factor()


#<factor> ::= <variable> | <constant> | ( <expression> )
def factor():

    if next_token == 'VARIABLE' or next_token == 'PROGNAME' or next_token == 'CONSTANT':
        lex()
        
    elif next_token == '(':
        lex()
        expression()

        if next_token == ')':
            lex()

        else:
            error(')') 
    else:
        error('( or VARIABLE or CONSTANT')
   

#<expression> ::=  <simple expr> | <simple expr> <relational_operator> <simple expr>
def expression():

    simple_expr()

    #optional: <relational_operator> <simple expr>
    if next_token == '<>' or next_token == '<' or next_token == '<=' or next_token == '>' or next_token == '>=' or next_token == '=': #<relational_operator> ::= <> | < | <= | > | >= | =
        lex()
        simple_expr()
    
    
#<while stmt> ::= while <expression> do <stmt>
def while_stmt():
    
    if next_token == 'while':
        lex()
        expression()

        if next_token == 'do':
            lex()
            stmt()
            
        else:
            error('do')
    else:
        error('while')
        

#<if stmt> ::= if <expression> then <stmt> | if <expression> then <stmt> else <stmt>
def if_stmt():

    if next_token == 'if':
        lex()
        expression()

        if next_token == 'then':
            lex()
            stmt()

            if next_token == 'else': #else is optional but if next_token = else, you need <stmt> after it
                lex()
                stmt()
        else:
            error('then')
    else:
        error('if')
    

def main():
    
    global whole_file_str
    infile = open(sys.argv[1]) #takes in the file as a command line argument
    whole_file_str = infile.read() #reads the whole file as a string
    whole_file_str = whole_file_str + '$' #the $ is the termination symbol
    infile.close()

    lex() #call lex to assign the first token to next_token
    program() #call function for start symbol program

    if next_token == '$':
        print('Valid expression')
    else:
        error('end of sentence') #extra stuff after the end of the sentential sentence that makes it invalid



main() #call main() to run program
