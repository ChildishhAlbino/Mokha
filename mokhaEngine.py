import json
import pyperclip
import subprocess
import platform
import sys
from click import clear
from os import path, chdir, getcwd, system
from pathlib import Path as FilePath
from mokhaUtils import getSelection, printOptions


def getMethodNameFromAccountMethods(methods, selectedMethodID):
    try:
        methodsFiltered = [
            method for method in methods if method['--id'] == selectedMethodID]
        return methodsFiltered[0]
    except Exception as e:
        raise Exception("Could not find a method with id: %s" %
                        (selectedMethodID["--id"]))


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
            "Couldn't find a method with that name in the module.")


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


def main(baseConfig, accounts, methods, modules):
    try:
        account = getSelection(accounts, key="title")
        selectedFunction = getSelection(account["methods"], key="title")
        method = getMethodNameFromAccountMethods(
            methods, selectedFunction["methodID"])
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
