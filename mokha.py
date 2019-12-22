import json
import pyperclip
import importlib
import subprocess
import platform
import sys
from click import clear
from os import path, chdir, getcwd, system
data = None
modules = {}
baseConfig = {}
application_path = ""


def createBaseConfig():
    configTypes = {"methods": "./methods.json",
                   "accounts": "./accounts.json", "dependencies": "./dependencies.json"}
    baseConfig = {"config-types": configTypes,
                  "dependencies-path": "./dependencies"}
    with open("./config.json", "w") as f:
        json.dump(baseConfig, f, indent=2)


def loadBaseConfig():
    if not (path.exists("./config.json")):
        createBaseConfig()
        raise Exception("Closing so you can configure application.")
    else:
        configJSON = loadJSON('./config.json')
        configTypes = configJSON["config-types"]
        for configType in configTypes.keys():
            baseConfig[configType] = configTypes[configType]
        baseConfig["dependencies-path"] = configJSON["dependencies-path"]


def loadJSON(filePath):
    with open(filePath) as file:
        jsonData = json.load(file)
    return jsonData


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


def getMethodNameFromUserFunction(methods, function):
    for method in methods:
        if(method["--id"] == function["methodID"]):
            return method
    else:
        return "closeSafely"


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
    with open(baseConfig["dependencies"]) as file:
        dependencyJSON = json.load(file)
    fileSystem = dependencyJSON["file-system"]
    checkFileSystemDependencies(fileSystem)
    python = dependencyJSON["python"]
    importPythonModules(python)


def checkFileSystemDependencies(folderDependencies):
    chdir(baseConfig["dependencies-path"])
    for folder in folderDependencies:
        dependencyPath = "%s" % (folder)
        if(path.exists(dependencyPath) == False):
            raise Exception("Error checking file system dependencies.")
    print("Filesystem dependencies loaded successfully.")
    chdir(application_path)


def importPythonModules(pythonDependencies):
    for dependency in pythonDependencies:
        try:
            moduleImport = dependency
            module = importlib.import_module(moduleImport)
            modules[dependency] = module
            print("Loaded module: %s" % (dependency))
        except ModuleNotFoundError as e:
            print(e)
            raise Exception("Error importing python dependecies.")


def main():
    try:
        accounts = loadJSON(baseConfig["accounts"])
        methods = loadJSON(baseConfig["methods"])
        user = getSelection(accounts, key="title")
        selectedFunction = getSelection(user["functions"], key="title")
        method = getMethodNameFromUserFunction(methods, selectedFunction)
        moduleName = method["dependency"]
        module = modules[moduleName]
        definition = getDefinitionFromModule(
            module, method["name"])
        arguments = createKWArgs(selectedFunction, method["schema"])
        # Changes the cwd to the dependencies path so module is run as if it were run in isolation.
        chdir(baseConfig["dependencies-path"])
        definition(**arguments)
    except KeyboardInterrupt:
        print("You pressed Ctrl + C!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    application_path = getcwd()
    # Clears console before program output begins, makes it look nicer in terminal.
    clear()
    loadBaseConfig()
    # Ensures python can see dependencies outside of root dir.
    sys.path.append(baseConfig['dependencies-path'])
    print("Attemping to import depencies from: %s" %
          (baseConfig['dependencies-path']))
    print("---------------------\n")
    try:
        importDepencies()
    except Exception as e:
        print(e)
        exit("Could not import dependencies correctly. Please check your config.")
    print("\n---------------------")
    print("Welcome to Mokha V1.0-a. This is a tool designed to enable configuration of shortcuts to python code.")
    main()
