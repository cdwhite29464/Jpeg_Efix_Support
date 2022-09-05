# Organization : Jefferson County Open Space
# Creator : Chris White and Eric Delynko
# Date Created : 5/9/2019
# Editor :
# Script Name : Jpg_Exif_Data_Extract
# File Location : "M:\GIS_TEAM\3_Resources\3_4_Tools_and_Software\Scripts\Python\Jpg_Exif_Data_Extract\Jpg_Exif_Extract.py"
# Short Description of Script : This script goes through a folder of jpg photos and extracts the exif metadata on filename
# and timestamp from each jpg and writes this information to a .csv file. The process creates a folder (Name based on inputs),
# copies jpgs from original SD folder (input) into newly created folder, generates a standard formatted csv file based
# on the meta data/efix data from the jpgs that were copied into the file, converts .csv to an .xlsx file, deletes the .csv.

import exifread
import csv
import os
import glob
import shutil
import math
from pyexcel.cookbook import merge_all_to_a_book
from os import walk



# TODO Step 1
# Step 1 Create Folder
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' +  directory)

# Set directory to location of photo folder place on M: Drive, so that script can generate a folder in the current directory
folderFinalLocation = r"BLANK"
os.chdir(folderFinalLocation)

# Create a list of values suitable for the park3lettercode variable
testList = ["Sunshine_1", "Sunshine_2", "Cynical_1", "Cynical_2"]

# User inputs for the folder and CSV naming -3 Letter Park code
park3lettercode = input("Enter the camera location at CSD (Sunshine_1, Sunshine_2, Cynical_1, or Cynical_2): ")


# User inputs for the folder and CSV naming -3 Letter Park code and Check to see if user input is within the range of
# the list of suitable values above
if park3lettercode in testList:
    pass
else:
    variableCheck = "False"
    while variableCheck == "False":
        park3lettercode = input("Re-enter CSD camera location - Sunshine_1, Sunshine_2, Cynical_1, or Cynical_2: ")
        if park3lettercode in testList:
            variableCheck = "True"

# User inputs for the folder and CSV naming - Date formatted YYYYMMDD
dateofPhotos = input("Enter the data (YYYYMMDD) that the camera card was collected: ")

# TODO Add try and except
# Input the location of the photos
src_dir = input("Input file location of Camera photos: ")


# Generates folder name out of concatenation of User Inputs
folderName = park3lettercode+"_"+dateofPhotos

# check to see if input location of photo exist. If it does not it asks for the file path again.
while os.path.isdir(src_dir) == False:
    src_dir = input("The filepath you entered does not exist. Please check your file path and enter it again: ")

print("\nThanks for providing that information - Lets get started...")

# Generates folder with folder name from above
createFolder(folderName)

# Destination of new folder
dst_dir = os.path.join(folderFinalLocation, folderName)

print(f"\nCreating Folder to move the Photos. This folder is called... \n{dst_dir}\n")

# TODO STEP 2
# Step 2 Move Photos from Camera Card to folder location created in step 1
# Destination of new folder
dst_dir = os.path.join(folderFinalLocation, folderName)

#TODO ADD Step 3
# Create subfolders of 500 photos per folder

# Count Number of Photos in source folder location
jpgCounter = len(glob.glob1(src_dir,"*.jpg"))

# Determines how many subfolders are needed based on count of photos
numSubFolders = math.ceil(jpgCounter / 500)

for i in range(1 , (numSubFolders + 1)):
   os.mkdir(os.path.join(dst_dir, folderName +"_"+ str(i)))

# generate a list of subfolders that was created in our destination folder
listOfFolders = os.listdir(dst_dir)


#TODO ADD STEP/Adjust Step 2
# Based on the current photo count move photos into specific folder


# TODO STEP 2
# Step 2 Move Photos from Camera Card to folder location created in step 1

print("Copying photos into the newly created folder in sub folders of 500 photos in each")
print(f"You provided {jpgCounter} photos\n\tIt takes about 0.1 seconds to move 1 photo....")
timeSec = int(jpgCounter * 0.13229)
timeMinRough = int(timeSec/60)
timeSecRemainder = int(((timeSec/60)-timeMinRough)*60)
print(f"\tIt will take {timeMinRough} minutes and {timeSecRemainder} seconds to move all the photos")

# Set a counter for photos
photoCounter = 0
for root, dirs, files in os.walk(src_dir):
    files.sort()
    for jpgfile in files:
        photoCounter += 1
        subfolderListValue = (math.ceil(photoCounter/500)-1)
        subfolderFilePath = os.path.join(dst_dir,listOfFolders[subfolderListValue])
        shutil.copy(os.path.join(src_dir,jpgfile), subfolderFilePath)

# TODO Step 4
# Step 4 Create CSV out of Folder
print("\nCreating CSV file out of each folder")
print("CSV Fields: \n\tFile Name, \n\tTimestamp, \n\tML Person Detected, \n\tCamera Location, \n\tCount hiker, \n\tCount dogs on leash, \n\tCount dogs off leash, \n\tDirection of Travel, \n\tRecreation Type, \n\tEstimated Time in Park, \n\tWildlife Species")

for subfolders in listOfFolders:
    csvName = subfolders+".csv"
    print(f"\nCreting .csv named...\n{csvName}")
    print("\tAttributing information for File Name and Timestamp for each photo in the subfolder")
    # CSV Output Location
    subfolderCSVfilepath = os.path.join(dst_dir,subfolders)
    csvFile = os.path.join(subfolderCSVfilepath, csvName)

    f = []
    for path, dir, file in walk(subfolderCSVfilepath):
        with open(str(csvFile), 'w') as myfile:
             wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
             wr.writerow(["File Name", "Timestamp", "ML_PersonDetected", "Camera_Location","Count_hiker", "Count_dogs_on_leash", "Count_dogs_off_leash",
                          "Direction_of_travel", "Recreation_type", "Estimated_time_in_park", "Wildlife_species"])
             for photos in file:
                 with open(os.path.join(subfolderCSVfilepath,photos), 'rb') as fh:
                     tags = exifread.process_file(fh)
                     try:
                         dateTaken = tags["EXIF DateTimeOriginal"]
                     except:
                         pass

                 if photos[len(photos)-5] == "P":
                     personDetected = "Yes"

                 elif photos[len(photos)-5] == "N":
                     personDetected = "No"
                 else:
                     personDetected = "Unprocessed"

                 wr.writerows([(photos, dateTaken,personDetected)])
        myfile.close()

    # TODO Step 5
    # Step 5 Convert CSV to Excel Document
    excelName = subfolders+".xlsx"

    # CSV Output Location
    excelFile = os.path.join(subfolderCSVfilepath, excelName)

    merge_all_to_a_book(glob.glob(csvFile), excelFile)

    # TODO Step 6
    # Step 6 Delete .csv file
    os.remove(csvFile)

print("\nDone with script")