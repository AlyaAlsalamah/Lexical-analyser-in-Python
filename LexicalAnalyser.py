# Define the set of keywords  & assumption were made to add 'str' to keywords
keywords = {'start', 'finish', 'then', 'if', 'repeat', 'var', 'int', 'float', 'do', 'read', 'print', 'void', 'return' , 'str'}
# Define the set of valid operators
operators = {'!=', '+', '-', '*', '/', '%' , '<' , '>' , '==' , '=' , '>=' , '<='}
# Define the set of valid delimiters & assumption were made to add '"' to delimiters
delimiters = {'.', '(', ')', ',', '{', '}', ';'  , ':' , '"'}

"""
The is_identifier() function is used to check: 
-If a given token is a valid identifier. 
-It checks if the first character is a letter, followed by any number of alphanumeric characters, 
-The length is no more than 8 characters.
""" 
def is_identifier(token,current_line,type):
    if token[0].isalpha() and all(c.isalnum() for c in token[1:]) and len(token) <= 8 :
            return True
    elif len(token) > 8:
                errors.append(f"Error: Identifier '{token}' on line {current_line} is longer than 8 characters.")
                return False 
    return False


def is_string(token):
    try:
        str(token)
        return True
    except ValueError:
        return False
    
def check_preceding_print(tokens, current_index):
    # Loop backwards from the current token to the beginning of the list
    for i in range(current_index - 1, -1, -1):
        # If the previous token is a ")" and a "(" is found before a "print",
        # return False because we are not inside a "print" statement
        if tokens[i][0] == ")" and  tokens[i-1][0] == "\"":
            return False
        elif tokens[i][0] == "(" and i > 0 and tokens[i+1][0] == "\"" and tokens[i-1][0] == "print":
            return True
    return False

def Quotation_or_brackets(tokens, current_index):
    for i in range(current_index - 1, -1, -1):
        # If the previous token is a ")" and a "(" is found before a "print",
        # return False because we are not inside a "print" statement
        if (current_index=="\"" and current_index[i-1][0] == "(") or (current_index=="\"" and current_index[i+1][0] == ")")  :
            return True
    return False
     
"""
The is_number() function is used to check:
-If a given token is a valid number. It first tries to convert the token to an integer using int(), 
-If that fails, it tries to convert it to a float using float(). 
-If both conversions fail, the token is not a valid number.
"""
def is_number(token):
    try:
        int(token)
        return True
    except ValueError:
        try:
            float(token)
            return True
        except ValueError:
            return False
    
"""
tokenizer() function is used to split the code into individual tokens.
It first splits the code into lines and strips out any comments (denoted by //). 
It then iterates over each character in each line, checking if the character is an operator or delimiter, a space, or a part of a number or identifier.
"""
def tokenizer(code):
    """Tokenizes the given code and returns a list of tokens"""  
    tokens = [] # Array of Tuples, to store the input with its type 
    lines = code.split('\n') # Cut the line, when reaching a '\n' which indicates a new line   
    for i, line in enumerate(lines):
        # Strip comment 
        if '//' in line:
            line = line.split('//')[0] # Checking first line, if their is a 'Comment'    
        # Split into tokens
        current_token = ''  
        for char in line: # Moving on the line by moving on each character 
            if char in operators or char in delimiters:
               # Negative conditions
               if char == '-' or '!' or '>' or '<' or '=': 
                     current_token+=char 
               # Float conditions
               elif char == '.':
                    current_token+=char 
               elif current_token:
                   tokens.append([current_token,i]) # Stored the token with its line
                   current_token = ''
               elif current_token == '':
                   tokens.append([char,i]) 
            # Spaces conditions
            elif char.isspace():  
                if current_token: #
                    tokens.append([current_token,i])  
                    current_token = ''
                continue # For the condtion of spaces that aren't needed and doesn't satisfy an if condition
            else:
                 current_token += char 
        if current_token:
            tokens.append([current_token,i]) 

        # Handle print statement as a single token
        j = 0
        while j < len(tokens):
            if tokens[j][0] == "\"" and j + 1 < len(tokens) and tokens[j - 1][0] == "(" and  tokens[j - 2][0] == "print" :
                k = j + 1
                while k < len(tokens) and tokens[k][0] != ")":
                    k +=  1
                if k < len(tokens):
                    start = j + 1
                    end = k - 2
                    if start <= end:
                        string_token = " ".join([tokens[i][0] for i in range(start, end+1)])
                        tokens[j+1:end+1] = [[string_token, tokens[j][1]]]
                    else:
                        tokens[j:k+1] = [["print", tokens[j][1]]]
            j += 1
    return tokens   

