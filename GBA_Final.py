# Import time for time.sleep() and datetime for timestamp
import time
from datetime import datetime

# Import sys for sys.exit()
import sys

# Main Code
def main():
    filename = "myplants Original.txt" # assigning myplants.txt to variable named "filename"

    # Main Menu
    mainMenu = {}
    mainMenu[0] = "==== Main Menu ===="
    mainMenu[1] = "1) Display Plant Records"
    mainMenu[2] = "2) Search for Plant Records"
    mainMenu[3] = "3) Add Plant Records"
    mainMenu[4] = "4) Edit Plant Records"
    mainMenu[5] = "5) Delete Plant Records"
    mainMenu[6] = "6) Exit Program"

    record = read(fn = filename)

    while True:
        print("\n")
        # inputValidation(typeofcommand = int, message = str, menu = dict)
        selection = inputValidation(1, "\nPlease enter selection: \n", mainMenu)

        # User selects Option 1: Display all records
        if selection == 1:
            display(record) # display(dict) prints all records. Refer to its definition.

            time.sleep(1)
            continue

        # User selects Option 2: Search for plant records
        elif selection == 2:
            search(record)
            continue

        # User selects Option 3: Add Plant Record
        elif selection == 3:
            addRecord(record)
            print("\nUpdated List of Plant Records:")
            display(record)
            continue

        # User selects Option 4: Edit Plant Record
        elif selection == 4:
            editMenu(record)
            continue

        # User selects Option 5: Delete  Plant Record
        elif selection == 5:
            delRecord(record)
            continue

        # User selects Option 6: Exit Program
        elif selection == 6:
            writetoFile(filename, record)
            sys.exit("\nExiting the program... \nGoodbye!")

        else:
            print("\nPlease enter a valid option.")
            time.sleep(1)
            continue

    return

# Define relevant functions
def read(fn):
    # This functions opens and reads data from file and transfers data into a dictionary.
    plantDict = {}
    with open(fn) as file:
        count = 0 # what is this?
        tempDict = {}
        tempList = []

        for row in file:
            s = row.split("\n")
            if s[0] == "":
                tempDict[count] = tempList
                count += 1
                tempList = []
                continue
            else:
                tempList.append(s[0])

    file.close()

    for i in tempDict.keys():
        title = tempDict[i][0] # Sets key as plant name
        timestamp = tempDict[i][1] # Sets nested key as timestamp

        plant_descr = []
        for v in range(2,len(tempDict[i])):
            plant_descr.append(tempDict[i][v]) # Appends plant desciption to list

        valueDict = {}
        valueDict[timestamp] = plant_descr
        plantDict[title] = valueDict

    return plantDict

def search(dictionary):
    # Display current list of plants
    listofPlantNames(dictionary)

    # User to select the plant or else key "0"
    selection = inputValidation(1, '\nPLease enter selection (Enter "0" if desired record is unavailable.): \n')
    # E.g. 1) Monstera

    if selection != 0:
        # match number to plant to display record
        plant_list = []
         # List of current plant names
        for title in dictionary.keys():
            plant_list.append(title)

        plantname = plant_list[selection - 1] # 1 - 1 = 0 (Calls up Monstera)

        print("\nFetching record...")
        time.sleep(1)
        print(f"\nPlant Name: \n{plantname}")
        print("\nPlant Description: \n")

        for timestamp in dictionary[plantname]:
            print(timestamp)
            for descr in dictionary[plantname][timestamp]:
                print(descr)

    else:
        addPlant = inputValidation(1, "\nWould you like to create a new plant record? \n1) Yes \n2) No \n")

        if addPlant == 1:
            addRecord(dictionary)

        elif addPlant == 2:
            return dictionary

def inputValidation(typeofcommand, message, menu = {}):
    # This function validates the user's input.
    # Type of command can be str or int.
    while True:
        # Print Menu
        if menu != None:
            for command in menu.keys():
                print(menu[command])
        if isinstance(typeofcommand, str):
            try:
                value = str(input(message))
            except ValueError:
                print("\nPlease enter a valid option.")
                continue
            else:
                break
        if isinstance(typeofcommand, int):
            try:
                value = int(input(message))
            except ValueError:
                print("\nPlease enter a valid option.")
                continue
            else:
                break

    return value

def display(dictionary):
    # This functions prints plant record(s).
    displayMenu = {}
    displayMenu[0] = "\n==== Display Menu ===="
    displayMenu[1] = "1) Alphabetical Order"
    displayMenu[2] = "2) Time Stamp"

    selection = inputValidation(1, "\nPlease enter selection: \n", displayMenu)

    # Return sorted dictionary
    if selection == 1:
        for title in sorted(dictionary):
            print("\n" + title)
            for timestamp in dictionary[title]:
                print(timestamp)
                for descr in dictionary[title][timestamp]:
                    print(descr)

    # elif selection == 2:
    #     for title in dictionary:
    #         print("\n" + title)
    #         for timestamp in sorted(dictionary[title]):
    #             print(timestamp)
    #             for descr in dictionary[title][timestamp]:
    #                 print(descr)
    
    elif selection == 2:
        timelist = list(map(lambda title : list(dictionary[title].items())[0][0], list(dictionary.keys())))

        timelist.sort(key = lambda date : datetime.strptime(date, "%Y-%m-%d %H:%M:%S"))

        descTL = sorted(timelist, reverse = True)
      
        count = 0
        while count < len(descTL):
            pR = {title:timestamp for (title,timestamp) in dictionary.items() if descTL[count] in timestamp}
            print(pR)
            count += 1
            continue
            


