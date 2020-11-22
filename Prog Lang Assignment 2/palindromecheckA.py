import re

#palindromecheckA.py takes input from the user and determines if it is a palindrome. It repeats that process until
#the user enters -1. This program contains two functions: is_palindrome(user_input) and get_user_input().
#Call get_user_input() to start this program.
#Author: Michael Shriner
#Date: October 21, 2020


#is_palindrome(user_input) takes the user input as a parameter and determines if it is a palindrome
#using regular expressions. It returns true if the user input is a palindrome. Otherwise, it returns false.
def is_palindrome(user_input): 

    p = re.compile('(.{0,1})(.*)(.+$)')
    #regex in English:
    #group 1: any character 0 or 1 times
    #group 2: any character 0 or more times
    #group 3: any character 1 or more times at the end of the text
    
    palindrome = True

    #loop iterates until the user input has been determined to not be a palindrome or
    #there is one or fewer characters left in the user input
    while len(user_input) > 1 and palindrome:
    
        m = p.match(user_input)#matches the regex with the user input
            
        first_char = m.group(1)#the first character in the user input
        #if user input = "racecar" then first_char = "r"
        
        middle = m.group(2)#the character(s) (if there are any) between the first character and the last in the user input
        #if user input = "racecar" then middle = "aceca"
        
        last_char = m.group(3)#the last character in the user input
        #if user input = "racecar" then last_char = "r"

        if first_char != last_char:
            palindrome = False

        user_input = middle

    return palindrome

#get_user_input() asks the user to enter a string. If the string equals "-1", then
#the program ends. Otherwise, is_palindrome(user_input) is called to determine whether
#the user input is a palindrome.
def get_user_input():
    
    #ask the user to enter a string or -1 to quit
    print("Enter a String to determine if it is a palindrome. Enter -1 to quit.")

    while True: #loops until the user enters -1
        
        print("Enter a String please:")
        user_input = input(">")

        if user_input == "-1":
            break;

        #if here, user input did not equal -1
        #call is_palindrome(user_input) to determine if the user input is a palindrome
        #if it is, print a statement to indicate that it is
        #otherwise, print a statement to indicate that the user input is not a palindrome
        
        if is_palindrome(user_input):
            print(user_input, "is a palindrome.")
        else:
            print(user_input,"is not a palindrome.")



get_user_input() #call to start program 
            
        