"""
The decider() function is the main function
that takes the input code, tokenizes it, and generates the lexeme count, tokens, and symbol table.
It also checks for errors by validating the symbols in the code.
"""
errors = []            
def decider(code):
    """Scans the given code and returns the total number of lexemes,
    a list of tokens, and a symbol table
    """
    tokens = tokenizer(code)  
    lexemes_count = len(tokens)  
    symbol_table = {}
    cc=''
    for i, token in enumerate(tokens): 
        current_type = ''
        tokenish,line = (token[0],token[1]) # --> token is composed of value and line so, tokenish --> stores individual tokens // token --> stores each token with its line

        if tokenish in operators:
            if check_preceding_print(tokens, i):
                current_type='string'   
                token.append(current_type) 
            else :
                current_type = 'operator'
                token.append(current_type) # Here we will add the "type" to each token besides the "vlaue", and "line"

        elif tokenish in delimiters:  
            if check_preceding_print(tokens, i) and  Quotation_or_brackets(tokens, i):
                current_type='string'   
                token.append(current_type) 
            else :
                current_type = 'delimeter' 
                token.append(current_type) # Here we will add the "type" to each token besides the "vlaue", and "line"

        elif tokenish.lower() in keywords : 
            if check_preceding_print(tokens, i):
                current_type='string'   
                token.append(current_type) 
            else : 
                  current_type='keyword'   
                  token.append(current_type)

        elif is_number(tokenish):
            if check_preceding_print(tokens, i):
                current_type='string'   
                token.append(current_type) 
            else :     
                  current_type='number'   
                  token.append(current_type)

        elif tokens[i-1][0] == "\"" and  tokens[i-2][0] == "(" and  tokens[i-3][0] == "print" :
                 current_type='string' 
                 token.append(current_type)
        elif tokens[i-1][0] == "\"" and  tokens[i+1][0] == "\"" :
                 current_type='string' 
                 token.append(current_type)

        
        elif is_identifier(tokenish,line,type):
                current_type='identfier'
                token.append(current_type) # Here we will add the "type" to each token besides the "vlaue", and "line"
                if i + 2 < len(tokens) and tokens[i+1][0] =='=':

                              
                  # checking only digits no minus
                        if tokens[i+2][0].isdigit() : 
                              current_type='integer'
                              if len(str(tokens[i+2][0])) <= 8: 
                                    if tokens[i-1][0] == ';' or tokens[i-1][0] =='then':
                                        cc= "none"
                                        symbol_table[tokenish] = {'type': cc , 'value': (tokens[i+2][0])} 
                                    elif tokens[i-1][0] == ",":
                                        symbol_table[tokenish] = {'type': cc , 'value': int(tokens[i+2][0])} 
                                    else :
                                         symbol_table[tokenish] = {'type': tokens[i-1][0], 'value': int(tokens[i+2][0])}
                                         cc = tokens[i-1][0]        
                              else: 
                                 errors.append(f"Invalid Value: Number '{token}' on line {line} its value is longer than 8 digits.") 
                
                    # checking minus and floats together  with paying attention to the order
                        elif '-'in tokens[i+2][0] and '.'in tokens[i+2][0]: 
                            current_type='float'
                            if (len(str(tokens[i+2][0]).replace(".", "")) <= 9):
                                    if tokens[i-1][0] == ';' or tokens[i-1][0] == 'then':
                                        cc= "none"
                                        symbol_table[tokenish] = {'type': cc , 'value': (tokens[i+2][0])} 
                                    elif tokens[i-1][0] == ",":
                                        symbol_table[tokenish] = {'type': cc , 'value': float(tokens[i+2][0])} 
                                    else :
                                         symbol_table[tokenish] = {'type': tokens[i-1][0], 'value': float(tokens[i+2][0])}
                                         cc = tokens[i-1][0]
                            else:
                                errors.append(f"Invalid Value: Number '{token}' on line {line} its value is longer than 8 digits.")
                    # checking only floats with  no minus       
                        elif '.' in tokens[i+2][0]  :  
                             current_type='float'
                             if (tokens[i+2][0] != '-') and (len(str(tokens[i+2][0]).replace(".", "")) > 8):
                                errors.append(f"Invalid Value: Number '{token}' on line {line} its value is longer than 8 digits.") 
                             else: 
                                    if tokens[i-1][0] == ';' or tokens[i-1][0] == 'then':
                                        cc= "none"
                                        symbol_table[tokenish] = {'type': cc , 'value': (tokens[i+2][0])} 
                                    elif tokens[i-1][0] == ",":
                                        symbol_table[tokenish] = {'type': cc , 'value': float(tokens[i+2][0])} 
                                    else :
                                         symbol_table[tokenish] = {'type': tokens[i-1][0], 'value': float(tokens[i+2][0])}
                                         cc = tokens[i-1][0]
                    # checking minus in integers  
                        elif '-' in tokens[i+2][0]: 
                           current_type='integer'
                           if len(str(tokens[i+2][0].replace("-", ""))) <= 8: 
                                    if tokens[i-1][0] == ';' or tokens[i-1][0] =='then':
                                            cc= "none"
                                            symbol_table[tokenish] = {'type': cc , 'value': (tokens[i+2][0])} 
                                    elif tokens[i-1][0] == "," :
                                        symbol_table[tokenish] = {'type':cc , 'value': int(tokens[i+2][0])} 
                                    else :
                                         symbol_table[tokenish] = {'type': tokens[i-1][0], 'value': int(tokens[i+2][0])}
                                         cc = tokens[i-1][0]
                           else: 
                                 errors.append(f"Invalid Value: Number '{token}' on line {line} its value is longer than 8 digits.")         
                    # cheking strings 
                        elif is_string(tokens[i+2][0]):
                                current_type='string' 
                                if tokens[i-1][0] == ';' or tokens[i-1][0] =='then':
                                    cc= "none"
                                    symbol_table[tokenish] = {'type': cc , 'value': (tokens[i+3][0])} 
                                elif tokens[i-1][0] == ",":
                                        symbol_table[tokenish] = {'type': cc , 'value': str(tokens[i+3][0])} 
                                else :
                                         symbol_table[tokenish] = {'type': tokens[i-1][0], 'value': str(tokens[i+3][0])}
                                         cc = tokens[i-1][0]
           # checking ERROR  
        elif tokenish not in delimiters and tokenish not in operators :
            errors.append(f"Invalid symbol '{token}' on line {line}") 

    return lexemes_count, tokens, symbol_table, errors
 