def listofPlantNames(dictionary):
    # This function prints the current list of plant names.
    print("\nCurrent List of Plants: \n")
    plant_list = []

    for title in dictionary:
        plant_list.append(title)

    for num in range(1, len(plant_list) + 1):
        print(f"{num}) {plant_list[num-1]}")

def updateTimestamp(dictionary, plant_name, selection):
    # This function updates the timestamp.
    # Used whenever user creates new or edits existing plant record
    timestamp_list = []
    nestedDictlist = []

    for title, values in dictionary.items():
        nestedDictlist.append(values)

    # Calls the specific nested dictionary from record.
    current_nDict = nestedDictlist[selection - 1] # type: dict

    # Calls the timestamp key of the specific dict.
    for timestamp, descr in current_nDict.items():
        current_timestamp = timestamp

    # Updates timestamp in dictionary
    new_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    current_nDict[new_timestamp] = current_nDict.pop(current_timestamp)
    dictionary[plant_name] = current_nDict

    # return new_timestamp

def addRecord(dictionary):
    # This functions allow the user to add a new plant record.
    # Prompt userr for new plant name
    newPlant_Name = inputValidation("1", "\nPlease enter new plant name:\n").title()

    descr_list = []
    newPlant_Descr = inputValidation("1", '\nPlease enter new plant description (Enter "0" if you have finished entering description.):\n').capitalize()
    descr_list.append(newPlant_Descr)
    while True:
        x = inputValidation("1", "").capitalize()
        if x != "0":
            descr_list.append(x)
            continue
        else:
            break

    print("\nCreating new record...")
    time.sleep(1)
    new_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    nestedDict = {}
    nestedDict[new_timestamp] = descr_list
    # dictionary[newPlant_Name] = nestedDict
    dictionary.update({newPlant_Name: nestedDict})

    print("\nNew Record Added!")
    print(f"\nPlant Name: {newPlant_Name}")
    print("\nPlant Description:")

    for timestamp in dictionary[newPlant_Name]:
        print(timestamp)
        for descr in dictionary[newPlant_Name][timestamp]:
            print(descr)

    return dictionary

def editMenu(dictionary):
    editMenu = {}
    editMenu[0] = "\n=== Edit Options ==="
    editMenu[1] = "1) Edit Plant Name"
    editMenu[2] = "2) Edit Plant Description"
    editMenu[3] = "3) Return to Main Menu"

    while True:
        option = inputValidation(1, "\nPlease enter selection:\n", editMenu)

        if option == 1:
            # User wants to edit plant name
            listofPlantNames(dictionary)
            selection = inputValidation(1, "\nPlease enter selection: \n")
            editPlantName(dictionary, selection)

        elif option == 2:
            # User wants to edit plant description
            listofPlantNames(dictionary)
            selection = inputValidation(1, "\nPlease enter selection: \n")
            editPlantDescr(dictionary, selection)

        elif option == 3:
            return dictionary

        else:
            print("\nPlease enter a valid option.")
            time.sleep(1)
            continue

def editPlantName(dictionary, selection):
    newPlant_Name = inputValidation("1", "\nPlease enter the new plant name: \n").title()
    plant_list = []

    for title in dictionary.keys():
        plant_list.append(title) # List of current plant names

    current_name = plant_list[selection - 1]

    # Update timestamp
    updateTimestamp(dictionary, current_name, selection)

    # Update new plant name
    dictionary[newPlant_Name] = dictionary.pop(current_name)

    print("\nUpdating record...")
    time.sleep(1)
    print("\nUpdated record!")
    print(f"\nPlant Name: \n{newPlant_Name}")
    print("\nPlant Description:")

    for timestamp in dictionary[newPlant_Name]:
        print(timestamp)
        for descr in dictionary[newPlant_Name][timestamp]:
            print(descr)

