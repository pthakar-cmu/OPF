
#Reading the file and storing
rd=open('Ymatrix_Case14.txt','r+')
contents=rd.read()

import numpy as np

# To include only the numbers and splitting them row wise by seperating (;)
contents = contents[1:-1]
contents = contents.split(';')

#Initialize null matrix
mat = []

#To convert each string inside the row as an individual string value
for line in contents:
    row = line.split(',')

#Python does not take i as imaginary value so replacing it with j; and for some reason the admittance matrix had +- sin together so i converted them all to +
    translated_row = []
    for element in row:
        ele = element.replace('i', 'j').replace(" + ","+").replace(" - ","-")
            # replace('+-', '+')

#Now to utilize the complex number we have to convert the string into complex form
        if 'j' in ele:
            translated_row.append(complex(ele))

#Since the last row is empty in the provided matrix so to utilize/see output such as second column, it would only show if it is greater than 0
    if len(translated_row) > 0:
        mat.append(translated_row)

#We have to convert it to array for getting the final Matrix
mat = np.array(mat)

#You can test the function from here!
# print(mat)
# print(mat.shape)