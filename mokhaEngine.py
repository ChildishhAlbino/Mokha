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
            method for method in methods if method["--id"] == selectedMethodID]
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


def getAccountSelection(accounts):
    selection = getSelection(accounts, key="title")
    if (not selection):
        return None
    return {"account": selection}


def getMethodSelection(account):
    selection = getSelection(account["methods"], key="title")
    if (not selection):
        return None
    return {"selectedMethod": selection}


def runSteps(steps, stepContexts):
    stepContext = None
    i = 0
    while True:
        step = steps[i]
        if (i in stepContexts.keys()):
            stepContext = stepContexts[i]
        else:
            stepContexts[i] = stepContext
        stepContext = step(**stepContext)
        # Check if user returned to previous step.
        if (not stepContext):
            if (i - 1 < 0):
                print("You can't go any further back than this step.")
            else:
                stepContexts.pop(i)
                i = i - 1
                clear()
            continue
        # do the logic to rerun the previous step
        i = i + 1
        if (i == len(steps)):
            break
    return stepContext


def main(baseConfig, accounts, methods, modules):
    stepContexts = {0: {"accounts": accounts}}
    try:
        steps = [getAccountSelection, getMethodSelection]
        finalStepContext = runSteps(steps, stepContexts)
        selectedMethod = finalStepContext["selectedMethod"]
        method = getMethodNameFromAccountMethods(
            methods, selectedMethod["methodID"])
        moduleName = method["dependency"]
        module = modules[moduleName]
        definition = getDefinitionFromModule(
            module, method["name"])
        arguments = createKWArgs(selectedMethod, method["schema"])
        # Changes the cwd to the dependencies path so module is run as if it were run in isolation.
        chdir(baseConfig["dependencies-path"])
        definition(**arguments)
    except KeyboardInterrupt:
        print("You pressed Ctrl + C!")
    except Exception as e:
        print(e)
