import json
import webbrowser
import pyperclip
from dependencies.encryptPasswords import encrypt
from dependencies.memetext import memeify
data = None


class MethodController:
    def openURL(self, URL):
        webbrowser.open(URL)

    def jasyptEncrypt(self, clipboardContext):
        encrypt(clipboardContext)

    def memetext(self, clipboardContext):
        memeify(clipboardContext)


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
                shortcut["arguments"] = function["arguments"]
                functions.append(shortcut)
    return functions


def getDefinitionFromController(methodController, methodName):
    if(hasattr(methodController, methodName)):
        try:
            func = getattr(methodController, methodName)
            return func
        except AttributeError:
            print("There was an attribute error.")
        except:
            print("There was some other error")


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


def main():
    with open('./mokha.json') as file:
        data = json.load(file)
    methodController = MethodController()
    accounts = data["accounts"]
    shortcuts = data["shortcuts"]
    methods = data["methods"]

    try:
        user = getSelection(accounts, key="title")
        functions = getUserFunctions(shortcuts, user)
        selectedFunction = getSelection(functions, key="title")
        method = getShortcutMethod(methods, selectedFunction)
        definition = getDefinitionFromController(
            methodController, method["name"])
        arguments = createKWArgs(selectedFunction, method["schema"])
        definition(**arguments)
    except KeyboardInterrupt:
        print("You pressed Ctrl + C!")
    except:
        print("Whoops! I encountered an error.")


if __name__ == "__main__":
    print("Welcome to Mokha V0.1-a. This is a tool designed to enable configuration of shortcuts to python code.")
    main()