#--------------------------Valid test cases-----------------------------------

# Test case1: The simple case of having an integer negative number and a string.
code = """
int x = 6 ;
int y = -5 ;
str z = " scanner " ;
"""

# Test case2: having two integer numbers, one is negative and the other one is positive next to each other.
"""code =
int x = 6 , y = -5 ;
str z = " scanner " ;
"""

# Test case3: having a comment the code.
"""code =
// skip the comment
int x = 6 , y = -7 ;
str z = " scanner " ; 
"""

# Test case4: having a float number.
"""code = 
// skip the comment
float x1 = -5.5 ;
float y1 = 7.56 ;
str y2 = " scanner " ;
print ( " x1 and y1 and y2 and y3 all start with a letter followed by a digit " ) ;
"""

# Test case5: The scanner handles if the keyword is written in uppercase or lowercase by always converting it to lowercase “FLOAT” .
"""code =
// skip the comment 
str name = " scanner " ;
FLOAT x = 2.2 ;
float y = 2.2 ;
"""

# Test case6: having an if statement.
"""code =
// skip the comment
float x = 2.2 ;
if x < 5 then 
print ( " x is less than 5 " ) ; 
finish
"""

# Test case7: A value is saved based on the data type the user selects when a value is kept in a simple table.
"""code = 
int x = " Compilers " , y = 3 ; 
"""

# Test case8: when the user forgets to specify the data type, the word "none" is stored in the basic table.
"""code = 
x = " word " , y = 4 , t = 7.0 ;
"""

# Test case9: Handling data types within the print statement.
"""code =
// skip the comment
if 7 == 6
then 
int x1 = 76 , c = " seventy-six " ;
print ( " number correct if x1 == 10 ; " ) ;
"""

# Test case10: Ruturn value  
"""code =
// skip the comment
int m = 7 ;
if m < 10
return m 
"""
#------------------------- Invalid test cases-----------------------------------

# Test case1: Invalid symbol
"""code = 
int 5e = 80 ;
float 2c = 5.2 ;
str 33q = " incorrect " ;
"""

# Test case2: Error Identifier is longer than 8 characters.
"""code =
int qwertyuiop = 5 ;
float ew428two78d = 2.4 ;
"""

# Test case3: In this test case (Invalid symbol) if the user enters the operator or symbol before the Identifier.
"""code =
int -x = 4 ;
float #r = 4.5 ;
str ?w = " incorrect " ;
if x < 5 then 
print ( " x is less than 5 " ) ; 
finish
"""

# Test case4: Invalid Value Number,value is longer than 8 digits
"""code =
str t = " Test_Numbers " ;
int n = 64328091378 ;
float x = 56880263333.2 ;
float y = 26.256823401679 ;
float z = 122096.2447 ; 
"""

lexemes_count, tokens, symbol_table, errors = decider(code)
print(f"Total number of lexemes available in the program: {lexemes_count}\n")
print(f"Tokens: {tokens}\n")
b ='\n'
print(f"Symbol table: {symbol_table}")
if errors:
    for error in errors:
        print(error)
else:
    print("No errors were found.")
