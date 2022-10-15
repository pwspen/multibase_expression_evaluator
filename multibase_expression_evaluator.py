# Base Converter and Calculator
# Converts numbers from any base 2-36 to any base 2-36
# Evaluates expressions ( (), ^, *, /, +, -) natively in any base from 2-36, with output in any base from 2-36
# Theoretically supports up to base 112, but recommended to not go above 36.
# Handling for negative numbers not implemented in any way

# At the most basic level, this program works by first converting all number inputs into base10, then parses the numerical expression
# and applies arithmetic operations. The numerical expression is represented by a list where each term is either a number or an
# operation. For each operation, it applies the operation to the two numbers next to the operation, and then replaces all three
# entries with the resultant number. It continues doing this until there is only one term remaining, and then converts that term
# from base10 into the target base and displays it.

import math
import os

frombase = 0 # Source base (input)
tobase = 0 # Destination base (output)
lib1 = ["0","1","2","3","4","5","6","7","8","9"]
lib2 = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
lib3 = ["a","b","c","d","e","f","g","h","i","j","k","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
lib4 = ["α","β","γ","δ","ε","ζ","η","θ","ι","κ","λ","μ","ν","ξ","ο","π","ρ","σ","τ","υ","φ","χ","ψ","ω"]
lib5 = ["😀","😄","😁","😆","😅","🤣","😂","🙂","🙃","😉","😊","😇","🥰","😍","🤩","😘","😗","😚","😋","😛","😜","🤪","😝","🤑","🤗","🤭","🤫","🤔","🤐","🤨","😐","😶","😏","😒","🙄","😬","🤥","😌","😔","😪","🤤","😴","😷","🤒","🤕","🤢","🤮","🤧","🥵","🥶","🥴","😵","🤯"]
lib6 = ["!","@","#","$","%","^","&","*","(",")","-","_","=","+","|","{","}","[","]",":",";","<",">",",",".","?","/"]
# The above are libraries of characters that get added to the main library, digequiv, as big base mode is turned on.
# The emoji dictionary does not display properly in output terminal, but may display properly elsewhere? Not used for anything in this version, just included in case I can get the display working in the future.

digequiv36 = lib1 + lib2
digequiv = lib1 + lib2
# digequiv is the base digit library to which the other libraries (except emojis) are added and subtracted as "big base mode" is turned on or off.
# the index of a digit in digequiv is its numerical value. Thus, "A" always has the numerical value of 10, 8 is always 8, 0 is always 0, etc.
# digequiv36 is used as the "from" set of digits. If the full set was always used, math in large bases would break because the arithmetic operators get added to the set of digits.

def base1(n): # Sets source base (from / input)
    global frombase
    frombase = n

def base2(n): # Sets destination base (to / output)
    global tobase
    tobase = n

def base12(n1,n2): # Sets source and destination bases
    base1(n1)
    base2(n2)

def inttobase(n): # Converts int_10 (int) into integer_tobase (str)
    n = int(n) # Sanitizes input
    if n == 0: # Undefined error (log of zero) if not caught
        return '0' 
    num = [] # resultant int_tobase (list)
    lenout = math.floor(math.log(n,tobase) + 1.0000000000001) # digits length of resultant (output) number. The 1.00001 is because in some cases, log(n) was returning incorrect results because of limitations of float precision in computers. Specifically, log(1000) was resulting in 2.9999... which causes problems when you're taking the floor of that number.
    for exp in range(lenout-1,-1,-1): # for each order of magnitude (number of digits) in integer_10, starting at highest (furthest left)
        mag = tobase**exp # tobase raised to power of digit currently being written
        times = math.floor(n/mag) # number of times mag fits into n, rounded down 
        n -= times * mag # determines remainder to feed into next loop iteration (rounded down portion in previous line)
        num.append(digequiv[times]) # appends the digit corresponding to how many times the current order of magnitude fit into the original number
    return((''.join(num))) # returns integer_tobase (str)


decimal_digits_maximum = 20
# Determines truncation of output decimals. This is to prevent numbers with repeating decimals holding up the program forever.

def flotobase(n): # Converts float_10 (float) into float_tobase (str)
    n = float(n) # Sanitizes input
    decim_list = [] # Resultant float_tobase
    decimal_digits = 0 # Number of digits to output after the .
    integ = inttobase(math.floor(n)) # Converts integer portion of number 
    decim = n % 1 # Removes integer portion of number
    while decimal_digits < decimal_digits_maximum and decim != 0: # While the digit cap has not been reached and there is still numerical value remaining to be represented
        decim = decim * tobase # Multiplies remainder by output base 
        digit = digequiv[math.floor(decim)] # Floors value from previous line to closest integer
        decim_list.append(digit) # Adds digit to list of decimal digits
        decim %= 1 # Discards integer portion of number
        decimal_digits += 1 # Increments number of digits already represnted
    return(integ + '.' + ''.join(decim_list)) # Returns float_tobase (str)
    
p = 1
# Hidden variable that removes most prints. I used this to play a game with friends where they had to try and figure out what the hell type of math ZZ * Z = YZ1 is without giving up the schtick right away by there being a "base36" on the screen. Type "p" while programming is running to enable less-prints mode.

def intparse(n): # Converts int_frombase (str) to int_10 (float)
    n = str(n).upper() # Sanitizes input
    num = 0.0 # Resultant int_10 (actually a float, but no decimal portion)
    leng = len(n) # Digit length of input number
    for i in range(leng): # For each digit in input number
        digit = digequiv36.index(n[i]) # Looks up numerical value of digit
        num += digit * (frombase**(leng-i-1)) # Multiplies numerical value of digit by the current digit-place "multiplier" (ex, _00, multiplier is 100) and adds it to resultant float
        if digit >= frombase: # Error handling, user should not input digit higher than the current base 
            print('Error - digit higher than base present. Raise input base with /b. Result very likely incorrect.') # Informs user
            return False # Causes main function to halt
    return float(num) # Returns resulting float

def floparse(n): # Converts float_frombase (str) to float_10 (float)
    n = list(str(n).upper()) # Sanitizes input
    decim_10 = 0 # Base10 decimal result
    decim = n.index(".") # Place of the decimal mark
    integ = n[0:decim] # Integer portion of input
    decim = n[decim+1:len(n)] # Decimal portion of input
    integ = intparse(''.join(integ)) # Converts integer to int and parses it into base10 
    for i in range(len(decim)): # For each digit in the input decimal
        digit = digequiv36.index(decim[i]) # Looks up numerical value of digit
        decim_10 += digit / frombase**(i+1) # Divides numerical value of digit by current digit-place "multiplier"
        if digit >= frombase: # Error handling, user should not input digit higher than the current base
            print('Error - digit higher than base present. Raise input base with /b. Result very likely incorrect.') # Informs user
            return False # Causes main function to halt
    return float(integ + decim_10) # Returns resulting float

# The above 4 functions (int_10 to any base, float_10 to any base, any base to int_10, any base to float_10) are used extensively

def numparse(n): # Converts int_frombase or float_frombase to int_10 or float_10
    try: # Assume number is a float
        return floparse(n) # Parses as float. Fails if there is not a decimal point in input number
    except: # If number is not a float
        return intparse(n) # Parses as int

def numtobase(n): # Converts int_10 or float_10 to int_tobase or float_tobase
    if n % 1 == 0: # If number is an int
        return inttobase(n) # Converts to base as int
    else: # If number is not an int
        return flotobase(n) # Converts to base as float

# It doesn't matter if the input is an int or float to the above 2 functions, so they can be used in any situation.

operators = ["(",")","^","*","/","+","-"]
# The operator library is used to test when something is a number or an operator, and is not used the same way the digit library is where the index of a digit is important.


def EMDAS(flist): # Evaluates expression until it is of length 1, then prints it
        iters = 0 # Iteration loop counter
        for i in range(len(flist) -1): # For each element in expression list
            if type(flist[i]) == float and type(flist[i+1]) == float: # If two numbers are next to each other
                flist.insert(i+1, '*') # Insert multiplication operator between them
        while len(flist) != 1: # While expression list is larger than 1
            if "^" in flist: # If operation is exponent
                index = flist.index('^') # Gets index of operator in expression list
                flist[index-1] = flist[index-1] ** flist[index+1] # Turns first number into result of operation between both numbers
                del flist[index:index+2] # Deletes operator and second number from list
            if "*" in flist: # If operation is multiplication
                index = flist.index('*')
                flist[index-1] = flist[index-1] * flist[index+1]
                del flist[index:index+2]
            elif "/" in flist: # If operation is division
                index = flist.index('/')
                flist[index-1] = flist[index-1] / flist[index+1]
                del flist[index:index+2]
            elif "+" in flist: # If operation is addition
                index = flist.index('+')
                flist[index-1] = flist[index-1] + flist[index+1]
                del flist[index:index+2]
            elif "-" in flist: # If operation is subtraction
                index = flist.index('-')
                flist[index-1] = flist[index-1] - flist[index+1]
                del flist[index:index+2]
            elif len(flist) == 0: # If length of list is zero (never should be)
                raise
            elif iters > 500: # If iterations is above 500 (evaluating massive expressions is not the purpose of this program)
                raise

def eq(inp): # "Solver" function. Evaluates result of input expression.
    def float_to_str(n):
            return n if type(n) != float else str(int(n)) if str(int(n)) + '.0' == str(float(n)) else (str(float(n)))
    num = '' # List of digits of current number being recorded
    eq_list = [] # Expression list
    eq = list(str(inp).upper().replace(" ", "")) # Accepts and sanitizes input (changes all letters to uppercase, removes all whitespace, turns into list)
    for i in range(len(eq)): # For each digit in expression list
        if eq[i] in digequiv36 or eq[i] == '.': # If digit is a number or .
            num += eq[i] # Add digit to current number being recorded
        if eq[i] in operators: # If digit is an operator
            if num != '': # If a number was recorded before operator
                eq_list.append(numparse(num)) # Append number to expression list
                num = '' # Reset number being recorded to nothing
            eq_list.append(eq[i]) # Append operator to expression list
        elif i == len(eq) - 1: # If digit is not operator and last digit of input list
            eq_list.append(numparse(num)) # Append recorded number to expression list
    if base10disp == 'ON' and inp != '': # If print base10 calculations is on
        print('                              B10 = ',' '.join([float_to_str(x) for x in eq_list])) # Print initial expression list in base10
    iters2 = 0 # Expression list iterations
    while len(eq_list) != 1: # While expression list is longer than 1
        if ("(" in eq_list) and (")" in eq_list): # If there are both parentheses in expression list
            for i in range(len(eq_list)): # For each digit in expression list, from the left
                if eq_list[i] == "(": # If digit is left parenthetical
                    left = i # Assign index of left parenthetical
            for i in range(len(eq_list)-1,left,-1): # For each digit in expression list, from the right
                if eq_list[i] == ")": # If digit is right parenthetical
                    right = i # Assign index of right parenthetical
            sublist = eq_list[left+1:right] # Generates sub expression list of internals of parentheses
            EMDAS(sublist) # Evaluate sublist
            eq_list[left] = sublist[0] # Sets left parentheses to result of sublist
            del eq_list[left+1:right+1] # Deletes internals of parentheses and right parentheses
        elif "(" in eq_list or ")" in eq_list: # If only one parentheses is in expression list (should never happen)
            raise # Interrupt main function
        else: # If there are no parentheses in expression list
            EMDAS(eq_list) # Evaluate expression list
        if len(eq_list) == 0: # If length of expression list is zero (should never happen)
            raise # Interrupt main function
        if iters2 > 500: # If iterations is above 500 (evaluating massive expressions is not the purpose of this program)
            raise # Interrupt main function
        iters2 +=1 # Increment iterations
    print('= ',numtobase(eq_list[0]),end ='') # Prints result of expression list
    if base10disp == 'ON' and p == 1: # If base10 prints are turned on
        print('                              B10 = ',float_to_str(eq_list[0])) # Prints result in base10
    print('\n')


def basechange():
    global frombase
    global tobase
   
    try: 
        inp = input("Type input (typed) base in base10: \nInput base > ").replace(" ", "")
        base1(int(inp)) # Attempts to assign 'to' base
    except:
        if inp == '':
            print('Input base unchanged.')
        else:
            print('Invalid base entered, input base unchanged.')
    if frombase > 36: # If user tries to set from base above 36
        print('Input only supported up to base36. Input base set to 36.')
        frombase = 36

    try:
        inp = input("Type output (printed) base in base10: \nOutput base > ").replace(" ", "")
        base2(int(inp)) # Attempts to assign 'to' base
    except:
        if inp == '':
            print('Output base unchanged.')
        else:
            print('Invalid base entered, output base unchanged.')
    if tobase > 36 and bigcharlib =='B36': # If big base mode is disabled and output is set higher than 36
        print('Output only supported up to base36 with current settings. Output base set to 36. /s -> /2 to increase maximum base to 112.')
        tobase = 36 # Reset output down to 36
    if tobase > 112 and bigcharlib == 'B112': # If big base mode is enabled and output is set higher than 112
        print('Output only supported up to base112. Output base set to 112.')
        tobase = 112 # Reset output down to 112

#input('')).upper().replace(" ", ""))

base12(36,36) # Sets default bases to input 36 and output 36
base10disp = 'OFF' # Disables printing of base10 calculations by default
bigcharlib = '36' # Disables "big base mode" by default
def helpme():
    print(' ')
    print('To evaluate an expression or number, simply type it as you would naturally, using these')
    print('operators if necessary: (), ^, *, /, +, -')
    print('   If you only want to convert a number, simply type that number without any operators.')
    print('   Expressions evaluated in PEMDAS order.')
    print('   The only current limitation is lack of support for negative input or output numbers.')
    print('      Evaluates fractions, decimals, intermediate negative numbers, etc.')
    print('   For bases using alphabetical digits, a = 10, b = 11 ... z = 35.')
    print(' ')
    print('Settings available: (/s to change)')
    print('   /s then /1: Toggle display of base10 math alongside input and output base math.')
    print('      Lets you look at the input / output in base10 even if not inputting / outputting base10.')
    print('   /s then /2: Toggle large character library for outputting bases above 36, up to 112.')
    print('      Digits are, in order: numbers, uppercase letters, lowercase letters, Greek alphabet, random symbols.') 
    print('      Note that you can still only input bases up to 36. Mode intended for fun rather than usefulness.')
    print(' ')
    print('Type / to show commands:')
    print('/: command menu, /h: view help message, /b: change bases, /s: change settings.') 
    print('Current bases in base10: input base = %d, output base = %d'%(frombase,tobase))
    print(' ')
    print('Note default base settings above. /b to change.')
    print(' ')
    print('At any time, press "enter" to exit current dialogue.')
    print('Type /h to view this help message again.')
helpme()
while True: # Main loop, always running
    choice = input('> ').lower().replace(" ", "")
    #choice = input('/b: change bases, /s: settings, /p: turn on or off "printless" mode. Current bases in base10: input base = %d, output base = %d\n'%(frombase,tobase)).replace(" ", "") # Main menu
    if len(choice) == 0 or choice[0] != '/': # If setting is not selected
        try: # Assume expression is entered sensibly / can be evaluated
           eq(choice) # Evaluate expression and return result
        except Exception as e: # If there is an error with entered expression
            print('Invalid expression entered, try again. Possible causes: no input, negative numbers in input or output, overflow, invalid operator syntax.')
            print('Enter / to change bases or settings.')
    elif choice[0] == '/':
        if len(choice) == 1:
            print('/: command menu, /h: view help message, /b: change bases, /s: settings.')
            print('Current bases in base10: input base = %d, output base = %d'%(frombase,tobase))
        elif choice[1] == 'h':
            helpme()
        elif choice == '/b': # If user wants to change bases
            basechange()
            print('Current bases in base10: input base = %d, output base = %d'%(frombase,tobase))
        elif choice == '/s': # If user wants to change settings
            print('Type /n to toggle setting.')
            print('/1: Toggle simultaneous base10 display of all math and numbers.   Currently:', base10disp)
            print('/2: Toggle maximum output base between 36 and 112. Info in /h.    Currently:', bigcharlib)
            choice = str(input("/1 or /2 > ").replace(" ", "")) 
            if choice == '/1' or choice == '1': # If user wants to enable/disable base10 display of math, flip value
                if base10disp == 'OFF':
                    base10disp = 'ON'
                else:
                    base10disp = 'OFF'
                print('Base10 Display: ',base10disp)
            elif choice == '/2' or choice == '2': # If user wants to toggle size of character library, flip value and reassign size of digit library
                if bigcharlib == '36':
                    bigcharlib = '112'
                    digequiv = lib1 + lib2 + lib3 + lib4 + lib6
                    print('Max Output Base: 112')
                else:
                    bigcharlib = '36'
                    digequiv = lib1 + lib2
                    if tobase > 36: # If output base was set higher than 36, reset back down to 36
                        tobase = 36
                    print('Max Output Base: 36')
            else:
                print('Invalid choice. Need to enter /1 or /2.') # Input was not 1 or 2
                print('/h: view help message, /b: change bases, /s: settings.')
                print('Current bases in base10: input base = %d, output base = %d\n'%(frombase,tobase))
        else:
            print('Invalid choice. Need to enter a numerical expression or number (without / at start), or command. Commands:')
            print('/: command menu, /h: view help message, /b: change bases, /s: settings.') 
            print('Current bases in base10: input base = %d, output base = %d\n'%(frombase,tobase))