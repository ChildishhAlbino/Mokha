from os import path, chdir, getcwd, system, listdir, scandir


def printOptions(options, key=None):
    for i, option in enumerate(options):
        if(key == None):
            print("%s: %s" % (i + 1, option))
        elif(key in option.keys()):
            print("%s: %s" % (i + 1, option[key]))
        else:
            print("Invalid Key")


def printDivider():
    print("\n---------------------\n")


def getSelection(options, key=None, previousOption=False):
    printOptions(options, key)
    if(previousOption):
        print("\n0: Previous menu.")
    while True:
        try:
            selection = int(
                input("\nSelect an option: "))
            if (previousOption == True):
                if (selection == 0):
                    break
            if(selection <= len(options)) and (selection > 0):
                break
            else:
                raise("ERROR: Please enter a value inside the array.")
        except ValueError:
            print("ERROR: Please input an integer value.")
    try:
        if (previousOption) and (selection == 0):
            return None
        return options[selection - 1]
    except:
        print("I got an error... I sense a disturbance in the force.")


def getAllSubFolders(startingPath):
    # get subfolders for starting path
    subfolders = [f.path for f in scandir(startingPath) if f.is_dir()]
    # check if subfolders contain any subfolders,
    for subfolder in subfolders:
        moreSubfolders = getAllSubFolders(subfolder)
        subfolders.extend(moreSubfolders)
    return subfolders
