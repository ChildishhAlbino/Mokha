import json
import pyperclip
import subprocess
import platform
import sys
from click import clear
from os import path, chdir, getcwd, system, environ
from pathlib import Path as FilePath
from mokhaUtils import getSelection, printOptions, printDivider


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
    min_params = schema.get("minParams", None)
    max_params = schema.get("maxParams", None)
    num_params = schema.get("numParams", None)
    if(num_params != None):
        min_params = num_params
        max_params = num_params
    args_length = len(arguments.keys())
    if(args_length not in range(min_params, max_params + 1)):
        print("Invalid")
        raise Exception(
            "Please supply the same # of arguments as outlined in numParams.")
    illegal_params = [item for item in arguments.keys(
    ) if item not in schema["parameterNames"]]
    if len(illegal_params) > 0:
        raise Exception(
            "Please supply the same argument names as outlined in paramatersNames. Please note this is case sensitive.")
    for parameter in schema["parameterNames"]:
        if(parameter == "clipboardContext"):
            KWArgs[parameter] = pyperclip.paste()
            continue
        argumentValue = arguments[parameter]
        if("$" in argumentValue and "/$" not in argumentValue):
            environment_var_name = argumentValue.replace("$", "")
            KWArgs[parameter] = environ.get(environment_var_name, None)
            continue
        KWArgs[parameter] = arguments[parameter]
    return KWArgs


def getAccountSelection(context):
    accounts = context["accounts"]
    previousOption = context["previousOption"]
    selection = getSelection(accounts, key="title",
                             previousOption=previousOption)
    if (not selection):
        return None
    return {"account": selection}


def getMethodSelection(context):
    account = context["account"]
    previousOption = context["previousOption"]
    selection = getSelection(account["methods"], key="title",
                             previousOption=previousOption)
    if (not selection):
        return None
    return {"selectedMethod": selection}


def runSteps(steps, stepContexts):
    stepContext = None
    i = 0
    while True:
        previousOption = i > 0
        step = steps[i]
        if (i in stepContexts.keys()):
            stepContext = stepContexts[i]
        else:
            stepContexts[i] = stepContext
        stepContext["previousOption"] = previousOption
        stepContext = step(stepContext)
        # Check if user returned to previous step.
        if (not stepContext):
            if (i - 1 < 0):
                printDivider()
                print("You can't go any further back than this step.")
            else:
                printDivider()
                stepContexts.pop(i)
                i = i - 1
            continue
        printDivider()
        # do the logic to rerun the previous step
        i = i + 1
        if (i == len(steps)):
            clear()
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
        (parentDir, fileName) = path.split(module.__file__)
        arguments = createKWArgs(selectedMethod, method["schema"])
        # Changes the cwd to the module's parent directory
        # so the module is run as if it were run in isolation.
        chdir(parentDir)
        definition(**arguments)
    except KeyboardInterrupt:
        print("You pressed Ctrl + C!")
    except Exception as e:
        print(e)
