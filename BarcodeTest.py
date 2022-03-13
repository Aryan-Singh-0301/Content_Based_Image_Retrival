import numpy as np
from PIL import Image
import statistics
from matplotlib import pyplot as plt

def CalculateProjection(img_array, angle, row_num, col_num):
    Projection_arr = []
    #Calculating Projection at 0 degrees
    if(angle == 0):
        for row in range(row_num):
            sum = 0
            for col in range(col_num):
                sum += img_array[row][col]
            Projection_arr.append(sum)
        RBC_1 = convertToBinary(Projection_arr)
        return RBC_1
    #Calculating Projection at 45 degrees
    elif(angle == 45):
        for col in range(col_num-2, -1, -1):
            sum = 0
            #sum up the diagonals
            count = 0
            row = 0
            while(row+count<row_num and col+count<col_num):
                sum+= img_array[row+count][col+count]
                count+=1
            Projection_arr.append(sum)
        for row in range(1, row_num-1):
            sum = 0
            count = 0
            col = 0
            while(row+count<row_num and col+count<col_num):
                sum+= img_array[row+count][col+count]
                count+=1
            Projection_arr.append(sum)
        RBC_2 = convertToBinary(Projection_arr)
        return RBC_2
    #Calculating Projection at 90 degrees
    elif(angle == 90):
        for col in range(col_num -1, -1, -1):
            sum = 0
            for row in range(row_num):
                sum+= img_array[row][col]
            Projection_arr.append(sum)
        RBC_3 = convertToBinary(Projection_arr)
        return RBC_3
    #Calculating Projection at 135 degrees
    else:
        for row in range(row_num-2,-1,-1):
            sum = 0
            col = col_num - 1
            count = 0
            while(row+count < row_num and col - count >= 0):
                sum+=img_array[row+count][col-count]
                count +=1
            Projection_arr.append(sum)
        for col in range(col_num-2, 0,-1):
            sum = 0
            row = 0
            count = 0
            while(row+count < row_num and col - count >= 0):
                sum+=img_array[row+count][col-count]
                count+=1
            Projection_arr.append(sum)
        RBC_4 = convertToBinary(Projection_arr)
        return RBC_4
# Using the threshold to convert each projection into binary 
def convertToBinary(projectionArr):
    thVal = int(statistics.mean(projectionArr)) # threshold Value
    for i in range(len(projectionArr)):
        if (projectionArr[i] < thVal):
            projectionArr[i] = 0
        else:
            projectionArr[i] = 1 
    stringVal = ConvertToString(projectionArr)
    return stringVal
# convert the interger projection into string
# this helps determine our hamming distance
def ConvertToString(binArr):
    code = ""
    for i in range(len(binArr)):
        code+=str(binArr[i])
    return code
# Generates the barcode
def BarCode_Generator(fileName):
    img = Image.open(fileName) # Opens the image file 
    imgArray1 = np.array(img) # Converts image to array
    imgArray = imgArray1[5:21,5:21] # Crops the image close to center giving a 16x16 matrix

    rowNum = np.shape(imgArray)[0] # Returns row number of matrix
    colNum = np.shape(imgArray)[1] # Returns columns number of matrix

    # concate all projections to create one barcode with respect to the given image
    RBC = CalculateProjection(imgArray, 0, rowNum, colNum) + CalculateProjection(imgArray, 45, rowNum, colNum) + CalculateProjection(imgArray, 90, rowNum, colNum) + CalculateProjection(imgArray, 135, rowNum, colNum)

    return RBC

# Finding the hamming distance between 2 barcodes
def hammingDistance(barcode1, barcode2):
    hammDist = 0
    for i in range((len(barcode1))):
        if(barcode1[i] != barcode2[i]):
            hammDist +=1
    return hammDist

# using the barcode generated to find the most similar image
def searchBarcode(barcodeArr): 
    imgClass = None # Class name of the similar image found 
    imgName = None  # Image name of the similar image found 
    successRate = 0 # Image retrival count 
    for row in range(10): # Image class value for image being compared and row value for barcode array
        for col in range(10): # Image name value for image being compared and col value for barcode array
            barcode1 = barcodeArr[row][col] # Barcode of the Image being compared
            shortestHamVal = len(barcodeArr[row][col]) # Shortest hamming distance value. Assuming worse case scenario
            for row2 in range(10): # row value for searching Image in same barcode array 
                for col2 in range(10): # col value for searching Image in in same barcode array
                    barcode2 = barcodeArr[row2][col2] # barcode value to compare the 
                    hdVal = hammingDistance(barcode1,barcode2) # returns hamming distance between the two barcodes
                     # compares the hamming distance found to shortest hamming distance 
                     # and make sure hamming distance is not zero, if hamming distance is zero, it would mean that two barcodes are indentical
                    if (hdVal < shortestHamVal and hdVal !=0):
                        shortestHamVal = hdVal # new shortest hamming distance value
                        imgClass = row2 # sets image class with respect of the shortest hamming distance value 
                        imgName = col2 # sets the image name with respect of the shortest hamming distance value
            
            # Output the images to show the comparsion
            plt.subplots(figsize=(10,5))
            imgOne = plt.imread('img/' + str(row) + '/' + 'img_' + str(col) + '.jpg')
            imgTwo = plt.imread('img/' + str(imgClass) + '/' + 'img_' + str(imgName) + '.jpg')
            plt.subplot(2,2,1)
            plt.title(f"Compasrion of: Image {col} Class {row}")
            plt.imshow(imgOne, cmap='gray', interpolation='nearest')
            plt.xticks([])
            plt.yticks([])
            plt.subplot(2,2,2)
            plt.title(f"Most Similar: Image {imgName} Class {imgClass}")
            plt.imshow(imgTwo, cmap='gray', interpolation='nearest')
            plt.xticks([])
            plt.yticks([])
            plt.show()
            print("For image " + str(col) + " belonging to the digit " + str(row))
            print("The most similiar image was found to be image " + str(imgName) + " in class " + str(imgClass))
            
            # If the row value of the compared image is the same to 
            # the row value of the similar searched image is a success 
            if (row == imgClass): 
                successRate += 1
    print("The success rate of the program is " + str(successRate) + "%")
    print("The failure rate of the program is " + str(100 - successRate) + "%")
    

barcodeArr = [[None for i in range(10)] for j in range(10)] # barcode array initialized to 100

file = open('barcodes.txt', 'w') # creates a text file 
for img_Row in range(10):
    for img_Name in range(10):
        fileName = "img/" + str(img_Row) + "/" + "img_" + str(img_Name) + ".jpg" # retrives are images 
        barcodeArr[img_Row][img_Name] = BarCode_Generator(fileName) # calls the barcode generator
        # writes the barcode of the image to the text
        file.write("For img " + str(img_Name) + " Belonging to " + str(img_Row) + ". The barcode of the image is " + barcodeArr[img_Row][img_Name] + "\n")

file.close() # closes the text file 

searchBarcode(barcodeArr) # calls the search barcode 