import json
import pyperclip
import importlib
from os import path
import subprocess
data = None
modules = {}


def loadJSON(filePath):
    with open(filePath) as file:
        jsonData = json.load(file)
    return jsonData


def printOptions(options, key=None):
    i = 1
    for option in options:
        if(key == None):
            print("%s: %s" % (i, option))
        elif(key in option.keys()):
            print("%s: %s" % (i, option[key]))
        else:
            print("Invalid Key")
        i = i + 1


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


def getShortcutMethod(methods, function):
    for method in methods:
        if(method["--id"] == function["methodID"]):
            return method
    else:
        return "closeSafely"


def getUserFunctions(shortcuts, user):
    functions = []
    for shortcut in shortcuts:
        for function in user["functions"]:
            if(shortcut["--id"] == function['shortcutID']):
                # Makes it easier to print the options later.
                # Hack-y solution - need to refactor language.
                shortcut["arguments"] = function["arguments"]
                functions.append(shortcut)
    return functions


def getDefinitionFromModule(module, methodName):
    if(hasattr(module, methodName)):
        try:
            func = getattr(module, methodName)
            return func
        except AttributeError as e:
            print(e)
            print("There was an attribute error.")
        except:
            print("There was some other error")
    else:
        raise Exception(
            "Couldn't find that a method with that name in the module.")


def createKWArgs(function, schema):
    KWArgs = {}
    arguments = function["arguments"]
    if(len(arguments.keys()) != schema["numParams"]):
        print("Invalid")
        raise Exception(
            "Please supply the same # of arguments as outlined in numParams.")
    if(list(arguments.keys()) != schema["parameterNames"]):
        raise Exception(
            "Please supply the same argument names as outlined in paramatersNames. Please note this is case sensitive.")
    for parameter in schema["parameterNames"]:
        if(parameter == "clipboardContext"):
            KWArgs[parameter] = pyperclip.paste()
            continue
        KWArgs[parameter] = arguments[parameter]
    return KWArgs


def importDepencies():
    dependencyJSON = None
    with open('./dependencies.json') as file:
        dependencyJSON = json.load(file)

    folders = dependencyJSON["folders"]
    checkFileSystemDependencies(folders)
    files = dependencyJSON["files"]
    checkFileSystemDependencies(files)
    python = dependencyJSON["python"]
    importPythonModules(python)


def checkFileSystemDependencies(folderDependencies):
    for folder in folderDependencies:
        dependencyPath = "dependencies/%s" % (folder)
        if(path.exists(dependencyPath) == False):
            raise Exception("Error checking file system dependencies.")
    print("Folder dependencies loaded successfully.")


def importPythonModules(pythonDependencies):
    global modules
    for dependency in pythonDependencies:
        try:
            moduleImport = "dependencies." + dependency
            module = importlib.import_module(moduleImport)
            modules[dependency] = module
            print("Loaded module: %s" % (dependency))
        except ModuleNotFoundError:
            raise Exception("Error importing python dependecies.")


def main():
    accounts = loadJSON('./accounts.json')
    shortcuts = loadJSON('./shortcuts.json')
    methods = loadJSON('./methods.json')
    try:
        user = getSelection(accounts, key="title")
        functions = getUserFunctions(shortcuts, user)
        selectedFunction = getSelection(functions, key="title")
        method = getShortcutMethod(methods, selectedFunction)
        moduleName = method["dependency"]
        module = modules[moduleName]
        definition = getDefinitionFromModule(
            module, method["name"])
        arguments = createKWArgs(selectedFunction, method["schema"])
        definition(**arguments)
    except KeyboardInterrupt:
        print("You pressed Ctrl + C!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # Clears console before program output begins, makes it look nicer in terminal.
    subprocess.run("clear")
    print("Attemping to import depencies.")
    print("---------------------\n")
    try:
        importDepencies()
    except Exception as e:
        print(e)
        exit("Coukd not import dependencies correctly. Please check your config.")
    print("\n---------------------")
    print("Welcome to Mokha V0.2-a. This is a tool designed to enable configuration of shortcuts to python code.")
    main()
