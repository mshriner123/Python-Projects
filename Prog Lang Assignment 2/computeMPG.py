
#Programming Languages Assignment 2, Skidmore College
#Professor Michael Eckmann

#computeMPG.py asks the user to enter a number of miles driven and a number of
#gallons used until the user enters -1. Once the user enters -1, the miles per gallon is printed
#to the console such that mpg = total number of miles driven / total number of gallons used.

#Author: Michael Shriner
#Date: October 19, 2020

#mpg() calculates the miles per gallon if the number of gallons used is greater than 0. Then, it prints
#the miles per gallon to the console with 4 decimal places.
def mpg():

    if num_gallons <= 0: #the number of gallons cannot be 0 because the denominator cannot be 0 when doing division
        print("You need to enter a value greater than 0 for the number of gallons to calculate miles per gallon.")
    else:
        miles_per_gallon = num_miles / num_gallons #calculates the miles per gallon

        print("Your vehicle gets", "{:.4f}".format(miles_per_gallon), "miles per gallon") #prints mpg to console


#get_num_gallons() asks the user to enter the number of gallons that the user used. If the user did not enter -1, then
#the number of gallons entered is added to the total number of gallons, and true is returned. Otherwise,false is returned.
def get_num_gallons():

    temp_num_gallons = 0 #temp_num_gallons will be assigned the user input
    global num_gallons #specifies to the method that num_gallons is global

    print("Enter the number of gallons that you used:")
    temp_num_gallons = float(input(">"))

    if temp_num_gallons == -1:
        return False #indicates to main() that it should call mpg() and break the while loop
    else:
        num_gallons += temp_num_gallons
        return True #indicates to main() that it should not call mpg() nor break the while loop


#get_num_miles() asks the user to enter the number of miles that the user drove. If the user did not enter -1, then
#the number of miles entered is added to the total number of miles, and true is returned. Otherwise,false is returned.
def get_num_miles():

    temp_num_miles = 0 #temp_num_miles will be assigned the user input
    global num_miles #specifies to the method that num_miles is global

    print("Enter the number of miles that you drove:")
    temp_num_miles = float(input(">"))

    if temp_num_miles == -1:
        return False #indicates to main() that it should call mpg() and break the while loop
    else:
        num_miles += temp_num_miles #adds user input to the total number of miles
        return True #indicates to main() that it should not call mpg() nor break the while loop


# main() iterates until the user enters -1, and the miles per gallon are printed to the console.
# It also prints the following statement prior to entering the loop:
#"Enter -1 to quit, and your miles per gallon will be printed to the console."
def main():
    
    print("Enter -1 to quit, and your miles per gallon will be printed to the console.")

    while True:

        if  not get_num_gallons(): #if condition is true, then user entered -1, call mpg() and break
            mpg()
            break;
        elif not get_num_miles(): #if condition is true, then user entered -1, call mpg() and break
            mpg()
            break;



num_gallons = 0 #a global variable to calculate the total number of gallons that the user entered
num_miles = 0 #a global variable to calculate the total number of miles that the user entered

main()#calls main to start the program

    
