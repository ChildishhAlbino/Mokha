from os import path, chdir, getcwd, system, listdir, scandir


def printOptions(options, key=None):
    for i, option in enumerate(options):
        if(key == None):
            print("%s: %s" % (i + 1, option))
        elif(key in option.keys()):
            print("%s: %s" % (i + 1, option[key]))
        else:
            print("Invalid Key")


def getSelection(options, key=None):
    printOptions(options, key)
    while True:
        try:
            selection = int(
                input("Select an option: "))
            if(selection <= len(options)):
                break
            else:
                print("ERROR: Please enter a value inside the array.")
        except ValueError:
            print("Please input an integer value.")
    try:
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
