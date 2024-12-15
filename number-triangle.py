#For Loop Exercises
#Print a Number Triangle:
#Use a for loop to print this pattern:
"""
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
"""

for n in range(1,6):
    for j in range(1, n+1):
        print(j, end=' ')
    print()

#Number Pyramid:
#Print a number pyramid like this:
"""
    1  
   1 2  
  1 2 3  
 1 2 3 4  
1 2 3 4 5  
"""
rows = 5  # Number of rows

for i in range(1, rows+1):  # Loop through rows 1 to 5
    # Print spaces for alignment
    print('  ' * (rows - i), end='')
    #when i=1, rows-i=4 spaces
  # Print numbers from 1 to i
    for j in range(1, i+1):
        print(j, end=' ')
    print()
