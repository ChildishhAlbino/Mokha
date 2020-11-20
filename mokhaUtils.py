from os import path, chdir, getcwd, system, listdir, scandir, walk
import concurrent.futures


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
                print(
                    "ERROR: Please enter a value inside the array.")
        except ValueError:
            print("ERROR: Please input an integer value.")
    try:
        if (previousOption) and (selection == 0):
            return None
        return options[selection - 1]
    except:
        print("I got an error... I sense a disturbance in the force.")


def getAllSubFolders(startingPath):

    dirs = [x[0] for x in walk(startingPath)]
    return dirs
    subfolders = [startingPath]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        subfolders = [f.path for f in scandir(startingPath) if f.is_dir()]
        if(len(subfolders) > 0):
            res = list(executor.map(getAllSubFolders, subfolders))
            if(len(res) > 0):
                subfolders.extend([r for r in res if r])
            return subfolders