def editPlantDescr(dictionary, selection):
    # Retrieve plant name
    plant_list = []
    for title in dictionary.keys():
        plant_list.append(title) # List of current plant names

    edit_name = plant_list[selection - 1]

    # Get plant description (type = list)
    edit_nestedDict = dictionary[edit_name]
    descr_list = []
    for description in edit_nestedDict.values():
        descr_list = description

    print('\nPlease select the description you would like to edit (Enter "0" if you have nothing to edit.): \n')
    # Print descr line by line
    for num in range(1, len(descr_list) + 1):
        print(f"{num}) {descr_list[num-1]}")

    option1 = inputValidation(1, "\nPlease enter selection: \n")

    while True:
        if option1 != 0:
            edited_descr = inputValidation("1", "\nPlease enter your new description: \n").capitalize()

            to_edit = descr_list[option1 -1]
            editedDes_list = [descr.replace(to_edit, edited_descr) for descr in descr_list]

            updateTimestamp(dictionary, edit_name, selection)
            # Update dictionary with updated description list
            for timestamp in edit_nestedDict.keys():
                edit_nestedDict[timestamp] = editedDes_list

            print("\nUpdating record...")
            time.sleep(1)
            print("\nUpdated record!")
            print(f"\nPlant Name: \n{edit_name}")
            print("\nPlant Description:")

            for timestamp in dictionary[edit_name]:
                print(timestamp)
                for descr in dictionary[edit_name][timestamp]:
                    print(descr)

            return dictionary

        elif option1 == 0:
            while True:
                print("\nWhat would you like to do? \n\n1) Add in a new description \n2) Return to Edit Menu")
                option2 = inputValidation(1, "\nPLease enter selection: \n")
                if option2 == 1:
                    # User to enter new description
                    edited_list = []
                    new_edit_line = inputValidation("1", '\nPlease enter your new description (Enter "0" if you have finished entering description. ): \n').capitalize()
                    edited_list.append(new_edit_line)

                    while True:
                        x = inputValidation("1", "").capitalize()
                        if x != "0":
                            edited_list.append(x)
                            continue
                        else:
                            break

                    for line in edited_list:
                        descr_list.append(line)

                    updateTimestamp(dictionary, edit_name, selection)
                    # Update dictionary with updated description list
                    for timestamp in edit_nestedDict.keys():
                        edit_nestedDict[timestamp] = descr_list

                    # Print updated records
                    print("\nUpdating record...")
                    time.sleep(1)
                    print("\nUpdated record!")
                    print(f"\nPlant Name: \n{edit_name}")
                    print("\nPlant Description:")

                    for timestamp in dictionary[edit_name]:
                        print(timestamp)
                        for descr in dictionary[edit_name][timestamp]:
                            print(descr)

                    return dictionary

                elif option2 == 2:
                    # Return to Exit Menu
                    return dictionary

                else:
                    print("\nPlease enter a valid option.")
                    time.sleep(1)
                    continue
        else:
            print("\nPlease enter a valid option.")
            time.sleep(1)
            continue

def delRecord(dictionary):
    #either use del or pop() to remove requested record
    delMenu = {}
    delMenu[0] = "\n==== Delete Menu ===="
    delMenu[1] = "1) Delete Plant Record"
    delMenu[2] = "2) Delete Plant Description"
    delMenu[3] = "3) Return to Main Menu"

    while True:
        option = inputValidation(1, "\nPlease enter selection:\n", delMenu)

        if option == 1:
            listofPlantNames(dictionary)
            selection = inputValidation(1, "Please enter selection:" + "\n")

            plant_list = []

            for title in dictionary.keys():
                plant_list.append(title) # List of current plant names

            del_name = plant_list[selection - 1]
            del dictionary[del_name]

            print("\nDeleting record...")
            time.sleep(1)
            print("\nRecord Deleted!")

        elif option == 2:
            listofPlantNames(dictionary)
            selection = inputValidation(1, "\nPlease enter selection:" + "\n")
            #e.g. 1) Monstera

            plant_list = []

            for title in dictionary.keys():
                plant_list.append(title) # List of current plant names

            del_name = plant_list[selection - 1] # (retrieve name from dictionary)

            # call out list from dictionary:
            del_nestedDict = dictionary[del_name]
            descr_list = []

            for descr in del_nestedDict.values():
                descr_list = descr

            print("\nPlease select the description you would like to delete: \n")
            for num in range(1, len(descr_list) + 1):
                print(f"{num}) {descr_list[num-1]}")

            option = inputValidation(1, "Please enter selection: \n")

            del descr_list[option - 1]

            updateTimestamp(dictionary, del_name, selection)

            # Update dictionary with updated description list
            for timestamp in del_nestedDict.keys():
                del_nestedDict[timestamp] = descr_list

            print("\nDeleting Record...")
            time.sleep(1)
            print("\nDescription deleted!")

        elif option == 3:
            return dictionary

        else:
            print("\nPlease enter a valid option.")
            time.sleep(1)
            continue

def writetoFile(fn, dictionary): # idk if this is correct i just anyhow whack first HAHAHA
    with open(fn, mode = "w+", encoding="utf-8") as file: # open file for writing and updating
        file.truncate()

        for title, values in dictionary.items():
            file.write(title)
            file.write("\n")
            for timestamp, descr in values.items():
                file.write(timestamp)
                file.write("\n")
                for item in descr:
                    file.write(item)
                    file.write("\n")
                file.write("\n")

        file.close()

if __name__ == '__main__':
    main()
